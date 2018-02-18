# Docker for Car and Docker For Training

## BUild the image for the car docker:

Currently, the images are going to ricklon Docker.com location. In the future it would be nice to have a FubarLabd Docker repo there.

Build the car image

``
$  docker build -f car.Dockerfile -t ricklon/otto-car:latest .
```

Run the car Docker Ineractively

```
$ docker run -it ricklon/otto-car bash

```

Run the car from commands sent into Docker:

```
TODO
```

## Docker for training

Build the training image

``
$  docker build -f train.Dockerfile -t ricklon/otto-train:latest .
```

Run the car Docker Ineractively

```
$ docker run -it ricklon/otto-train bash

```

Run the car from commands sent into Docker:

```
TODO
```




