
docker build --platform linux/arm32v7 -t rianders/tensorflow32:2.4.0 -f tensorflow32.dockerfile .
docker push rianders/tensorflow32:2.4.0
