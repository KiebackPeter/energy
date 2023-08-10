from time import sleep
from schedule import run_pending, every
from datetime import datetime
from app.internal.session import www


def main():
    print(f"running update: {datetime.now()}")
    www.set_token()
    www.update()
    print("waiting for next day...")


def loop():
    every().day.at("12:00").do(main)
    while True:
        run_pending()
        sleep(60*30)

if __name__ == "__main__":
    loop()
