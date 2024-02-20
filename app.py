import numpy as np
import io
from PIL import Image
import base64
import keras
from keras import backend as K
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import Flask, request, jsonify, url_for, render_template, flash

app = Flask(__name__)

def get_model():
    global model
    model = load_model('cats_and_dogs.h5')
    print(' * Model loaded!')

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image

print(" * Loading Keras model...")
get_model()

@app.route("/")
def index():
    return render_template("Index.html")

@app.route("/predict", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))

    prediction = model.predict(processed_image).tolist()

    response = {
        'prediction': {
            'dog': prediction[0][0],
            'cat': prediction[0][1]
        }
    }  
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)