import time

counter = 0
while True:
    time.sleep(3)
    counter += 1
    print('Iteration {i}'.format(i=counter))