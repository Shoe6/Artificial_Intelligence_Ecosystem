import cv2  # We use OpenCV for this filter
import os   # This is for file path handling

def apply_sketch_filter(image_path, output_path="sketch_image.png"):
    """
    Applies a pencil sketch filter to an image using OpenCV.
    """
    try:
        # 1. Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise Exception(f"Failed to load image from {image_path}")

        # 2. Convert the image to grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Invert the grayscale image
        inverted_gray_img = 255 - gray_img

        # 4. Blur the inverted image.
        # The (21, 21) is the "kernel size" - a larger number means a stronger blur.
        blurred_img = cv2.GaussianBlur(inverted_gray_img, (21, 21), 0)

        # 5. Invert the blurred image
        inverted_blurred_img = 255 - blurred_img

        # 6. This is the "Dodge" blend that creates the sketch.
        # We divide the original grayscale by the inverted-blurred image.
        pencil_sketch = cv2.divide(gray_img, inverted_blurred_img, scale=256.0)

        # 7. Save the final sketch
        cv2.imwrite(output_path, pencil_sketch)
        
        print(f"Processed image saved as '{output_path}'.")

    except Exception as e:
        print(f"Error processing image: {e}")

# --- This is the main part of the script that runs ---
if __name__ == "__main__":
    print("Pencil Sketch Processor (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename (or 'exit' to quit): ").strip()
        
        if image_path.lower() == 'exit':
            print("Goodbye!")
            break
            
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            continue
            
        # Create a new output name, e.g., "pic_sketch.png"
        base, ext = os.path.splitext(image_path)
        output_file = f"{base}_sketch{ext}"
        
        # Run our new sketch function
        apply_sketch_filter(image_path, output_file)