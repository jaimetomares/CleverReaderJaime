import unittest
from unittest.mock import patch

from django.test import RequestFactory

from .views import consume_file


class ConsumeFileTests(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_request(self):
        """Tests that the view returns an HttpResponse when a POST request is made"""
        request = self.factory.post('/consume_file', {'file': 'test.pdf'})
        response = consume_file(request)
        self.assertEqual(response.status_code, 200)

    def test_get_request(self):
        """Tests that the view returns a Bad Request when a GET request is made"""
        request = self.factory.get('/consume_file')
        response = consume_file(request)
        self.assertEqual(response.status_code, 400)

    def test_file_extension(self):
        """Tests that the view returns an error message if the file is not a PDF"""
        request = self.factory.post('/consume_file', {'file': 'test.docx'})
        response = consume_file(request)
        self.assertEqual(response.content, b"The file must be a PDF.")

    @patch('PyPDF2.PdfFileReader')
    def test_pdf_file_processing(self, mock_reader):
        """Tests that the view processes the PDF file correctly"""
        mock_reader.return_value.getNumPages.return_value = 2
        mock_reader.return_value.pages = [{}, {}]
        request = self.factory.post('/consume_file', {'file': 'test.pdf'})
        consume_file(request)
        self.assertEqual(mock_reader.return_value.getNumPages.call_count, 1)
        self.assertEqual(mock_reader.return_value.pages, [{}, {}])

    @patch('PyPDF2.PdfFileReader')
    def test_pdf_file_processing_error(self, mock_reader):
        """Tests that the view handles errors when processing the PDF file"""
        mock_reader.side_effect = Exception("Error processing PDF file")
        request = self.factory.post('/consume_file', {'file': 'test.pdf'})
        response = consume_file(request)
        self.assertEqual(response.status_code, 500)

    @patch('PyPDF2.PdfFileReader')
    def test_text_extraction(self, mock_reader):
        """Tests that the view extracts the text from the PDF correctly"""
        mock_reader.return_value.getNumPages.return_value = 2
        mock_reader.return_value.pages = [
            {'extract_text': lambda: 'Text from page 1'},
            {'extract_text': lambda: 'Text from page 2'},
        ]
        request = self.factory.post('/consume_file', {'file': 'test.pdf'})
        response = consume_file(request)
        self.assertEqual(response.content, b'Text from page 1 Text from page 2')



 