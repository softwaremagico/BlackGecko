import cv2
import sys
import logging
import datetime as datetime
import time

from config import ConfigurationReader

class FaceDetection():
	
	def __init__(self, cascade_file):
		self._cascade_file = cascade_file
		self.faceCascade = cv2.CascadeClassifier(cascade_file)
		self.video_capture = cv2.VideoCapture(0)
		self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, ConfigurationReader._frame_width)
		self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, ConfigurationReader._frame_heigh)
		self.video_capture.set(cv2.CAP_PROP_FPS, 5)
		

	def _detect(self, output_file, time_of_capture):
		time_duration = time.time() + time_of_capture
		best_face_size = 0
		
		while (time.time() < time_duration):
			# Capture frame-by-frame
			ret, frame = self.video_capture.read()

			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			faces = self.faceCascade.detectMultiScale(
				gray,
				scaleFactor=1.1,
				minNeighbors=5,
				minSize=(30, 30)
				# flags=cv2.HAAR_SCALE_IMAGE
			)

			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				#Write biggest face.
				if (w*h > best_face_size):
					best_face_size = w*h
					cv2.imwrite(output_file, frame)
					
			
			# Display the resulting frame
			cv2.imshow('Video', frame)			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# When everything is done, release the capture
		self.video_capture.release()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	FaceDetection("./haarcascade_frontalface_default.xml")._detect("frame.jpg", 10)