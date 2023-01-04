from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import PyPDF2
import re

import concurrent.futures

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
 

        pattern = r'(http|https).+?(?=\s|$)'
        # Utiliza re.sub() para buscar el patrón y reemplazarlo con una cadena vacía
        text = re.sub(pattern, '', text)
 
        text = re.sub("’", "'", text)
        text = re.sub("[^a-zA-Z0-9'\"():;,.!?— ]+", " ", text)
        text = re.sub('()', '', text)
        text = re.sub(r'\[[0-9]*\]', ' ', text)  
        text = re.sub(r'\s+', ' ', text)
        text = re.sub("’", "'", text)
        text = re.sub("[^a-zA-Z' ]+", " ", text)


        text = re.sub('Fig', '', text)
        text = re.sub('Figure', '', text)
        text = re.sub('page', '', text)
        text = re.sub('Page', '', text)

        res = ""
        summary = "Summarize the following text and group it by its content, ignoring the unsense phrases \n" #Instrucción que darle a GPT
        context_parts = [(summary + "Fragment: " + str(i) + "\n" + text[i:i+4000]) for i in range(0, len(text), 3200)] #Se divide el texto en chunks

        # Crea un Executor con un número de hilos igual al número de procesadores de tu máquina
        with concurrent.futures.ThreadPoolExecutor() as executor:
    # Crea una lista de futuros con los hilos que se encargarán de realizar el resumen de cada fragmento
            futures = [executor.submit(lambda context_part: openai.Completion.create(engine=model_engine, prompt=context_part, max_tokens=150, n=1,stop=None,temperature=0.75, top_p=1, frequency_penalty=0, presence_penalty=0).choices[0].text, context_part) for context_part in context_parts]

    # Recorre la lista de futuros y recoge el resultado de cada uno
            for future in concurrent.futures.as_completed(futures):
                res += future.result()


        return HttpResponse(res)


       

