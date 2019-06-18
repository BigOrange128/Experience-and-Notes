#函数方法
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

#类方法

# import threading
# import time
#
# class MyThread(threading.Thread):
#     def __init__(self, n):
#         super().__init__()
#         self.n = n
#     def run(self):
#         time.sleep(1)
#         print('task', self.n)
# start_time = time.time()
# t_objs = []
# for i in range(10):
#     t = MyThread(i)
#     t.start()
#     t_objs.append(t)
# for t in t_objs:
#     t.join()
# print("run time:{}".format(time.time()-start_time))
