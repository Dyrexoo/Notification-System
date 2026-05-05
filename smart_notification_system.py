import datetime
# ─────────────────────────────
# Singleton + Observer Manager
# ─────────────────────────────
class NotificationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.subscribers = []
            cls._instance.log = []
            print("NotificationManager created")
        return cls._instance

    def subscribe(self, user):
        if user not in self.subscribers:
            self.subscribers.append(user)
            print(user.name, "subscribed")

    def unsubscribe(self, user):
        if user in self.subscribers:
            self.subscribers.remove(user)
            print(user.name, "unsubscribed")

    def notify_all(self, notification):
        msg = f"{datetime.datetime.now().strftime('%H:%M:%S')} → {notification}"
        self.log.append(msg)
        print("\n", msg)

        for user in self.subscribers:
            user.receive(notification)

    def get_log(self):
        return self.log


# ─────────────────────────────
# User (Observer)
# ─────────────────────────────
class User:
    def __init__(self, name, channel="email"):
        self.name = name
        self.channel = channel
        self.inbox = []

    def receive(self, notification):
        msg = f"[{self.channel}] {self.name} got: {notification.message}"
        self.inbox.append(msg)
        print(msg)


# ─────────────────────────────
# Notifications
# ─────────────────────────────
class Notification:
    def __init__(self, message, ntype="GENERIC"):
        self.message = message
        self.type = ntype
        self.time = datetime.datetime.now()
    def __str__(self):
        return f"[{self.type}] {self.message}"


class Alert(Notification):
    def __init__(self, message):
        super().__init__(message, "ALERT")


class Reminder(Notification):
    def __init__(self, message):
        super().__init__(message, "REMINDER")


class Promo(Notification):
    def __init__(self, message):
        super().__init__(message, "PROMO")


# ─────────────────────────────
# Simple Factory
# ─────────────────────────────
def create_notification(ntype, message):
    if ntype == "alert":
        return Alert(message)
    elif ntype == "reminder":
        return Reminder(message)
    elif ntype == "promo":
        return Promo(message)
    else:
        return Notification(message)


# ─────────────────────────────
# Demo
# ─────────────────────────────
def main():
    manager = NotificationManager()

    alice = User("Alice", "email")
    bob = User("Bob", "sms")

    manager.subscribe(alice)
    manager.subscribe(bob)

    n1 = create_notification("alert", "Server is down!")
    n2 = create_notification("reminder", "Meeting in 10 min")

    manager.notify_all(n1)
    manager.notify_all(n2)

    manager.unsubscribe(bob)

    n3 = create_notification("promo", "50% OFF!")

    manager.notify_all(n3)

    print("\nLog:")
    for l in manager.get_log():
        print(l)


if __name__ == "__main__":
    main()