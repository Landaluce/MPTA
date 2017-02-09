import PyPDF2


def main():
    pdf_file = open('DataFiles/ByCompany/Bank of NY Mellon/BYN Mellon 2012.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    page = read_pdf.getPage(10)
    page_content = page.extractText()
    print page_content.encode('utf-8')


if __name__ == "__main__":
    main()
