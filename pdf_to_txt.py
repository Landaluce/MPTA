import PyPDF2


# input:  path to a pdf file (string)
# return: file content in a string
def pdf_to_txt(filepath):
    pdf_file = open(filepath, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    page = read_pdf.getPage(10)
    page_content = page.extractText()
    return page_content.encode('utf-8')

def main():
    txt = pdf_to_txt('DataFiles/ByCompany/Bank of NY Mellon/BYN Mellon 2012.pdf')
    print txt


if __name__ == "__main__":
    main()
