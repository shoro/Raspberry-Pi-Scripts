# RPi Fan Control

> [!CAUTION]
> Make sure to set the **_FAN_PIN_** correctly in the **_'RPi-fancontrol.py'_** script.

### Download the script

```
curl -O https://raw.githubusercontent.com/shoro/Raspberry-Pi-Scripts/main/RPi%20Fan%20Control/RPi-fancontrol.py
```

### Edit the script
Make sure to set the **_FAN_PIN_**, TEMP_ON, TEMP_OFF, TEMP_CHECK
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

[Using **_'cron'_** with **_'@reboot'_**](https://github.com/shoro/Raspberry-Pi-Scripts/blob/main/RPi%20-%20startup%20autorun/2.Using%20'cron'%20with%20'@reboot'.md)

OR

[Create a **_'systemd'_** Service](https://github.com/shoro/Raspberry-Pi-Scripts/blob/main/RPi%20-%20startup%20autorun/3.Creating%20a%20'systemd'%20Service.md)
