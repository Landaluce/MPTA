import PyPDF2
from docx import opendocx, getdocumenttext
#testing
# input:  path to a pdf file (string)
# return: file content in a string
def docx_to_txt(filepath):
    document = opendocx(filepath)
    return " ".join(getdocumenttext(document)).encode("utf-8")


# dont need it anymore
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


def save_txt(text,filepath):
    try:
        txt_file = open(filepath, 'w')
        txt_file.write(text)
    except IOError:
        print "Could not save file: ", filepath


def genetare_txt_files(company_name):
    start_year = 2010
    end_year = 2016
    folder_path = 'DataFiles/ByCompany/' + company_name + '/' + company_name + " "
    for i in range(start_year, end_year + 1):
        pdf_path = folder_path + str(i) + ".pdf"
        text = pdf_to_txt(pdf_path)
        if text:
            txt_path = "TestSuite/" + company_name
            if not os.path.exists(txt_path):
                os.makedirs(txt_path)
                print "test"
            save_txt(text, txt_path + "/" + company_name + str(i) + ".txt")


def main():
            # PDF to TXT:
            # error "Capital One", "Keycorp",  "M&T"
            # ok "BNY Mellon", "BB&T","Citigroup", "Comerica",
            # "Fifth Third","Huntington", "JP Morgan","M&I",
            # "Northern Trust", "PNC Financial","State Street",
            # "SunTrust", "Synovus", "US Bancorp","WellsFargo","Zions"
    companies = ["Northern Trust", "PNC Financial",
                 "State Street", "SunTrust", "Synovus", "US Bancorp",
                 "WellsFargo","Zions"]

    # PDF
    #jpm2001pdf = pdf_to_txt('DataFiles/ByCompany/JP Morgan/JP Morgan 2000.pdf')
    #save_txt(jpm2001pdf, 'TestSuite/JP Morgan/JP Morgan2000.txt')

    # docx
    jpm2001docx = docx_to_txt('DataFiles/ByCompany/JP Morgan/JP Morgan 2000.docx')
    save_txt(jpm2001docx, 'TestSuite/JP Morgan/JP Morgan2000docx.txt')

if __name__ == "__main__":
    main()
