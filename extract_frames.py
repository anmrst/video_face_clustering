from import_packages import *

class ResizeUtils:
    # Given a target height, adjust the image by calculating the width and resize
    def rescale_by_height(self, image, target_height, method=cv2.INTER_LANCZOS4):
        """Rescale `image` to `target_height` (preserving aspect ratio)."""
        w = int(round(target_height * image.shape[1] / image.shape[0]))
        return cv2.resize(image, (w, target_height), interpolation=method)

    # Given a target width, adjust the image by calculating the height and resize
    def rescale_by_width(self, image, target_width, method=cv2.INTER_LANCZOS4):
        """Rescale `image` to `target_width` (preserving aspect ratio)."""
        #print(image.shape)
        h = int(round(target_width * image.shape[0] / image.shape[1]))
        return cv2.resize(image, (target_width, h), interpolation=method)

class FramesGenerator:
    def __init__(self, VideoSource):
        self.VideoSource = "video/"+VideoSource

    def AutoResize(self, frame):
        resizeUtils = ResizeUtils()

        height, width, _ = frame.shape

        if height > 500:
            frame = resizeUtils.rescale_by_height(frame, 500)
            self.AutoResize(frame)

        if width > 700:
            frame = resizeUtils.rescale_by_width(frame, 700)
            self.AutoResize(frame)

        return frame

    def GenerateFrames(self, output_dir):
        cap = cv2.VideoCapture(self.VideoSource)
        _, frame = cap.read()

        fps = cap.get(cv2.CAP_PROP_FPS)
        TotalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        print("[INFO] Total Frames ", TotalFrames, " @ ", fps, " fps")
        print("[INFO] Calculating number of frames per second")

        current_dir = os.path.curdir
        output_dir_path = os.path.join(current_dir, output_dir)

        if os.path.exists(output_dir_path):
            shutil.rmtree(output_dir_path)
            time.sleep(0.5)
        os.mkdir(output_dir_path)

        CurrentFrame = 1
        FrameWrittenCount = 1
        frames_to_skip = fps 
        while CurrentFrame < TotalFrames:
            _, frame = cap.read()
            if (frame is None):
                continue

            if CurrentFrame % frames_to_skip == 0:


                frame = self.AutoResize(frame)

                filename = "frame_" + str(FrameWrittenCount) + ".jpg"
                cv2.imwrite(os.path.join(output_dir_path, filename), frame)

                FrameWrittenCount += 1

            CurrentFrame += 1

        print('[INFO] Frames extracted')
        cap.release()
