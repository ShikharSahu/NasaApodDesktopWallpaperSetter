from tkinter import *
from tkcalendar import DateEntry
from datetime import date
from datetime import timedelta
from win10toast import ToastNotifier  
import apod_object_parser
import wallpaperUtility
import threading

# user define function
def setWallpaperFunc(cal):
    response = apod_object_parser.get_data_by_date( wallpaperUtility.APOD_API_KEY, cal.get_date() )
    hd_url = setResultAndGetHdUrl(response)
    image_date = apod_object_parser.get_date(response)
    setWallpaperByHdUrl(hd_url, image_date)

def setResultAndGetHdUrl(response):
    try:
        hd_url = apod_object_parser.get_hdurl(response)
        result.set("success")
        return hd_url
    except:
        result.set("This date's post is not a image")
        return None

def setTodaysPicAsWalpaper():
    response = apod_object_parser.get_data(wallpaperUtility.APOD_API_KEY)
    hd_url = setResultAndGetHdUrl(response)
    image_date = apod_object_parser.get_date(response)
    setWallpaperByHdUrl(hd_url, image_date)

def setWallpaperByHdUrl(hd_url, image_date):
    if (hd_url != None):
        image_downloaded_path = apod_object_parser.download_image(hd_url, image_date)
        wallpaperUtility.changeBG(image_downloaded_path)
        n.show_toast(wallpaperUtility.SERVICE_NAME, "Wallpaper changed!", duration = 10)

root = Tk()
root.title("NASA APOD Image Setter") 
root.configure(bg='light grey')

n = ToastNotifier()

result = StringVar()
path = StringVar()

Label(root, text="Status : ", bg = "light grey").grid(row=3, sticky=W)

yesterdayDate = date.today() - timedelta(days=1)
cal = DateEntry(root, maxdate = yesterdayDate)
cal.grid(row = 0, column = 2, columnspan=2, rowspan=2, padx=5, pady=5,)
 
setButton = Button(root, text="Set as wallpaper", command= lambda : setWallpaperFunc(cal), bg="white")
setButton.grid(row=2, column=2, columnspan=2, rowspan=2, padx=5, pady=5,)

useTodaysPic = Button(root, text="use today's Pic", command= lambda : setWallpaperFunc(cal), bg="white")
useTodaysPic.grid(row=4, column=2, columnspan=2, rowspan=2, padx=5, pady=5,)

Label( root, text = "Choose a day from when you need the pic from:", bg="light grey" ).grid(row=0, sticky=W)
print(cal)

mainloop()