import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Function to check product availability
def check_product_availability(product_url, target_price):
    headers = {
        'User-Agent': 'Your User Agent',  # Set your user agent
    }
    
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract information to determine availability (modify as per the website structure)
    product_title = soup.find('h1', {'class': 'seoDescription'}).text.strip()
    product_price = float(soup.find('span', {'class': 'big'}).text.strip().replace('$', '').replace(',', '.'))
    
    # Check if the product is available and the price is below the target
    if 'out of stock' not in soup.text.lower() and product_price <= target_price:
        return True, product_title, product_price
    else:
        return False, product_title, product_price

# Function to send email notification
def send_email(subject, body):
    smtp_server = 'smtp.gmail.com'  # Use Gmail's SMTP server
    smtp_port = 587
    sender_email = 'your_email@gmail.com'  # Your Gmail email address
    sender_password = 'your_password'  # Your Gmail password
    receiver_email = 'recipient_email@example.com'  # Recipient's email address

    message = f'Subject: {subject}\n\n{body}'

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        print('Email notification sent successfully.')
    except Exception as e:
        print(f'Error sending email: {str(e)}')
    finally:
        server.quit()

# Main function
if __name__ == "__main__":
    product_url = 'https://www.eprice.it/Schede-Video-GIGABYTE-Geforce-Rtx-4070-Windforce-Oc-12g-Oc-Edition-Grafikkarten-Geforce-Rtx-4070-12gb-Gddr6x-Pcie-4-0-Hdmi-3-X-Displayport-gv-n4070wf3oc-12gd-/d-67104691'  # URL of the product page
    target_price = 500  # Set your target price
    
    while True:
        available, product_title, product_price = check_product_availability(product_url, target_price)
        
        if available:
            subject = 'Product Available!'
            body = f'The product "{product_title}" is now available at ${product_price}. Buy it now!'
            send_email(subject, body)
            break
        
        print('Product is not available yet. Checking again in 10 minutes...')
        time.sleep(600)  # Check every hour
