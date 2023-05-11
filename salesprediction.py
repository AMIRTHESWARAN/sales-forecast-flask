from flask import jsonify
import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta
import re
def notValEmail(mail):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if(re.fullmatch(regex, mail)):
        return False
    return True

def predict_sales(csv_file, fromdate, todate):
    # Load data from CSV file
    from_date = datetime.strptime(fromdate, "%m %Y") 
    to_date =  datetime.strptime(todate, "%m %Y")
    df = pd.read_csv(csv_file)
    df = df.loc[:, ['Order_Date', 'Sales']]
    df.to_csv('my_dat.csv', index=False)

    # Convert date column to datetime format
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df = df.dropna()
    df.to_csv('my_data.csv', index=False)

    # Filter data between from_date and to_date
    # mask = (df['Order_Date'] >= from_date) & (df['Order_Date'] <= to_date)
    # df = df.loc[mask]
    df.to_csv('my_dataDate.csv', index=False)

    # Rename columns to fit Prophet requirements
    df = df.rename(columns={'Order_Date': 'ds', 'Sales': 'y'})
    df.to_csv("pre.csv", index=False)
    # Train Prophet model on sales data
    model = Prophet()
    model.fit(df)
    
    # Generate future date range
    # future = list()
    # for i in range(1, 13):
    #     date = '1968-%02d' % i
    #     future.append([date])
    # future = pd.DataFrame(future)
    # future.columns = ['ds']
    # future['ds']= datetime.strptime(future['ds'])

    # future = model.make_future_dataframe(periods=365)
    # future = future.loc[(future['ds'] >= from_date) & (future['ds'] <= to_date)]
    future = []
    for d in range((to_date - from_date).days + 1):
        current_date = from_date + timedelta(d)
        future.append([current_date])
    future = pd.DataFrame(future)
    future.columns = ['ds']

    # Make predictions using trained model
    forecast = model.predict(future)
    forecast['yhat'] = forecast['yhat'].round(2)
    # forecast['ds'] = 
    date = forecast['ds'].tolist()
    price = forecast['yhat'].tolist()
    # forecast.to_csv("future.csv", index=False)
    data = {'date': date, 'price': price}
    # Return predicted graph points as a pandas DataFrame

    return jsonify(data)
