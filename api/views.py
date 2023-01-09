import json
import os

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import PyPDF2
import re
import concurrent.futures
import openai
from unidecode import unidecode


def consume_file(request):
    if request.method == 'POST':
        file = request.FILES['file']

        # Verifica si la extensión del archivo es '.pdf'
        if not file.name.endswith('.pdf'):
            return HttpResponseBadRequest("The file must be a PDF.")

        # Read the PDF file
        doc = PyPDF2.PdfFileReader(file)

        # Initialize a PDF writer
        output = PyPDF2.PdfWriter()

        # Get the number of pages in the PDF
        pages = doc.getNumPages()

        # Set the API key and model for OpenAI
        openai.api_key = os.environ.get("API_KEY")
        model_engine = "text-davinci-003"

        # Get the number of pages in the PDF
        pages = doc.getNumPages()

        # Initialize an empty string to store the text
        text = ""

        # Iterate through each page in the PDF
        for i in range(pages):
            # Get the current page
            curr_page = doc.pages[i]
            # Add the current page to the output PDF
            output.add_page(curr_page)
            # Remove images from the current page
            output.remove_images()
            # Remove links from the current page
            output.remove_links()
            # Get the current page from the output PDF
            curr_page = output.pages[i]
            # Extract the text from the current page
            curr_text = curr_page.extract_text()
            # Append the extracted text to the text string
            text = unidecode(text)

            text += curr_text

        # Delete the reference sections from the text
        text = re.sub(r'References.*', '', text, flags=re.DOTALL)

        # Delete tables from the text
        text = re.sub(r'\n\s*\n\s*\|.*\|\s*\n', '\n', text, flags=re.DOTALL)

        # Define a pattern for URLs
        pattern = r'(http|https).+?(?=\s|$)'
        # Use re.sub() to search for the pattern and replace it with an empty string
        text = re.sub(pattern, '', text)

        # Replace curly quotes with straight quotes
        text = re.sub("’", "'", text)
        # Replace any non-alphanumeric, non-quote, non-colon, non-semicolon, non-period, non-exclamation, non-question mark characters with a space
        # Replace any non-alphanumeric, non-quote characters with a space
        text = re.sub("[^a-zA-Z0-9\s\"\':;,.!?]+", " ", text)
        # Remove empty parentheses
        text = re.sub('()', '', text)
        # Remove bracketed numbers
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        # Replace curly quotes with straight quotes
        text = re.sub("’", "'", text)
        # Replace any non-alphanumeric, non-quote characters with a space
        text = re.sub("[^a-zA-Z' ]+", " ", text)

        # Remove the word 'Fig' from the text
        text = re.sub('Fig', '', text)
        # Remove the word 'Figure' from the text
        text = re.sub('Figure', '', text)
        # Remove the word 'page' from the text
        text = re.sub('page', '', text)
        # Remove the word 'Page' from the text
        text = re.sub('Page', '', text)

        # Initialize an empty string to store the summary
        res = ""

        # Set the summary instruction for the GPT model
        summary = "Summarize the following text and group it by its content, ignoring the unsense phrases \n"

        # Divide the text into chunks of x characters
        context_parts = [(summary + "Fragment: " + str(i) + "\n" + text[i:i + 4500]) for i in range(0, len(text), 4500)]

        # Create a ThreadPoolExecutor with the same number of threads as the number of processors in your machine
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of futures with the threads that will perform the summary of each fragment
            futures = [executor.submit(lambda context_part:
                                       openai.Completion.create(engine=model_engine, prompt=context_part,
                                                                max_tokens=160, n=1, stop=None, temperature=0.75,
                                                                top_p=1, frequency_penalty=0,
                                                                presence_penalty=0).choices[0].text, context_part) for
                       context_part in context_parts]

            # Iterate through the list of futures and collect the result of each one
            for future in concurrent.futures.as_completed(futures):
                res += future.result()
        response_data = {'data': res}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
