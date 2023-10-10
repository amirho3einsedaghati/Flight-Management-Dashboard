FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y wget bzip2 ca-certificates

# Download and install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    /bin/bash miniconda.sh -b -p /opt/miniconda && \
    rm miniconda.sh

# Add Miniconda to PATH
ENV PATH="/opt/miniconda/bin:$PATH"

WORKDIR /app
COPY requirements.txt .

# Install the required system dependencies for the regex and pyodbc packages
RUN apt-get update && apt-get install -y \
    build-essential \
    unixodbc-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5006

LABEL version='1.0'
LABEL description='Fight Management Dashboard'
LABEL maintainer="Amir Hosein Sedaghati <<amirhosseinsedaghati42@gmail.com>>"

CMD ["bokeh", "serve", "--allow-websocket-origin=localhost:5006", "main.py"]
