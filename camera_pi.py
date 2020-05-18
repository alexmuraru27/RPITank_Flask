import io
import time
import picamera
from base_camera import BaseCamera

#Camera library code imported from miguelgrinberg ->https://github.com/miguelgrinberg/flask-video-streaming
class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(1)
            camera.rotation=90
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()