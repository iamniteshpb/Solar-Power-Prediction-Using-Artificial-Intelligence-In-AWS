
from APi import Api
from Prediction_using_ML import Predict
from Notification import NotificationManager
import time

api = Api()
predict = Predict()
file_names = api.obtaining_api()

####
file_name = predict.predection_power(file_names)

time.sleep(40)
notify = NotificationManager()
notify.send_sms_online(file_name)