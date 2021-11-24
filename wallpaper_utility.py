import ctypes

APOD_API_KEY = "DEMO_KEY"
SERVICE_NAME = "NASA Wallpaper"

# constant to work with windows 
SPI_SETDESKWALLPAPER = 20
# changes the wallpaper of our system
def changeBG(path):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)