"""Unzip CS2 demo rar files and extract .dem files for a subset of maps.

Arguments:
    --maps-path: Path to a .txt file where each line contains a map name. Represents the subset of maps to download
    --demorar-path: Directory containing the demo .rar files
    --output-path: Directory to store demos in
"""

import logging
import argparse
import pyunpack
import os
import shutil

from util import parse_txt_file_list


# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def config_parser() -> None:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--maps-path', type=str, required=True, 
                            help='Path to a .txt file where each line contains a map name')
    parser.add_argument('--demorar-path', type=str, required=True, 
                            help='Directory containing the demo .rar files')
    parser.add_argument('--output-path', type=str, required=True, 
                            help='Directory to store demos in')
    
    return parser.parse_args()


def unrar_and_extract_all(demorar_path: str, output_path: str) -> None:
    """Extract all demo rars at demorar_path
    
    Args:
        - demorar_path: path of the directory containing the demo rars
        - output_path: path to the output directory
    """
    
        
    for file in os.listdir(demorar_path):
        path = os.path.join(demorar_path, file)
        
        if file.endswith('.rar'):
            pyunpack.Archive(path).extractall(output_path)
    
    
def pathify(names: list[str]) -> list[str]:
    """Pathify each name in strs by lowercasing it
    and replacing spaces with dashes.
    
    Args:
        - names: a list of strings including alphnum chars and spaces
    """
    
    return [s.lower().replace(' ', '-') for s in names]
    

def filter_demos_and_maps(directory: str, maps: list[str]) -> None:
    """Filter all files at directory, keeping only .dem files on a
    map in maps.
    
    Args:
        - maps: a list of map names
        - directory: path to the directory of .dem files
    """
    
    pathified_maps = pathify(maps)
        
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        
        if not os.path.isfile(path):
            shutil.rmtree(path)
        elif not (file.endswith('.dem') and \
                any(m in file for m in pathified_maps)):
            os.remove(path)
            

if __name__ == '__main__':
    args = config_parser()
    
    if not os.path.isdir(args.output_path):
        os.makedirs(args.output_path)
        
    maps = parse_txt_file_list(args.maps_path)
    
    unrar_and_extract_all(args.demorar_path, args.output_path)
    filter_demos_and_maps(args.output_path, maps)
