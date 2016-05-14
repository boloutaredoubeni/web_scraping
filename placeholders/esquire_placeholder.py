#-*- coding: utf-8 -*-
import requests
import bs4
import csv
import time

# NOTE: For this class, I am providing the urls for the pages we will scrape.
rank_movie_lst = []
for i in xrange(1,100):
    # Step 1: Identify page to scrape.
    url = "http://www.esquire.com/entertainment/movies/g2419/100-best-sci-fi-movies/?slide={}".format(i)

    # Step 2: Determine what data you'll be retrieving.
        # movie_name, rank
    # Step 3: Inspect and analyze the website's structure to learn how to get the data.

    # Step 4: Think about how you want to structure your data.
    # Step 5: request for the page’s content with Python Requests and store the content in a variable.
    # Step 6: Create a beautiful soup object by passing the variable into the beautiful soup
    # Step 7: Parse/Find your desired content with Beautiful Soup methods.
    # Step 8: Transform and Store the data in dictionary format.


    # Step 9: Use Python’s CSV module to write a CSV file with the web page’s content.

    r = requests.get(url)
    html = r.content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    movies = soup.findAll('div', {'class': 'gallery-slide--title'})
    get_movie_rank = lambda m: (m.getText().split('.')[1].encode('utf-8'), m.getText().split('.')[0].encode('utf-8'),)
    rank_movies = {m_r for m_r in (get_movie_rank(movie) for movie in movies if len(movie.getText()) > 0)}
    rank_movie_lst += [{'movie_name': m_r[0], 'movie_rank': m_r[1]} for m_r in rank_movies]

with open('top_scifi_movies.csv', 'w') as csvfile:
    fieldnames = rank_movie_lst[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    rank_movie_lst = {k['movie_rank']:k for k in rank_movie_lst}.values()
    # TODO: sort
    rank_movie_lst.sort(cmp=lambda a, b: cmp(int(a['movie_rank']), int(b['movie_rank'])))
    map(writer.writerow, rank_movie_lst)
