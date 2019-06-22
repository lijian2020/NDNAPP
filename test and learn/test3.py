import config
import time
from change import change_name

for i in range(100):
    name = config.get_name()
    print(name)
    config.set_name('new_name')
    print(config.get_name())
    time.sleep(1)
    change_name()

