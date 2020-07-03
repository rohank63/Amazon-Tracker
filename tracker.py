import requests
from bs4 import BeautifulSoup
import smtplib
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def check_price():
    check_label = Label(window, text="Checking")
    check_label.grid(row=4, columnspan=2)
    window.update()
    URL = url.get()
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text().strip()

    try:
        str_price = soup.find(id="priceblock_ourprice").get_text()
        price = str_price[2:].replace(',','')
        price = float(price)

        curr_price_label = Label(window, text="Current Price: ")
        price_label = Label(window, text=price)
        curr_price_label.grid(row=5, column=0, padx=5)
        price_label.grid(row=5, column=1)
        window.update()

        if price < float(user_price.get()):
            text = "Email Sent"
            send_mail(URL)
        else:
            text = "Wait for a while!"

        mssg_label = Label(window, text=text)
        mssg_label.grid(row=6, columnspan=2)
    except AttributeError:
        mssg_label = Label(window, text="Currently Unavailable")
        mssg_label.grid(row=6, columnspan=2)


def send_mail(URL):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('rohankandhari63@gmail.com', 'ggizaspgajjyiyip')
    subject = "Price Fell Down"
    body = "Check amazon link"
    message = f"Subject: {subject}\n\n{body}\n\n{URL}"
    server.sendmail(
        'rohankandhari63@gmail.com', 'rohankan73@gmail.com', message
    )
    server.quit()


window = Tk()
window.geometry("300x220")
window.title("Amazon Tracker")
amazon = StringVar()
amazon.set("Amazon")

img = Image.open("C:/Users/Rohan/Downloads/amazon.png").resize((32, 32))
photo = ImageTk.PhotoImage(img)
img_label = ttk.Label(window, image=photo, textvariable=amazon, compound="left")
img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
window.columnconfigure(1, weight=1)
link_label = Label(window, text="URL: ")
url = Entry(window)
url.focus()
price_label = Label(window, text="Your Price: ")
user_price = Entry(window)
submit = Button(window, text="Submit", command=check_price)


link_label.grid(row=1, column=0, pady=5, padx=5)
url.grid(row=1, column=1, pady=5, sticky=EW)
price_label.grid(row=2, column=0, pady=5, padx=5)
user_price.grid(row=2, column=1, pady=5)
submit.grid(row=3, column=1, columnspan=2, pady=5)

window.update()
window.mainloop()
