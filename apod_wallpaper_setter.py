from logging import error
import wallpaperUtility
from win10toast import ToastNotifier  
import random
from datetime import datetime

from apod_object_parser import download_image, get_data, get_data_array, get_date, get_hdurl, get_url, is_connected

# NASA Astronomical Picture of the Day API Key. "DEMO_KEY" value works too but with 30 requests per hour
# still since we update our wallpaper less frequently we need not worry about the key


def startSetWallpaperProcedure():
    response = get_data(wallpaperUtility.APOD_API_KEY)
    print(response)
    url = get_url(response)
    if not "youtube" in url:
        try:
            # best case, we'll get a hd walpaper for the day.
            hd_url = get_hdurl(response)
        except:
            hd_url = getOneWorkingImageFromArchive()
    else:
        hd_url = getOneWorkingImageFromArchive()
    
    wallpaper_image_path = download_image(hd_url,get_date(response))
    print(wallpaper_image_path)
    wallpaperUtility.changeBG(wallpaper_image_path)
    n.show_toast(wallpaperUtility.SERVICE_NAME, "Wallpaper changed!", duration = 10)


def getOneWorkingImageFromArchive():
    responses_array = get_data_array(wallpaperUtility.APOD_API_KEY)
    print("checking archives:")
    archive_responses_list = []
    print(responses_array)

    for res in responses_array:
        try:
            hd_url = get_hdurl(res)
            archive_responses_list.append(hd_url)
        except:
            pass
    
    if  len(archive_responses_list) == 0 :
        n.show_toast(wallpaperUtility.SERVICE_NAME, "Archive retrieval failed", duration = 10)
        return error
    else :
        return random.seed(datetime.now()).choice(archive_responses_list)

n = ToastNotifier()

if __name__ == "__main__":
    print("Program Started")
    if not is_connected() :
        print("Internet Not Connected")
        n.show_toast(wallpaperUtility.SERVICE_NAME, "Internet not connected")
    else:
        print("Internet is connected")
        startSetWallpaperProcedure()
