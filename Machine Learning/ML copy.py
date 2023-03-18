import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1)) #scale each feature from 0 to 1

num_inputs = 4
num_outputs = 3

df = pd.read_excel('pcf_data.xlsx', sheet_name='Sheet1') #retrieve data from excel
df_scaler = scaler.fit_transform(df) #transform data to the given range

X = df_scaler[:,range(0, num_inputs)]
y = df_scaler[:,range(num_inputs, num_inputs+num_outputs)]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)

epochs = 1000 #each data point will be used for 1000 times
mlp = MLPRegressor(shuffle=True, random_state=1, max_iter=epochs) #optimise the squared loss
mlp.fit(X_train, y_train)

def prediction(data):
    # data is already scaled
    pred_output = mlp.predict(data)
    reshaped = pred_output.reshape(-1,3)
    #reshaped = np.dot(reshaped,data)
    final = np.concatenate((data, reshaped), axis=1) #join the sequence of output arrays to data arrays column wise
    return scaler.inverse_transform(final)

print(prediction(X_test))

def predict_on_user_input(user_input):
    user_input = np.append(user_input, 0).reshape(1,-1)
    user_input = scaler.transform(user_input)
    return prediction(user_input[:,0:num_inputs])

output = predict_on_user_input([20, 20, 4.89, 0.313])
print('output: ', output)

