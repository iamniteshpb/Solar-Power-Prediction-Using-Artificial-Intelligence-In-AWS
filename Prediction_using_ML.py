import pandas as pd
import numpy as np
import tensorflow as tf
from keras.layers import Dense, Activation, BatchNormalization, Dropout
from keras import regularizers

class Predict:

    def predection_power(self,file):
        import datetime
        import matplotlib.pyplot as plt
        import seaborn as sns

        dts = pd.read_csv(
            '/home/ec2-user/solar/{}.csv'.format(file[1]))

        #dts = pd.read_csv(
            #"C:/Users/dhyan/PycharmProjects/Full Test Copy of solar/weather_output_data2022-08-26T04-30-00.csv")

        dt = pd.read_csv(
            '/home/ec2-user/solar/{}.csv'.format(file[0]))

        #dt = pd.read_csv(
             #"C:/Users/dhyan/PycharmProjects/Full Test Copy of solar/solarpower_output_data2022-08-26T04-30-00.csv")

        dts.head(10)

        X = dts.iloc[:, :-2].values
        y = dt.iloc[:, :-2].values
        print(X.shape, y.shape)
        y = np.reshape(y, (-1, 1))
        print(y.shape)

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        print("Train Shape: {} {} \nTest Shape: {} {}".format(X_train.shape, y_train.shape, X_test.shape, y_test.shape))

        from sklearn.preprocessing import StandardScaler
        # input scaling
        sc_X = StandardScaler()
        X_train = sc_X.fit_transform(X_train)
        X_test = sc_X.transform(X_test)

        # outcome scaling:
        sc_y = StandardScaler()
        y_train = sc_y.fit_transform(y_train)
        y_test = sc_y.transform(y_test)

        def create_spfnet(n_layers, n_activation, kernels):
            model = tf.keras.models.Sequential()
            for i, nodes in enumerate(n_layers):
                if i == 0:
                    model.add(
                        Dense(nodes, kernel_initializer=kernels, activation=n_activation, input_dim=X_train.shape[1]))
                    # model.add(Dropout(0.3))
                else:
                    model.add(Dense(nodes, activation=n_activation, kernel_initializer=kernels))
                    # model.add(Dropout(0.3))

            model.add(Dense(1))
            model.compile(loss='mse',
                          optimizer='adam',
                          metrics=[tf.keras.metrics.RootMeanSquaredError()])
            return model

        spfnet = create_spfnet([32, 64], 'relu', 'normal')
        spfnet.summary()

        hist = spfnet.fit(X_train, y_train, batch_size=32, validation_data=(X_test, y_test), epochs=150, verbose=2)

        plt.plot(hist.history['root_mean_squared_error'])
        # plt.plot(hist.history['val_root_mean_squared_error'])
        plt.title('Root Mean Squares Error')
        plt.xlabel('Epochs')
        plt.ylabel('error')
        plt.show()

        spfnet.evaluate(X_train, y_train)

        from sklearn.metrics import mean_squared_error

        y_pred = spfnet.predict(X_test)  # get model predictions (scaled inputs here)
        y_pred_orig = sc_y.inverse_transform(y_pred)  # unscale the predictions
        y_test_orig = sc_y.inverse_transform(y_test)

        train_pred = spfnet.predict(X_train)  # get model predictions (scaled inputs here)
        train_pred_orig = sc_y.inverse_transform(train_pred)  # unscale the predictions
        y_train_orig = sc_y.inverse_transform(y_train)

        np.concatenate((train_pred_orig, y_train_orig), 1)

        np.concatenate((y_pred_orig, y_test_orig), 1)

        results = np.concatenate((y_test_orig, y_pred_orig), 1)
        results = pd.DataFrame(data=results)
        results.columns = ['Real Solar Power Produced', 'Predicted Solar Power']
        # results = results.sort_values(by=['Real Solar Power Produced'])
        pd.options.display.float_format = "{:,.2f}".format
        # results[800:820]
        print(results[1:18])
        # updating the data in csv file for future reference
        from datetime import date

        today =str(date.today())+"predected_power.csv"
        results.to_csv(today, index=False, float_format='%.2f')

        sc = StandardScaler()
        pred_whole = spfnet.predict(sc.fit_transform(X))
        pred_whole_orig = sc_y.inverse_transform(pred_whole)
        print(pred_whole_orig)

        """# New Section"""

        plt.figure(figsize=(16, 6))
        plt.subplot(1, 2, 2)
        plt.scatter(y_pred_orig, y_test_orig)
        plt.xlabel('Predicted Generated Power on Test Data')
        plt.ylabel('Real Generated Power on Test Data')
        plt.title('Test Predictions vs Real Data')
        # plt.scatter(y_test_orig, sc_X.inverse_transform(X_test)[:,2], color='green')
        plt.subplot(1, 2, 1)
        plt.scatter(train_pred_orig, y_train_orig)
        plt.xlabel('Predicted Generated Power on Training Data')
        plt.ylabel('Real Generated Power on Training Data')
        plt.title('Training Predictions vs Real Data')
        plt.show()
        return today
