#!/bin/bash

hash=$(git rev-parse --short HEAD)
docker build --platform linux/arm32/v7 -t rianders/car32:$hash -f car32.dockerfile .
docker push rianders/car32:$hash
echo $hash

# use latest for release PARITy

#TODO:
# Bare metal machine and vscode remote -ssh  to chameleon and

# Find the containter: % docker image ls

# run local and clean up % docker run --rm   -it  car
# To save it for use: docker run --name localname   -it  rianders/car:1506f2
#docker run --rm   -it --entrypoint=/bin/bash rianders/car:$hash   
#
#docker run --rm --privileged multiarch/qemu-user-static --reset -p yes 

# Run and remove
#docker run   --rm --device=/dev/vchiq -v /opt/vc:/opt/vc --env LD_LIBRARY_PATH=/opt/vc/lib  --device /dev/gpiomem  --device=/dev/ttyACM0 --privileged  -it --entrypoint=/bin/bash rianders/car:9bfb475
#
# Run and save data once per host
# docker volume create foocarsdata
# docker volume ls
##docker run   --rm --device=/dev/vchiq -v foocarsdata:/foocars/cars/chiaracer -v /opt/vc:/opt/vc --env LD_LIBRARY_PATH=/opt/vc/lib  --device /dev/gpiomem  --device=/dev/ttyACM0 --privileged  -it --entrypoint=/bin/bash rianders/car:9bfb475
# docker volume inspect foocarsdata
# tar up the volume
# 
# review the data collected
# docker run --rm -v foocarsdata:/foocars/cars/chiaracer -it debian:10

# container that can upload to openstack to move the data up
# copy the data from the volume
# docker cp ce3365f10ef8:/foocars/cars/chiaracer.tar.gz .

# Example mount the data folder
# docker run   --device=/dev/vchiq -v /home/pi/data:/data -v /opt/vc:/opt/vc --env LD_LIBRARY_PATH=/opt/vc/lib  --device /dev/gpiomem  --device=/dev/ttyACM0 --device=/dev/ttyACM1  --privileged  -it --entrypoint=/bin/bash rianders/car:60a97f6 



