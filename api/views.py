from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import PyPDF2
import re



def consume_file(request):
    if request.method == 'POST':
        file = request.FILES['file']

        extension = file.name.split(".")
        extension[1] != "pdf"
        extension = ["sample", "pdf"]
        if(extension[1] != "pdf"):
            return HttpResponse("El archivo debe ser un PDF.")

        doc = PyPDF2.PdfFileReader(file)


        pages = doc.getNumPages()
        text = ""
        for i in range(pages):
            curr_page = doc.getPage(i)
            curr_text = curr_page.extractText()
            text += curr_text.strip()


        
        
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


       

