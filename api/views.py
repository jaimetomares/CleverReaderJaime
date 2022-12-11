from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import re
import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer

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
        extracted_text = ""
        
        # Extract text from PDF file
        # Get each page and extract text
        for i in range(pages):
            curr_page = doc.getPage(i)
            curr_text = curr_page.extractText()
            extracted_text += curr_text


        extracted_text = re.sub(r'\[[0-9]*\]', ' ', extracted_text)  
        extracted_text = re.sub(r'\s+', ' ', extracted_text)  


        processedText = re.sub("’", "'", extracted_text)
        processedText = re.sub("[^a-zA-Z' ]+", " ", processedText)
        stopWords = set(stopwords.words("english"))
        words = word_tokenize(processedText)

        # Normalize words with Porter stemming and build word frequency table
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            elif stemmer.stem(word) in freqTable:
                freqTable[stemmer.stem(word)] += 1
            else:
                freqTable[stemmer.stem(word)] = 1

        # Normalize every sentence in the text
        sentences = sent_tokenize(extracted_text)
        stemmedSentences = []
        sentenceValue = dict()
        for sentence in sentences:
            stemmedSentence = []
            for word in sentence.lower().split():
                stemmedSentence.append(stemmer.stem(word))
            stemmedSentences.append(stemmedSentence)

        # Calculate value of every normalized sentence based on word frequency table
        # [:12] helps to save space
        for num in range(len(stemmedSentences)):
            for wordValue in freqTable:
                if wordValue in stemmedSentences[num]:
                    if sentences[num][:12] in sentenceValue:
                        sentenceValue[sentences[num][:12]] += freqTable.get(wordValue)
                    else:
                        sentenceValue[sentences[num][:12]] = freqTable.get(wordValue)

        # Determine average value of a sentence in the text
        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue.get(sentence)

        average = int(sumValues / len(sentenceValue))

        # Create summary of text using sentences that exceed the average value by some factor
        # This factor can be adjusted to reduce/expand the length of the summary
        summary = ""
        for sentence in sentences:
                if sentence[:12] in sentenceValue and sentenceValue[sentence[:12]] > (3.0 * average):
                    summary += " " + " ".join(sentence.split())

        
        # Process the text in summary and write it to a new file
        summary = re.sub("’", "'", summary)
        summary = re.sub("[^a-zA-Z0-9'\"():;,.!?— ]+", " ", summary)

        summary = re.sub('(https:? )', '', summary)
        summary = re.sub('Fig', '', summary)
        summary = re.sub('Figure', '', summary)
        summary = re.sub('page', '', summary)
        summary = re.sub('Page', '', summary)
        summary = re.sub('doi.org', '', summary)
        summary = re.sub('doi.', '', summary)
        summary = re.sub('org', '', summary)
        summary = re.sub('.com', '', summary)


        summary = re.sub('()', '', summary)
        summary = re.sub(':', '', summary)

        summary = re.sub('0', '', summary)
        summary = re.sub('1', '', summary)
        summary = re.sub('2', '', summary)
        summary = re.sub('3', '', summary)
        summary = re.sub('4', '', summary)        
        summary = re.sub('5', '', summary)
        summary = re.sub('6', '', summary)
        summary = re.sub('7', '', summary)
        summary = re.sub('8', '', summary)
        summary = re.sub('9', '', summary)





        
        return HttpResponse(summary)