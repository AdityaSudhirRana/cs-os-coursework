print("S105 - Aditya Rana")

import threading
import math

def factorial_task(num):
    print(f"Factorial of {num} = {math.factorial(num)}")

numbers = [4, 5, 6, 7]
threads = []

print("Factorial using Multithreading\n")

for num in numbers:
    t = threading.Thread(target=factorial_task, args=(num,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nAll threads completed.")
