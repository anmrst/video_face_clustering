from import_packages import *

class ClusterFaces(object):
    """docstring for ClusterFaces."""

    def __init__(self, encoding_outfile):
        super(ClusterFaces, self).__init__()
        self.encoding_outfile = encoding_outfile

    def cluster(self):
        encoding_outfile = self.encoding_outfile

        if not (os.path.isfile(encoding_outfile) and os.access(encoding_outfile, os.R_OK)):
            print('The input encoding file, ' +
                    str(encoding_outfile) + ' does not exists or unreadable')
            exit()

        print("[INFO] Loading encodings")
        data = pickle.loads(open(encoding_outfile, "rb").read())
        data = np.array(data)

        encodings = [d["encoding"] for d in data]

        print("[INFO] Clustering")
        cluster = DBSCAN(eps=0.4, metric="euclidean", n_jobs=-1)
        cluster.fit(encodings)

        # determine the total number of unique faces found in the video
        labels = np.unique(cluster.labels_)

        unique_faces = len(np.where(labels > -1)[0])
        print("[INFO] # unique faces in the video: {}".format(unique_faces))

        return cluster.labels_
