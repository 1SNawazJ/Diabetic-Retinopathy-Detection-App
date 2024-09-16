from flask import Flask, render_template, request, jsonify
from PIL import Image
from tensorflow import keras
from keras.models import load_model
from keras.layers.experimental.preprocessing import Rescaling
import numpy as np
from keras.preprocessing import image as keras_image

app = Flask(__name__)

# Load the model with custom layers
model_path = 'effB3_CNN_DR_model.h5'
try:
    # Custom layers should be added to the custom_objects dictionary
    model = load_model(model_path, custom_objects={'Rescaling': Rescaling})
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    print(f"Error loading the model: {e}")

# Function to preprocess the image
def preprocess_image(img):
    img = img.resize((224, 224))  # Resize the image to match the model's input shape
    img_array = keras_image.img_to_array(img)
    img_array = img_array / 255.0
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # Read the image from the file object
        img = Image.open(uploaded_file)
        processed_img = preprocess_image(img)

        # Predict using the loaded model
        prediction = model.predict(np.expand_dims(processed_img, axis=0))
        class_names = ['Healthy', 'Mild DR', 'Moderate DR', 'Proliferate DR', 'Severe DR']
        predicted_class = class_names[np.argmax(prediction)]

        return jsonify({'prediction': predicted_class})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
