''' Importing required libraries/packages for the project '''
from import_packages import *

if __name__ == "__main__":

    ''' Defining variables used in the project '''
    current_dir = os.getcwd()
    frames_dir = 'Frames'
    encodings_dir = "Encodings"
    encoding_outfile = "encodings.pickle"
    face_directory_name = "ClusteredFaces"
    montage_name = "Montage"

    ''' Defining the model used for face detection '''
    detector = MTCNN()

    ''' Defining the model used for face recognition and encoding '''
    model = FaceNet()

    print('[INFO] Loading Video')

    ''' Dashboard runs on flask app '''

    ''' Extraction of frames from Input Video '''
    frames_generator = FramesGenerator("Footage.mp4")
    frames_generator.GenerateFrames("Frames")

    print('[INFO] Video Loaded')
    print('[INFO] DashboardRunning on http://127.0.0.1:5000')

    ''' Creating custom batch processing to process video frames in real time '''

    for root, dirs, files in os.walk(frames_dir, topdown=False):
        frames_list = []
        number_of_files = len(files)
        counter = 0
        for i in range(number_of_files):

            frames_list.append(f"frame_{i+1}.jpg")
            counter +=1

            if counter == 10 or i == number_of_files - 1:
                counter = 0
                files_processed = i+1


                ''' Encoding faces in frames '''
                encoding_faces = EncodingFaces(current_dir, frames_dir, encodings_dir, detector, model, frames_list)
                encoded_files =encoding_faces.FaceEncoding()

                ''' Merge all the batch encodings pickle files into one '''
                encoding_faces.MergeEncodings(encoding_outfile, files_processed)
                time.sleep(1)

                ''' Cluster faces using the face encodings '''
                cluster_faces = ClusterFaces(encoding_outfile)
                cluster_labels = cluster_faces.cluster()
                #print('labels_unique = ',labels)
                face_generation = FaceGenerator(current_dir, encoding_outfile, face_directory_name )
                face_generation.FaceImages(cluster_labels)

                frames_list = []
