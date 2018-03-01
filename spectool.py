from appJar import gui
from collections import OrderedDict as OD
import os
import PyPDF2


def execute(btnName):
    global location
    task = app.getRadioButton('task')
    options = app.getRadioButton('options')
    location = app.getEntry('location')

    if location == '':
        app.errorBox('Empty Location', 'Choose the directory with the files in it.')
    else:
        directory = os.listdir(location)
        if task == 'Build Specs':
            build_specs(directory)
        elif task == 'Rename Files':
            if options == 'Add Spaces':
                rename_to_spaces(directory)
            elif options == 'Remove Spaces':
                rename_no_spaces(directory)
        app.infoBox('Done', 'Done!')


def rename_to_spaces(directory):
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


def rename_no_spaces(directory):
    for file in directory:
        if file[0].isdigit() and file[2] == ' ':
            a = file[:2]
            b = file[3:5]
            c = file[6:8]
            d = file[8:]
            names = [a, b, c, d]
            new_filename = ''.join(names)
            os.rename(os.path.join(location, file), os.path.join(location, new_filename))


def build_specs(directory):
    global pages, pdfFile
    pages = 0
    pdfWriter = PyPDF2.PdfFileWriter()
    bookmarks = OD()
    os.chdir(location)

    def write_to_file():
        global pages
        for pageNum in range(pdfReader.numPages):
            pages += 1
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

    for file in directory:
        try:
            pdfFile = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFile, strict=False)
            bookmarks[file] = pages
        except Exception:
            app.errorBox('Stupid File', '{} is stupid.  \nResave the PDF and try again'.format(file))
            return

        write_to_file()

        if pdfReader.numPages % 2 != 0:
            pdfWriter.addBlankPage()
            pages += 1

    for books in bookmarks:
        pdfWriter.addBookmark(books, bookmarks[books])

    OutputFile = open('CombinedSpecs.pdf', 'wb')
    pdfWriter.write(OutputFile)
    OutputFile.close()
    pdfFile.close()


if __name__ == '__main__':


    app =  gui("SpecTool")
    app.setBg("dark gray")
    app.setFont(15, font="Google Sans Medium")
    app.setSticky('ew')
    app.setTitle('SpecTool')

    app.startLabelFrame('Task')
    app.addRadioButton('task', 'Build Specs')
    app.addRadioButton('task', 'Rename Files')
    app.stopLabelFrame()

    app.startLabelFrame('Renaming Options')
    app.addRadioButton('options', 'Add Spaces')
    app.addRadioButton('options', 'Remove Spaces')
    app.stopLabelFrame()

    app.addDirectoryEntry('location')
    app.addButton('Start', execute)
    app.addButton('Quit', lambda btnName: app.stop())
    app.go()
