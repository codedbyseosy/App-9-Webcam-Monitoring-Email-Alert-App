import smtplib, imghdr
from email.message import EmailMessage

PASSWORD = "mkracfvqfywzjydt" # mkra cfvq fywz jydt
SENDER = "odioneseose@gmail.com"
RECEIVER = "odioneseose@gmail.com"

def send_email(image_path):
    email_message = EmailMessage() # create an object instance of the class
                                    # EmailMessage() behaves like a dictionary
    email_message["Subject"] = "New customer showed up!" # create the subject of the email
    email_message.set_content("Hey we just saw a new customer!") # create the body of the email

    # Create attachment to email
    with open(image_path, "rb") as file: # 'rb' because it is a binary file
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # To send out the email
    #gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    gmail.ehlo() # routine code
    # gmail.starttls() # routine code
    gmail.login(SENDER, PASSWORD) # log in to mail
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path="images/19.png")
