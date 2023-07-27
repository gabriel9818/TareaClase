import smtplib
import ssl

smtp_server = "smtp.gmail.com"
port = 465  # For SSL

sender_email = "gabrielvega18@outlook.es"
receiver_email = "gabrielruales18@gmail.com"

password = input("Type your password and press enter:")

message = """\
Subject: Hi there
This message is sent from Python."""

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)