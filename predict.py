from flask import Flask
from flask import Flask, render_template, request
import pickle
import sklearn
import numpy as np
try:
    model_KNN = pickle.load(open('parkinson_KNN.pkl', 'rb'))
    model_LG = pickle.load(open('parkinson_LG.pkl', 'rb'))
    model_RFC = pickle.load(open('parkinson_RFC.pkl', 'rb'))
    model_SVC = pickle.load(open('parkinson_SVC.pkl', 'rb'))
    model_XGBC = pickle.load(open('parkinson_XGBC.pkl', 'rb'))
except FileNotFoundError as e:
    print(e)
app = Flask(__name__)
@app.route("/", methods = ['GET'])
def index():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def prediction():
    if request.method == 'POST':
        mdvp_fo = float(request.form['Median pitch'])
        mdvp_fhi = float(request.form['Maximum pitch'])
        mdvp_flo = float(request.form['Minimum pitch'])
        mdvp_jitter_per = float(request.form['Jitter (local)'])
        mdvp_jitter_abs = float(request.form['Jitter (local, absolute)'])
        mdvp_rap = float(request.form['Jitter (rap)'])
        mdvp_ppq = float(request.form['Jitter (ppq)'])
        jitter_ddp = float(request.form['Jitter (ddp)'])
        mdvp_shimmer = float(request.form['Shimmer (local)'])
        mdvp_shimmer_db = float(request.form['Shimmer (local,dB)'])
        shimmer_apq3 = float(request.form['Shimmer (apq3)'])
        shimmer_apq5 = float(request.form['Shimmer (apq5)'])
        mdvp_apq = float(request.form['Shimmer (apq)'])
        shimmer_dda = float(request.form['Shimmer (dda)'])
        nhr = float(request.form['Mean noise-to-harmonics ratio'])
        hnr = float(request.form['Mean harmonics-to-noise ratio'])


    output = model_RFC.predict(np.array([[mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter_per, mdvp_jitter_abs, mdvp_rap,
                                          mdvp_ppq, jitter_ddp, mdvp_shimmer, mdvp_shimmer_db, shimmer_apq3,
                                          shimmer_apq5, mdvp_apq, shimmer_dda, nhr, hnr]]))
    res = ""
    if output == 1:
        res = "You are in risk"
        return render_template('Prediction', predict_res=res)
    else:
        res = "You are risk free"
        return render_template('Prediction_RF', predict_res=res)


@app.route("/result", methods=['GET'])
def result():
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()