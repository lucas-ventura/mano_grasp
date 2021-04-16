#!/usr/bin/env python2

import argparse
import json
import os
import time

from graspit_process import GraspitProcess
from graspit_scene import GraspitScene
from grasp_miner import GraspMiner

parser = argparse.ArgumentParser(description='Grasp mining')
parser.add_argument('-m', '--models', nargs='*', default=['glass'])
parser.add_argument('-l', '--models_file', type=str, default='')
parser.add_argument('-n', '--n_jobs', type=int, default=1)
parser.add_argument('-o', '--path_out', type=str, default='')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-e', '--headless', action='store_true', help="Start in headless mode")
parser.add_argument('-x',
                    '--xvfb',
                    action='store_true',
                    help="Start with Xserver Virtual Frame Buffer (Xvfb)")
parser.add_argument('--graspit_dir',
                    type=str,
                    default=os.environ['GRASPIT'],
                    help="Path to GraspIt root directory")
parser.add_argument('--plugin_dir',
                    type=str,
                    default=os.environ['GRASPIT_PLUGIN_DIR'],
                    help="Path to directory with a graspit_interface plugin")
parser.add_argument('-s', '--max_steps', type=int, default=0, help="Max search steps per object")
parser.add_argument('-g', '--max_grasps', type=int, default=0, help="Max best grasps per object")
parser.add_argument('--relax_fingers',
                    action='store_true',
                    help="Randomize squezzed fingers positions")
parser.add_argument('--change_speed', action='store_true', help="Try several joint's speed ratios")
parser.add_argument('-ds', '--dataset', type=str, default='', help="dataset name")


def main(args):
    if not os.path.isdir(args.graspit_dir):
        print('Wrong GraspIt path: "{}"'.format(args.graspit_dir))
        exit(0)

    if not os.path.isdir(args.plugin_dir):
        print('Wrong plugins path: "{}"'.format(args.plugin_dir))
        exit(0)

    if args.models_file and not os.path.isfile(args.models_file):
        print('File not exists: "{}"'.format(args.models_file))
        exit(0)

    if not args.path_out:
        print('Output directory not specified')
        exit(0)

    if not os.path.isdir(args.path_out):
        os.makedirs(args.path_out)

    if not args.models_file and args.models:
        models = args.models
    else:
        with open(args.models_file) as f:
            models = f.read().splitlines()

    proccess = GraspitProcess(graspit_dir=args.graspit_dir,
                              plugin_dir=args.plugin_dir,
                              headless=args.headless,
                              xvfb_run=args.xvfb,
                              verbose=args.verbose)

    generator = GraspMiner(graspit_process=proccess,
                           max_steps=args.max_steps,
                           max_grasps=args.max_grasps,
                           relax_fingers=args.relax_fingers,
                           change_speed=args.change_speed)

    if args.n_jobs > 1:
        from joblib import Parallel, delayed
        grasps = Parallel(n_jobs=args.n_jobs, verbose=50)(delayed(generator)(m) for m in models)
    else:
        grasps = [generator(body) for body in models]

    for body_name, body_grasps in grasps:
        print('{}: saving {} grasps'.format(
            body_name,
            len(body_grasps),
        ))
        with open(os.path.join(args.path_out, '{}.json'.format(body_name)), 'w') as f:
            scale = 1
            split = body_name.split('_scale_')
            if len(split) > 1:
                scale = float(split[1])
            object_id = split[0]
            grasps_description = {
                'grasps': body_grasps,
                'dataset': args.dataset,
                'object_scale': scale,
                'object_cat': '',
                'object_id': object_id
            }
            json.dump(grasps_description, f)

    if args.debug:
        with GraspitProcess(graspit_dir=args.graspit_dir, plugin_dir=args.plugin_dir) as p:
            for body_name, body_grasps in grasps:
                scene = GraspitScene(p.graspit, 'ManoHand', body_name)
                for grasp in body_grasps:
                    scene.grasp(grasp['pose'], grasp['dofs'])
                    time.sleep(5.0)


if __name__ == '__main__':
    main(parser.parse_args())
