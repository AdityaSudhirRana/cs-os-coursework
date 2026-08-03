print("S105 - Aditya Rana")

import threading

def print_even():
    print("Even Numbers:")
    for i in range(2, 11, 2):
        print(i, end=" ")
    print()

def print_odd():
    print("Odd Numbers:")
    for i in range(1, 10, 2):
        print(i, end=" ")
    print()

def reverse_string(text):
    print("Original String:", text)
    print("Reversed String:", text[::-1])


t1 = threading.Thread(target=print_even)
t2 = threading.Thread(target=print_odd)
t3 = threading.Thread(target=reverse_string, args=("Operating System",))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print("\nAll threads completed.")
