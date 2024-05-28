from flask import Flask, jsonify, request
import numpy as np
from datetime import datetime
import yfinance as yf
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from pandas_datareader import data as pdr
from flask_cors import CORS

app = Flask(__name__)
KEY="TT43CKXJ945STF1P"
CORS(app)
# Prediction function as defined earlier
import numpy as np
import pandas as pd
import datetime
from alpha_vantage.timeseries import TimeSeries
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

def predict_stock_price(stock_symbol):
    # Your Alpha Vantage API key
    api_key = KEY
    
    # Create a TimeSeries object
    ts = TimeSeries(key=api_key, output_format='pandas')
    
    # Fetch data from Alpha Vantage
    df, meta_data = ts.get_daily(symbol=stock_symbol, outputsize='full')
    
    # Sort the dataframe so that the oldest data is first
    df = df.sort_index()
    
    # Create a new dataframe with only the 'close' column 
    data = df.filter(['4. close'])
    # Rename the column to 'Close'
    data = data.rename(columns={'4. close': 'Close'})
    
    # Convert the dataframe to a numpy array
    dataset = data.values
    # Get the number of rows to train the model on
    training_data_len = int(np.ceil(len(dataset) * .95))
    
    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    
    # Create the training data set 
    # Create the scaled training data set
    train_data = scaled_data[0:int(training_data_len), :]
    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []
    
    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
    
    # Convert the x_train and y_train to numpy arrays 
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Train the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)
    
    # Create the testing data set
    last_60_days = scaled_data[-60:]
    # Reshape the data to be 3D (samples, time steps, features)
    last_60_days = np.reshape(last_60_days, (1, last_60_days.shape[0], 1))
    
    # Get the predicted scaled price
    predicted_price_scaled = model.predict(last_60_days)
    
    # Undo the scaling
    predicted_price = scaler.inverse_transform(predicted_price_scaled)
    print("Predicted Next Day Price: ", predicted_price[0][0])
    return float(predicted_price[0][0])

# Example usage:
# stock_symbol = 'AMZN'
# predicted_price = predict_stock_price(stock_symbol)
# print("Predicted Stock Price for next day:", predicted_price)


# Flask route for predictions
@app.route('/predict/<string:stock_symbol>', methods=['GET'])
def predict(stock_symbol):
    try:
        predicted_price = predict_stock_price(stock_symbol)
        return jsonify({'predictedPrice': predicted_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in a production environment
