#!/bin/bash

mkdir -p ycb_grasps

# If you get Impot failed, install dos2unix and convert the prepared_ycb_objects.txt file
while read obj; do
  echo "Converting $obj"
  python -m mano_grasp.generate_grasps --change_speed --path_out ycb_grasps --models $obj
  # Wait for json file in folder
  while [ ! -f ycb_grasps/"$obj".json ]; do sleep 1; done
done <prepared_ycb_objects.txt



