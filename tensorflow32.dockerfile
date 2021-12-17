FROM --platform=linux/arm32/v7 arm32v7/python:3.7-buster AS python3

WORKDIR tensorflow
RUN apt-get update && apt-get install -y \
    gcc libhdf5-dev vim

RUN wget https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl
RUN pip3 install tensorflow-2.4.0-cp37-none-linux_armv7l.whl
RUN echo "Done"

