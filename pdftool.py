from os.path import isfile
from sys import argv

from PyPDF2.merger import PdfFileMerger


class Configuration(object):
    merge = False
    files = []

    outfile = None
    password = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    class File(object):
        path = None
        pages = []

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    @staticmethod
    def help():
        print("Usage: python pdftool.py [options]")
        print("\t-m\t--merge")
        print("\t\t--file")
        print("\t\t--page\t',' for multiple pages")
        print("\t\t\tex: 1,2,5,16")
        print("\t-o\t--outfile")
        print("\t-p\t--password")
        exit(0)

    @staticmethod
    def parse():
        cfg = Configuration()
        i = 0
        while i < len(argv):
            a = argv[i]
            if a in ["-m", "--merge"]:
                cfg.merge = True
            elif a in ["-o", "--outfile"]:
                cfg.outfile = argv[i + 1]
            elif a in ["-p", "--password"]:
                cfg.password = argv[i + 1]  # todo as input()

            if cfg.merge:
                if a in ["--file"]:
                    cfg.files.append(argv[i + 1])
                elif a in ["--page"]:
                    p = argv[i + 1]
                    if "," in p:
                        cfg.files[-1].pages = [int(_) for _ in argv[i + 1].split(",")]
                    else:
                        cfg.files[-1].pages = int(argv[i + 1])
            i += 1
        return cfg


class Tool(object):
    def __init__(self, cfg):
        self.cfg = cfg

    def merge(self):
        pdfmerge = PdfFileMerger(False)
        i = 0
        for f in self.cfg.files:
            if isfile(f.path):
                pdfmerge.merge(i, f.path)
            i += 1
        pdfmerge.write(self.cfg.outfile)
        pdfmerge.close()

    def do_stuff(self):
        self.merge()


def main():
    c = Configuration.parse()
    if isfile(c.outfile):
        print(c.outfile, "exists. exiting.")
        exit()
    Tool(c).do_stuff()
    print("done.")


if __name__ == '__main__':
    Tool(Configuration.parse()).do_stuff()
