# Learning Joint Reconstruction of Hands and Manipulated Objects - ManoGrasp

Porting the [MANO](http://mano.is.tue.mpg.de/) hand model to [GraspIt!](http://graspit-simulator.github.io/) simulator

Yana Hasson, Gül Varol, Dimitris Tzionas, Igor Kalevatykh, Michael J. Black,  Ivan Laptev, Cordelia Schmid, CVPR 2019

- [Project page](https://hassony2.github.io/obman)

## Install

### Setup ROS interface

This package uses a ROS [interface](https://github.com/graspit-simulator/graspit_commander) for the GraspIt! simulator.

To install and setup this interface follow the instructions at https://github.com/graspit-simulator/graspit_interface.

### Install package

```
git clone https://github.com/ikalevatykh/mano_grasp.git
cd mano_grasp
python setup.py install --user --graspit_dir=$GRASPIT
```

## Model

Model ManoHand will be automatically copied to $GRASPIT directory during the installation.

To copy a model without the code installation use the command:

    python setup.py --copy_model_only --graspit_dir=$GRASPIT


## Prepare objects

Make sure you have meshlab installed:

    sudo apt install meshlab

To prepare object files (.obj, .stl, .ply, .off) for graspit:

    python -m mano_grasp.prepare_objects --models_folder /PATH/TO/YOURDATASET/ --file_out YOURDATASET_objects.txt

Usually you want to apply some scaling to the objects to fit the hand, therefore append scales options:

    --scales 1000

Use 

    python -m mano_grasp.prepare_objects --help

to see all available options.


## Generate grasps

Start [ROS master](http://wiki.ros.org/roscore) in one terminal:

    roscore

Then in a second terminal start generator:

    python -m mano_grasp.generate_grasps --models_file YOURDATASET_objects.txt --path_out PATH_TO_DATASET

Use 

    python -m mano_grasp.generate_grasps --help

to see all available options.

# Generate grasps from YBC dataset
First, we will need to dowload the dataset with the script provided here: https://github.com/sea-bass/ycb-tools/blob/main/download_ycb_dataset.py

## Downloading YCB objects
### Modification to the download_ycb_dataset.py
- Add `.decode('utf-8')` at the end of line 25
```diff
-    html = response.read()
+    html = response.read().decode('utf-8')
```

- Change line 35: 
```diff
-    files_to_download = ["berkeley_processed", "google_16k"]
+    files_to_download = ["google_16k"] # You can also use google_64k or google_512k
```

You can now download the models with the script with the following command:
```python
python download_ycb_dataset.py
```

## Convert objects for graspIt
``prepare_ycb_objects.py`` will scale the objects and genreate the necessary off and xml files for graspIt.
```python
python prepare_ycb_objects.py --ycb_folder PATH_TO_YCB_FOLDER --graspit_dir=$GRASPIT
```

## Generate grasps
``./generate_ycb_grasps.sh`` will create a ycb_grasps folder and save the generated json files there.
```console
foo@bar:~/graspit_ros_ws/src/mano_grasp$ ./generate_ycb_grasps.sh
```

# Citations

If you find this code useful for your research, consider citing:

```
@INPROCEEDINGS{hasson19_obman,
  title     = {Learning joint reconstruction of hands and manipulated objects},
  author    = {Hasson, Yana and Varol, G{\"u}l and Tzionas, Dimitris and Kalevatykh, Igor and Black, Michael J. and Laptev, Ivan and Schmid, Cordelia},
  booktitle = {CVPR},
  year      = {2019}
}
```
