# CleverReaderJaime

        Repository for summary service

This program runs in a Django environment and is located in a folder called 'api/views.py'. A PDF file submitted via a POST request is processed and returns the result of an OpenAI model processing the text of the file.

To use this feature, you must ensure that you have Django and PyPDF2 installed in your environment, and that you set up a valid API key for OpenAI. You must also specify the model engine you want to use in the line model_engine = "text-davinci-003".

The file is obtained from a POST request and is checked to see if it is a PDF file.
This function consumes a PDF file and processes its content to remove images, links, and tables.
The pages of the PDF file are read and the images and links are removed from each page using PyPDF2.
The text extracted from each page is concatenated into a text string.
The text string is cleaned of reference sections, tables, URLs and special characters.
Some specific keywords are removed from the text.
The processed text is sent to an OpenAI model for processing and the result is returned to the user.
