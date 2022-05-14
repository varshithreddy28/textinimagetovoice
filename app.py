# from crypt import methods
from unittest import result
from flask import Flask, render_template, request,flash,redirect
import easyocr
import os
import pyttsx3
import cv2
from pygame import mixer
mixer.init()

app = Flask(__name__)

engine = pyttsx3.init()
engine.setProperty('rate', 140)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def toVoice(result):
    sentence = ' Text is :               '
    totalAcc = 0
    c = 0
    for (bbox, text, prob) in result:
        sentence += f'{text} '
        totalAcc+=prob*100
        c+=1
    print(sentence)
    # Voice 
    engine.save_to_file(sentence, './static/audio.mp3')
    return engine.runAndWait()
    # engine.stop()
    # print("COMPLETED")
    # return sentence

def convertToVoice():
    img_path = './images/convert.jpg'
    img = cv2.imread(img_path)
    
    # Image PreProcessing : 
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    reader = easyocr.Reader(['en'],gpu=True)
    result = reader.readtext(img_gray)
    if result:
        toVoice(result)
    else:
        print("Unable to extract text from Image")

@app.route("/",methods=["POST","GET"])

def home():
    if request.method == 'GET':
        return render_template('index.html')

@app.route("/upload",methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
        os. mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
        print(request.files.getlist("fłle"))
        for upload in request.files.getlist("file"):
            print (upload)
            print("{} is the file name".format (upload.filename))
            filename = upload.filename
            destination = "/".join([target, "convert.jpg"])
            print ("Accept incoming file:", filename)
            print ("Save it to:", destination)
            upload.save(destination)
        
    convertToVoice()
    
    return render_template("convertion.html")



if __name__ == " __main__":
    app.run(debug=True)