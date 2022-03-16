### MNI_TO_BRODMANN

Simple script to obtain brain areas of different hierachies from
 either normalized MNI coordinates or talairach coordinates. 
 Works by first converting MNI to talairach coordinates and then using the talairach client 
 (as found under talairach.org/client) to obtain brain areas.
 
### Requirements

* Talairach Client, downloadable from http://www.talairach.org/talairach.jar
* \>= Java 1.4

### Instructions

You will need a tab delimited text/csv file with only the (x,y,z) coordinates per electrode.
Each electrode should be indicated by a newline (see coordinates.txt for an example file).

Then, run main.py with the following arguments

* -coords: Path to file with coordinates
* -tal_file: Path for saving intermediate talairach coordinates. Default is `tal_coords.txt`
* -client: Path to talairach client
* -tal: Optional parameter. Use if passed coordinates are already talairach.
* -cube_range: Cube range around coordinates for which regions are outputted. 
See www.talairach.org/manual for more info. Default value is `3`.

## Example

From within this repo, run

    python main.py -coords coordinates.txt -client path_to_client -tal_file delete_me_later.txt
    
