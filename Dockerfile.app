# Get YouToxic image from Docker Hub
FROM jhochmuth/youtoxic-base

# Set working directory.
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Download LFS files
RUN rm -rf ./youtoxic/app/models
RUN mkdir ./youtoxic/app/models

# Download insult model files
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128507&authkey=AKe42dUFHCRSfuE' youtoxic/app/models/insult_model.h5
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128502&authkey=AMTSBoSZKnng9fM' youtoxic/app/models/insult_mappings.pkl

# Download toxicity model files
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128509&authkey=AK9EkRYEQE5aguA' youtoxic/app/models/toxicity_model.h5
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128506&authkey=AN6iLYSFF6ZoD6w' youtoxic/app/models/toxicity_mappings.pkl

# Download identity model files
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128505&authkey=AJLy7x9J3eItG8Y' youtoxic/app/models/identity_model.h5
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128503&authkey=AAv1e1vVnh6_I2w' youtoxic/app/models/identity_mappings.pkl

# Download obscenity model files
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128508&authkey=AIUnliUvbWj8llY' youtoxic/app/models/obscenity_model.h5
ADD 'https://onedrive.live.com/download?cid=F27A5B9996AB72E1&resid=F27A5B9996AB72E1%2128504&authkey=AJyPEKKxd9bkddU' youtoxic/app/models/obscenity_mappings.pkl

# Run setup of YouToxic
RUN pip install -e .

# Run __main__.py when the container launches
CMD ["youtoxic", "runserver", "--host=0.0.0.0", "--port=8050"]
