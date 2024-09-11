from datetime import datetime

class Base:
    def __init__(self, name):
        self.name = name

class Admin(Base):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email.lower()  # Ensure email is in lowercase
    
    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email
    
    @staticmethod
    def create_admin():
        while True:
            name = input("Enter Admin Name: ")
            email = input("Enter Admin Email: ")
            email_lower = email.lower()
            if Admin.validate_email(email_lower):
                if email == email_lower:
                    print("Admin validation successful!")
                    print(f"ALERT: Someone is using the admin email: {email_lower}")
                    return Admin(name, email_lower)
                else:
                    print("Email must be in lowercase. Please try again.")
            else:
                print("Invalid email, please try again.")

    def sign_out(self):
        print(f"Admin {self.name} signed out successfully!")

class Event:
    def __init__(self, event_id, event_name, amount, date, available_tickets):
        self.event_id = event_id
        self.event_name = event_name
        self.amount = amount
        self.date = date
        self.available_tickets = available_tickets

    def display_event(self):
        print(f"{self.event_id:<10}{self.event_name:<25}${self.amount:<10}{self.date:<15}{self.available_tickets:<10}")

    def reduce_tickets(self):
        if self.available_tickets > 0:
            self.available_tickets -= 1
        else:
            print("No tickets available!")

class Registration(Base):
    def __init__(self, name):
        super().__init__(name)
        self.registered_events = []

    def register_event(self, event):
        event.reduce_tickets()
        self.registered_events.append(event)
        print(f"Registration successful for {event.event_name} on {event.date}")

    def display_registered_events(self):
        if self.registered_events:
            print("\nRegistered Events:")
            for event in self.registered_events:
                print(f"- {event.event_name}, Date: {event.date}, Fee: ${event.amount}")
        else:
            print("No events registered.")

class Payment:
    def __init__(self, amount):
        self.amount = amount

    def process_payment(self, mode):
        if mode in ['c', 'ca', 'car', 'card']:
            print(f"Payment of ${self.amount} done using Card. Payment successful!")
        elif mode in ['n', 'ne', 'net', 'netb', 'netba', 'netban', 'netbanking']:
            print(f"Payment of ${self.amount} done using Net Banking. Payment successful!")
        else:
            print("Invalid payment mode.")

class EventManagementSystem:
    def __init__(self):
        self.events = [
            Event(1, "Music Concert", 50, "2024-01-10", 100),
            Event(2, "Art Exhibition", 40, "2024-02-15", 50),
            Event(3, "Tech Talk", 30, "2024-03-20", 200),
            Event(4, "Dance Competition", 45, "2024-04-25", 80),
            Event(5, "Comedy Show", 35, "2024-05-30", 120),
            Event(6, "Gaming Tournament", 25, "2024-06-10", 150),
            Event(7, "Cooking Workshop", 20, "2024-07-15", 70),
            Event(8, "Photography Walk", 15, "2024-08-20", 60),
            Event(9, "Film Screening", 10, "2024-09-25", 90),
            Event(10, "Theater Play", 60, "2024-10-30", 110)
        ]
        self.admin = None
        self.registration = None

    def display_events(self):
        print("\nAvailable Events:")
        print(f"{'Event ID':<10}{'Event Name':<25}{'Entry Fee':<10}{'Date':<15}{'Tickets Left':<10}")
        print("="*75)
        for event in self.events:
            event.display_event()

    def remove_registered_event(self, registered_event):
        self.events = [event for event in self.events if event.event_id != registered_event.event_id]

    def register_for_event(self):
        name = input("Enter your name: ")
        self.registration = Registration(name)

        while True:
            if not self.events:
                print("All events have been registered for.")
                break

            self.display_events()
            event_choice = int(input("Select Event ID to register: "))
            selected_event = next((event for event in self.events if event.event_id == event_choice), None)

            if selected_event:
                if selected_event.available_tickets > 0:
                    self.registration.register_event(selected_event)
                    amount = selected_event.amount
                    payment_mode = input("Enter mode of payment (Card/NetBanking): ").lower()
                    payment = Payment(amount)
                    payment.process_payment(payment_mode)
                    self.remove_registered_event(selected_event)

                    another_event = input("Do you want to register for another event? (yes/no): ").lower()
                    if another_event != 'yes':
                        break

                    same_admin = input("Do you want to continue with the same admin? (yes/no): ").lower()
                    if same_admin != 'yes':
                        self.admin = Admin.create_admin()
                else:
                    print(f"The event {selected_event.event_name} is fully booked. Please choose another event.")
            else:
                print("Invalid Event ID. Please try again.")
        
        self.registration.display_registered_events()
        sign_out = input("Do you want to sign out from the admin account? (yes/no): ").lower()
        if sign_out == 'yes':
            self.admin.sign_out()

    def start(self):
        self.admin = Admin.create_admin()
        self.register_for_event()

if __name__ == "__main__":
    system = EventManagementSystem()
    system.start()