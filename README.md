# NOTE
This repository is under construction. Only the scripts under the target triangulatation folder are ready to be used.

# COLMAP_scripts
This repository contains some scripts to extend "COLMAP 3.6 and 3.7" (https://colmap.github.io/) functionalities. If you find these scripts useful, please consider citing the paper for which these scripts were developed:

```
@Article{isprs-archives-XLVI-2-W1-2022-73-2022,
AUTHOR = {Bellavia, F. and Morelli, L. and Menna, F. and Remondino, F.},
TITLE = {IMAGE ORIENTATION WITH A HYBRID PIPELINE ROBUST TO ROTATIONS AND WIDE-BASELINES},
JOURNAL = {The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences},
VOLUME = {XLVI-2/W1-2022},
YEAR = {2022},
PAGES = {73--80},
URL = {https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLVI-2-W1-2022/73/2022/},
DOI = {10.5194/isprs-archives-XLVI-2-W1-2022-73-2022}
}
```

To replicate the results obtained in the paper, you have to match the keypoints found with the various feature extractors tested (see the related projects on GitHub), generate the sparse model with COLMAP and run the main.py script contained in the TargetTriangulation repository.
Repository for the hand-crafted methods (SIFT, SURF and AKAZE):

Repositories for the learning-based methods:
https://github.com/vcg-uvic/lf-net-release
https://github.com/rpautrat/SuperPoint
https://github.com/naver/r2d2
https://github.com/axelBarroso/Key.Net
https://github.com/lzx551402/ASLFeat

Others interesting learning-based keypoint extractors not tested in the paper:
https://github.com/kimphys/UnsuperPoint.pytorch
https://github.com/TRI-ML/KP2D
https://github.com/ignacio-rocco/sparse-ncnet

Many other interesting projects related to image matching:
https://github.com/shamangary/awesome-local-global-descriptor

# Target triangluation
This folder contains a script useful to triangulate targets marked on images starting from a COLMAP sparse cloud. Edit the config.py file to set the input/output paths, then run the "main.py" script.
NOTE: This script manage only numerical target ID.

### Create a conda environment named opencv
Open Anaconda prompt as administrator
```
>conda create --name opencv
>conda activate opencv
>conda install -c conda-forge opencv
>conda install -c anaconda pandas
>conda install -c conda-forge matplotlib
```

### Usage
Set inputs and options in the config.py file. See the script for more details.
```
>conda activate opencv
>python main.py
```

### Notes
*All images in ./input/imgs must be registered in the sparse model

# Other functionalities
Untill now only the scripts in the target triangulation folder are ready to be used. We are updating the other scripts.



...
