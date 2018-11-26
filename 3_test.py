# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
import re
import matplotlib.pyplot as plt
from sys import platform
import numpy as np

# ----------count the number of files----------
def count_files():
  directory = os.path.expanduser('~') + "/opencv_test/images"
  files = os.listdir(directory)
  count = 0
  for file in files:
    index = re.search('.png', file)
    if index:
      count = count + 1
  return count

# ----------set paramaters----------
# Remember to add your installation path here
# Option a
dir_path = os.path.dirname(os.path.realpath(__file__))
if platform == "win32": sys.path.append(dir_path + '/../../python/openpose/');
else: sys.path.append('../../python');
# Option b
# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
# sys.path.append('/usr/local/python')

# Parameters for OpenPose. Take a look at C++ OpenPose example for meaning of components. Ensure all below are filled
try:
    from openpose import *
except:
    raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
params = dict()
params["logging_level"] = 3
params["output_resolution"] = "-1x-1"
params["net_resolution"] = "-1x368"
params["model_pose"] = "BODY_25"
params["alpha_pose"] = 0.6
params["scale_gap"] = 0.3
params["scale_number"] = 1
params["render_threshold"] = 0.05
# If GPU version is built, and multiple GPUs are available, set the ID here
params["num_gpu_start"] = 0
params["disable_blending"] = False
# Ensure you point to the correct path where models are located
params["default_model_folder"] = dir_path + "/../../../models/"
# Construct OpenPose object allocates GPU memory
openpose = OpenPose(params)

# ----------sample code----------
# while 1:
#   # Read new image
#   img = cv2.imread("../../../examples/media/COCO_val2014_000000000192.jpg")
#   # Output keypoints and the image with the human skeleton blended on it
#   keypoints, output_image = openpose.forward(img, True)
#   # Print the human pose keypoints, i.e., a [#people x #keypoints x 3]-dimensional numpy object with the keypoints of all the people on that image
#   print(keypoints)
#   # Display the image
#   cv2.imshow("output", output_image)
#   cv2.waitKey(15)

# ----------print keypoints once----------
#img = cv2.imread(os.path.expanduser('~') + "/opencv_test/images/img0.png")
#keypoints, output_image = openpose.forward(img, True)
#print(keypoints)
#print(keypoints.shape)
#print("detect " + str(keypoints.shape[0]) + " persons.")
##plt.imshow(output_image)
#
#plt.imshow(img)
##print(keypoints[0, :, 0])
##print(keypoints[0, :, 1])
#plt.scatter(keypoints[0, :, 0], keypoints[0, :, 1])
#plt.show()
#cv2.waitKey(0)
#
#cv2.imshow("output", output_image)
#cv2.waitKey(0)

# ----------print keypoints in for loop----------
current_num = 0 # num of persons
last_num=0 # num of last persons

# loop for all images
for i in range(0, count_files()):
  img = cv2.imread(os.path.expanduser('~') + "/opencv_test/images/img" + str(i) + ".png")
  keypoints, output_image = openpose.forward(img, True)

  cv2.imshow("output", output_image)
  print("Frame" + str(i))

  # does find new person?
  current_num = keypoints.shape[0]
  if current_num > last_num:
    print("find a new person!")
  last_num = current_num
  print("detect " + str(keypoints.shape[0]) + " persons.")

  # calculate mean coordinate
  if keypoints.shape[0] != 0: # if no person then donot calculate
    for j in range(0, keypoints.shape[0]):
      #print("x: " + str(np.average(keypoints[i, :, 0])))
      #print("y; " + str(np.average(keypoints[i, :, 1])))
      x = keypoints[j, :, 0]
      y = keypoints[j, :, 1]
      size = 0
      for k in range(0, keypoints.shape[1]):
        if not (keypoints[0, :, 0][k]==0 and keypoints[0, :, 1][k]==0):
          size = size + 1
      x_mean = np.sum(x) / size
      y_mean = np.sum(y) / size
      print("x: " + str(x_mean))
      print("y: " + str(y_mean))

  print("--------------------")
  #print("shape: " + str(keypoints.shape))
  cv2.waitKey(15)
