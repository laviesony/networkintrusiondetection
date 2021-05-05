#import imghdr
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
import xgboost as xgb
import time
#import numpy as np
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = 'uploads'



@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
	uploaded_file = request.files['file']
	t0=time.time()
	filename = secure_filename(uploaded_file.filename)
	if filename != '':
		file_ext = os.path.splitext(filename)[1]
	if file_ext not in app.config['UPLOAD_EXTENSIONS']:
		abort(400)

	uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
	print("yes")
	model = pickle.load(open("xgb_model.pkl", "rb"))    
	new_df = pd.read_csv('uploads/'+filename)
	#X_test = np.load('X_test.npy')
	y_pred = model.predict(new_df)

	o1 = "The list contains all the predicted outputs"
	o2 = ""
	for i in y_pred:
		o2 = o2+str(i)+"\n"

	t1=time.time()
	o3=t1-t0
	return render_template('home.html', output1=o1, output2=o2,output3="Time elpased = "+str(o3))
 


@app.route('/uploads/<filename>')
def upload(filename):
	return send_from_directory(app.config['UPLOAD_PATH'], filename)




if __name__ == '__main__':
   app.run(debug = True)

