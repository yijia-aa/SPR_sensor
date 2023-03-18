import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))

num_inputs = 3
num_outputs = 1

df = pd.read_excel('20sets_3input_1output.xlsx', sheet_name='Sheet1')

scaler.fit(df)
df_scaler = scaler.transform(df)

X = df_scaler[:,range(0, num_inputs)]
y = df_scaler[:,range(num_inputs, num_inputs+num_outputs)]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)

epochs = 1000
mlp = MLPRegressor(shuffle=True, random_state=1, max_iter=epochs)
mlp.fit(X_train, y_train)

def prediction(data):
    # data is already scaled
    pred_output = mlp.predict(data)
    final = np.concatenate((data, pred_output.reshape(-1,1)), axis=1)
    return scaler.inverse_transform(final)

print(prediction(X_test))

def predict_on_user_input(user_input):
    user_input = np.append(user_input, 0).reshape(1,-1)
    user_input = scaler.transform(user_input)
    return prediction(user_input[:,0:num_inputs])

output = predict_on_user_input([25,30,1])
print('output: ', output)
