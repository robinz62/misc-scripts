from bs4 import BeautifulSoup
from urllib import request
import time

# codeforces ratings page
URL = 'http://codeforces.com/ratings/page/'

# number of pages of ratings
MAX_PAGE = 510

# where the ratings table appears in the html doc
RATING_TABLE_INDEX = 5


def scrape_ratings(filename):
    """Scrapes the codeforces ratings pages and writes a list of all ratings
    of users who have participated in at least 5 contests to a file."""
    ratings = []
    for page in range(1, MAX_PAGE + 1):
        print('opening page ' + str(page))
        fp = request.urlopen(URL + str(page))
        html = fp.read().decode('utf8')
        fp.close()

        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find_all('table')[RATING_TABLE_INDEX]
        rows = table.find_all('tr')
        for i, row in enumerate(rows[1:]):
            cells = row.find_all('td')
            num_contests = int(cells[2].get_text().strip())
            rating = cells[3].get_text().strip()
            if (num_contests >= 5):
                ratings.append(rating)
        time.sleep(1)

    with open(filename, 'w') as f:
        f.write(','.join(ratings))

def rating_to_title(rating):
    if rating <= 1199:
        return 'Newbie'
    if rating <= 1399:
        return 'Pupil'
    if rating <= 1599:
        return 'Specialist'
    if rating <= 1899:
        return 'Expert'
    if rating <= 2099:
        return 'Candidate Master'
    if rating <= 2299:
        return 'Master'
    if rating <= 2399:
        return 'International Master'
    if rating <= 2599:
        return 'Grandmaster'
    if rating <= 2999:
        return 'International Grandmaster'
    return 'Legendary Grandmaster'

if __name__ == '__main__':
    # Comment out the following line if file is already generated
    # Last grabbed 10/2020
    # scrape_ratings('data/ratings.txt')

    ratings = []
    with open('data/ratings.txt', 'r') as file:
        for line in file:
            ratings.extend([int(num) for num in line.split(',')])

    freq = {}
    for r in ratings:
        freq[rating_to_title(r)] = freq.get(rating_to_title(r), 0) + 1

    curr = 0
    for rank in ['Newbie', 'Pupil', 'Specialist', 'Expert', 'Candidate Master',
                 'Master', 'International Master', 'Grandmaster',
                 'Legendary Grandmaster']:
        curr += freq[rank]
        print(rank + ': ' + str(freq[rank]) + ' ' + str((curr / len(ratings))))

    p = int(input('Enter rating to get percentile: '))
    count = 0
    for r in ratings:
        if r < p:
            count += 1

    print(count / len(ratings))
