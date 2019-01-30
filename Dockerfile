FROM ubuntu

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# First add the NextGIS repo
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:nextgis/ppa

RUN mkdir -p /code
WORKDIR /code

RUN apt-get update && apt-get install -y python3-dev python3-pip \
    gdal-bin python3-gdal gcc \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /code
RUN pip3 install -r /code/requirements.txt \
    && rm -rf $HOME/.cache/pip

ADD ingest /code/ingest
RUN mkdir -p /code/data && \
    mkdir -p /code/tmp && \
    mkdir -p /code/out
