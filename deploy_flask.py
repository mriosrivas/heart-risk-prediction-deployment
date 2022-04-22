import pickle as pkl
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify

app = Flask('heart_model')
CORS(app)

file_dictVect = 'dict_vectorizer.bin'
with open(file_dictVect, 'rb') as dictVect:
    dv = pkl.load(dictVect)

file_model = 'logistic_regression.bin'
with open(file_model, 'rb') as model:
    lr = pkl.load(model)


@app.route('/predict', methods=['POST'])
def predict():
    user = request.get_json()
    X = dv.transform([user])
    y = lr.predict_proba(X)[0][1]
    danger = y >= 0.5

    result = {'danger': bool(danger),
              'probability':float(y)}
    return jsonify(result)
    
    
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=9696)
