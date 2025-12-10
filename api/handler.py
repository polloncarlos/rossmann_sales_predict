import pickle
import pandas as pd
from rossmann.Rossmann import Rossmann
from flask import Flask, request, Response, jsonify

# load model
model = pickle.load(open('/mnt/c/Users/carlo/OneDrive/repos/ds_producao/model/model_rossmann.pkl', 'rb'))

# instantiate pipeline
pipeline = Rossmann()

# initialize API
app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    try:
        test_json = request.get_json()

        if not test_json:
            return jsonify({'error': 'No input data provided'}), 400

        # convert to DataFrame
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame([test_json])
        else:
            test_raw = pd.DataFrame(test_json)

        # pipeline
        df1 = pipeline.data_cleaning(test_raw)
        df2 = pipeline.feature_engineering(df1)
        df3 = pipeline.data_preparation(df2)

        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return Response(df_response, status=200, mimetype='application/json')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run('0.0.0.0')
