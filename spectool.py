import PyPDF2
import os
from appJar import gui
from collections import OrderedDict as OD

def execute(btnName):
    global location
    location = app.getEntry('location')
    opts = app.option('Options')

    if location == '':
        app.popUp('Empty Location', 'Choose the directory with the files in it.', kind='warning')
    else:
        directory = os.listdir(location)
        if opts == 'Build Specs':
            build_specs(directory)
        elif opts == 'Add Spaces':
            rename_to_spaces(directory)
        elif opts == 'Remove Spaces':
            rename_no_spaces(directory)
        app.infoBox('Done', 'Done!')

def rename_to_spaces(directory):
    for file in directory:
        if ' ' not in file[:6] and file[0].isdigit():
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
            first = file[:8].replace(' ', '')
            last = file[8:]
            new_filename = first + last
            os.rename(os.path.join(location, file), os.path.join(location, new_filename))

def build_specs(directory):
    global pages, pdfFile
    pages = 0
    pdfWriter = PyPDF2.PdfFileWriter()
    bookmarks = OD()
    os.chdir(location)
    errors = []

    for file in directory:
        try:
            pdfFile = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFile, strict=False)
            bookmarks[file] = pages
        except Exception:
            errors.append(file)            

        for pageNum in range(pdfReader.numPages):
            pages += 1
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        if pdfReader.numPages % 2 != 0:
            pdfWriter.addBlankPage()
            pages += 1

    for books in bookmarks:
        pdfWriter.addBookmark(books, bookmarks[books])

    if errors == []:
        OutputFile = open('CombinedSpecs.pdf', 'wb')
        pdfWriter.write(OutputFile)
        OutputFile.close()
        pdfFile.close()
    else:
        errors = '\n'.join([x[:8] for x in errors])
        return app.popUp('Errors', 'These files are stupid:\n{}\nPlease resave as PDF and try again.'.format(errors))


if __name__ == '__main__':

    app =  gui("SpecTool")
    app.font = 16
    app.setSticky('ew')
    app.setTitle('SpecTool')

    app.option('Options', ['Build Specs', '- Rename Files -', 'Add Spaces', 'Remove Spaces'])

    app.addDirectoryEntry('location')
    app.addButton('Start', execute)
    app.addButton('Quit', lambda btnName: app.stop())
    app.go()