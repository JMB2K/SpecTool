# SpecTool

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/07d623c6d9b2419daceb9fcce2712bf1)](https://www.codacy.com/app/JMB2K/SpecTool?utm_source=github.com&utm_medium=referral&utm_content=JMB2K/SpecTool&utm_campaign=badger)

Builds spec books for printing

This takes individual PDF files and combines them, checking each file to see if it has an odd or even number of pages.  If it's an odd number, it adds a blank page behind the last sheet.

For files that were created in Microsoft Office, this throws up an error because they use paeth to create the PDF files and PyPDF2 can't read that.  It throws up an error, to fix you just need to open, resave, overwriting the original file and it works everytime for me.
