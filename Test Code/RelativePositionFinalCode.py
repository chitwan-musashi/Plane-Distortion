
import cv2
import numpy as np
import os

images_folder = r'C:\Users\chitwan.singh\Plane-Distortion\Endface1'

# Filter out folders and select only image files
image_files = [
    f
    for f in os.listdir(images_folder)
    if os.path.isfile(os.path.join(images_folder, f))
    and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))
]

def detect_lines(image):
    min_line_length = 150
    # Create the LineSegmentDetector object
    lsd = cv2.createLineSegmentDetector()

    # Detect line segments in the image
    lines, _, _, _ = lsd.detect(image)

    # Filter out lines based on the minimum line length
    filtered_lines = []
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) >= min_line_length:
                    filtered_lines.append(line)

    # Draw the filtered lines on the original image
    line_img = image.copy()
    if filtered_lines:
        for line in filtered_lines:
            for x1, y1, x2, y2 in line:
                pt1 = (int(x1), int(y1))
                pt2 = (int(x2), int(y2))
                cv2.line(line_img, pt1, pt2, (0, 0, 255), 2)

    # Display the image with detected lines
    cv2.imshow("Detected Lines", line_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return filtered_lines


def line_angles(image, orientation):
    lines = detect_lines(image)
    angles_list = []
    if orientation == 'horizontal':
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                    if 0 <= angle <= 45:                    # or (135 < angle <= 225)
                        angles_list.append(angle)
                    elif 135 < angle <= 225:
                        angle = 180 - angle
                        angles_list.append(angle)
                    elif 315 < angle <= 360:
                        angle = angle - 360
                        angles_list.append(angle)
        if len(angles_list) > 0:
            # Calculate the average angle of inclination
            avg_angle = np.mean(angles_list)
            return avg_angle
        

    elif orientation == 'vertical':
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                    if 45 < angle <= 135:
                        angle = 90 - angle
                        angles_list.append(angle)
                    elif 225 < angle <= 315:
                        angle = 270 - angle
                        angles_list.append(angle)
        if len(angles_list) > 0:
            # Calculate the average angle of inclination
            avg_angle = np.mean(angles_list)
            return avg_angle

    else:
        print("Wrong Input Orientation!")
        orientation = str(input("Re-enter orientation ('vertical' or 'horizontal'): "))
        line_angles(image, orientation)
        


# Process each image

for image_file in image_files:
    if "_left_bottom_" in image_file:
        left_image = cv2.imread(os.path.join(images_folder, image_file))
        left_gray = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
        left_distortion_angle = line_angles(left_gray, 'vertical')
        print("Plane distortion in the left bottom image: " + str(left_distortion_angle) + " degrees")

    elif "_right_bottom_" in image_file:
        right_image = cv2.imread(os.path.join(images_folder, image_file))
        right_gray = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)
        right_distortion_angle = line_angles(right_gray, 'vertical')        
        print("Plane distortion in the right bottom image: " + str(right_distortion_angle) + " degrees")

    elif "_bottom_" in image_file:
        bottom_image = cv2.imread(os.path.join(images_folder, image_file))
        bottom_gray = cv2.cvtColor(bottom_image, cv2.COLOR_BGR2GRAY)
        bottom_distortion_angle = line_angles(bottom_gray, 'horizontal')
        print("Plane distortion in the bottom image: " + str(bottom_distortion_angle) + " degrees")

    elif "_top_" in image_file:
        top_image = cv2.imread(os.path.join(images_folder, image_file))
        top_gray = cv2.cvtColor(top_image, cv2.COLOR_BGR2GRAY)
        top_distortion_angle = line_angles(top_gray, 'horizontal')
        print("Plane distortion in the top image: " + str(top_distortion_angle) + " degrees")

    else:
        image = cv2.imread(os.path.join(images_folder, image_file))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(image_file)
        orientation = str(input("Orientation of lines to use (vertical or horizontal): "))
        distortion_angle = line_angles(gray, orientation)
        print("Plane distortion in the given image: " + str(distortion_angle) + " degrees")
    
if left_distortion_angle is not None and right_distortion_angle is not None:
    difference_angle = left_distortion_angle - right_distortion_angle
    print("The left side is relatively distorted at an angle of " + str(difference_angle) + " degrees wrt the right side")

if top_distortion_angle is not None and bottom_distortion_angle is not None:
    difference_angle_top = top_distortion_angle - bottom_distortion_angle
    print("The top side is relatively distorted at an angle of " + str(difference_angle_top) + " degrees wrt the bottom side")
