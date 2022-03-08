FROM pytorch/pytorch
MAINTAINER lmorelli@fbk.eu

RUN apt-get -y update
RUN apt-get -y install git
RUN pip install git+https://github.com/kornia/kornia
RUN pip install kornia_moons
RUN apt-get install ffmpeg libsm6 libxext6 -y