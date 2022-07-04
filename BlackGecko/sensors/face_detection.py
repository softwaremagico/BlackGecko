from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import numpy
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
		#self.video_capture = cv2.VideoCapture(0)
		#self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, ConfigurationReader._frame_width)
		#self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, ConfigurationReader._frame_heigh)
		#self.video_capture.set(cv2.CAP_PROP_FPS, 5)

		# Initialize the picam
		try:
			self.camera = PiCamera()
		except picamera.exc.PiCameraMMALError :
			raise BusyCamera("Camera already in use!")	


		self.camera.resolution = (ConfigurationReader._frame_width, ConfigurationReader._frame_heigh)
		self.camera.framerate = 5
		self.rawCapture = PiRGBArray(self.camera, size=(ConfigurationReader._frame_width, ConfigurationReader._frame_heigh))

		# Allow the camera to warmup
		self.camera.start_preview()
		time.sleep(0.1)

		

	def detect(self, output_file, time_of_capture):
		print("Detecting.....")
		time_duration = time.time() + time_of_capture
		best_face_size = 0
		
		store_raw_image = True
		while (time.time() < time_duration):
			# Capture frame-by-frame
			with picamera.array.PiRGBArray(self.camera) as stream:
				self.camera.capture(stream, format='bgr')
				frame = stream.array
				if ConfigurationReader._rotate_image != 0 :
					frame = self.rotate_image(frame)

			#Send at least first image in RGB if no face has been detected
			if(store_raw_image) :
				#Convert BGR to RGB
				cv2.imwrite(output_file, frame[:, :, ::-1])
				store_raw_image = False

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
					cv2.imwrite(output_file, frame[:, :, ::-1])
					
			
			# Display the resulting frame
			#cv2.imshow('Video', frame)			
			#if cv2.waitKey(1) & 0xFF == ord('q'):
			#	break

		# When everything is done, release the capture
		self.camera.close()
		#self.video_capture.release()
		cv2.destroyAllWindows()

	def rotate_image(self, frame):
		image_center = tuple(numpy.array(frame.shape[0:2])/2)
		rotation_matrix = cv2.getRotationMatrix2D(image_center, ConfigurationReader._rotate_image, 1.0)
		return cv2.warpAffine(frame, rotation_matrix, frame.shape[0:2],flags=cv2.INTER_LINEAR)
				


class BusyCamera(Exception):
	def __init__(self, message):
		# Call the base class constructor with the parameters it needs
		super(BusyCamera, self).__init__(message)


if __name__ == '__main__':
	FaceDetection("./haarcascade_frontalface_default.xml")._detect("frame.jpg", 10)
