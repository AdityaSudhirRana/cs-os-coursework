print("S105 - Aditya Rana")

import threading

# Function to generate Fibonacci sequence
def generate_fibonacci(n):
    a, b = 0, 1
    sequence = []

    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b

    return sequence


# Function executed by each thread
def task(n):
    result = generate_fibonacci(n)
    print(f"Fibonacci({n}) = {result}")


print("Multi-threaded Fibonacci Sequence Generator\n")

values = [4, 5, 6]
threads = []

for n in values:
    t = threading.Thread(target=task, args=(n,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nAll threads completed.")
