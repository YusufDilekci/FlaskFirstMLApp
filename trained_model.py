import numpy as np
import tensorflow as tf
from keras.preprocessing import image





def predict_model(filename):
    new_model = tf.keras.models.load_model('cat_dog_model.h5')
    img = image.load_img(filename, target_size=(150,150))
    x = image.img_to_array(img)
    x = x / 255
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    prediction = new_model.predict(images, batch_size=10)[0,0]
    result = round(prediction, 2)
    return f"Bu {1 - result} oraninda bir kedidir." if prediction < 0.5 else f"Bu {result} oraninda bir köpektir." 
