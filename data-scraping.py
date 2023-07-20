from bs4 import BeautifulSoup
import requests
import json
import base64

BASE_URL = "https://www.themoviedb.org"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

JSON_DATA = {
    "content" : []
}

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
        img = base64.b64encode(res.content).decode()
    else:
        img = ""

    data = {
        "title" : extractText(title),
        "release-date" : extractText(releaseDate),
        "duration" : extractText(duration),
        "score" : score,
        "genres" : extractText(genres),
        "tagline" : extractText(tagLine),
        "overview" : extractText(overview),
        "director" : extractText(director),
        "budget" : budget,
        "revenue" : revenue,
        "video-id" : video,
        "image" : img
     }
    
    JSON_DATA['content'].append(data)
    
    
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

dataString = json.dumps(JSON_DATA, indent = 2, ensure_ascii=False)

with open("test.json", "w") as f:
    f.write(dataString)