import psutil                   # Library for retrieving system information (CPU, memory, disk, network, processes).
import requests                 # Library for making HTTP requests.
from datetime import datetime   # Module for working with dates and times.
import sched                    # Module for event scheduling.

SERVER_URL = "http://localhost:8000/measurements"  # URL of the server endpoint to send measurements.
SERVER_HEADERS = {'Accept': 'application/json', 'Content-type': 'application/json'}  # Headers for the HTTP request.  Specifies that we expect and send JSON data.

def measureBatteryAndSend():
    """
    Measures the battery percentage and sends it to the server.
    """
    timestamp = datetime.now()  # Get the current timestamp.
    value = psutil.sensors_battery().percent  # Get the battery percentage using psutil.
    data = {"sensor_id": "battery", "value": value, "timestamp": timestamp.isoformat()}  # Create a dictionary containing the sensor ID, value, and timestamp in ISO format.
    r = requests.post(SERVER_URL, headers=SERVER_HEADERS, json=data)  # Send a POST request to the server with the measurement data as JSON.
    if r.status_code != 200:  # Check if the request was successful (status code 200 OK).
        print(f"Warning: Error {r}")  # Print a warning message if the request failed, including the response object.
    print(data)  # Print the measurement data to the console for debugging.


def measureCPUAndSend():
    """
    Measures the CPU usage percentage and sends it to the server.
    """
    timestamp = datetime.now()  # Get the current timestamp.
    value = psutil.cpu_percent(interval=1)  # Get the CPU usage percentage over a 1-second interval using psutil.
    data = {"sensor_id": "cpu", "value": value, "timestamp": timestamp.isoformat()}  # Create a dictionary containing the sensor ID, value, and timestamp in ISO format.
    r = requests.post(SERVER_URL, headers=SERVER_HEADERS, json=data)  # Send a POST request to the server with the measurement data as JSON.
    if r.status_code != 200:  # Check if the request was successful (status code 200 OK).
        print(f"Warning: Error {r}")  # Print a warning message if the request failed, including the response object.
    print(data)  # Print the measurement data to the console for debugging.


def periodic_call(scheduler, period, func):
    """
    Schedules a function to be called periodically.

    Args:
        scheduler: The scheduler object.
        period: The time interval in seconds between calls.
        func: The function to be called.
    """
    # schedule the next call first
    scheduler.enter(period, 1, periodic_call, (scheduler, period, func))  # Schedule the next call to this function itself, creating a recursive loop.
    # do the stuff
    func()  # Call the specified function.


my_scheduler = sched.scheduler()  # Create a scheduler object.
periodic_call(my_scheduler, 15, measureBatteryAndSend)  # Schedule the measureBatteryAndSend function to be called every 15 seconds.
periodic_call(my_scheduler, 5, measureCPUAndSend)  # Schedule the measureCPUAndSend function to be called every 5 seconds.
my_scheduler.run()  # Start the scheduler. This will block until all scheduled events have been executed.