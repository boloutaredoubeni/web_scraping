#-*- coding: utf-8 -*-
import requests
import bs4
import csv

# NOTE: For this class, I am providing the urls for the pages we will scrape.
# Step 1: Identify page to scrape.
url = "https://www.zumper.com/blog/2015/07/the-10-most-luxurious-apartments-for-rent-in-nyc-right-now/"


# Step 2: Determine what data you'll be retrieving.
    #rank, location, info, price

# Step 3: Inspect and analyze the website's structure to learn how to get the data.
# Step 4: Think about how you want to structure your data.
# Step 5: request for the page’s content with Python Requests and store the content in a variable.
# Step 6: Create a beautiful soup object by passing the variable into the beautiful soup
# Step 7: Parse/Find your desired content with Beautiful Soup methods.
# Step 8: Transform and Store the data in dictionary format.
# Step 9: Use Python’s CSV module to write a CSV file with the web page’s content.

if __name__ == '__main__':
    table = []
    r = requests.get(url)
    html = r.content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    article = soup.find('div', {'class': 'post-body'})
    listings = article.findChildren(name='h3')
    results = [elem.getText().encode('utf-8') for elem in listings]
    DASH = '\xe2\x80\x93'


    def get_entries_as_dict(entry):
        rank, tail = entry.split('.')[0], ''.join(entry.split('.')[1:]).lstrip()
        rank = int(rank)
        location, tail = tail.split(DASH)[0], ' '.join(tail.split(DASH)[1:]).lstrip()
        location = location.rstrip()
        tail = ' '.join(tail.split(' ')).lstrip()
        tail = tail.split(', ')
        #print tail
        info, price = ' '.join(tail[:len(tail)-1]), tail[len(tail)-1]
        return {'rank':rank, 'location':location, 'info':info, 'price':price}

    table += [get_entries_as_dict(entry) for entry in results]


    with open('zumper_data.csv', 'w') as zumper_csv:
        fieldnames = table[0].keys()
        writer = csv.DictWriter(zumper_csv, fieldnames=fieldnames)
        writer.writeheader()
        map(writer.writerow, table)
