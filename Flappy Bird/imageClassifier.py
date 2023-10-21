import gradio as gr
import tensorflow as tf
import numpy as np
import requests
#load the model
inception_net = tf.keras.applications.InceptionV3()
#inceptionV3 categorises the images data set

response = requests.get("https://git.io/JJkYN")
labels = response.text.split("\n")

def classify_image(inp):
    inp=inp.reshape((-1,299,299,3))
    inp=tf.keras.applications.inpcetion_v3.preprocess_input(inp)
    prediction=incpetion_net.predict(inp).flatten()
    return {labels[i]:float(prediction[i])for i in range(1000)}

image=gr.inputs.Image(shape=(299,299))
label=gr.outputs.Label(num_top_classes=3)
gr.Interface(fn=classify_image,inputs=image,outputs=label,capture_session=True).launch()