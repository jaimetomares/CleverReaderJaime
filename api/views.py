from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import PyPDF2
import re
import json


import spacy
import pytextrank
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import pipeline

from heapq import nlargest

def consume_file(request):
    if request.method == 'POST': 

        file = request.FILES['file']

        extension = file.name.split(".")
        extension[1] != "pdf"
        extension = ["sample", "pdf"]
        if(extension[1] != "pdf"):
            return HttpResponseBadRequest

        doc = PyPDF2.PdfFileReader(file)
        pages = doc.getNumPages()
        text = ""
        
        # Extract text from PDF file
        # Get each page and extract text
        for i in range(pages):
            curr_page = doc.getPage(i)
            curr_text = curr_page.extractText()
            text += curr_text.strip()



        #Here we will create a list of stopwords.
        stopwords = list(STOP_WORDS)

        #This will return a language object nlp containing all components and data needed to process text.
        nlp = spacy.load('en_core_web_sm')

        #Calling the nlp object on a string of text will return a processed Doc. During processing, spaCy first tokenizes the text, i.e. segments it into words, punctuation and so on.
        doc = nlp(text)

        #list of tokens
        tokens = [token.text for token in doc]
#print(tokens)

        #punctuation contains a string of all the punctuations
        punctuation = ""
        punctuation = punctuation + '\n'
#print(punctuation)

        #number of occurrences of all the distinct words in the text which are not punctuations or stop words


        word_frequencies = {}
        for word in doc:
                if word.text.lower() not in stopwords:
                        if word.text.lower() not in punctuation:
                                if word.text not in word_frequencies.keys():
                                        word_frequencies[word.text] = 1
                                else:
                                        word_frequencies[word.text] += 1
                
        #print(word_frequencies)


        max_frequency = max(word_frequencies.values())
        #print(max_frequency)

        #divide each frequency value in word_frequencies with the max_frequency to normalize the frequencies.
        for word in word_frequencies.keys():
                word_frequencies[word] = word_frequencies[word]/max_frequency

        #print(word_frequencies)

        #sentence tokenization. The entire text is divided into sentences.
        sentence_tokens = [sent for sent in doc.sents]
        #print(sentence_tokens)

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
                
#print(sentence_scores)

        #We want the length of summary to be 15% of the original length
        select_length = int(len(sentence_tokens)*0.15)
#print(sentence_scores)

        summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
#print(summary)

        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)


        patron = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' 
        urls = re.findall(patron, text)

        
        summary = re.sub("’", "'", summary)
        summary = re.sub("[^a-zA-Z0-9'\"():;,.!?— ]+", " ", summary)

        summary = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "'", summary)
        summary = re.sub('(https:? )', '', summary)
        summary = re.sub('Fig', '', summary)
        summary = re.sub('Figure', '', summary)
        summary = re.sub('page', '', summary)
        summary = re.sub('Page', '', summary)




        print(text)

        print(summary)

        print(len(text))

        print(len(summary))

        return HttpResponse(summary)


        #1st way to do it would be using textrank and spacy
        #--------------------------------------------------
"""
nlp= spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")
doc = nlp(text)


for line in doc._.textrank.summary(limit_sentences=5):
    print(line)
"""

        #2nd way to do it would be using pegasus tokenizer
        #-------------------------------------------------
""""
model_name = "google/pegasus-xsum"
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)
tokens = pegasus_tokenizer(text, truncation=True, padding="longest", return_tensors="pt")

encoded_summary = pegasus_model.generate(**tokens)
decoded_summary = pegasus_tokenizer.decode(encoded_summary[0], skip_special_tokens=True)


        #3rd way is simmilar, but uses pipeline, preferable way
        #-------------------------------------------------

summarizer = pipeline("summarization", model=model_name, tokenizer=pegasus_tokenizer, framework="pt")

summary = summarizer(text, min_length=60)

print(decoded_summary)

"""


        #OR.........
"""
try:
    summary = summarizer(summarizer, text, max_length=max_len, min_length=10, do_sample=False)
    return summary
except IndexError as ex:
    return summarize_text(summarizer, text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

"""