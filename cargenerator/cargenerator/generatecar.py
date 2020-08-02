import toml
import argparse
import tqdm
import os
import sys
from shutil import copytree, copyfile
import glob



def generate_car():
        
    #This code sets up the parser for command line arguments specifying parameters for generating your new car.
    parser=argparse.ArgumentParser()
    parser.add_argument('--config', 
            action='store', 
            default='config.toml', 
            help='specify a car configuration or use the default config.toml')
    parser.add_argument('--output_dir', 
            action='store', 
            default='', 
            help='specifies an output directory or use the default directoy of the car name')
    parser.add_argument('--name', 
            action='store', 
            default='', 
            help='specify a car name or use a random name')

    args=parser.parse_args()
    print(args)

    # load car configuration into memory
    car = toml.load(args.config, _dict=dict)

    #check args and apply
    if args.name != '':
            NAME = args.name
    else:
            NAME = car["Name"]
    print("CarName: ",NAME)

    if args.config != '':
            CONFIG = args.config
    else:
            CONFIG = "config.toml"
    print("Config File: ",CONFIG)

    if args.output_dir != '':
            OUTPUT_DIR = args.output_dir + NAME
    else:
            OUTPUT_DIR = NAME
    print("OUTPUT_DIR: ", OUTPUT_DIR)

    # create the directory and copy necessary files

    print(car["computer"]["kind"])
    print(car["arduino"]["kind"])
    print(car["camera"]["kind"])


    copytree(car["src"]["default_car_dir"], OUTPUT_DIR)

    # get car Runner

    # cp ../cars/templatecar/serices.* OUTPUT_DIR/python/
    # copytree("../cars/templatecar/services/*", OUTPUT_DIR+"/services", ignore=["services"])

    for file in glob.glob(car["src"]["default_car_dir"] + " /services/*"):
        print(f"source: {file}")
        print(f"file: {os.path.basename(file)}")
        print(f"dest: {OUTPUT_DIR}/services/")
        copyfile(file, OUTPUT_DIR + "/services/" + os.path.basename(file))



    outfile = open(OUTPUT_DIR + "/" + CONFIG, 'w')
    toml.dump(car, outfile)
    outfile.close()

if __name__ == "__main__":
    generate_car()

