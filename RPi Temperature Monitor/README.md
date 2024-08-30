# RPi Temperature Monicor

### Installation of Required Libraries
Before running the script, ensure that **'psutil'** is installed:
```
pip install psutil
```

If you get an error try:
```
sudo apt install python3-psutil
```

If you're using Python 3, you may need to use pip3:
```
pip3 install psutil
```

If you get an error try:
```
sudo apt update
```
```
sudo apt install python3-psutil
```

### Download the script

```
curl -O https://github.com/shoro/Raspberry-Pi-Scripts/blob/main/RPi%20Temperature%20Monitor/RPi_tempmon.py
```

### Edit the script
```
sudo nano RPi_tempmon.py
```
> [!CAUTION]
> Make sure to set the **_fan_pin_** if you have a fan conected to your Raspberry Pi.

### Save and Exit
Press: **Ctrl+X, then Y, and ENTER**.

### Run the script

```
sudo python3 RPi_tempmon.py
```

### Stop the script
Press: **CTRL+C**

### FINISH
