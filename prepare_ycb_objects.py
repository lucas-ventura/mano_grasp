import os
import argparse
import pymeshlab
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Prepare objects for GraspIt')
parser.add_argument('-f', '--ybc_folder', type=str,
                    default='',
                    help="Path to ycb folder containing objects")

parser.add_argument('--graspit_dir', type=str,
                    default=os.environ['GRASPIT'],
                    help="Path to GraspIt root directory")
parser.add_argument('-sc', '--scale', default=1000, help="scales to apply to each model")
parser.add_argument('-v', '--vertices', type=int, default=16, choices=[16, 64, 512], help="Number of k vertices to use")

GRASPIT_OBJECT_XML_TEMPLATE = '<root><geometryFile type="off">{}.off</geometryFile></root>'


def main(args):
    if not os.path.isdir(args.graspit_dir):
        print('Wrong GraspIt path: "{}"'.format(args.graspit_dir))
        exit(0)

    if not args.ybc_folder:
        print('YBC folder path not specified')
        exit(0)

    object_names = []
    for obj_name in tqdm(os.listdir(args.ybc_folder)):
        obj_pth = os.path.join(args.ybc_folder, obj_name, "google_{}k".format(args.vertices), 'nontextured.ply')

        if os.path.exists(obj_pth):
            tqdm.write(f"Converting {obj_name}")

            # Load object
            ms = pymeshlab.MeshSet()
            ms.load_new_mesh(obj_pth)

            # Scale object
            ms.transform_scale_normalize(axisx=args.scale, uniformflag=True)

            # Save object to the objects folder in the graspit folder
            output_dir = os.path.join(args.graspit_dir, 'models/objects')
            output_pth = os.path.join(output_dir, obj_name + '.off')
            ms.save_current_mesh(output_pth, save_face_color=False)

            # Save xml file
            xml_path = os.path.join(output_dir, obj_name + '.xml')
            with open(xml_path, 'w') as xml_file:
                xml_file.write(GRASPIT_OBJECT_XML_TEMPLATE.format(obj_name))

            object_names.append(obj_name)

        else:
            tqdm.write(f"Can't find nontextured file for {obj_name}")

    with open("prepared_ycb_objects.txt", 'w') as f:
        for object_name in object_names:
            f.write('%s\n' % object_name)


if __name__ == '__main__':
    main(parser.parse_args())
