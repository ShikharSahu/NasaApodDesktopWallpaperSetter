from tkinter import *
from tkcalendar import DateEntry
from datetime import date
from datetime import timedelta
from win10toast import ToastNotifier  
import apod_object_parser
import wallpaper_utility
import threading

def setWallpaperByDate(cal):
    disableButtons()
    response = apod_object_parser.get_data_by_date( wallpaper_utility.APOD_API_KEY, cal.get_date() )
    hd_url = setResultAndGetHdUrl(response)
    image_date = apod_object_parser.get_date(response)
    setWallpaperByHdUrl(hd_url, image_date)
    enableButtons()
    exit()

def setWallpaperByDateThreaded(cal):
    print("setting wallpaper by date")
    e = threading.Event()

    t = threading.Thread(target=setWallpaperByDate, args=(cal,))
    t.start()
    # t.join(30)
    # if t.is_alive:
    #     result.set("request timed out")
    #     e.set()
    # t.join()

def setTodaysPicAsWalpaper():
    disableButtons()
    response = apod_object_parser.get_data(wallpaper_utility.APOD_API_KEY)
    hd_url = setResultAndGetHdUrl(response)
    image_date = apod_object_parser.get_date(response)
    setWallpaperByHdUrl(hd_url, image_date)
    enableButtons()
    exit()


def setTodaysPicAsWalpaperThreaded():
    e = threading.Event()
    t = threading.Thread(target=setTodaysPicAsWalpaper)
    t.start()
    # t.join(30)
    # if t.is_alive:
    #     result.set("request timed out")
    #     e.set()
    # t.join()
# user define function


def setResultAndGetHdUrl(response):
    try:
        print("Sending request")
        hd_url = apod_object_parser.get_hdurl(response)
        print("Request received")
        result.set("url received! :)")
        return hd_url
    except:
        result.set("This date's post is not a image :(")
        return None


def setWallpaperByHdUrl(hd_url, image_date):
    print(" hd_url's image date: "+image_date)
    if (hd_url != None):
        image_downloaded_path = apod_object_parser.download_image(hd_url, image_date)
        wallpaper_utility.changeBG(image_downloaded_path)
        result.set("success! :)")
        n.show_toast(wallpaper_utility.SERVICE_NAME, "Wallpaper changed!", duration = 7,)

def disableButtons():
    setButton["state"] = "disabled"
    useTodaysPic["state"] = "disabled"

def enableButtons():
    setButton["state"] = "normal"
    useTodaysPic["state"] = "normal"

root = Tk()
root.title("NASA APOD Image Setter") 
root.configure(bg='light grey')

n = ToastNotifier()

result = StringVar()
path = StringVar()

Label(root, text="Status : ", bg = "light grey").grid(row=3, sticky=W)
Label(root, text="",textvariable=result, bg = "light grey").grid(row=3, column=1, sticky=W)
yesterdayDate = date.today() - timedelta(days=1)
cal = DateEntry(root, maxdate = yesterdayDate, date_pattern='dd/mm/yyyy')
cal.grid(row = 0, column = 2, columnspan=2, rowspan=2, padx=5, pady=5,)
 
setButton = Button(root, text="Set as wallpaper", command= lambda : setWallpaperByDateThreaded(cal), bg="white")
setButton.grid(row=2, column=2, columnspan=2, rowspan=2, padx=5, pady=5,)

useTodaysPic = Button(root, text="use today's Pic", command= setTodaysPicAsWalpaperThreaded, bg="white")
useTodaysPic.grid(row=4, column=2, columnspan=2, rowspan=2, padx=5, pady=5,)

Label( root, text = "Choose a day from when you need the pic from:", bg="light grey" ).grid(row=0, sticky=W)


mainloop()