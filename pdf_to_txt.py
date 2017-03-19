import PyPDF2
#it works

# input:  path to a pdf file (string)
# return: file content in a string
def pdf_to_txt(filepath):
    try:
        pdf_file = open(filepath, 'rb')
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        page_content = ""
        for i in range(number_of_pages):
            page = read_pdf.getPage(i)
            page_content += page.extractText()
        return page_content.encode('utf-8')
    except IOError:
        print "Could not read file: ", filepath

def main():
    txt = pdf_to_txt('DataFiles/ByCompany/JP Morgan/JP Morgan 2001.pdf')
    print txt


if __name__ == "__main__":
    main()
