import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template
import json
import plotly

app = Flask(__name__)

@app.route('/plot6')
def index6():

    df = pd.read_csv('diabetes_prediction_dataset.csv')

    diabetes_data = df[df['diabetes'] == 1]
    non_diabetes_data = df[df['diabetes'] == 0]

    diabetes_counts = {
        'Smoking History': diabetes_data['smoking_history'].value_counts(),
        'Heart Disease': diabetes_data['heart_disease'].value_counts()
    }

    non_diabetes_counts = {
        'Smoking History': non_diabetes_data['smoking_history'].value_counts(),
        'Heart Disease': non_diabetes_data['heart_disease'].value_counts()
    }

    fig_diabetes_smoking = go.Figure(data=[go.Pie(labels=diabetes_counts['Smoking History'].index, values=diabetes_counts['Smoking History'].values, name='Smoking History - Diabetes')])
    fig_diabetes_heart = go.Figure(data=[go.Pie(labels=diabetes_counts['Heart Disease'].index, values=diabetes_counts['Heart Disease'].values, name='Heart Disease - Diabetes')])

    fig_non_diabetes_smoking = go.Figure(data=[go.Pie(labels=non_diabetes_counts['Smoking History'].index, values=non_diabetes_counts['Smoking History'].values, name='Smoking History - Non-Diabetes')])
    fig_non_diabetes_heart = go.Figure(data=[go.Pie(labels=non_diabetes_counts['Heart Disease'].index, values=non_diabetes_counts['Heart Disease'].values, name='Heart Disease - Non-Diabetes')])

    graphJSON_diabetes_smoking = json.dumps(fig_diabetes_smoking, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_diabetes_heart = json.dumps(fig_diabetes_heart, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_non_diabetes_smoking = json.dumps(fig_non_diabetes_smoking, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_non_diabetes_heart = json.dumps(fig_non_diabetes_heart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index10.html', graphJSON_diabetes_smoking=graphJSON_diabetes_smoking,
                           graphJSON_diabetes_heart=graphJSON_diabetes_heart,
                           graphJSON_non_diabetes_smoking=graphJSON_non_diabetes_smoking,
                           graphJSON_non_diabetes_heart=graphJSON_non_diabetes_heart)

if __name__ == '__main__':
    app.run(debug=True)
