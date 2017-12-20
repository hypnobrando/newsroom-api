# Use an official Python runtime as a parent image
FROM python:3.6





#FROM ubuntu:latest
#MAINTAINER fnndsc "dev@babymri.org"

#RUN apt-get update \
#  && apt-get install -y python3-pip python3-dev \
#  && cd /usr/local/bin \
#  && ln -s /usr/bin/python3 python \
#  && pip3 install --upgrade pip





# Set the working directory to /
WORKDIR /

# Copy the current directory contents into the container at /
ADD . /

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "main.py"]
