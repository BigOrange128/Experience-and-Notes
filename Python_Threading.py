#函数方式

import threading
import time

def run(name):
    time.sleep(1)
    print('task', name)
start_time = time.time()
t_objs = []
for i in range(10):
    t = threading.Thread(target=run, args=(i,))
    t.start()
    t_objs.append(t)
#等待所有进程执行完毕
for t in t_objs:
    t.join()
print("run time:{}".format(time.time()-start_time))

#类方式
