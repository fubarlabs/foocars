FROM --platform=linux/arm32/v7 rianders/tensorflow32:2.4.0 AS base

WORKDIR foocars
ENV READTHEDOCS=True
RUN apt-get update && apt-get install -y \
    rustc

FROM base as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv
RUN poetry config virtualenvs.create false

# From the base get the cargenerator
FROM poetry AS cargenerator
COPY ./cargenerator /foocars/cargenerator
COPY ./tests /foocars/tests

WORKDIR /foocars/cargenerator

RUN poetry install
RUN poetry run generatecar --name chiaracer --output_dir /foocars/cars/
VOLUME ["/foocars/cars/chiaracer"]


FROM base AS carservices

RUN apt-get update && apt-get install -y \
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

