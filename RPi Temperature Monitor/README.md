# RPi Temperature Monicor

> [!CAUTION]
> Make sure to set the **_FAN_PIN_** correctly in the **_'RPi_fancontrol.py'_** script.

### Download the script

```
curl -O https://github.com/shoro/Raspberry-Pi-Scripts/blob/main/RPi%20Temperature%20Monitor/RPi_tempmon.py
```

### Edit the script
Make sure to set the **_FAN_PIN_**, TEMP_ON, TEMP_OFF, TEMP_CHECK
```
sudo nano RPi_fancontrol.py
```

### Save and Exit
Press: **Ctrl+X, then Y, and ENTER**.

### Run the script

```
sudo python3 RPi_fancontrol.py
```

### Stop the script
Press: **CTRL+C**

# Set the script to run automaticaly on startup

### Create a **'systemd'** Service File:
Create a service file for your script:
```
sudo nano /etc/systemd/system/RPi-fancontrol.service
```

### Configure the Service:
Add the following content to the service file:
```
[Unit]
Description=RPi Fan Control Script
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/'user'/RPi_fancontrol.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
> [!CAUTION]
> Make sure to replace **'/home/"user"/RPi_fancontrol.py'** with the full path to your script.<br>

### Save and Exit
Press: **Ctrl+X, then Y, and ENTER**.

### Enable and Start the Service:
Enable the service to start automatically at boot:
```
sudo systemctl enable RPi-fancontrol.service
```
Start the service immediately to check if it works correctly:
```
sudo systemctl start RPi-fancontrol.service
```

### Check the Service Status:
You can check the service status to see if it is running correctly:
```
sudo systemctl status RPi-fancontrol.service
```

### Restart Service:
You can restart the service after editing the code
```
sudo systemctl restart RPi-fancontrol.service
```

### FINISH

[Create a **_'systemd'_** Service](https://github.com/shoro/Raspberry-Pi-Scripts/blob/main/RPi%20-%20startup%20autorun/3.Creating%20a%20'systemd'%20Service.md)

