#Audiutor

This project has been developed for the Computer Programming course at the University of Bolzano, Ed Faculty. 
It allows you to automatically transcribe and summarize a Youtube video in English using Watson IBM speech to text API. 

Youtube is full of interesting lectures and educational videos, but not everyone has time to watch them. This little program was developed with one goal in mind -- reduce time and allow students and working people to retrieve the information contained in such educational videos, faster. At the moment, the program is available for English videos only and it works with larger files as well.

Before running this program you will need to create your own Watson Speech to text API key and URL, it will literally take 2 minutes of your time. You can do so by (last update June 2021):

1. Registering for free here: https://cloud.ibm.com/registration

2. Creating your Watson Speech to text API key and URL. Just hit the CREATE button (in the right-hand corner below) on this page: https://cloud.ibm.com/catalog/services/speech-to-text'


Call the function:

- audiutor() to run the program 
- transcript_wordcloud() to create a wordcloud
- kws_extraction() to extract keywords

In order for the program to function correctly, please do not change the filenames.

Used dependencies:

from pytube import YouTube
import os
import moviepy.editor as mp
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import subprocess
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from wordcloud import WordCloud
from string import punctuation
import re
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from gensim.summarization import summarize
from random import randrange
from time import sleep
import pprint
import spacy
import textacy.ke
from textacy import *
from docx import Document
import sys









