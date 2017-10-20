import time
import os

try:
    user = os.environ['APP_USER']
except KeyError:
    print('APP_USER not defined!')
    exit(1)

while True:
    time.sleep(3)
    print('Who\'s in here? {u}'.format(u=user))