#!python3

import os.path
import os
import PyPDF2

location = os.getcwd()
directory = os.listdir(location)
pdfWriter = PyPDF2.PdfFileWriter()


def rename_to_spaces(location):
    for file in directory:
        if ' ' not in file[:6] and file[0].isdigit():
            # print(new_filename)
            a = file[:2]
            b = file[2:4]
            c = file[4:6]
            d = file[7:]
            names = [a, b, c, d]
            new_filename = ' '.join(names)
            os.rename(os.path.join(location, file), os.path.join(location, new_filename))


def rename_no_spaces(location):
    for file in directory:
        if file[0].isdigit() and file[2] == ' ':
            a = file[:2]
            b = file[3:5]
            c = file[6:8]
            d = file[8:]
            names = [a, b, c, d]
            new_filename = ''.join(names)
            os.rename(os.path.join(location, file), os.path.join(location, new_filename))


# noinspection PyUnboundLocalVariable
def build_specs(location):
    rename_to_spaces(location)
    for file in directory:
        pdf_file = open(file, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file, strict=False)
        # Checking if there are an odd or even number of pages in file.
        if pdf_reader.numPages % 2 == 0:
            for page in range(pdf_reader.numPages):
                page_obj = pdf_reader.getPage(page)
                pdfWriter.addPage(page_obj)
        else:
            # If odd number of pages, write to file then add blank page after.
            for page in range(pdf_reader.numPages):
                page_obj = pdf_reader.getPage(page)
                pdfWriter.addPage(page_obj)
                blank = 'yes'

            if blank == 'yes':
                pdfWriter.addBlankPage()
                blank = 'no'

    output_file = open('CombinedSpecs.pdf', 'wb')
    pdfWriter.write(output_file)
    output_file.close()
    pdf_file.close()
