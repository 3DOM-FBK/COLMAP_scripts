## Setup from PYTORCH

Create a container in docker using the pytorch/pytorch image:
> docker run -ti --rm --name pytorch_container -v path:/home pytorch/pytorch
> docker run --runtime=nvidia =all -ti --rm --name pytorch_container -v path:/home pytorch/pytorch

Inside the container:
> apt-get -y update
> cd ../home/kornia-master
> python setup.py install
> pip install kornia_moons
> apt-get install ffmpeg libsm6 libxext6 -y


## Build the Docker file for KORNIA (NOT updated to KeyNetAffNetHardNet)

In general:
```> docker build -t ImageNam:TagName dir```

An example:
```> docker build -t kornia_img:0.1 C:\Users\User\Desktop\Luca\GitProjects\Github_3DOM\COLMAP_scripts\Keypoints```


## Run a container
Con CPU:
```> docker run -ti --rm --name kornia_container -v C:\Users\User\Desktop\Luca\GitProjects\Github_3DOM\COLMAP_scripts\Keypoints:/home kornia_img:0.1```

Con GPU:
```> sudo docker run --runtime=nvidia =all -ti --rm --name kornia_container -v /home/luca/Scrivania/3DOM/Github_3DOM/COLMAP_scripts/Keypoints/KeyNetAffNetHardNet:/home kornia_img:0.1```


## Run KeyNetAffNetHardNet
```> python KeyNetAffNetHardNet.py```
