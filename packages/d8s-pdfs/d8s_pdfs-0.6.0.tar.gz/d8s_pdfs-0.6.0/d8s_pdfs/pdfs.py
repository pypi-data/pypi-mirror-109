import tempfile
from typing import Iterable

import PyPDF2
from d8s_file_system import file_write
from d8s_networking import get
from d8s_urls import is_url


def pdf_read(pdf_path: str) -> Iterable[str]:
    """Get the string from the PDF at the given path/URL."""
    temp_file = None

    # check if the pdf_path is a url
    if is_url(pdf_path):
        temp_file = tempfile.TemporaryFile()
        temp_file_path = str(temp_file.name)
        file_write(temp_file_path, get(pdf_path, process_response_as_bytes=True))
        pdf_path = temp_file_path

    with open(pdf_path, 'rb') as f:
        try:
            pdf = PyPDF2.PdfFileReader(f)
        except PyPDF2.utils.PdfReadError as e:
            message = 'Unable to read the pdf at {}: {}'.format(pdf_path, e)
            raise RuntimeError(message)
        else:
            for i in range(0, pdf.numPages):
                page = pdf.getPage(i)
                page_content = page.extractText()
                yield page_content

    if temp_file is not None:
        result = temp_file.close()
