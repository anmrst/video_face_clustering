from import_packages import *

class EncodingFaces():

    def __init__(self, current_dir, frames_dir, encodings_dir, detector, model, frames_list):
        super(EncodingFaces, self).__init__()
        self.current_dir = current_dir
        self.frames_dir = frames_dir
        self.encodings_dir = encodings_dir
        self.detector = detector
        self.model = model
        self.frames_list = frames_list

        ''' Function to encode faces present in the frames '''
    def FaceEncoding(self):

        current_dir = self.current_dir
        frames_dir = self.frames_dir
        encodings_dir = self.encodings_dir
        detector = self.detector
        model = self.model
        frames_list = self.frames_list

        frames_dir_path = os.path.join(current_dir,frames_dir)


        encodings_dir_path = os.path.join(current_dir, encodings_dir)

        frames = os.listdir(frames_dir_path)

        data = []
        encoded_files = []

        for frame in frames_list:
          st = frame.split('_')
          i = int(st[1].split('.')[0])
          print("[INFO] processing video frame".format(i))
          frame_path = os.path.join(frames_dir_path,frame)
          image_orig = cv2.imread(frame_path)

          image = cv2.cvtColor(image_orig, cv2.COLOR_BGR2RGB)
          #using the detector to detect faces in the frames
          result = detector.detect_faces(image)
          boxes = []
          encodings = []

          #for every face in the frame we are encoding
          for index,person in enumerate(result):
              bounding_box = person['box']
              x,y,width,height = person['box']
              #start co-ordinates
              left_x, left_y = x,y
              #end co-ordinates
              right_x, right_y = x+width, y+height
              #slicing the current face from main image
              current_face_image = image[left_y:right_y,left_x:right_x]
              current_face_image = cv2.resize(current_face_image, (160, 160))
              current_face_image = current_face_image.astype('float32')
              current_face_image = np.expand_dims(current_face_image, axis=0)

              #encoding a face with the model
              face_encoding = model.embeddings(current_face_image)
              face_encoding = face_encoding.flatten()

              encodings.append(face_encoding)
              boxes.append(bounding_box)


          d = [{"imagePath": frame_path, "loc": box, "encoding": enc}
              for (box, enc) in zip(boxes, encodings)]
          #saving individual encodings

          with open(os.path.join(encodings_dir_path,
                              'encodings_' + str(i) + '.pickle'), 'wb') as f:
              f.write(pickle.dumps(d))
              encoded_files.append('encodings_' + str(i) + '.pickle')
        return(encoded_files)

        ''' For Merging encodings of all video frames '''
    def MergeEncodings(self, encoding_outfile, files_processed):
      current_dir = self.current_dir
      encodings_dir = self.encodings_dir

      pickle_data = []
      pickle_files = []

      encodings_dir_path = os.path.join(current_dir, encodings_dir)
      #for file in os.listdir(encodings_dir_path):
      for file in range(1,files_processed+1):

              file_name = "encodings_"+str(file)+".pickle"
              pickle_files.append(os.path.join(encodings_dir_path,file_name))

      for file in pickle_files:
          with open(file, "rb") as f:
              data = pickle.loads(f.read())
              pickle_data.extend(data)

      if os.path.exists(encoding_outfile):
          os.remove(encoding_outfile)
      time.sleep(0.5)

      with open(encoding_outfile, 'wb') as f:
          f.write(pickle.dumps(pickle_data))
