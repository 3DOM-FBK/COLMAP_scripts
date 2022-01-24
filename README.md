# COLMAP_scripts
This repository contains some useful scripts to extend "COLMAP 3.6" (https://colmap.github.io/) functionalities. If you find these scripts useful, please consider citing the paper for which these scripts were developed:

```
@inproceedings{bellavia2022,
	author={F. Bellavia and L. Morelli and F. Menna and F. Remondino},
	year={2022},
	title={Image orientation with a hybrid pipeline robust to rotations and wide-baselines},
	booktitle={ISPRS International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences},
	volume={xxx},
	chapter={xxx},
	pages={xxx}
}
```

To replicate the results obtained in the paper, you have to match the keypoints found with the various feature extractors tested (see the related projects on GitHub), generate the sparse model with COLMAP and run the main.py script contained in the TargetTriangulation repository.

# Target triangluation
This folder contains a script useful to triangulate targets marked on images. Edit the config.py file to set the input/output paths, then run the "main.py" script.
NOTE: This script manage only numerical target ID.

### Create a conda environment named opencv
Open Anaconda prompt as administrator
```
>conda create --name opencv
>conda activate opencv
>conda install -c conda-forge opencv
>conda install -c anaconda pandas
>conda install -c conda-forge matplotlib
>conda deactivate opencv
```

### Usage
Set inputs and options in config.py
```
>conda activate opencv
>python main.py
```

### Notes
*All images in ./input/imgs must be registered in the sparse model