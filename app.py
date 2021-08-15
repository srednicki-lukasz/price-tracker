from bs4 import BeautifulSoup
import requests, smtplib, re

class PriceTracker:
    def __init__(
        self, target_price, request_agent, product_url, product_container, mail_username, mail_password, mail_from, mail_to
    ):
        self.request_agent = request_agent
        self.target_price = target_price
        self.product_url = product_url
        self.product_container = product_container
        self.mail_username = mail_username
        self.mail_password = mail_password
        self.mail_from = mail_from
        self.mail_to = mail_to

    def track(self):
        headers = { "User-Agent": 'user_agent_placeholder' }
        product = requests.get(self.product_url, headers = headers)
        product_soup = BeautifulSoup(product.content, 'html.parser')
        product_price = product_soup.find(attrs = { 'class': self.product_container }).get_text()
        product_price_int = int(re.search(r'\d+', product_price).group(0))

        if product_price_int < self.target_price:
            self.notify(product_price_int)

    def notify(self, new_price):
        smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
        smtpServer.ehlo()
        smtpServer.starttls()
        smtpServer.ehlo()

        smtpServer.login(self.mail_username, self.mail_password)

        mailSubject = 'Price Tracker Notification'
        mailBody = f'The price of the tracked product has changed.\nNew price: {new_price}.\n{self.product_url}'
        message = f'Subject: {mailSubject}\n\n{mailBody}'

        smtpServer.sendmail(self.mail_from, self.mail_to, message)
        print('User Notified')
        smtpServer.quit()

priceTracker = PriceTracker()

priceTracker.track()
