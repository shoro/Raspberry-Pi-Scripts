import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

# Configuration
TEXT_X = 0  # X position of the text
TEXT_Y = 0  # Y position of the text
FONT_SIZE = 36  # Font size
UPDATE_INTERVAL = 1.0  # Interval for updating the display in seconds
BOLD_TEXT = True  # Set to True to use bold text, False for normal text
BOLD_OFFSET = 1  # Offset for simulating bold text

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 32

# Initialize I2C and OLED display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display
oled.fill(0)
oled.show()

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Font setup
font = ImageFont.truetype('PixelOperator.ttf', FONT_SIZE)  # Use the configured font size

def draw_text(draw, text, position, font, fill, bold=False):
    """Draw text with optional bold style."""
    if bold:
        # Draw text in a bold style by overlapping it with slight offsets
        offsets = [(0, 0), (BOLD_OFFSET, 0), (0, BOLD_OFFSET), (BOLD_OFFSET, BOLD_OFFSET)]
        for offset in offsets:
            draw.text((position[0] + offset[0], position[1] + offset[1]), text, font=font, fill=fill)
    else:
        # Draw normal text
        draw.text(position, text, font=font, fill=fill)

while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Get CPU temperature
    cmd = "vcgencmd measure_temp | cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    # Process temperature to ensure one decimal place and add the Celsius symbol
    try:
        temp_value = float(temp.split("'")[0])
        temp_display = f"{temp_value:.1f} \u00B0C"  # Format to one decimal place and append °C symbol
    except ValueError:
        temp_display = "N/A"  # In case of an error, display "N/A"

    # Draw the text on OLED at the configured position
    draw_text(draw, temp_display, (TEXT_X, TEXT_Y), font, 255, bold=BOLD_TEXT)
        
    # Display image
    oled.image(image)
    oled.show()
    
    # Wait before updating the display again
    time.sleep(UPDATE_INTERVAL)
