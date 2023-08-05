from setuptools import setup,find_packages
import codecs

VERSION='0.0.1'
DESCRIPTION ='scrap all the data from the website and convert it into requried language'
lONG_DESCRIPTION='scrap all the data from the website and convert it into requried language we use bs4 for scrapping data and google_trans_new module '

setup(
    name = "codeaj",
    version = VERSION,
    author="ajay pandit",
    author_email="<ajayoneness123@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    long_description=lONG_DESCRIPTION,
    install_requires=['requests','bs4','google_trans_new'],
    keywords=['python','scrap',"googe translate"],
   



)