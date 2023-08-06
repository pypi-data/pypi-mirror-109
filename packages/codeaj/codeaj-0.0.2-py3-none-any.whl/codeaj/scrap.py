import requests
from bs4 import BeautifulSoup
from google_trans_new import google_translator


def googleTranslate(text, language):
    translator = google_translator()
    translate_text = translator.translate(text, lang_tgt=language)
    print(translate_text)


def scrapall_translate(url, tag, n, language):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    data = soup.find_all(tag)
    for i in range(0, n):
        #try:
        #return data[i].text.strip()
        return googleTranslate(str(data[i].text.strip()),language)
        #except:
         #   break


def scrapallparagraph(url, tag, n):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    data = soup.find_all(tag)
    par = ""
    for i in range(0, n):
        try:
            # print (data[i].text.strip())
            par = par + str(data[i].text.strip())

            # print(par)
        except:
            break
    # print(type(par))
    return par


#  print('after translation')
#   for i in range(0,499):
# print(googleTranslate(par[i],language))


def scrapalldata(url, tag):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    data = soup.find_all(tag)
    for i in range(0, 1000):
        try:
            print(f"{i}. {data[i].text.strip()}")
        except:
            break
        # googleTranslate(str(data[i].text.strip()),language)


def scrapone(url, htmltag):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    data = soup.find_all(htmltag)
    print(data[0].text.strip())


def scrap_div_class(url, clas):
    req = requests.get(url)
    bsobj = BeautifulSoup(req.text, 'html.parser')
    data = bsobj.find_all('div', class_=clas)
    print(data[0].text.strip())
    # googleTranslate(str(data[i].text.strip()),language)


