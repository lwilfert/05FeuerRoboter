import time
from play import path

# simulate start method
print('start')
with open(path, 'w') as file:
    file.write('0\n')

# simulate driving time
time.sleep(8)

# simulate stop method
print('stop')
with open(path, 'w') as file:
    file.write('1\n')
