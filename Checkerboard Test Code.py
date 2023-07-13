import cv2
import numpy as np

# Load the image
img = cv2.imread('g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Testing\Image__2023-06-23__10-39-09.jpg')

# Define the chessboard size and pattern
chessboard_size = (3, 3)
pattern_points = np.zeros((np.prod(chessboard_size), 3), dtype=np.float32)
pattern_points[:, :2] = np.indices(chessboard_size).T.reshape(-1, 2)
object_points = []
image_points = []

# Find the corners of the chessboard pattern in the image
ret, corners = cv2.findChessboardCorners(img, chessboard_size, None)

if ret:
    # Add the corners to the image and object points lists
    image_points.append(corners)
    object_points.append(pattern_points)

    # Calibrate the camera and obtain the distortion coefficients
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, img.shape[:2], None, None)

    # Check for tangential distortion
    if abs(dist[0][1]) > 0.001 or abs(dist[0][2]) > 0.001:
        print("The image has tangential distortion.")
    else:
        print("The image does not have tangential distortion.")
else:
    print("Chessboard pattern not found in the image.")
