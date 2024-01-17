from import_packages import *

class FaceGenerator(object):
	"""docstring for FaceGenerator."""

	def __init__(self, current_dir, encoding_outfile, face_directory_name):
		super(FaceGenerator, self).__init__()
		self.current_dir = current_dir
		self.encoding_outfile = encoding_outfile
		self.face_directory_name = face_directory_name


	def FaceImages(self, cluster_labels):
		current_dir = self.current_dir
		encoding_outfile = self.encoding_outfile
		face_directory_name = self.face_directory_name


		face_directory = os.path.join(current_dir, face_directory_name)

		if not os.path.exists(face_directory):
			os.makedirs(face_directory)

		data = pickle.loads(open(encoding_outfile, "rb").read())
		data = np.array(data)

		#checking for unique cluster labels from our clustering algo
		labels_unique = np.unique(cluster_labels)

		for i,d in enumerate(labels_unique):
		    if d == -1:
		        labels_unique = np.delete(labels_unique,i)
		print('unique::', labels_unique)

		#checking every face of that cluster label and saving it individually
		for label in labels_unique:
			print("[INFO] faces for face ID: {}".format(label))

			face_folder = os.path.join(face_directory, "face_" + str(label))
			if not os.path.exists(face_folder):
				os.makedirs(face_folder)

			ids = np.where(cluster_labels == label)[0]
			# initialize the list of faces to include in the montage
			portraits = []
			counter = 1
			for i in ids:
				image = cv2.imread(data[i]["imagePath"])

				x,y,width,height = data[i]["loc"]
				left_x, left_y = x,y
				#end co-ordinates
				right_x, right_y = x+width, y+height
				o_top, o_right, o_bottom, o_left= left_y,right_x,right_y,left_x
				height, width, channel = image.shape
				widthMargin = 60
				heightMargin = 100
				top = o_top - heightMargin
				if top < 0:
				    top = 0

				bottom = o_bottom + heightMargin
				if bottom > height:
				    bottom = height

				left = o_left - widthMargin
				if left < 0:
				    left = 0

				right = o_right + widthMargin
				if right > width:
				    right = width

				portrait = image[top:bottom, left:right]

				if len(portraits) < 25:
					portraits.append(portrait)

				resizeUtils = ResizeUtils()
				portrait = resizeUtils.rescale_by_width(portrait, 300)

				FaceFilename = "face_" + str(counter) + ".jpg"

				face_image_path = os.path.join(face_folder, FaceFilename)
				cv2.imwrite(face_image_path, portrait)
				counter += 1
