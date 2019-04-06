# Get YouToxic image from Docker Hub
FROM python:3.7.2

# Set working directory.
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run setup of YouToxic
RUN python setup.py install

# Run __main__.py when the container launches
CMD ["youtoxic", "runserver"]