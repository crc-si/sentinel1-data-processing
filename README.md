# Sentinel 1 data processor for the ODC

## Requirements
You need to have GDAL installed, and a number of Python libraries that are listed in the file `requirements.txt`.

## Usage
You can run the script at `ingest/automation/prepare_S1Google.sh` with a single argument, which is a directory with a GeoTIFF and a CSV in it.

## Docker
The Docker Compose process works also, and can be run like `docker-compose run processor /code/ingest/automation/prepare_S1Google.sh /code/data`.
