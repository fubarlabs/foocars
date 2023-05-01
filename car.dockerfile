ARG BASE_IMAGE=kumatea/tensorflow:2.4.1-py39

FROM --platform=linux/arm64/v8 ${BASE_IMAGE} as userland

RUN apt-get update && apt-get install -f -y \
    cmake \
    build-essential \
    git \
    sudo

RUN git clone \
    https://github.com/msherman64/userland \
    -b wip/64bit \
    /usr/local/src/userland
WORKDIR /usr/local/src/userland
RUN ./buildme --aarch64



FROM --platform=linux/arm64/v8 ${BASE_IMAGE} AS base


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
ENV LD_LIBRARY_PATH=/opt/vc/lib

CMD ["/usr/local/bin/car_runner"]

