"""
This module converts normalized MNI coordinates to Talairach space.
It uses the transformation method developed and validated by the Research Imaging Center in San Antonia, TX:
http://www3.interscience.wiley.com/cgi-bin/abstract/114104479/ABSTRACT
Transformation coordinates taken from icbm2tal Matlab file found here:
https://brainmap.org/icbm2tal/
"""
import numpy as np
import subprocess
import argparse
import os


def mni2tal(elecs):
    """
    Function to convert MNI to talairach coordinates.
    Input: numpy array of (elecs,coords) format
    Output: Talairach coordinates"""

    if elecs.shape == (3, 3):
        print('Ambiguous Input shape. Assuming (No. Electrodes, 3) shape')
    elif elecs.shape[0] == 3:
        elecs = elecs.T
    elif elecs.shape[1] != 3:
        raise ValueError(
            'Wrong input dimensions: {}. Make sure that at least one dimension represents the three coordinates'.format(
                elecs.shape))
    trafo_matrix = np.array([0.9254, 0.0024, -0.0118, -1.0207,
                             -0.0048, 0.9316, -0.0871, -1.7667,
                             0.0152, 0.0883, 0.8924, 4.0926,
                             0.0000, 0.0000, 0.0000, 1.0000]).reshape(4, 4)
    affine = np.append(elecs, np.ones((elecs.shape[0], 1)), axis=1)
    tala = np.dot(affine, trafo_matrix.T)[:, :3]
    return tala


def tal2brain(file_path, client, cube_range):
    """
    Function to obtain brain areas of different hierachies. Presupposes that the Talairach daemon is installed.
    Input: Input file path, client path
    """
    # lel = subprocess.run(['java', '-cp', client, 'org.talairach.ExcelToTD', '3:{},{}'.format(cube_range, file_path)], check=True,
    lel = subprocess.run(['java', '-cp', client, 'org.talairach.ExcelToTD', '4,{}'.format(file_path)], check=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                         # capture_output=True, text=True)
    print(lel.stdout)

def main(coord_file, tal_file, client_path, tal=False, cube_range=3):
    """
    Function to call from other modules. Combining steps to convert MNI to areas
    :param coord_file: File to txt file with coordinates
    :param tal_file: Filename to save talairach coordinates to
    :param client_path: Path to talairach client
    :param tal: Bool indicating whether coordinates are already talairach
    :param cube_range: Range around point for which regions are outputted
    :return:
    """
    # read in our coords:
    elecs = []
    with open(coord_file, 'r') as f:
        for line in f:
            elecs.append([float(s) for s in line.split('\t')])  # assuming tab delimited coordinate file

    # now, convert to talairach if needed
    if tal:
        tal_elecs = np.asarray(elecs)
    else:
        tal_elecs = mni2tal(np.asarray(elecs))

    # save them to file
    tal_file = os.path.splitext(coord_file)[0] + '_tal.txt'
    with open(tal_file, 'w') as f:
        np.savetxt(f, tal_elecs, delimiter='\t', fmt='%.2f')

    # call client to recieve area info stuff
    tal2brain(tal_file, client_path, cube_range)
    brod_file = os.path.splitext(coord_file)[0] + '_brod_areas.txt'
    os.rename('./{}.td'.format(tal_file), brod_file)
    print('Done. Output file can be found under {}'.format(brod_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-coords", help="Path to MNI coordinates txt file")
    parser.add_argument("-tal_file", help="File path to write talairach coordinates to. Needed for client",
                        default='tal_coords.txt')
    parser.add_argument("-client", help="Path to Talairach Client")
    parser.add_argument("-tal", help="Use if coordinates entered are already Talairach", action='store_true')
    parser.add_argument("-cube_range", help='Cube range in which to search for area.'
                                            ' See http://www.talairach.org/manual.html', default=3)
    args = parser.parse_args()
    if args.tal is not None:
        tal=True
    else:
        tal=False
    main(args.coords, args.tal_file, args.client, tal, args.cube_range)


