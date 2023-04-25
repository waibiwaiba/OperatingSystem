import threading
import time
import random

# 全局共享数据，存储生产者生产的物品和消费者消费的物品
items = []

# 互斥锁，用于保护共享数据
lock = threading.Lock()

# 条件变量，用于线程间通信和同步
not_empty = threading.Condition(lock)
not_full = threading.Condition(lock)

# 消费者已消费的物品数量
consumed_items = 0


# 生产者线程类
class Producer(threading.Thread):
    def run(self):
        global items
        while True:
            # 检查是否已经消费了足够的物品
            if consumed_items >= x:
                print(f"[stop]     生产者 {self.name} 停止运行")
                break
            # 模拟生产物品的过程
            time.sleep(random.randint(1, 3))

            # 获取互斥锁
            lock.acquire()

            # 如果共享数据已满，则等待消费者消费
            while len(items) >= 10:
                not_full.wait()

            # 生产物品并添加到共享数据中
            item = random.randint(1, 100)
            items.append(item)
            print(f"[+]        生产者 {self.name} 生产了物品 {item}")

            print(f"[{consumed_items}]{items}")
            # 通知消费者线程有新物品可供消费
            not_empty.notify()

            # 释放互斥锁
            lock.release()


# 消费者线程类
class Consumer(threading.Thread):
    def run(self):
        global items, consumed_items
        while True:
            # 检查是否已经消费了足够的物品
            if consumed_items >= x:
                print(f"[stop]     消费者 {self.name} 停止运行")
                break

            # 模拟消费物品的过程
            time.sleep(random.randint(1, 3))

            # 获取互斥锁
            lock.acquire()

            # 如果共享数据为空，则等待生产者生产
            while not items:
                not_empty.wait()

            # 从共享数据中取出一个物品并消费
            item = items.pop(0)
            consumed_items += 1
            print(f"[-]        消费者 {self.name} 消费了物品 {item}")

            print(f"[{consumed_items}]{items}")
            # 通知生产者线程有空位可供生产
            not_full.notify()

            # 释放互斥锁
            lock.release()


# 设置消费者需要消费的物品数量
x = 10

print(f"当有{x}个物品被消费时，程序会结束运行。")
print(f"[consumed_items][items]\n")
# 创建3个生产者线程和3个消费者线程并启动它们
for i in range(3):
    Producer().start()
    Consumer().start()

# 等待所有线程运行结束
for thread in threading.enumerate():
    if thread != threading.current_thread():
        thread.join()

