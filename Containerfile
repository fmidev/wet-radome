FROM python:3

WORKDIR /usr/src/app

COPY . .

# Install gdal and python-gdal
RUN apt-get update && apt-get install -y gdal-bin python3-gdal

RUN pip install -U pip && pip install --no-cache-dir .

ENV PYART_QUIET=1

ENTRYPOINT ["/usr/local/bin/wetrad"]
