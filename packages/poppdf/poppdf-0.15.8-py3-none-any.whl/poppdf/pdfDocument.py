from poppdf.poppler import image_from_path, xml_from_path, text_from_path, pdfinfo_from_path, image_info_from_path
from poppdf.common import parse_pages
import pytesseract
from poppdf.alto_xml import process_alto_xml
from math import isclose
from poppdf.common import update_object_dict_pos

class PdfPage():
    def __init__(self, page):
        self.text_lines=page["texts"]
        self.words=[]
        self.images=page["images"]
        self.width=page["width"]
        self.height=page["height"]
        self.number=page["number"]
        self.page_image=None
        self.text=None
    def rescale_page(self, new_width, new_height):
        width_ratio=new_width/self.width
        height_ratio=new_height/self.height
        for tl in self.text_lines:
            tl["top"]*=height_ratio
            tl["left"] *= width_ratio
            tl["right"] *= width_ratio
            tl["bottom"] *= height_ratio
            tl["height"]=tl["bottom"]-tl["top"]
            tl["width"]=tl["right"]-tl["left"]
            update_object_dict_pos(tl)
    def rescale_page_to_image(self):
        return self.rescale_page(self.page_image.size[0], self.page_image.size[1])
class PdfDocument():
    def __init__(self, path, userpw=None, use_ocr=False, laguages="eng"):
        self.pdf_info = pdfinfo_from_path(path, userpw)
        self.pdf_pages=[]
        xml_data= xml_from_path(pdf_path=path)
        pages=parse_pages(xml_data)

        for p_num, p in pages.items():
            page=PdfPage(p)
            size=(p["width"], p["height"])
            page.page_image=image_from_path(pdf_path=path, first_page=p_num, last_page=p_num,dpi=300, grayscale=True)[0]
            page.rescale_page_to_image()
            page.text = text_from_path(path, first_page=p_num, last_page=p_num)
            ocr_text_lines=[]

            if use_ocr or page.text.strip()=="":

                options = "--psm 3"
                alto_xml=pytesseract.image_to_alto_xml(page.page_image,config=options, lang=laguages)
#                text=pytesseract.image_to_string(page.page_image,config=options, lang=laguages)

                ocr_text_lines, page.text, confidence=process_alto_xml(alto_xml)

            if page.text.strip()=="":
                page.text_lines=ocr_text_lines
            elif use_ocr:
                text_lines_to_remove=[]
                for tl in page.text_lines:
                    if not self.__find_match(ocr_text_lines, tl):
                        text_lines_to_remove.append(tl)
                page.text_lines=[x for x in page.text_lines if x not in text_lines_to_remove]

            self.pdf_pages.append(page)
    def __find_match(self, sorted_list, item):
        i=0
        while i<len(sorted_list) and not isclose(sorted_list[i]["top"], item["top"], rel_tol=0.1):
            i+=1

        if i<len(sorted_list):
            return True
        return False


if __name__=="__main__":

    pdf=PdfDocument("/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Documents/Mentis/Development/Python/pdf2text/pdfs/images/FR_FFG_GlobalFlex_Sust_AccR.pdf", use_ocr=False)
    print(pdf.pdf_pages[0].text)