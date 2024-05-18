from datetime import datetime
import json
import os

class DogSpaReservationSystem:
    def __init__(self):
        self.reservations_file = 'reservations.json'
        self.load_reservations()

    def load_reservations(self):
        if os.path.exists(self.reservations_file):
            with open(self.reservations_file, 'r') as file:
                self.reservations = json.load(file)
        else:
            print("No reservations file found. Starting with empty reservations list.")
            self.reservations = []

    def save_reservations(self):
        with open(self.reservations_file, 'w') as file:
            json.dump(self.reservations, file)

    def make_reservation(self, start_time):
        end_time = start_time.replace(minute=start_time.minute + 50)
        for reservation in self.reservations:
            if start_time < datetime.fromisoformat(reservation['end_time']) and end_time > datetime.fromisoformat(reservation['start_time']):
                print("Failed to make reservation. Time already booked.")
                return False

        self.reservations.append({'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()})
        self.save_reservations()
        print("Reservation successful!")
        return True

    def cancel_reservation(self, start_time):
        for reservation in self.reservations:
            if start_time == datetime.fromisoformat(reservation['start_time']):
                self.reservations.remove(reservation)
                self.save_reservations()
                print("Reservation canceled successfully.")
                return True
        print("No reservation found at the specified time.")
        return False

    def view_reservations(self):
        print("Current Reservations:")
        if self.reservations:
            for i, reservation in enumerate(self.reservations, start=1):
                print(f"{i}. Start Time: {reservation['start_time']}, End Time: {reservation['end_time']}")
        else:
            print("No reservations found.")

if __name__ == "__main__":
    reservation_system = DogSpaReservationSystem()

    while True:
        print("\nWelcome to the Dog Spa Reservation System!\n")
        print("1. Make a Reservation")
        print("2. Cancel a Reservation")
        print("3. View Reservations")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            start_time_input = input("Enter the desired start time (YYYY-MM-DD HH:MM:SS): ")
            try:
                start_time = datetime.fromisoformat(start_time_input)
                reservation_system.make_reservation(start_time)
            except ValueError:
                print("Invalid date and time format. Please enter in the format YYYY-MM-DD HH:MM:SS.")

        elif choice == '2':
            start_time_input = input("Enter the start time of the reservation to cancel (YYYY-MM-DD HH:MM:SS): ")
            try:
                start_time = datetime.fromisoformat(start_time_input)
                reservation_system.cancel_reservation(start_time)
            except ValueError:
                print("Invalid date and time format. Please enter in the format YYYY-MM-DD HH:MM:SS.")

        elif choice == '3':
            reservation_system.view_reservations()

        elif choice == '4':
            print("Exiting the Dog Spa Reservation System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")