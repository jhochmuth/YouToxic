# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Copy the current directory contents into the container at /app
COPY . .

RUN conda env create --file environment.yml
RUN conda activate YouToxic
RUN python setup.py install

# Run __main__.py when the container launches
CMD ["python", "youtoxic/app/__main__.py", "runserver"]