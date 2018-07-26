from bs4 import BeautifulSoup
from io import StringIO
import requests
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import re
from nltk.tokenize import sent_tokenize

def convert(fname):
    fp = open(fname, 'rb')
    
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
    return extracted_text

def download(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return requests.get(url, headers=agent)

def get_text_from_html(url):
    r  = download(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    text = soup.get_text()
    return text


def get_text_from_pdf(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    r = requests.get(url, headers=agent, stream=True)
    name = url[url.rfind("/")+1:]
    filename = "/tmp/" + name
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    text = convert(filename)
    return text


def get_sentences(text):
    output = ""
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence = re.sub('\s+', ' ', sentence).strip()
        if len(sentence) < 10:
            continue
        output += sentence + "\n"
    return output

def get_text_from_urls(urls):
    output = ""
    for url in urls:
        if not url.startswith("http"):
            continue
        output += "\n=============\n" + url + "\n===============\n"
        print("Scraping ", url)
        if url.endswith("pdf"):
            text = get_text_from_pdf(url)
        else:
            text = get_text_from_html(url)
        print("Read %d chars" % len(text))
        output += get_sentences(text)
    return output


import sys
filename = sys.argv[1]

with open(filename) as fp:
    lines = fp.readlines()
    text = get_text_from_urls(lines)
    print(text)
    
