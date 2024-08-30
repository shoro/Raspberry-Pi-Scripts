import time
import psutil
import os
import RPi.GPIO as GPIO

# Version 1.16 - Display highest CPU core usage

# Configuration
fan_pin = 14  # Set the GPIO pin number for the fan
color_on_hex = '#00FF00'  # Set the hex color for Fan: ON (bright green)
color_off_hex = '#FF0000'  # Set the hex color for Fan: OFF (bright red)
color_text_hex = '#FFFFFF'  # Set the hex color for text (white)

# Convert hex color to ANSI escape code
def hex_to_ansi(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

# ANSI escape code for reset (to reset color to default)
reset = "\033[0m"

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT)

def get_cpu_temperature():
    """Get the CPU temperature in Celsius."""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            temp = int(temp_file.read().strip()) / 1000.0
        return temp
    except Exception as e:
        print(f"Error reading CPU temperature: {e}")
        return None

def get_highest_cpu_usage():
    """Get the highest CPU usage percentage across all cores."""
    try:
        cpu_usages = psutil.cpu_percent(percpu=True, interval=1)
        return max(cpu_usages)
    except Exception as e:
        print(f"Error getting CPU usage: {e}")
        return None

def get_power_consumption():
    """Calculate the power consumption in watts (simplified)."""
    voltage = 5.0  # Raspberry Pi typically operates at 5V
    current = 0.5 + (get_highest_cpu_usage() / 100.0)  # Simplified current draw model (Amps)
    power = voltage * current  # Power in Watts (P = V * I)
    return power

def display_system_stats():
    stats = []  # List to store the last 10 entries

    # Convert hex colors to ANSI escape codes
    color_on = hex_to_ansi(color_on_hex)
    color_off = hex_to_ansi(color_off_hex)
    color_text = hex_to_ansi(color_text_hex)

    # Clear the screen at the start
    os.system('clear')

    while True:
        # Get fan status
        fan_status = GPIO.input(fan_pin)
        fan_indicator = (
            f"{color_on}● {color_text}Fan: ON{reset}" if fan_status == GPIO.HIGH
            else f"{color_off}● {color_text}Fan: OFF{reset}"
        )

        # Get CPU temperature
        cpu_temp = get_cpu_temperature()

        # Get highest CPU usage percentage
        cpu_usage = get_highest_cpu_usage()

        # Get power consumption (simplified calculation)
        power_consumption = get_power_consumption()

        # Append the current stats to the list
        if cpu_temp is not None and cpu_usage is not None:
            stats.append(f"{cpu_temp:<15.2f} | {cpu_usage:<15.2f} | {power_consumption:<15.2f}")

        # Keep only the last 10 entries
        if len(stats) > 10:
            stats.pop(0)

        # Determine the width of the lines
        max_width = max(len("CPU Temp (°C)   | CPU Usage (%)   | Power (W)"), len(fan_indicator))

        # Clear the screen
        os.system('clear')

        # Print the fan status at the top with color
        print(f"{fan_indicator:<{max_width}}")
        print("-" * max_width)

        # Print the header
        header = "CPU Temp (°C)   | CPU Usage (%)   | Power (W)"
        print(header)
        print("-" * max_width)

        # Print the last 10 entries
        for stat in stats:
            print(stat)

        time.sleep(1)

if __name__ == "__main__":
    try:
        display_system_stats()
    except KeyboardInterrupt:
        os.system('clear')  # Clear the screen after interruption
