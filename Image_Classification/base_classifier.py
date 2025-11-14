import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
from tensorflow.keras.models import Model
import traceback

# This is the critical layer name for MobileNetV2.
LAST_CONV_LAYER_NAME = "out_relu"

model = MobileNetV2(weights="imagenet")

# This function generates the Grad-CAM heatmap.
def generate_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    grad_model = Model(
        inputs=model.inputs,
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

# --- This is the main function ---
def classify_image(image_path):
    try:
        # --- PREPARE IMAGE ---
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array_processed = preprocess_input(img_array.copy())
        img_array_expanded = np.expand_dims(img_array_processed, axis=0)

        # --- GET PREDICTIONS ---
        predictions = model.predict(img_array_expanded, verbose=0) # verbose=0 HIDES the progress bar
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        print("\nTop-3 Predictions for", image_path)
        for i, (_, label, score) in enumerate(decoded_predictions):
            print(f"   {i + 1}: {label} ({score:.2f})")

        # --- GENERATE AND SAVE GRAD-CAM HEATMAP ---
        heatmap = generate_gradcam_heatmap(img_array_expanded, model, LAST_CONV_LAYER_NAME)
        
        original_img = cv2.imread(image_path)
        
        if original_img is None:
            raise Exception(f"Failed to load image with OpenCV from path: {image_path}")

        heatmap_resized = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
        
        superimposed_img = heatmap_color * 0.4 + original_img * 0.6
        superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)

        output_image_path = "gradcam_output.jpg"
        cv2.imwrite(output_image_path, superimposed_img)
        
        print(f"\n   -> Grad-CAM heatmap saved to '{output_image_path}'")
    
    except Exception as e:
        # --- THIS BLOCK IS NOW CORRECTLY INDENTED ---
        print("\n--- An Error Occurred. Stopping script to show details. ---")
        raise # This will crash the program and show us the error

if __name__ == "__main__":
    print("Image Classifier (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename: ").strip()
        if image_path.lower() == "exit":
            print("Goodbye!")
            break
        classify_image(image_path)