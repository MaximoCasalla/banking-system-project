import threading
import time

# Shared resource
balance = 100

# Lock for synchronization
lock = threading.Lock()


# -----------------------------
# WITH LOCK (Correct Solution)
# -----------------------------
def withdraw(amount):
    global balance
    print(f"Trying to withdraw {amount}")

    lock.acquire()

    if balance >= amount:
        temp = balance
        time.sleep(0.1)
        temp -= amount
        balance = temp
        print(f"Withdrawn {amount}, Balance = {balance}")
    else:
        print("Insufficient balance")

    lock.release()


def deposit(amount):
    global balance
    print(f"Trying to deposit {amount}")

    lock.acquire()

    temp = balance
    time.sleep(0.1)
    temp += amount
    balance = temp

    print(f"Deposited {amount}, Balance = {balance}")

    lock.release()


# -----------------------------
# SIMULATION
# -----------------------------
def run_simulation():
    global balance
    balance = 100

    print("\n--- BANKING SYSTEM WITH SYNCHRONIZATION ---")

    t1 = threading.Thread(target=withdraw, args=(50,))
    t2 = threading.Thread(target=withdraw, args=(50,))
    t3 = threading.Thread(target=deposit, args=(30,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print(f"Final Balance = {balance}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    run_simulation()