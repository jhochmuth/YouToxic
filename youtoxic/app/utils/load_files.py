"""Todo: Delete this file after LFS is enabled."""


def create_model():
    files = list()
    files.append("models/model_1.pt")
    files.append("models/model_2.pt")
    files.append("models/model_3.pt")
    files.append("models/model_4.pt")
    files.append("models/model_5.pt")

    with open("models/models.pt", "wb") as outfile:
        for file in files:
            with open(file, "rb") as infile:
                outfile.write(infile.read())


def create_embeddings():
    files = list()
    files.append("embedding_matrix/embedding_matrix_1.npy")
    files.append("embedding_matrix/embedding_matrix_2.npy")
    files.append("embedding_matrix/embedding_matrix_3.npy")
    files.append("embedding_matrix/embedding_matrix_4.npy")
    files.append("embedding_matrix/embedding_matrix_5.npy")
    files.append("embedding_matrix/embedding_matrix_6.npy")
    files.append("embedding_matrix/embedding_matrix_7.npy")
    files.append("embedding_matrix/embedding_matrix_8.npy")
    files.append("embedding_matrix/embedding_matrix_9.npy")
    files.append("embedding_matrix/embedding_matrix_10.npy")

    with open("embedding_matrix/embedding_matrix.npy", "wb") as outfile:
        for file in files:
            with open(file, "rb") as infile:
                outfile.write(infile.read())
