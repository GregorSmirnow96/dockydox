import DocumentType

import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def read_document(document_path):
    document_image = cv2.imread(document_path)
    document_image = cv2.inRange(document_image, (0, 0, 0), (90, 90, 90))
    document_image = cv2.bitwise_not(document_image)
    # while True:
    #     cv2.imshow('', document_image)
    #     cv2.waitKey(1)

    text = pytesseract.image_to_string(document_image)
    
    subdivision = _get_subdivision(text)
    block = _get_block(text)
    grantor = _get_grantor(text)
    grantee = _get_grantee(text)

    # Parse document for data.
    document_data = {
    }

    # Derive type from data fields.
    document_type = DocumentType.WARRANTY_DEED

    return document_data, document_type

def _get_subdivision(text):
    lines = text.split('\n')
    for i in range(0, len(lines)):
        line = lines[i]
        try:
            next_line = lines[i + 1]
        except:
            next_line = ''
        lower_case_line = line.lower()
        if 'lot' in lower_case_line:
            print('Subdivision: ' + line + ' ' + next_line)
    return '' in text

def _get_block(text):
    lines = text.split('\n')
    for i in range(0, len(lines)):
        line = lines[i]
        try:
            next_line = lines[i + 1]
        except:
            next_line = ''
        lower_case_line = line.lower()
        if 'block' in lower_case_line:
            print('Block: ' + line + ' ' + next_line)
    return '' in text

def _get_instrument(text):
    lines = text.split('\n')
    return '' in text

def _get_instrument_date(text):
    lines = text.split('\n')
    return '' in text

def _get_reception(text):
    lines = text.split('\n')
    return '' in text

def _get_recording_date(text):
    lines = text.split('\n')
    return '' in text

def _get_grantor(text):
    lines = text.split('\n')
    for i in range(0, len(lines)):
        line = lines[i]
        try:
            next_line = lines[i + 1]
        except:
            next_line = ''
        lower_case_line = line.lower()
        if 'between' in lower_case_line:
            print('Grantor(s): ' + line + ' ' + next_line)
    return '' in text

def _get_grantee(text):
    lines = text.split('\n')
    for i in range(0, len(lines)):
        line = lines[i]
        try:
            next_line = lines[i + 1]
        except:
            next_line = ''
        lower_case_line = line.lower()
        if 'between' in lower_case_line:
            print('Grantee(s): ' + line + ' ' + next_line)
    return '' in text

def _get_lots(text):
    lines = text.split('\n')
    for line in lines:
        lower_case_line = line.lower()
        if 'lot' in lower_case_line or 'lots' in lower_case_line:
            print('Lot(s): ' + line)
    return '' in text



if __name__ == '__main__':
    read_document('TestData/doc6.jpg')
