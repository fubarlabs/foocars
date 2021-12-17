FROM --platform=linux/arm32/v7 rianders/tensorflow:2.4.0 AS base

WORKDIR foocars
ENV READTHEDOCS=True
#TODO: use the get poetry install script
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
##CMD ["/usr/local/bin/car_runner"]
CMD ["/bin/bash"]

