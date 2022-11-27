from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import nltk
import pytesseract
import re
import slate3k as slate
import pdf2image
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def consume_file(request):
    if request.method == 'POST':
        print(request.FILES['file'])
        return HttpResponse(request.FILES['file'].name)