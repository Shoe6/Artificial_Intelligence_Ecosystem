# AI Image Processing and Classification Project

This project is designed to give you hands-on experience working with an image classifier and enhancing your programming skills using AI assistance. The project has two parts, each focused on different aspects of image classification and processing. By the end, you'll have explored fundamental concepts like Grad-CAM, image classification, and creative image filtering.


# Project 3.3: Image Classification and Processing

This project is part of the Artificial Intelligence Ecosystem course. It involves two parts:
1.  Using a pre-trained image classifier (MobileNetV2) and implementing Grad-CAM to understand its decisions.
2.  Creating a custom artistic image filter using AI assistance.

---

## Part 1: Classifier and Grad-CAM

This part of the project used the `base_classifier.py` script to classify a test image and then generate a Grad-CAM heatmap to visualize the model's "attention."

### 1. Test Image
The image used for this project was pic.png. This image is unique because it was selected by asking my AI partner (the AI assistant I worked with) to provide its own visual interpretation of "artificial intelligence." The resulting image features a glowing brain and a central eye, connected to a city and abstract data, which I then used as the test subject for the classifier.

### 2. Classifier Predictions
The `base_classifier.py` script produced the following top-3 predictions for `pic.png`:

| Rank | Prediction | Confidence Score |
| :--- | :--- | :--- |
| 1 | `jellyfish` | 0.44 (44%) |
| 2 | `bubble` | 0.43 (43%) |
| 3 | `fountain` | 0.05 (5%) |

### 3. Grad-CAM Heatmap Analysis
The model was clearly not confident, with its top two guesses being almost a 50/50 split. The `gradcam_output.jpg` heatmap was generated to understand *why*.

The analysis showed:
* The model's "hot spots" (the red/yellow areas) were focused on the **large, floating, dome-like shape** of the brain.
* This shape, being translucent and floating in a dark space, is visually very similar to both a **`jellyfish`** and a **`bubble`**, which explains the model's confusion.
* A secondary hot spot was on the **vertical stream of light** connecting the brain to the city, which explains the model's low-confidence guess of **`fountain`**.

---

## Part 2: Creating and Experimenting with Image Filters

This part of the project involved creating a new, custom image filter with AI assistance.

### 1. Basic Filter
The `basic_filter.py` script was analyzed. It demonstrated how to use the `Pillow` library to apply a simple blur filter.

### 2. New Artistic Filter: Pencil Sketch
Using `opencv-python`, a new script `new_filter.py` was created to apply a **"Pencil Sketch"** filter.

This filter works by:
1.  Converting the image to grayscale.
2.  Inverting the colors.
3.  Applying a heavy Gaussian blur to the inverted image.
4.  Using a "Color Dodge" blend to divide the original grayscale image by the blurred image, which creates the final sketch lines.

The output from this filter was saved as `pic_sketch.png`.

---

## Part 3: Reflection on AI Collaboration
> My experience working with an AI to explain and write Python code was very positive. The struggle was setting up VS to do so lol. The AI was able to provide clear, line-by-line explanations of unfamiliar code. When we encountered bugs, like the Grad-CAM file not saving, the AI was a key debugging partner, helping me methodically change the code to find and fix the silent error. It was also very effective at writing the new 'Pencil Sketch' filter from a simple English prompt, which was much faster than trying to find the code myself."