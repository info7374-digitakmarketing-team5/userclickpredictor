#import all of the required packages and libraries
from flask import Flask, render_template, request
from datetime import datetime
import clickclassifier

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_data():
    if request.method == 'POST':
        # Get user demographic inputs
        daily_time_spent = float(request.form['daily_time_spent'])
        age = int(request.form['age'])
        income = float(request.form['income'])
        daily_internet_usage = float(request.form['daily_internet_usage'])
        male = int(request.form['male'])
        date_clicked = datetime.strptime(request.form['date_clicked'], "%Y-%m-%d")
        date_clicked_ts = datetime.strptime(request.form['date_clicked'], "%Y-%m-%d")
        month = datetime.strftime(date_clicked, '%m')
        day_month = datetime.strftime(date_clicked, '%d')
        weekday = datetime.strftime(date_clicked, '%w')

    #Call the classification model function
    pred_click = clickclassifier.click_classifier(daily_time_spent, age, income, daily_internet_usage, male, month, day_month, weekday)
    #print(pred_click)

    pred_click_azure = clickclassifier.azure_classifier(daily_time_spent, age, income, daily_internet_usage, male, date_clicked_ts)
    #return the response to the results page
    return render_template('results.html', prediction = pred_click, azure_prediction = pred_click_azure)
    
if __name__ == '__main__':
    app.run(debug=True)

