import smtplib

SENDER_EMAIL = "EMAIL"
SENDER_PASSWORD = "PASS"
RECEIVER_EMAIL = "EMAIL"

try:
    print("Connecting to Gmail SMTP Server...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    print("Secure connection established!")

    print("Logging in...")
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    print("Login successful!")
    server.quit()

except Exception as e:
    print(f"\nError: {e}")
