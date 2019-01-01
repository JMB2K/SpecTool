import PyPDF2
import os
from appJar import gui
import logging

logging.basicConfig(level=logging.DEBUG)
#logging.disable(logging.CRITICAL)


def execute(btnName):
    global location
    location = app.getEntry('location')
    opts = app.option('Options')

    if not location:
        return app.popUp('Empty Location', 'Choose the directory with the files in it.', kind='warning')

    directory = os.listdir(location)
    if opts == 'Build Specs':
        build_specs(directory)
    elif opts == 'Add Spaces':
        rename_to_spaces(directory)
    elif opts == 'Remove Spaces':
        rename_no_spaces(directory)
    return app.infoBox('Done', 'Done!')

def rename_to_spaces(directory):
    for file in directory:
        if ' ' not in file[:6] and file[0].isdigit():
            new_filename = f'{file[:2]} {file[2:4]} {file[4:6]}{file[6:]}'
            os.rename(os.path.join(location, file), os.path.join(location,new_filename))

def rename_no_spaces(directory):
    for file in directory:
        if file[0].isdigit() and file[2] == ' ':
            first = file[:8].replace(' ', '')
            last = file[8:]
            new_filename = first + last
            os.rename(os.path.join(location, file), os.path.join(location, new_filename))

def build_specs(directory):
    pages = 0
    pdfWriter = PyPDF2.PdfFileWriter()
    bookmarks = dict()
    os.chdir(location)
    errors = []

    for file in directory:
        logging.debug(f'Next File: {file}')
        try:
            pdfFile = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFile, strict=False)
            bookmarks[file] = pages
        except Exception as E:
            logging.debug(E)
            errors.append(file)
            continue

        for pageNum in range(pdfReader.numPages):
            pages += 1
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        if pdfReader.numPages % 2 != 0:
            pdfWriter.addBlankPage()
            pages += 1

    for books in bookmarks:
        pdfWriter.addBookmark(books, bookmarks[books])

    if not errors:
        OutputFile = open('CombinedSpecs.pdf', 'wb')
        pdfWriter.write(OutputFile)
        OutputFile.close()
        pdfFile.close()
    else:
        errors = '\n'.join([x[:8] for x in errors])
        return app.popUp('Errors', f'These files are stupid:\n{errors}\nPlease resave as PDF and try again.')
    


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
