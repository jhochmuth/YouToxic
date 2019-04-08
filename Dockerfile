# Get YouToxic image from Docker Hub
FROM python:3.7.2-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Download LFS files
RUN rm -rf ./youtoxic/app/models
RUN mkdir ./youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/embedding_matrix.npy youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/identity_model_state.pt youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/insult_model_state.pt youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/obscenity_model_state.pt youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/toxicity_model_state.pt youtoxic/app/models

# Install dependencies
RUN pip install -r requirements-container.txt

# Run setup of YouToxic
RUN pip install -e .

# Run __main__.py when the container launches
CMD ["youtoxic", "runserver", "--host=0.0.0.0", "--port=8050"]
