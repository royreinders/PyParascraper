from bs4 import BeautifulSoup
import requests
import os
import telegram
import time

# Global variables to set parameters for search queries and notifications
city = 'utrecht'
min_m2 = 40
min_price = 600
max_price = 1100
filename = "new_listings.txt"
telegram_API_TOKEN = 'APITOKEN'
# Start a chat with your bot, then visit https://api.telegram.org/bot<YourBOTToken>/getUpdates to see your token
telegram_chat_ID = 'ID'
interval = 10   # minutes


# Send push-notification to the desired chat
def notify(new_listings):
    bot = telegram.Bot(token=telegram_API_TOKEN)
    for listing in new_listings:
        listing = listing
        bot.send_message(chat_id=telegram_chat_ID, text=f'New apartment available!\n{listing}')
        print(listing)


# Check whether given listings have already been found in a previous run
def containsnew(listings):
    # If file does not exist, create it
    if not os.path.exists(filename):
        open(filename, 'w').close()
    with open(filename, 'r+') as f:
        known_listings = [line.rstrip() for line in f]
        listings = [str(listing) for listing in listings]
        new_listings = list(set(listings) - set(known_listings))

        if new_listings:
            for listing in new_listings:
                f.write(str(listing) + '\n')
            return new_listings


# Scrape Pararius page and get the first 30 listings
def get_listings():
    url = 'https://www.pararius.nl/huurwoningen/' + city + '/' + str(min_price) + '-' + str(max_price) + '/' + str(min_m2) + 'm2'

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    headers = {'User-Agent': user_agent}
    content = requests.get(url, headers=headers)
    soup = BeautifulSoup(content.text, features='html.parser')
    # Search for the a-tag containing the listings
    listings = soup.find_all('a', class_='listing-search-item__link listing-search-item__link--title')

    new_listings = containsnew(listings)
    if new_listings:
        notify(new_listings)


def main():
    while True:
        try:
            get_listings()
        except Exception:
            notify(['!! SOMETHING WENT WRONG !!'])
        finally:
            time.sleep(interval * 60)   # Poor mans delay


if __name__ == "__main__":
    main()
