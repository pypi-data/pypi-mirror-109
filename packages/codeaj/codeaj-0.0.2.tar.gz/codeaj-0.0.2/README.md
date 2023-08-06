codeaj
Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Ajay Pandit from Codeaj (c) 2021

Examples of How To Use
#install
pip install codeaj

#translate Text

from codeaj import googleTranslate

#googleTranslate(text, language):
googleTranslate("hello ajay", 'hi'):

hi = hindi
ne = nepali
en = english

#scrap data and translate it

from codeaj import scrapall_translate

url= 'https://github.com/NeuralNine/vidstream/blob/main/README.md'
#scrapall_translate(url, tag, n, language):
data=scrapall_translate(url, 'p', 5 , hi):


#to scrap all paragrph

from codeaj import scrapallparagraph

scrapallparagraph(url, p, 10):

#scrap all data

from  codeaj import scrapalldata

#scrapalldata(url, tag):
scrapalldata(url, 'p'):
#you can use any html tag

#scrap one data

from codeaj import scrapone

#scrapone(url, htmltag):
scrapone(url, 'title'):

#scrap data of div class

from codeaj import scrap_div_class

#scrap_div_class(url, clas):
scrap_div_class(url, 'Box d-flex flex-column flex-shrink-0 mb-3'):

----------> AJAY PANDIT