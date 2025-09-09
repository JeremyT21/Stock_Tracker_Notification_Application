import undetected_chromedriver as uc
import smtplib
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#store search page URL
URL = "STORE_URL"

#email setup (use app password for gmail)
SENDER_EMAIL = "EMAIL_SEND"
SENDER_PASSWORD = "PASS"
RECEIVER_EMAIL = "EMAIL_RECEIVE"

#store previously found products to avoid duplicate emails
previous_links = set()
keywords = []

def check_stock():
    global previous_links
    global keywords

    print("Initializing Undetected ChromeDriver...")
    driver = uc.Chrome(headless=False)  #set headless=True so program runs in background

    print("Loading Store item page...")
    driver.get(URL)

    try:
        #wait for product links to be visible (timeout after 30 seconds)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/ip/')]")))
        print("Store page loaded successfully!")

    except Exception as e:
        print("Error: Store page did not load product links in time.")
        print(driver.page_source)  #for debugging: print the whole store HTML page
        driver.quit()
        return

    #find all product links
    product_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/ip/')]")

    print("\nFound HREFs:")
    found_products = {}

    #keywords representing items you want to be notified for - to search in href (links in webpage) (case insensitive)
    keywords = ["new","apple"]

    for product in product_links:
        href = product.get_attribute("href")  #extract actual link object
        
        if href:
            print(href)  #for debugging: print all found links

            #check if any keyword is in the href link (case-insensitive)
            if any(keyword in href.lower() for keyword in keywords):
                found_products[href] = href  #store the matching product link

    driver.quit()  #close browser session

    print(f"\nFound {len(found_products)} matching products.")

    #see if found new products not seen before
    new_products = {href: link for href, link in found_products.items() if href not in previous_links}

    if new_products:
        print("\nNew matching products found! Sending email...")
        previous_links.update(new_products.keys())  #update the stored products
        send_email(new_products)

    else:
        print("\nNo new products found.")
        send_email_no_products()

def send_email(products):
    subject = "New items found at Store!"
    body = "Check out the new items:\n\n" + "\n".join([f"{link}" for link in products.values()])
    message = f"Subject: {subject}\n\n{body}"

    print("\nAttempting to send email with the following content:")
    print(message)  #for debug: print email content before sending

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            print("\nLogging into email...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Sending email...")
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)

        print("\nEmail sent successfully!")

    except Exception as e:
        print(f"\nError sending email: {e}")

def send_email_no_products():
    global keywords

    subject = "NO new items found at Store!"
    body = f"NOTHING found relating to the keywords: {keywords}"
    message = f"Subject: {subject}\n\n{body}"

    print("\nAttempting to send email with the following content:")
    print(message)  #for debug: print email content before sending

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            print("\nLogging into email...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Sending email...")
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)

        print("\nEmail sent successfully!")

    except Exception as e:

        print(f"\nError sending email: {e}")

if __name__ == "__main__":
    check_stock()
