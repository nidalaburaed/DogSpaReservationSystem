from datetime import datetime
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

class DogSpaReservationSystem:
    def __init__(self):
        self.reservations_file = 'reservations.json'
        self.load_reservations()

    def load_reservations(self):
        if os.path.exists(self.reservations_file):
            with open(self.reservations_file, 'r') as file:
                self.reservations = json.load(file)
        else:
            self.reservations = []

    def save_reservations(self):
        with open(self.reservations_file, 'w') as file:
            json.dump(self.reservations, file)

    def make_reservation(self, start_time):
        end_time = start_time.replace(minute=start_time.minute + 50)
        for reservation in self.reservations:
            if start_time < datetime.fromisoformat(reservation['end_time']) and end_time > datetime.fromisoformat(reservation['start_time']):
                return jsonify({"message": "Failed to make reservation. Time already booked."}), 400

        self.reservations.append({'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()})
        self.save_reservations()
        return jsonify({"message": "Reservation successful!"}), 200

    def cancel_reservation(self, start_time):
        for reservation in self.reservations:
            if start_time == datetime.fromisoformat(reservation['start_time']):
                self.reservations.remove(reservation)
                self.save_reservations()
                return jsonify({"message": "Reservation canceled successfully."}), 200
        return jsonify({"message": "No reservation found at the specified time."}), 404

    def view_reservations(self):
        if self.reservations:
            return jsonify({"reservations": self.reservations}), 200
        else:
            return jsonify({"message": "No reservations found."}), 404

reservation_system = DogSpaReservationSystem()

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    data = request.get_json()
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        return reservation_system.make_reservation(start_time)
    except ValueError:
        return jsonify({"message": "Invalid date and time format. Please enter in the format YYYY-MM-DD HH:MM:SS."}), 400

@app.route('/cancel_reservation', methods=['DELETE'])
def cancel_reservation():
    data = request.get_json()
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        return reservation_system.cancel_reservation(start_time)
    except ValueError:
        return jsonify({"message": "Invalid date and time format. Please enter in the format YYYY-MM-DD HH:MM:SS."}), 400

@app.route('/view_reservations', methods=['GET'])
def view_reservations():
    return reservation_system.view_reservations()

if __name__ == "__main__":
    app.run(debug=True)