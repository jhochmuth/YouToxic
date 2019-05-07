# Get YouToxic image from Docker Hub
FROM jhochmuth/youtoxic-base

# Set working directory.
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Download LFS files
RUN rm -rf ./youtoxic/app/models
RUN mkdir ./youtoxic/app/models

ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/toxicity_model.h5 youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/insult_model.h5 youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/obscenity_model.h5 youtoxic/app/models
ADD https://github.com/jhochmuth/YouToxic/raw/Flask/Dash/youtoxic/app/models/identity_model.h5 youtoxic/app/models

# Run setup of YouToxic
RUN pip install -e .

# Run __main__.py when the container launches
CMD ["youtoxic", "runserver", "--host=0.0.0.0", "--port=8050"]