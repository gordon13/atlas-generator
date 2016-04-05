from PIL import Image
import json
import os

"""
Takes images in parent folder and generates an atlas image as well as the json data
"""
def generate_atlas_from_images():
	# Settings
	size = 2048
	start_size = size # pixels
	final_size = size # pixels

	# vars
	data = {}
	last_y_pos = 0
	last_x_pos = 0
	i0 = 0
	i = 0
	images = []
	path = os.path.dirname(os.path.realpath(__file__))
	new_im = Image.new('RGBA', (final_size, final_size))

	# get all images in directory
	for file in os.listdir(path):
		if file.endswith((".jpeg", ".jpg", ".png")):
			im = Image.open("%s\%s"%(path, file))
			images.append((im.size, file, im))

	sorted_x = sorted(images, key=lambda tup: tup[0][0], reverse=True)
	sorted_y = sorted(images, key=lambda tup: tup[0][1], reverse=True)


	for image in sorted_y:
		if (last_x_pos + sorted_y[i0][0][1] > start_size):
			last_x_pos = 0
			last_y_pos += sorted_y[i0][0][1]
			i0 = i

		# image[0]['position'] = last_x_pos
		# image[0]['position'] = last_y_pos

		new_im.paste(image[2], (last_x_pos, last_y_pos))


		data[image[1]] = {
			"frame": {"x":last_x_pos,"y":last_y_pos,"w":image[0][0],"h":image[0][1]},
			"rotated": "false",
			"trimmed": "false",
			"spriteSourceSize": {"x":0,"y":0,"w":image[0][0],"h":image[0][1]},
			"sourceSize": {"w":image[0][0],"h":image[0][1]}
		}
		last_x_pos += image[0][0]

		i += 1
	
	# save png
	new_im.save("%s\\generated\\texture_atlas.png"%path)

	# save json data
	save_json(data, size, size, path)



"""
Generate json file for atlas
"""
def save_json(frames, sizex, sizey, path):
	data = {
		"frames": frames,
		"meta": {
			"app": "http://www.arcticentertainment.com",
			"version": "1.0",
			"image": "texture_atlas.png",
			"format": "RGBA8888",
			"size": {"w":sizex,"h":sizey},
			"scale": "1"
		}
	}
	with open('%s\\generated\\texture_atlas.json'%path, 'w') as outfile:
		json.dump(data, outfile, indent=4)




if __name__ == '__main__':
	generate_atlas_from_images()
