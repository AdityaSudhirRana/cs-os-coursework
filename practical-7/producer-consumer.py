import threading
import time

print("S105 - Aditya Rana")

BUFFER_SIZE = 5
buffer = [None] * BUFFER_SIZE

# Circular queue pointers
in_index = 0
out_index = 0

# Mutex for synchronized access to the buffer
mutex = threading.Lock()

# Semaphores
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)


# Producer function
def producer():
    global in_index

    for item in range(1, 11):

        # Wait for an empty slot
        empty.acquire()

        # Enter critical section
        with mutex:
            buffer[in_index] = item
            print(f"Producer produced: {item} at position {in_index}")

            # Move circularly
            in_index = (in_index + 1) % BUFFER_SIZE

        # Signal that an item is available
        full.release()

        time.sleep(0.5)


# Consumer function
def consumer():
    global out_index

    for _ in range(1, 11):

        # Wait for an available item
        full.acquire()

        # Enter critical section
        with mutex:
            item = buffer[out_index]
            buffer[out_index] = None

            print(f"Consumer consumed: {item} from position {out_index}")

            # Move circularly
            out_index = (out_index + 1) % BUFFER_SIZE

        # Signal that an empty slot is available
        empty.release()

        time.sleep(0.8)


# Create producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start threads
producer_thread.start()
consumer_thread.start()

# Wait for both threads to finish
producer_thread.join()
consumer_thread.join()

print("\nProducer and Consumer execution completed.")
print("Final Buffer:", buffer)
