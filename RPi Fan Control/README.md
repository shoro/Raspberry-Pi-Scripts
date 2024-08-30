# RPi Fan Control

### Download the script

```
curl -O https://raw.githubusercontent.com/shoro/Raspberry-Pi-Scripts/main/RPi%20Fan%20Control/RPi-fancontrol.py
```

### Edit the script
Make sure to set the FAN_PIN, TEMP_ON, TEMP_OFF, TEMP_CHECK
```
sudo nano RPi-fancontrol.py
```

### Save and exit
CTRL+X > Y > ENTER

### Run the script

```
sudo python3 RPi-fancontrol.py
```

### Stop the script
CTRL+C

### Set the script to run automaticaly on startup
Use one of the following methods

[Add script to **_'rc.local'_**](https://github.com/shoro/Raspberry-Pi-Scripts/blob/main/RPi%20-%20startup%20autorun/1.Add%20script%20to%20'rc.local'.md)

OR

CRON

OR

SERVICE
