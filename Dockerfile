# Use an official Python runtime as a parent image
FROM python:3.7.2

WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

RUN pip install -r requirements.txt

RUN python setup.py install

# Run __main__.py when the container launches
CMD ["youtoxic", "runserver", "--host=0.0.0.0", "--port=8050"]