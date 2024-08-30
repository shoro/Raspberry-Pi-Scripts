import time
import psutil
import os
import RPi.GPIO as GPIO

# Version 1.31 - Added configurable update interval and display columns

# Configuration
fan_pin = 14  # Set the GPIO pin number for the fan
color_on_hex = '#00FF00'  # HEX color for Fan: ON (green)
color_off_hex = '#FF0000'  # HEX color for Fan: OFF (red)
last_row_color_hex = '#00FF00'  # HEX color for the last row (green)
update_interval = 0.5  # Set the update interval in seconds (e.g., 0.5 for faster updates)
display_columns = ['temp', 'cpu', 'power']  # Choose which columns to display: 'temp', 'cpu', 'power'

# Convert HEX color to ANSI escape code for the bullet
def hex_to_ansi_bullet(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m●\033[0m"

# Convert HEX color to ANSI escape code for text
def hex_to_ansi_text(hex_color):
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
        cpu_usages = psutil.cpu_percent(percpu=True, interval=0.1)  # Reduced interval for faster update
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

    # Convert HEX colors to ANSI escape codes
    color_on = hex_to_ansi_text(color_on_hex)
    color_off = hex_to_ansi_text(color_off_hex)
    last_row_color = hex_to_ansi_text(last_row_color_hex)
    
    # Clear the screen at the start
    os.system('clear')

    while True:
        # Get fan status
        fan_status = GPIO.input(fan_pin)
        if fan_status == GPIO.HIGH:
            fan_indicator = f"{hex_to_ansi_bullet(color_on_hex)} Fan: ON"
        else:
            fan_indicator = f"{hex_to_ansi_bullet(color_off_hex)} Fan: OFF"

        # Get CPU temperature
        cpu_temp = get_cpu_temperature()

        # Get highest CPU usage percentage
        cpu_usage = get_highest_cpu_usage()

        # Get power consumption (simplified calculation)
        power_consumption = get_power_consumption()

        # Create a line for the stats based on selected columns
        line = []
        if 'temp' in display_columns and cpu_temp is not None:
            line.append(f"{cpu_temp:<15.2f}")
        if 'cpu' in display_columns and cpu_usage is not None:
            line.append(f"{cpu_usage:<15.2f}")
        if 'power' in display_columns and power_consumption is not None:
            line.append(f"{power_consumption:<15.2f}")

        # Append the current stats to the list if any columns are selected
        if line:
            stats.append(" | ".join(line))

        # Keep only the last 10 entries
        if len(stats) > 10:
            stats.pop(0)

        # Determine the width of the lines
        header_parts = []
        if 'temp' in display_columns:
            header_parts.append(f"{'CPU Temp (°C)':<15}")
        if 'cpu' in display_columns:
            header_parts.append(f"{'CPU Usage (%)':<15}")
        if 'power' in display_columns:
            header_parts.append(f"{'Power (W)':<15}")
        header = " | ".join(header_parts)

        max_width = max(len(fan_indicator), len(header))
        for stat in stats:
            max_width = max(max_width, len(stat))

        # Clear the screen
        os.system('clear')

        # Print the fan status at the top
        print(f"{fan_indicator:<{max_width}}")
        print("-" * max_width)

        # Print the header based on selected columns
        print(header)
        print("-" * max_width)

        # Print the last 10 entries with the last row colored
        for i, stat in enumerate(stats):
            if i == len(stats) - 1:  # Check if it's the last row
                print(f"{last_row_color}{stat:<{max_width}}{reset}")
            else:
                print(stat)

        time.sleep(update_interval)  # Use the configurable update interval

if __name__ == "__main__":
    try:
        display_system_stats()
    except KeyboardInterrupt:
        os.system('clear')  # Clear the screen after interruption
