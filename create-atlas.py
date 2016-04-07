from PIL import Image
import json
import os

class Stacker(object):

	# Settings
	size = 2048
	start_size = size # pixels
	final_size = size # pixels
	container_prevx = 0
	container_prevy = 0


	# vars
	container = {
		"x": 0, 
		"y": 0, 
		"w": start_size, 
		"h": start_size
	}
	containers = [container] # store the container dimensions where images can go
	packed_arr = [] # store custom image object that cotaines the image, dimensions and 
					# position on the packed image
		
	"""
	Takes images in parent folder and generates an atlas image as well as the json data
	"""
	def generate_atlas_from_images(self):

		# vars
		data = {} # used for json generation
		images = [] # used to store the raw images
		path = os.path.dirname(os.path.realpath(__file__))
		new_im = Image.new('RGBA', (self.final_size, self.final_size))

		# get all images in directory
		for file in os.listdir(path):
			if file.endswith((".jpeg", ".jpg", ".png")):
				im = Image.open("%s\%s"%(path, file))
				images.append((im.size, file, im))

		"""
		Sort raw images
		"""
		sorted_x = sorted(images, key=lambda tup: tup[0][0], reverse=True)
		sorted_y = sorted(images, key=lambda tup: tup[0][1], reverse=True)

		"""
		Image object array with position etc
		"""
		sorted_obj_arr = []
		last_x_pos = 0
		last_y_pos = 0
		for image in sorted_x:
			imageObj = {
				"image": image,
				"x": last_x_pos,
				"y": 0,
				"w": image[0][0],
				"h": image[0][1]
			}
			sorted_obj_arr.append(imageObj)
			last_x_pos += image[0][0]

		"""
		Main logic v2
		"""
		print("Start")
		print("=== sorted array ===")
		for im in sorted_obj_arr:
			print(im['x'], im['y'])

		print("\nContainers:")
		for im in sorted_obj_arr:
			print("\nPack input")
			print("---------------")
			print("Image Pos:%s, %s, Width:%s, %s"%(im['x'], im['y'], im['image'][0][0], im['image'][0][1]))
			self.pack(self.containers, im) # pack
			#self.containers = self.findContainers(self.packed_arr) # find containers

		"""
		# save png
		"""
		new_im.save("%s\\generated\\texture_atlas.png"%path)
		#new_im.show()
		"""
		# save json data
		"""
		self.save_json(data, self.start_size, self.start_size, path)

	def pack(self, containers, im_obj):
		print("Pack function")
		print("==============")
		num = len(containers)
		for i in range(0, num):
			c_cont = containers[i]
			if im_obj['w'] < c_cont['w'] and im_obj['h'] < c_cont['h']:
				"""
				add the image to the packed array, using the container position
				"""
				im_obj['x'] = c_cont['x']
				im_obj['y'] = c_cont['y']
				print(c_cont)
				print(im_obj)
				self.packed_arr.append(im_obj)
				"""
				Find the rest of the containers around the packed image
				"""
				new_cont1 = new_cont2 = {} # side
				new_cont1['x'] = c_cont['x'] + im_obj['w']
				new_cont1['y'] = c_cont['y']
				new_cont1['w'] = c_cont['w'] - im_obj['w']
				new_cont1['h'] = im_obj['h']

				new_cont2['x'] = c_cont['x'] # bottom
				new_cont2['y'] = c_cont['h'] + im_obj['h']
				new_cont2['w'] = c_cont['w']
				new_cont2['h'] = c_cont['h'] - im_obj['h']
				print("Countainers 1: %s"%new_cont1)
				print("Countainers 2: %s"%new_cont2)
				del containers[i]
				containers.append(new_cont1)
				containers.append(new_cont2)
			else:
				print("Image too big, switch container")
				new_container = switch_container()
				self.pack()
				continue

	def switch_container():
		pass


	def findContainers(self, packed_arr):
		pass



	def save_json(self, frames, sizex, sizey, path):
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
	stacker = Stacker()
	stacker.generate_atlas_from_images()
