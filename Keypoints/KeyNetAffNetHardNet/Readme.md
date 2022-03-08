## Build the Docker file

In general:
```> docker build -t ImageNam:TagName dir```

An example:
```> docker build -t kornia_img:0.1 C:\Users\User\Desktop\Luca\GitProjects\Github_3DOM\COLMAP_scripts\Keypoints```

## Run a container

```> docker run -ti --rm --name kornia_container -v C:\Users\User\Desktop\Luca\GitProjects\Github_3DOM\COLMAP_scripts\Keypoints:/home kornia_img:0.1```

## Run KeyNetAffNetHardNet
```> python KeyNetAffNetHardNet.py```
