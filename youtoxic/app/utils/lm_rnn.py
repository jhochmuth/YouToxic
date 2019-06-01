"""Contains implementation of the ULMFiT RNN model. Code is taken from fastai library.

"""

import contextlib
import warnings

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd.variable import Variable


IS_TORCH_04 = True


def noop(*args, **kwargs):
    return


def set_grad_enabled(mode):
    return torch.set_grad_enabled(mode) if IS_TORCH_04 else contextlib.suppress()


def repackage_var(h):
    if IS_TORCH_04:
        return (
            h.detach()
            if type(h) == torch.Tensor
            else tuple(repackage_var(v) for v in h)
        )
    else:
        return (
            Variable(h.data)
            if type(h) == Variable
            else tuple(repackage_var(v) for v in h)
        )


class LinearBlock(nn.Module):
    def __init__(self, ni, nf, drop):
        super().__init__()
        self.lin = nn.Linear(ni, nf)
        self.drop = nn.Dropout(drop)
        self.bn = nn.BatchNorm1d(ni)

    def forward(self, x):
        return self.lin(self.drop(self.bn(x)))


class PoolingLinearClassifier(nn.Module):
    def __init__(self, layers, drops):
        super().__init__()
        self.layers = nn.ModuleList(
            [
                LinearBlock(layers[i], layers[i + 1], drops[i])
                for i in range(len(layers) - 1)
            ]
        )

    def pool(self, x, bs, is_max):
        f = F.adaptive_max_pool1d if is_max else F.adaptive_avg_pool1d
        return f(x.permute(1, 2, 0), (1,)).view(bs, -1)

    def forward(self, input):
        raw_outputs, outputs = input
        output = outputs[-1]
        sl, bs, _ = output.size()
        avgpool = self.pool(output, bs, False)
        mxpool = self.pool(output, bs, True)
        x = torch.cat([output[-1], mxpool, avgpool], 1)
        for l in self.layers:
            l_x = l(x)
            x = F.relu(l_x)
        return l_x, raw_outputs, outputs


def dropout_mask(x, sz, dropout):
    return x.new(*sz).bernoulli_(1 - dropout) / (1 - dropout)


class LockedDropout(nn.Module):
    def __init__(self, p=0.5):
        super().__init__()
        self.p = p

    def forward(self, x):
        if not self.training or not self.p:
            return x
        m = dropout_mask(x.data, (1, x.size(1), x.size(2)), self.p)
        return Variable(m, requires_grad=False) * x


class WeightDrop(torch.nn.Module):
    def __init__(self, module, dropout, weights=["weight_hh_l0"]):
        super().__init__()
        self.module, self.weights, self.dropout = module, weights, dropout
        self._setup()

    def _setup(self):
        if isinstance(self.module, torch.nn.RNNBase):
            self.module.flatten_parameters = noop
        for name_w in self.weights:
            w = getattr(self.module, name_w)
            del self.module._parameters[name_w]
            self.module.register_parameter(name_w + "_raw", nn.Parameter(w.data))

    def _setweights(self):
        for name_w in self.weights:
            raw_w = getattr(self.module, name_w + "_raw")
            w = torch.nn.functional.dropout(
                raw_w, p=self.dropout, training=self.training
            )
            if hasattr(self.module, name_w):
                delattr(self.module, name_w)
            setattr(self.module, name_w, w)

    def forward(self, *args):
        self._setweights()
        return self.module.forward(*args)


class EmbeddingDropout(nn.Module):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed

    def forward(self, words, dropout=0.1, scale=None):
        if dropout:
            size = (self.embed.weight.size(0), 1)
            mask = Variable(dropout_mask(self.embed.weight.data, size, dropout))
            masked_embed_weight = mask * self.embed.weight
        else:
            masked_embed_weight = self.embed.weight

        if scale:
            masked_embed_weight = scale * masked_embed_weight

        padding_idx = self.embed.padding_idx
        if padding_idx is None:
            padding_idx = -1

        if IS_TORCH_04:
            X = F.embedding(
                words,
                masked_embed_weight,
                padding_idx,
                self.embed.max_norm,
                self.embed.norm_type,
                self.embed.scale_grad_by_freq,
                self.embed.sparse,
            )
        else:
            X = self.embed._backend.Embedding.apply(
                words,
                masked_embed_weight,
                padding_idx,
                self.embed.max_norm,
                self.embed.norm_type,
                self.embed.scale_grad_by_freq,
                self.embed.sparse,
            )

        return X


class RNNEncoder(nn.Module):
    initrange = 0.1

    def __init__(
        self,
        ntoken,
        emb_sz,
        n_hid,
        n_layers,
        pad_token,
        bidir=False,
        dropouth=0.3,
        dropouti=0.65,
        dropoute=0.1,
        wdrop=0.5,
        qrnn=False,
    ):
        super().__init__()
        self.ndir = 2 if bidir else 1
        self.bs, self.qrnn = 1, qrnn
        self.encoder = nn.Embedding(ntoken, emb_sz, padding_idx=pad_token)
        self.encoder_with_dropout = EmbeddingDropout(self.encoder)

        self.rnns = [
            nn.LSTM(
                emb_sz if l == 0 else n_hid,
                (n_hid if l != n_layers - 1 else emb_sz) // self.ndir,
                1,
                bidirectional=bidir,
            )
            for l in range(n_layers)
        ]
        if wdrop:
            self.rnns = [WeightDrop(rnn, wdrop) for rnn in self.rnns]
        self.rnns = torch.nn.ModuleList(self.rnns)
        self.encoder.weight.data.uniform_(-self.initrange, self.initrange)

        self.emb_sz, self.n_hid, self.n_layers, self.dropoute = (
            emb_sz,
            n_hid,
            n_layers,
            dropoute,
        )
        self.dropouti = LockedDropout(dropouti)
        self.dropouths = nn.ModuleList(
            [LockedDropout(dropouth) for l in range(n_layers)]
        )

    def forward(self, input):
        sl, bs = input.size()
        if bs != self.bs:
            self.bs = bs
            self.reset()
        with set_grad_enabled(self.training):
            emb = self.encoder_with_dropout(
                input, dropout=self.dropoute if self.training else 0
            )
            emb = self.dropouti(emb)
            raw_output = emb
            new_hidden, raw_outputs, outputs = [], [], []
            for l, (rnn, drop) in enumerate(zip(self.rnns, self.dropouths)):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    raw_output, new_h = rnn(raw_output, self.hidden[l])
                new_hidden.append(new_h)
                raw_outputs.append(raw_output)
                if l != self.n_layers - 1:
                    raw_output = drop(raw_output)
                outputs.append(raw_output)

            self.hidden = repackage_var(new_hidden)
        return raw_outputs, outputs

    def one_hidden(self, l):
        nh = (self.n_hid if l != self.n_layers - 1 else self.emb_sz) // self.ndir
        if IS_TORCH_04:
            return Variable(self.weights.new(self.ndir, self.bs, nh).zero_())
        else:
            return Variable(
                self.weights.new(self.ndir, self.bs, nh).zero_(),
                volatile=not self.training,
            )

    def reset(self):
        if self.qrnn:
            [r.reset() for r in self.rnns]
        self.weights = next(self.parameters()).data
        if self.qrnn:
            self.hidden = [self.one_hidden(l) for l in range(self.n_layers)]
        else:
            self.hidden = [
                (self.one_hidden(l), self.one_hidden(l)) for l in range(self.n_layers)
            ]


class SequentialRNN(nn.Sequential):
    def reset(self):
        for c in self.children():
            if hasattr(c, "reset"):
                c.reset()


class MultiBatchRNN(RNNEncoder):
    def __init__(self, bptt, max_seq, *args, **kwargs):
        self.max_seq, self.bptt = max_seq, bptt
        super().__init__(*args, **kwargs)

    def concat(self, arrs):
        return [torch.cat([l[si] for l in arrs]) for si in range(len(arrs[0]))]

    def forward(self, input):
        sl, bs = input.size()
        for l in self.hidden:
            for h in l:
                h.data.zero_()
        raw_outputs, outputs = [], []
        for i in range(0, sl, self.bptt):
            r, o = super().forward(input[i : min(i + self.bptt, sl)])
            if i > (sl - self.max_seq):
                raw_outputs.append(r)
                outputs.append(o)
        return self.concat(raw_outputs), self.concat(outputs)


def get_rnn_classifier(
    bptt,
    max_seq,
    n_class,
    n_tok,
    emb_sz,
    n_hid,
    n_layers,
    pad_token,
    layers,
    drops,
    bidir=False,
    dropouth=0.3,
    dropouti=0.5,
    dropoute=0.1,
    wdrop=0.5,
    qrnn=False,
):
    rnn_enc = MultiBatchRNN(
        bptt,
        max_seq,
        n_tok,
        emb_sz,
        n_hid,
        n_layers,
        pad_token=pad_token,
        bidir=bidir,
        dropouth=dropouth,
        dropouti=dropouti,
        dropoute=dropoute,
        wdrop=wdrop,
        qrnn=qrnn,
    )
    return SequentialRNN(rnn_enc, PoolingLinearClassifier(layers, drops))
