from heavensabove import HAUtil, Satellite, Iridium
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def main():
    utils = HAUtil(34.0854, -106.8914, 1403, "MST")

    message  = "Interesting astronomical events in the next ten days:\n\n"
    message += "==== Satellite Passes =======================================\n"
    message += str(Satellite("International Space Station", 25544, utils))
    message += str(Satellite("Tiangong-1",                  37820, utils))
    message += "==== Iridium Flares =========================================\n"
    message += str(Iridium(utils))

    email = MIMEText(message)
    email["To"]       = "atl@jbcrawford.us"
    email["Subject"]  = "Upcoming astronomical events"
    p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    p.communicate(email.as_string())

if __name__ == "__main__":
    main()