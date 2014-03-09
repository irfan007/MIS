# myapp/cron.py
import cronjobs
import time
from misApp.pp import i_notifier
@cronjobs.register
def cronJob1():
    while True:
        i_notifier()
        time.sleep(24*60*60)
        
     




