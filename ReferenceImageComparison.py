import cv2
import numpy as np

def detect_distortion(reference_image_path, new_image_path):
    # Load the undistorted reference image and the new image to be checked for distortion
    reference_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
    new_image = cv2.imread(new_image_path, cv2.IMREAD_GRAYSCALE)

    # Detect keypoints and extract descriptors for the reference and new images
    sift = cv2.SIFT_create()
    kp_ref, des_ref = sift.detectAndCompute(reference_image, None)
    kp_new, des_new = sift.detectAndCompute(new_image, None)

    # Match keypoints between the reference and new images
    matcher = cv2.BFMatcher()
    matches = matcher.match(des_ref, des_new)

    # Extract matched keypoints from both images
    points_ref = np.float32([kp_ref[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    points_new = np.float32([kp_new[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Estimate affine transformation between the reference and new images
    transformation_matrix, _ = cv2.estimateAffine2D(points_ref, points_new)

    # Calculate distortion angles in x and y axes
    angle_x = np.degrees(np.arctan2(transformation_matrix[1, 0], transformation_matrix[0, 0]))
    angle_y = np.degrees(np.arctan2(transformation_matrix[0, 1], transformation_matrix[1, 1]))

    # Calculate distortion values in x and y axes
    distortion_x = np.sqrt(transformation_matrix[0, 0]**2 + transformation_matrix[1, 0]**2) - 1.0
    distortion_y = np.sqrt(transformation_matrix[0, 1]**2 + transformation_matrix[1, 1]**2) - 1.0

    # Calculate overall distortion angle
    angle_overall = np.degrees(np.arctan2(transformation_matrix[1, 0], transformation_matrix[0, 0]))

    # Draw keypoints on the reference image and new image
    img_ref = cv2.cvtColor(reference_image, cv2.COLOR_GRAY2BGR)
    img_new = cv2.cvtColor(new_image, cv2.COLOR_GRAY2BGR)
    cv2.drawKeypoints(img_ref, kp_ref, img_ref)
    cv2.drawKeypoints(img_new, kp_new, img_new)

    # Display the reference image and new image with keypoints
    cv2.imshow("Reference Image", img_ref)
    cv2.imshow("New Image", img_new)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return distortion_x, distortion_y, angle_x, angle_y, angle_overall


# File paths of the undistorted reference image and the new image to be checked for distortion
reference_image_path = r'g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Endface\outer_flange_part1_bottom_92.482_degree.jpg'
new_image_path = r'g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Endface\outer_flange_part2_bottom_92.482_degree.jpg'

# Detect distortion
distortion_x, distortion_y, angle_x, angle_y, angle_overall = detect_distortion(reference_image_path, new_image_path)

# Print the distortion values and angles
print("Distortion in x-axis: {:.2f}".format(distortion_x))
print("Distortion in y-axis: {:.2f}".format(distortion_y))
print("Angle of distortion in x-axis: {:.2f}".format(angle_x))
print("Angle of distortion in y-axis: {:.2f}".format(angle_y))
print("Overall distortion angle: {:.2f}".format(angle_overall))
