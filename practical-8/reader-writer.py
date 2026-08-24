import threading
import time
import random

# Semaphores
mutex = threading.Semaphore(1)       # Protects read_count
rw_mutex = threading.Semaphore(1)    # Controls access to shared resource
queue = threading.Semaphore(1)       # Ensures fairness

# Shared variables
read_count = 0
shared_data = 0


# Reader function
def reader(reader_id):
    global read_count

    # Simulate arrival time
    time.sleep(random.uniform(0.1, 1))

    # Entry section
    queue.acquire()       # Wait in queue
    mutex.acquire()

    read_count += 1

    if read_count == 1:
        rw_mutex.acquire()    # First reader blocks writers

    mutex.release()
    queue.release()

    # Critical section
    print(f"Reader {reader_id} is reading. Shared Data = {shared_data}")
    time.sleep(random.uniform(0.1, 0.5))

    # Exit section
    mutex.acquire()

    read_count -= 1

    if read_count == 0:
        rw_mutex.release()    # Last reader allows writers

    mutex.release()


# Writer function
def writer(writer_id):
    global shared_data

    # Simulate arrival time
    time.sleep(random.uniform(0.1, 1))

    # Entry section
    queue.acquire()           # Wait in queue
    rw_mutex.acquire()        # Exclusive access
    queue.release()

    # Critical section
    shared_data += 1
    print(
        f"Writer {writer_id} is writing. "
        f"New Shared Data = {shared_data}"
    )
    time.sleep(random.uniform(0.1, 0.5))

    # Exit section
    rw_mutex.release()


# Create reader and writer threads
reader_threads = [
    threading.Thread(target=reader, args=(i,))
    for i in range(3)
]

writer_threads = [
    threading.Thread(target=writer, args=(i,))
    for i in range(2)
]


# Start threads
for t in reader_threads + writer_threads:
    t.start()


# Wait for all threads to complete
for t in reader_threads + writer_threads:
    t.join()


print("All readers and writers have finished.")
