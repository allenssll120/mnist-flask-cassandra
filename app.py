from flask import Flask,request
import cv2
import time
import argparse
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import record
from redis import Redis,RedisError
#import os
import socket
redis = Redis(host="redis",db=0,socket_connect_timeout=2,socket_timeout=2)
tf.compat.v1.disable_eager_execution()
x = tf.compat.v1.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.matmul(x, W) + b 
sess = tf.compat.v1.Session()
saver=tf.compat.v1.train.Saver()
saver.restore(sess,'saver/model.ckpt')
    
app = Flask(__name__)
@app.route('/')
#@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    file = request.files['file']
    filename=secure_filename(file.filename)
    im = cv2.imread(filename,cv2.IMREAD_COLOR).astype(np.float32)
    im = cv2.resize(im,(28,28),interpolation=cv2.INTER_CUBIC)
    img_gray = (im - (255 / 2.0)) / 255
    x_img = np.reshape(img_gray , [-1 , 784])
    output=sess.run(y ,feed_dict={x:x_img})
    result = str(np.argmax(output))
    t=int(round(time.time()*1000))
    date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t/1000))
    record.recordData(date,filename,result)
    return "The prediction of picture is:"+result
  
if __name__ == '__main__':
    app.run(host='localhost', port=33)
    record.createKeySpace()