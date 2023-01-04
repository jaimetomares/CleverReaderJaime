from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import PyPDF2
import re

import openai



def consume_file(request):
    if request.method == 'POST':
        file = request.FILES['file']

        extension = file.name.split(".")
        extension[1] != "pdf"
        extension = ["sample", "pdf"]
        if(extension[1] != "pdf"):
            return HttpResponse("El archivo debe ser un PDF.")

        doc = PyPDF2.PdfFileReader(file)

        output = PyPDF2.PdfWriter()

        pages = len(doc.pages)

        openai.api_key = "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"
        model_engine = "text-davinci-003"


        pages = doc.getNumPages()
        text = ""
        for i in range(pages):
            curr_page = doc.pages[i]
            output.add_page(curr_page)
            output.remove_images()
            output.remove_links()
            curr_page = output.pages[i]
            curr_text = curr_page.extract_text()
            text += curr_text


        
        
        # Delete reference sections
        text = re.sub(r'References.*', '', text, flags=re.DOTALL)
 
            # Delete tables
        text = re.sub(r'\n\s*\n\s*\|.*\|\s*\n', '\n', text, flags=re.DOTALL)
 
            # Detect titles títulos
        titles = re.findall(r'^\s*#+ .*$', text, flags=re.MULTILINE)

        pattern = r'(http|https).+?(?=\s|$)'
        # Utiliza re.sub() para buscar el patrón y reemplazarlo con una cadena vacía
        text = re.sub(pattern, '', text)
 
            # Delete titles of the text
        for title in titles:
            text = text.replace(title, '')





        


        text = re.sub(r'\[[0-9]*\]', ' ', text)  
        text = re.sub(r'\s+', ' ', text)  

        processedText = re.sub("’", "'", text)
        processedText = re.sub("[^a-zA-Z' ]+", " ", processedText)


        





        return HttpResponse(summary)


       

