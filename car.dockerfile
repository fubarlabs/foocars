ARG BUILD_TAG=3.10-jammy-build-20230328
FROM balenalib/raspberrypi4-64-ubuntu-python:${BUILD_TAG} as userland
RUN install_packages \
    cmake

RUN git clone \
    https://github.com/msherman64/userland \
    -b wip/64bit \
    /usr/local/src/userland
WORKDIR /usr/local/src/userland
RUN ./buildme --aarch64



FROM --platform=linux/arm64/v8 kumatea/tensorflow:2.4.1-py39 AS base


WORKDIR foocars
ENV READTHEDOCS=True

RUN pip3 install --upgrade pip poetry
RUN poetry config virtualenvs.create false

# From the base get the cargenerator
FROM base AS cargenerator
COPY ./cargenerator /foocars/cargenerator
COPY ./tests /foocars/tests

WORKDIR /foocars/cargenerator

RUN poetry install
RUN poetry run generatecar --name chiaracer --output_dir /foocars/cars/
VOLUME ["/foocars/cars/chiaracer"]


FROM base AS carservices

RUN apt update && apt install -y \
    gcc libhdf5-dev vim

RUN pip install h5py platformio

COPY ./cars/carservices /foocars/cars/carservices
COPY ./tests /foocars/tests

WORKDIR /foocars/cars/carservices/

RUN poetry install
COPY --from=cargenerator /foocars/cars/chiaracer /foocars/cars/chiaracer
#ENTRYPOINT ["python3"]
#ENTRYPOINT ["/bin/bash"]
COPY --from=userland /opt/vc/ /opt/vc/

CMD ["/usr/local/bin/car_runner"]

