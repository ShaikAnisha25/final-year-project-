import cv2
import numpy as np
import os

def process_image(image_path):
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert to grayscale
    grayScale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Black hat filter
    kernel = cv2.getStructuringElement(1, (9, 9))
    blackhat = cv2.morphologyEx(grayScale, cv2.MORPH_BLACKHAT, kernel)
    bhg = cv2.GaussianBlur(blackhat, (3, 3), cv2.BORDER_DEFAULT)

    # Binary thresholding (MASK)
    _, mask = cv2.threshold(bhg, 10, 255, cv2.THRESH_BINARY)

    # Apply inpainting
    dst = cv2.inpaint(img, mask, 6, cv2.INPAINT_TELEA)

    # Save processed image
    processed_path = image_path.replace("uploads", "processed")
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    cv2.imwrite(processed_path, dst)

    return processed_path
