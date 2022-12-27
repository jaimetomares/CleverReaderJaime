from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import PyPDF2
import re

from langdetect import detect

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from heapq import nlargest


def consume_file(request):
    if request.method == 'POST':
        file = request.FILES['file']

        extension = file.name.split(".")
        extension[1] != "pdf"
        extension = ["sample", "pdf"]
        if(extension[1] != "pdf"):
            return HttpResponse("El archivo debe ser un PDF.")

        doc = PyPDF2.PdfFileReader(file)

        nlp = spacy.load('en_core_web_sm')

        pages = doc.getNumPages()
        text = ""
        for i in range(pages):
            curr_page = doc.getPage(i)
            curr_text = curr_page.extractText()
            text += curr_text.strip()


        pattern = r'(http|https).+?(?=\s|$)'
        # Utiliza re.sub() para buscar el patrón y reemplazarlo con una cadena vacía
        text = re.sub(pattern, '', text)
        
        # Delete reference sections
        text = re.sub(r'References.*', '', text, flags=re.DOTALL)
 
            # Delete tables
        text = re.sub(r'\n\s*\n\s*\|.*\|\s*\n', '\n', text, flags=re.DOTALL)
 
            # Detect titles títulos
        titles = re.findall(r'^\s*#+ .*$', text, flags=re.MULTILINE)
 
            # Delete titles of the text
        for title in titles:
            text = text.replace(title, '')


        # Detect PDF text language
        language = detect(text)
        # Load the appropriate language model based on the detected language
        nlp = spacy.load(f'{language}_core_web_sm')
        #This will return a language object nlp containing all components and data needed to process text.



        


        text = re.sub(r'\[[0-9]*\]', ' ', text)  
        text = re.sub(r'\s+', ' ', text)  

        processedText = re.sub("’", "'", text)
        processedText = re.sub("[^a-zA-Z' ]+", " ", processedText)

        #Here we will create a list of stopwords.
        stopwords = list(STOP_WORDS)

        

        #Calling the nlp object on a string of text will return a processed Doc. During processing, spaCy first tokenizes the text, i.e. segments it into words, punctuation and so on.
        doc = nlp(text)

        #list of tokens
        tokens = [token.text for token in doc]

        #punctuation contains a string of all the punctuations
        punctuation = ""
        punctuation = punctuation + '\n'

        #number of occurrences of all the distinct words in the text which are not punctuations or stop words


        word_frequencies = {}
        for word in doc:
                if word.text.lower() not in stopwords:
                        if word.text.lower() not in punctuation:
                                if word.text not in word_frequencies.keys():
                                        word_frequencies[word.text] = 1
                                else:
                                        word_frequencies[word.text] += 1
                


        max_frequency = max(word_frequencies.values())

        #divide each frequency value in word_frequencies with the max_frequency to normalize the frequencies.
        for word in word_frequencies.keys():
                word_frequencies[word] = word_frequencies[word]/max_frequency


        #sentence tokenization. The entire text is divided into sentences.
        sentence_tokens = [sent for sent in doc.sents]

        # The sentence score for a particular sentence is the sum of the normalized frequencies of the words in that sentence. All the sentences will be 
        # stored with their score in the dictionary sentence_scores.
        sentence_scores = {}
        for sent in sentence_tokens:
                for word in sent:
                        if word.text.lower() in word_frequencies.keys():
                                if sent not in sentence_scores.keys():
                                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                                else:
                                        sentence_scores[sent] += word_frequencies[word.text.lower()]
                

        #We want the length of summary to be 10% of the original length
        select_length = int(len(sentence_tokens)*0.10)

        summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)


        patron = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' 
        urls = re.findall(patron, text)

        
        summary = re.sub("’", "'", summary)
        summary = re.sub("[^a-zA-Z0-9'\"():;,.!?— ]+", " ", summary)

        summary = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", " ", summary)
        summary = re.sub("http[s]?: (?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", " ", summary)

        summary = re.sub('Fig', '', summary)
        summary = re.sub('Figure', '', summary)
        summary = re.sub('page', '', summary)
        summary = re.sub('Page', '', summary)

        summary = re.sub('()', '', summary)


        return HttpResponse(summary)


       

