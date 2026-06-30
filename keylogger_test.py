import os
import os
import smtplib
import time
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def mail_it():
    from_address = os.environ.get('EMAIL_ADDRESS')
    from_address_password = os.environ.get('EMAIL_PASSWORD')
    to_address = os.environ.get('EMAIL_TO')

    # If environment variables are not set, prompt the user (interactive fallback).
    if not from_address:
        from_address = input('EMAIL_ADDRESS not set. Enter sender email address: ').strip()
    if not to_address:
        to_address = input('EMAIL_TO not set. Enter' \
        ' recipient email address: ').strip()
    if not from_address_password:
        # use getpass so password is not echoed
        from_address_password = getpass.getpass('EMAIL_PASSWORD not set. Enter app password (input hidden): ').strip()

    # final validation
    if not from_address or not from_address_password or not to_address:
        raise ValueError("EMAIL_ADDRESS, EMAIL_PASSWORD and EMAIL_TO must be provided (env or interactive).")

    # Quick ASCII validation: SMTP auth uses ASCII; non-ASCII in credentials will fail
    if any(ord(ch) > 127 for ch in (from_address + from_address_password + to_address)):
        raise ValueError(
            "EMAIL_ADDRESS, EMAIL_PASSWORD and EMAIL_TO must contain only ASCII characters. "
            "If you pasted a password, ensure there are no non-ASCII characters or accidental newlines/spaces. "
            "For Gmail use an App Password (16 ASCII chars)."
        )

    subject = 'Test Email from E-Guard'
    body = 'This is a test message sent from the E-Guard keylogger_test script.'
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            try:
                server.login(from_address, from_address_password)
            except UnicodeEncodeError:
                print("Login failed: username or password contains non-ASCII characters.")
                print("Use a Gmail App Password (16 ASCII characters) or re-enter credentials using only ASCII.")
                raise
            server.sendmail(from_address, to_address, msg.as_string())
        print(f"Email sent to {to_address}")
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication failed. Please check your email address and app password.")
        raise
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise

def main():
    times_run = 10
    for i in range(times_run, 0, -1):
        mail_it()
        print(f'Sent email # {i}')
        time.sleep(5)

if __name__ == "__main__":
    main()
