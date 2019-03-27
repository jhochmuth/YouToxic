# Get YouToxic image from Docker Hub
FROM jhochmuth/youtoxic

# Set working directory.
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Run setup of YouToxic
RUN python setup.py install

# Run __main__.py when the container launches
CMD ["youtoxic", "runserver", "--host=0.0.0.0", "--port=8050"]