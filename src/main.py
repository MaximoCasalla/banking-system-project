import threading
import time

# Shared data
users = {}
lock = threading.Lock()


# -----------------------------
# USER CLASS
# -----------------------------
class User:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance


# -----------------------------
# CORE OPERATIONS (CRITICAL SECTION)
# -----------------------------
def deposit_thread(name, amount):
    global users

    print(f"[THREAD] {name} trying to deposit {amount}")

    lock.acquire()  # CRITICAL SECTION START

    temp = users[name].balance
    time.sleep(0.2)  # simulate delay
    temp += amount
    users[name].balance = temp

    print(f"[THREAD] {name} deposited {amount}, Balance = {users[name].balance}")

    lock.release()  # CRITICAL SECTION END


def withdraw_thread(name, amount):
    global users

    print(f"[THREAD] {name} trying to withdraw {amount}")

    lock.acquire()  # CRITICAL SECTION START

    if users[name].balance >= amount:
        temp = users[name].balance
        time.sleep(0.2)
        temp -= amount
        users[name].balance = temp
        print(f"[THREAD] {name} withdrew {amount}, Balance = {users[name].balance}")
    else:
        print(f"[THREAD] {name} insufficient balance")

    lock.release()  # CRITICAL SECTION END


# -----------------------------
# NORMAL (MENU) OPERATIONS
# -----------------------------
def create_user():
    name = input("Enter username: ")
    if name in users:
        print("User already exists")
    else:
        users[name] = User(name, 100)
        print("User created with initial balance 100")


def deposit():
    name = input("Enter username: ")
    amount = int(input("Enter amount: "))

    if name in users:
        t = threading.Thread(target=deposit_thread, args=(name, amount))
        t.start()
        t.join()
    else:
        print("User not found")


def withdraw():
    name = input("Enter username: ")
    amount = int(input("Enter amount: "))

    if name in users:
        t = threading.Thread(target=withdraw_thread, args=(name, amount))
        t.start()
        t.join()
    else:
        print("User not found")


def check_balance():
    name = input("Enter username: ")
    if name in users:
        print(f"Balance = {users[name].balance}")
    else:
        print("User not found")


def show_all():
    for name, user in users.items():
        print(f"{name}: {user.balance}")


# -----------------------------
# CONCURRENCY DEMO (IMPORTANT)
# -----------------------------
def concurrent_demo():
    print("\n--- CONCURRENT TRANSACTION DEMO ---")

    name = input("Enter username for demo: ")

    if name not in users:
        print("User not found")
        return

    # Two threads accessing same account
    t1 = threading.Thread(target=withdraw_thread, args=(name, 50))
    t2 = threading.Thread(target=withdraw_thread, args=(name, 50))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Final Balance = {users[name].balance}")


# -----------------------------
# MAIN MENU
# -----------------------------
def main():
    while True:
        print("\nMain Menu")
        print("1. Create User")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Show All Users")
        print("6. Concurrent Demo (OS Concept)")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            show_all()
        elif choice == "6":
            concurrent_demo()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid option")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()