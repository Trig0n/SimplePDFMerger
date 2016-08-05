from os.path import isfile
from sys import argv

from PyPDF2.merger import PdfFileMerger

if len(argv) < 3:
    print "Usage: python pdfmerger.py [options]"
    print "\t-f[int]\tFiles you want to merge. [int] is the page it shall be (for the right order)"
    print "\t-o\tThe output file."
    exit(0)

i = 0
documents = {}
outfile = ""
while i < len(argv):
    if argv[i].startswith('-f'):
        documents[argv[i].strip('-f')] = argv[i + 1]
    if argv[i].startswith('-o'):
        outfile = argv[i + 1]
    i += 1

for pdf in documents:
    if not isfile(documents[pdf]):
        print "Cannot find the file '%s'" % documents[pdf]
        exit(0)

if isfile(outfile):
    print "The file '%s' already exists." % outfile

pdfmerger = PdfFileMerger(False)
for pdf in documents:
    pdfmerger.merge(int(pdf) - 1, documents[pdf])

pdfmerger.write(outfile)
pdfmerger.close()

print "Done."
