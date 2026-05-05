"""
Smart Notification System
=========================
Demonstrates three design patterns:
  1. Singleton   – NotificationManager (one central hub)
  2. Observer    – Users subscribe/unsubscribe and receive notifications
  3. Factory     – NotificationFactory creates the right notification type

Language: Python 3
"""

from __future__ import annotations
import datetime
from abc import ABC, abstractmethod
from typing import List


# ─────────────────────────────────────────────
# PATTERN 1 — SINGLETON: NotificationManager
# ─────────────────────────────────────────────
class NotificationManager:
    """
    Singleton class that acts as the central hub for the notification system.
    Guarantees only ONE instance exists throughout the program's lifetime.
    Holds the list of subscribers and dispatches notifications.
    """
    _instance: NotificationManager | None = None

    def __new__(cls) -> "NotificationManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers: List[Observer] = []
            cls._instance._log: List[str] = []
            print("[Singleton] NotificationManager instance created.")
        return cls._instance

    # ── Observer pattern helpers ──────────────────────────────────────────
    def subscribe(self, observer: "Observer") -> None:
        if observer not in self._subscribers:
            self._subscribers.append(observer)
            print(f"[Observer]  '{observer.name}' subscribed.")

    def unsubscribe(self, observer: "Observer") -> None:
        if observer in self._subscribers:
            self._subscribers.remove(observer)
            print(f"[Observer]  '{observer.name}' unsubscribed.")

    def notify_all(self, notification: "Notification") -> None:
        entry = (f"[{datetime.datetime.now().strftime('%H:%M:%S')}] "
                 f"Broadcast → {notification}")
        self._log.append(entry)
        print(f"\n{entry}")
        for subscriber in self._subscribers:
            subscriber.receive(notification)

    def get_log(self) -> List[str]:
        return list(self._log)


# ─────────────────────────────────────────────
# PATTERN 2 — OBSERVER: User (Concrete Observer)
# ─────────────────────────────────────────────
class Observer(ABC):
    """Abstract base class for all observers (subscribers)."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def receive(self, notification: "Notification") -> None: ...


class User(Observer):
    """
    Concrete Observer that represents an end-user.
    When a notification is dispatched, receive() is called automatically.
    """

    def __init__(self, username: str, preferred_channel: str = "email") -> None:
        self._name = username
        self.preferred_channel = preferred_channel
        self.inbox: List[str] = []

    @property
    def name(self) -> str:
        return self._name

    def receive(self, notification: "Notification") -> None:
        msg = (f"  📬 [{self.preferred_channel.upper()}] "
               f"{self._name} received [{notification.type}]: {notification.message}")
        self.inbox.append(msg)
        print(msg)


# ─────────────────────────────────────────────
# PATTERN 3 — FACTORY: Notification types
# ─────────────────────────────────────────────
class Notification(ABC):
    """Abstract product class for all notification types."""

    def __init__(self, message: str, priority: str = "normal") -> None:
        self.message = message
        self.priority = priority
        self.timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    @property
    @abstractmethod
    def type(self) -> str: ...

    def __str__(self) -> str:
        return f"[{self.type}|{self.priority}] {self.message}"


class AlertNotification(Notification):
    """High-priority alert (e.g., system outage, security breach)."""
    @property
    def type(self) -> str:
        return "ALERT"


class ReminderNotification(Notification):
    """Scheduled reminder (e.g., meeting, deadline)."""
    @property
    def type(self) -> str:
        return "REMINDER"


class PromotionNotification(Notification):
    """Marketing promotion (e.g., sale, discount)."""
    @property
    def type(self) -> str:
        return "PROMO"


class NotificationFactory:
    """
    Factory class that creates the correct Notification subclass
    based on a string type key — the caller never imports concrete classes.
    """
    _registry = {
        "alert":    AlertNotification,
        "reminder": ReminderNotification,
        "promo":    PromotionNotification,
    }

    @classmethod
    def create(cls, ntype: str, message: str, priority: str = "normal") -> Notification:
        key = ntype.lower()
        if key not in cls._registry:
            raise ValueError(f"[Factory] Unknown notification type: '{ntype}'. "
                             f"Valid types: {list(cls._registry)}")
        obj = cls._registry[key](message, priority)
        print(f"[Factory]   Created {obj.type} notification → '{message}'")
        return obj


# ─────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────
def main() -> None:
    print("=" * 60)
    print("   SMART NOTIFICATION SYSTEM — Design Patterns Demo")
    print("=" * 60)

    # ── Singleton: both calls return the same instance ──────────────────
    print("\n── Singleton Demo ──────────────────────────────────────────")
    mgr1 = NotificationManager()
    mgr2 = NotificationManager()
    print(f"mgr1 is mgr2 → {mgr1 is mgr2}")   # True

    # ── Observer: subscribe users ────────────────────────────────────────
    print("\n── Observer Demo ───────────────────────────────────────────")
    alice = User("Alice", preferred_channel="email")
    bob   = User("Bob",   preferred_channel="sms")
    carol = User("Carol", preferred_channel="push")

    mgr1.subscribe(alice)
    mgr1.subscribe(bob)
    mgr1.subscribe(carol)

    # ── Factory + Observer: create and broadcast notifications ────────────
    print("\n── Factory + Broadcast Demo ────────────────────────────────")
    n1 = NotificationFactory.create("alert",    "Server CPU at 95%!",        "high")
    n2 = NotificationFactory.create("reminder", "Team standup in 10 minutes","normal")
    n3 = NotificationFactory.create("promo",    "50% off — today only!",     "low")

    mgr1.notify_all(n1)
    mgr1.notify_all(n2)

    # Unsubscribe Bob, then send promo — Bob won't receive it
    print("\n── Unsubscribe Demo ────────────────────────────────────────")
    mgr1.unsubscribe(bob)
    mgr1.notify_all(n3)

    # ── Audit log ────────────────────────────────────────────────────────
    print("\n── Audit Log ───────────────────────────────────────────────")
    for entry in mgr1.get_log():
        print(entry)

    # ── Alice's inbox ────────────────────────────────────────────────────
    print(f"\n── Alice's Inbox ({len(alice.inbox)} messages) ──────────────────────")
    for msg in alice.inbox:
        print(msg)

    print("\n" + "=" * 60)
    print("   Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()
