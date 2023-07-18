from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.themoviedb.org"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def retrieveMovieData(moviePath):

    url = BASE_URL + moviePath
    movieContent = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(movieContent.text, "html.parser")
    
    title = soup.find("section", {"class" : "header poster"}).find("a")
    releaseDate = soup.find("section", {"class" : "header poster"}).find("span", {"class" : "release"})
    duration = soup.find("section", {"class" : "header poster"}).find("span", {"class" : "runtime"})
    score = soup.find("section", {"class" : "header poster"}).find("div", {"class" : "user_score_chart"})["data-percent"]
    genres = soup.find("section", {"class" : "header poster"}).find("span", {"class" : "genres"})
    tagLine = soup.find("section", {"class" : "header poster"}).find("h3", {"class" : "tagline"})
    overview = soup.find("section", {"class" : "header poster"}).find("div", {"class" : "overview"})
    director = soup.find("section", {"class" : "header poster"}).find("li", {"class" : "profile"}).find("a")
    budget = soup.find("section", {"class" : "facts"}).find_all("p", {"class" : None})[2].text.split(" ")[1]
    revenue = soup.find("section", {"class" : "facts"}).find_all("p", {"class" : None})[3].text.split(" ")[1]

    # Some movies have no video in the web page
    video = soup.find("section", {"class" : "header poster"}).find("li", {"class" : "video"})
    video = video.find("a")["data-id"] if video is not None else ''
    
    img = soup.find("img", {"class" : "poster"})["src"]
    res = requests.get((BASE_URL + img).replace("_filter(blur)", "")
                       .replace("w300", "w600")
                       .replace("h450", "h900"), headers=HEADERS)
    

    if res.status_code == 200:
        img = res.raw


    print (f"""Tittle: {title.text.strip() if title is not None else ""} 
            Release date: {releaseDate.text.strip() if releaseDate is not None else ""}
            Duration: {duration.text.strip() if duration is not None else ""}
            Score: {score if score is not None else ""}
            Genres: {genres.text.strip() if genres is not None else ""}
            Tagline: {tagLine.text.strip() if tagLine is not None else ""}
            Overview: {overview.text.strip() if overview is not None else ""}
            Director: {director.text.strip() if director is not None else ""}
            Budget: {budget if budget is not None else ""}
            Revenue: {revenue if revenue is not None else ""}
            VideoId: {video}
            Image: {img}
            """)
    
def retrieveTopRatedMoviesByPageParam(pageNumber):

    url = BASE_URL + f"/movie/top-rated?page={pageNumber}"
    pageContent = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(pageContent.text, "html.parser")
    cardContent = soup.find_all("div", {"class":"card style_1"})

    for card in cardContent:
        retrieveMovieData(card.find("a")["href"])


# Loop through the pages

for i in range(1, 2):
    retrieveTopRatedMoviesByPageParam(i)