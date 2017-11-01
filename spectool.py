#!python3

import os.path, os, PyPDF2
from collections import OrderedDict as OD

location = os.getcwd()
directory = os.listdir(location)
pdfWriter = PyPDF2.PdfFileWriter()
pages=0


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


def build_specs(location):
    global pages
    rename_to_spaces(location)
    pdfWriter = PyPDF2.PdfFileWriter()
    blank= input("\n\n\n{}\n{}   Blank sheet needed after first odd number of pages?   {}\n\n{}\nIf there is a cover sheet, type 'no', if there is no cover, type 'yes':  ".format('*~'*40, '*~'*6, '*~'*5, '~*'*40))
    bookmarks=OD()

    def write_to_file(sect):
        global pages
        for pageNum in range(pdfReader.numPages):
            pages+=1
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)


    for file in directory:
        pdfFile = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile, strict=False)
        bookmarks[file] = pages

        write_to_file(file)

        if pdfReader.numPages % 2 != 0:
            if blank == 'yes':
                pdfWriter.addBlankPage()
                pages+=1
            else:
                blank = 'yes'

    for books in bookmarks:
        pdfWriter.addBookmark(books, bookmarks[books])

    OutputFile = open('CombinedSpecs.pdf', 'wb')
    pdfWriter.write(OutputFile)
    OutputFile.close()
    pdfFile.close()
