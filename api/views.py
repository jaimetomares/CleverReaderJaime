import json
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import PyPDF2
import requests
import urllib.parse

# Define Semantic Scholar API endpoint and headers
SS_API_URL = "https://api.semanticscholar.org/v1/paper/"

# Function to extract paper title from PDF file
def get_paper_title(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    title = pdf_reader.getDocumentInfo().title
    return title

# Function to search for paper on Semantic Scholar API
def search_paper_on_ss(title):
    query = urllib.parse.quote(title)
    search_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=1"
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        if len(data["data"]) > 0:
            return data["data"][0]["paperId"]
    return None

# Function to get TLDR summary for paper
def get_paper_summary(paper_id):
    if paper_id is not None:
        paper_url = SS_API_URL + paper_id
        response = requests.get(paper_url)
        if response.status_code == 200:
            data = response.json()
            summary = data["abstract"]
            return summary
    return None


def consume_file(request):
    if request.method == 'POST':
        file = request.FILES['file']

        # Verifica si la extensión del archivo es '.pdf'
        if not file.name.endswith('.pdf'):
            return HttpResponseBadRequest("The file must be a PDF.")

        title = get_paper_title(file)
        paper_id = search_paper_on_ss(title)
        summary = get_paper_summary(paper_id)

        if summary is not None:
            print(f"TLDR Summary: {summary}")
            return HttpResponse(json.dumps(summary), content_type="application/json")
        else:
            print("Summary not found.")
            return HttpResponse('Not found', content_type='application/json')
    else:
        return HttpResponseBadRequest("Bad request")
