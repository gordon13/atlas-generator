# Atlas generator
Texture atlas generator. Takes independant images and packs them into a single image. It then creates a json file containing the name of each image along with pertinent information about each e.g. image width/height and x/y position in the atlas.

This allows you to work on your texture assets as independant files and combine them later for performance purposes.

# Requirements
Python 2.x

PIL

# Instructions
1. Create a folder where you want to do the atlas creation and copy the script to it.
2. Add the images you want to combine 
3. A a folder called "generated"
4. Run script
5. Check the "generated folder for your texture and json files

Note: the packing algorithm isn't particularly smart. You may need to adjust the "size" variable to change the final texture size 
