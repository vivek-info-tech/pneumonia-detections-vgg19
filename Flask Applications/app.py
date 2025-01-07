from flask import Flask, request, render_template,jsonify
from keras.api.models import load_model
import numpy as np
import cv2
from PIL import Image
import os
from werkzeug.utils import secure_filename
from keras.api.applications.vgg19 import  VGG19
from keras.api.layers import Flatten,Dense,Dropout
from keras.api.preprocessing import image


# base_model=VGG19(include_top=False,input_shape=(128,128,3),weights= "imagenet")
# x=base_model.output
# flat=Flatten()(x)
# class1=Dense(4608,activation='relu')(flat)
# dropout1=Dropout(0.2)(class1)
# class2=Dense(1152, activation='relu')(dropout1)
# dropout2=Dropout(0.2)(class2)
# output=Dense(2,activation='softmax')(class2)
# model=models.Model(base_model.inputs,output)
# model.load_weights("vgg_unfrozen.h5")




 





app=Flask(__name__)
model=load_model("./model/vgg_unfrozen.h5")

def get_className(classno):
    if classno==0:
        return 'NORMAL'
    elif classno==1:
        return "PNEUMONIA"



def getResult(file):
    img = image.load_img(file, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    return predicted_class



@app.route('/',methods=['GET'])

def home():
    return render_template('index.html')



@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
          #Ensure a file is uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
         
        base_path=os.path.dirname(__file__)
        upload_folder = os.path.join(base_path, 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)  # Create the folder if it doesn't exist
        file_path = os.path.join(upload_folder, secure_filename(file.filename))
        file.save(file_path)
        value=getResult(file_path)
        res=get_className(value)
        return jsonify({'result':res})
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
