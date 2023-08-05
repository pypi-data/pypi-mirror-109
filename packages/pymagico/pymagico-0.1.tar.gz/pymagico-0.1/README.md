# PyMagic

### Local

```
export PYTHONPATH=/path/to/pymagic:$PYTHONPATH
```

### Docker

0. Buid local **development** docker image

```
bash development.sh
```

1. Run **development** image with local source

```
sudo docker run \
  -it \
  --name pymagic --rm \
  -p 5000:5000 \
  -v /home/ermiry/Documents/Work/magic/pymagic:/home/pymagic \
  -e RUNTIME=development \
  -e PORT=5000 \
  -e CERVER_RECEIVE_BUFFER_SIZE=4096 -e CERVER_TH_THREADS=4 \
  -e CERVER_CONNECTION_QUEUE=4 \
  ermiry/pymagic:development /bin/bash
```

2. Handle **pymagic** module

```
export PYTHONPATH=$pwd:$PYTHONPATH
```
