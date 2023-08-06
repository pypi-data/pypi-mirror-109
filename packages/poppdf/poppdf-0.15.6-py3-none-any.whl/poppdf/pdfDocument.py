from poppdf.poppler import image_from_path, xml_from_path, text_from_path, pdfinfo_from_path, image_info_from_path
from poppdf.common import parse_pages
import pytesseract
from poppdf.alto_xml import process_alto_xml


class PdfPage():
    def __init__(self, page):
        self.text_lines=page["texts"]
        self.words=[]
        self.images=page["images"]
        self.width=page["width"]
        self.height=page["height"]
        self.number=page["number"]
        self.image=None
        self.text=None

class PdfDocument():
    def __init__(self, path, userpw=None):

        self.pdf_info = pdfinfo_from_path(path, userpw)
        self.pdf_pages=[]
        xml_data= xml_from_path(pdf_path=path)
        pages=parse_pages(xml_data)

        for p_num, p in pages.items():
            page=PdfPage(p)
            size=(p["width"], p["height"])
            page.page_image=image_from_path(pdf_path=path, first_page=p_num, last_page=p_num,size=size)[0]
            page.text = text_from_path(path, first_page=p_num, last_page=p_num)

            if page.text.strip()=="":
                options = "--psm 3"
                alto_xml=pytesseract.image_to_alto_xml(page.page_image,config=options)

                page.text_lines, page.text, confidence=process_alto_xml(alto_xml)


            self.pdf_pages.append(page)

if __name__=="__main__":

    pdf=PdfDocument("/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Documents/Mentis/Development/Python/pdf2text/pdf3/Allianz Global Small Cap Equity WT USD.pdf")
    print(pdf.pdf_pages[1].text)