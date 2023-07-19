from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.themoviedb.org"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def retrieveData(path):

    url = BASE_URL + path
    movieContent = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(movieContent.text, "html.parser")

    posterSection = soup.find("section", {"class" : "header poster"})
    factsSection = soup.find("section", {"class" : "facts"}).find_all("p", {"class" : None})

    title = posterSection.find("a")
    releaseDate = posterSection.find("span", {"class" : "release"})
    duration = posterSection.find("span", {"class" : "runtime"})
    score = posterSection.find("div", {"class" : "user_score_chart"})["data-percent"]
    genres = posterSection.find("span", {"class" : "genres"})
    tagLine = posterSection.find("h3", {"class" : "tagline"})
    overview = posterSection.find("div", {"class" : "overview"})
    profile = posterSection.find("li", {"class" : "profile"})
    director = posterSection.find("li", {"class" : "profile"}).find("a") if profile is not None else None
    budget = factsSection[2].text.split(" ")[1] if len(factsSection) >= 4 else ""
    revenue = factsSection[3].text.split(" ")[1] if len(factsSection) >= 4 else ""

    video = posterSection.find("li", {"class" : "video"})
    video = video.find("a")["data-id"] if video is not None else ""
    
    img = soup.find("img", {"class" : "poster"})["src"]
    res = requests.get((BASE_URL + img).replace("_filter(blur)", "")
                       .replace("w300", "w600")
                       .replace("h450", "h900"), headers=HEADERS)
    

    if res.status_code == 200:
        img = res.raw


    print (f"""Title: {extractText(title)} 
            Release date: {extractText(releaseDate)}
            Duration: {extractText(duration)}
            Score: {score}
            Genres: {extractText(genres)}
            Tagline: {extractText(tagLine)}
            Overview: {extractText(overview)}
            Director: {extractText(director)}
            Budget: {budget}
            Revenue: {revenue}
            VideoId: {video}
            Image: {img}
            """)
    
def retrieveTopRatedMoviesByPageParam(pageNumber):

    url = BASE_URL + f"/movie/top-rated?page={pageNumber}"
    pageContent = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(pageContent.text, "html.parser")
    cardContent = soup.find_all("div", {"class":"card style_1"})

    for card in cardContent:
        retrieveData(card.find("a")["href"])


def retrieveTopRatedSeriesByPageParam(pageNumber):

    url = BASE_URL + f"/tv/top-rated?page={pageNumber}"
    pageContent = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(pageContent.text, "html.parser")
    cardContent = soup.find_all("div", {"class":"card style_1"})

    for card in cardContent:
        retrieveData(card.find("a")["href"])


def extractText(value):
    return value.text.strip() if value is not None else ""


# Loop through the pages

for i in range(1, 2):
    retrieveTopRatedMoviesByPageParam(i)
    retrieveTopRatedSeriesByPageParam(i)