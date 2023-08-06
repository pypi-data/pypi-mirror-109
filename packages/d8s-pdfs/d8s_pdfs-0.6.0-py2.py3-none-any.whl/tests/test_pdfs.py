import pytest

from d8s_pdfs import pdf_read

EXPECTED_RESULT = [
    ' A Simple PDF File  This is a small demonstration .pdf file -  just for use in the Virtual Mechanics tutorials. More text. And more  text. And more text. And more text. And more text.  And more text. And more text. And more text. And more text. And more  text. And more text. Boring, zzzzz. And more text. And more text. And  more text. And more text. And more text. And more text. And more text.  And more text. And more text.  And more text. And more text. And more text. And more text. And more  text. And more text. And more text. Even more. Continued on page 2 ...',
    ' Simple PDF File 2  ...continued from page 1. Yet more text. And more text. And more text.  And more text. And more text. And more text. And more text. And more  text. Oh, how boring typing this stuff. But not as boring as watching  paint dry. And more text. And more text. And more text. And more text.  Boring.  More, a little more text. The end, and just as well. ',
]


def test_pdf_read__local_file():
    result = pdf_read('./tests/data/sample.pdf')
    assert list(result) == EXPECTED_RESULT


def test_pdf_read__url():
    result = pdf_read('http://africau.edu/images/default/sample.pdf')
    assert list(result) == EXPECTED_RESULT


def test_pdf_read__file_not_pdf():
    with pytest.raises(RuntimeError):
        result = pdf_read('./tests/data/sample.txt')
        list(result)
