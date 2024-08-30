# RPi Fan Control

### Create new file named fancontrol.py

```
sudo nano fancontrol.py
```

### Copy code below
Make sure to set the FAN_PIN, TEMP_ON, TEMP_OFF, TEMP_CHECK

```
import RPi.GPIO as GPIO
import time

# Disable warnings for GPIO pins
GPIO.setwarnings(False)

# Set the GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Define the pin to which the fan is connected
FAN_PIN = 14  # GPIO pin 14

# Set the pin as OUTPUT
GPIO.setup(fan_pin, GPIO.OUT)

# Function to read the CPU temperature
def get_cpu_temperature():
    try:
        # Read the CPU temperature from the file
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            temp = int(temp_file.read().strip()) / 1000.0
        return temp
    except Exception as e:
        print(f"Error reading CPU temperature: {e}")
        return None

# Define temperature thresholds
TEMP_ON = 50.0  # Temperature (in Celsius) to turn the fan ON
TEMP_OFF = 40.0 # Temperature (in Celsius) to turn the fan OFF
TEMP_CHECK = 1 # Time before checking the temperature again (seconds)

try:
    while True:
        # Get the current CPU temperature
        temp = get_cpu_temperature()

        if temp is not None:
            print(f"Current CPU Temperature: {temp:.1f}°C")

            # Turn the fan ON if the temperature exceeds TEMP_ON
            if temp > TEMP_ON:
                GPIO.output(FAN_PIN, GPIO.HIGH)
                print("Fan is ON.")
            # Turn the fan OFF if the temperature drops below TEMP_OFF
            elif temp < TEMP_OFF:
                GPIO.output(FAN_PIN, GPIO.LOW)
                print("Fan is OFF.")
        
        # Wait for a while before checking the temperature again
        time.sleep(TEMP_CHECK)

except KeyboardInterrupt:
    # If Ctrl+C is pressed, clean up GPIO settings
    GPIO.cleanup()
    print("Script interrupted. GPIO cleaned.")

```

### Save and exit
CTRL+X > Y > ENTER

### Run the script

```
sudo python3 fancontrol.py
```
