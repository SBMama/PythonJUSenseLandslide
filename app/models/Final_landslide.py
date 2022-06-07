import os
import cv2
from keras.models import load_model
from werkzeug.utils import secure_filename


class ClassifyImage:
    def __init__(self):
        self.model = load_model('./app/models/Land-CNN_final.h5')

    def classify(self, file, folder):
        if file:
            file = file['image']
            patt = os.path.join(folder, secure_filename(file.filename))
            file.save(patt)
            img_12 = cv2.imread(patt, cv2.IMREAD_GRAYSCALE)
            img_12 = cv2.resize(img_12, (60, 60))
            X_12 = img_12.reshape(-1, 60, 60, 1)
            X_12 = X_12 / 255.0
            pred = self.model.predict(X_12)
            if pred < 0.5:
                return "This is a Landslide. " \
                       "Consider reporting it through our Crowd Reporting Section."
            else:
                return "This is not a Landslide"
        else:
            return "This is not a Landslide"