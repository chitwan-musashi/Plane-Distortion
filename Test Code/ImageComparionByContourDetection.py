import cv2
import numpy as np

# Load the undistorted image and convert to grayscale
undistorted_image = cv2.imread(r'g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Endface\End_face_complete_part1_91.5_degree.jpg')
gray_undistorted = cv2.cvtColor(undistorted_image, cv2.COLOR_BGR2GRAY)

# Apply edge detection using Canny
edges = cv2.Canny(gray_undistorted, 50, 130)

cv2.imshow("images", edges)
cv2.waitKey(0)

# Apply Hough Circle Transform to detect circles with a larger search space
circles_undistorted = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=10, param1=50, param2=30, minRadius=20, maxRadius=300000)

if circles_undistorted is not None:
    # Sort the detected circles by radius in descending order
    circles_undistorted = np.uint16(np.around(circles_undistorted))
    circles_undistorted = sorted(circles_undistorted[0], key=lambda x: x[2], reverse=True)

    # Assuming the first circle in the sorted list is the larger one
    center_x, center_y, radius = circles_undistorted[0]

    # Complete the arc of the circle by extending it outside the image boundaries
    start_angle = 0
    end_angle = 360

    # Draw the complete circle arc on the undistorted image
    circle_image = np.zeros_like(undistorted_image)
    cv2.ellipse(circle_image, (center_x, center_y), (radius, radius), 0, start_angle, end_angle, (0, 255, 0), 2)

    # Combine the original image with the circle arc image
    combined_image = cv2.addWeighted(undistorted_image, 0.5, circle_image, 0.5, 0)

    # Display the combined image
    cv2.imshow("Undistorted Image with Complete Circle Arc", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No circle detected in the undistorted image.")
    exit()


# Load the distorted image and convert to grayscale
distorted_image = cv2.imread(r'g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Endface\outer_flange_part2_bottom_92.482_degree.jpg')
gray = cv2.cvtColor(distorted_image, cv2.COLOR_BGR2GRAY)

# Apply edge detection using Canny
edges = cv2.Canny(distorted_image, 50, 130)

cv2.imshow("edges", edges)
cv2.waitKey(0)

# Find contours in the binary image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Define maximum area threshold for ellipses
min_area_threshold = 200  # Adjust this value as per your requirement
max_area_threshold = 500000000000  # Adjust this value as per your requirement

# Filter out larger contours based on the maximum area
filtered_contours = [cnt for cnt in contours if min_area_threshold < cv2.contourArea(cnt) < max_area_threshold]

# Fit ellipses to the contours
ellipse_img = distorted_image.copy()  # Create a copy of the image
for contour in filtered_contours:
    if len(contour) >= 5:
        ellipse = cv2.fitEllipse(contour)
        ellipse_area = np.pi * (ellipse[1][0] / 2) * (ellipse[1][1] / 2)
        if ellipse_area < max_area_threshold and ellipse[1][0] >= 0 and ellipse[1][1] >= 0:
            cv2.ellipse(ellipse_img, ellipse, (0, 255, 0), 2)

            # Calculate semi-major axis
            semi_major_axis = max(ellipse[1][0] / 2, ellipse[1][1] / 2)
            print("Semi-Major Axis:", semi_major_axis)

# Display the image with detected contours
cv2.imshow("Contours", ellipse_img)
cv2.waitKey(0)

# Calculate the distortion angle using the radius of the circle and semi-major axis of the ellipse
angle = 90 - np.arccos(radius/semi_major_axis) * (180 / np.pi)

print("Distortion angle: ", angle)