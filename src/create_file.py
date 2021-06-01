import datetime
from datetime import date, datetime
import os
import pandas as pd


def create_file():
    df = pd.DataFrame([], columns=['Name', 'Time'])

    today = date.today()
    a = datetime.now()
    true_hour = a.hour
    true_min = a.minute
    true_sec = a.second

    path = '/Users/namluu/Downloads/face-recognition/data/'
    newname = path+ str(today) + "_" + str(true_hour) + ":" + str(true_min) + ":" + str(true_sec) + '.csv'

    try:
        if (true_hour == 6 and true_min == 0 and true_sec == 0) or (true_hour == 16 and true_min == 50 and true_sec == 10):
            if os.path.exists(newname):
                pass
            else:
                os.rename('data/attendance.csv', newname)
                df.to_csv("data/attendance.csv", index=False)
    except FileNotFoundError:

        pass