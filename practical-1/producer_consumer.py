from multiprocessing import Process, Semaphore, Lock, Array, Value
import time
import random

# Total buffer size (how many items the buffer can hold at once)
BUFFER_SIZE = 5

# Total number of items to produce and consume
ITEM_COUNT = 10

# Producer Function
def producer(buffer, in_index, out_index, empty, full, mutex):
    for _ in range(ITEM_COUNT):
        item = random.randint(1, 100)  # Produce a random number
        empty.acquire()  # Wait until there is at least one empty slot
        mutex.acquire()  # Enter critical section (only one process allowed at a time)

        # Place the item in the buffer at the current in_index
        idx = in_index.value
        buffer[idx] = item
        print(f"[Producer] Produced item {item} at index {idx}", flush=True)

        # Update in_index circularly
        in_index.value = (idx + 1) % BUFFER_SIZE

        mutex.release()  # Leave critical section
        full.release()  # Signal that one item is available in the buffer

        # Simulate delay in production
        time.sleep(random.uniform(0.1, 0.3))

# Consumer Function
def consumer(buffer, in_index, out_index, empty, full, mutex):
    print("[Consumer] Process started", flush=True)

    for _ in range(ITEM_COUNT):
        full.acquire()  # Wait until there is at least one full slot
        mutex.acquire()  # Enter critical section

        # Remove item from the buffer at current out_index
        idx = out_index.value
        item = buffer[idx]
        print(f"[Consumer] Consumed item {item} from index {idx}", flush=True)

        # Update out_index circularly
        out_index.value = (idx + 1) % BUFFER_SIZE

        mutex.release()  # Leave critical section
        empty.release()  # Signal that a slot is now free

        # Simulate delay in consumption
        time.sleep(random.uniform(0.1, 0.3))

def main():
    # Create shared memory
    # buffer: shared array of fixed size
    # in_index, out_index: shared integers to track position
    buffer = Array('i', BUFFER_SIZE)  # Shared buffer (Array of integers)
    in_index = Value('i', 0)  # Where producer will insert next
    out_index = Value('i', 0)  # Where consumer will remove next

    # Synchronization primitives:
    empty = Semaphore(BUFFER_SIZE)  # Initially, buffer is empty (all slots available)
    full = Semaphore(0)  # Initially, nothing to consume
    mutex = Lock()  # For mutual exclusion (one process in critical section)

    print("Starting processes...", flush=True)

    # Create producer and consumer processes, passing all shared objects
    p = Process(target=producer, args=(buffer, in_index, out_index, empty, full, mutex))
    c = Process(target=consumer, args=(buffer, in_index, out_index, empty, full, mutex))

    # Start both processes
    p.start()
    c.start()

    # Wait for both to complete
    p.join()
    c.join()

    print("Producer and Consumer processes have finished.", flush=True)

# Run the main function only if this script is executed directly
if __name__ == "__main__":
    main()
