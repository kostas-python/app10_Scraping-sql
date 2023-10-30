import requests
import selectorlib
import smtplib, ssl
import time
import sqlite3

"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.15')"
"SELECT * FROM events WHERE date='2088.10.15'"

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    text = response.text
    return text


# Extract the text
def extract(text):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(text)["tours"]
    return value


# Build email function
def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "kostas.com2@gmail.com"
    password = "crbsgaqgrfkcsdgr"

    receiver = "kostas.com2@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


# While loop for keep the programme running

if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
            send_email(message="Hey new event is coming!")
        time.sleep(2)