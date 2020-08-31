# -*- coding: utf8 -*-
from io import StringIO

import click

from chorse.imaging import imaging_cli
from chorse.nas import nas_cli
from chorse.nipa import nipa_cli
from chorse.path import path_cli
from chorse.video import video_cli


@click.group(name='main')
def main_cli():
    pass


main_cli.add_command(nipa_cli)
main_cli.add_command(imaging_cli)
main_cli.add_command(nas_cli)
main_cli.add_command(video_cli)
main_cli.add_command(path_cli)

if __name__ == "__main__":
    main_cli()
    #
    # from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    # from pdfminer.converter import TextConverter, HTMLConverter
    # from pdfminer.layout import LAParams
    # from pdfminer.pdfpage import PDFPage
    #
    # path = '/Users/lucakim/Desktop/1.pdf'
    # outpath = '/Users/lucakim/Desktop/1.html'
    # rsrcmgr = PDFResourceManager()
    # retstr = StringIO()
    # codec = 'utf-8'
    # laparams = LAParams()
    # outfp = open(outpath, 'w')
    # device = HTMLConverter(rsrcmgr, outfp=outfp, laparams=laparams)
    # fp = open(path, 'rb')
    # interpreter = PDFPageInterpreter(rsrcmgr, device)
    # password = ""
    # maxpages = 0
    # caching = True
    # pagenos = set()
    #
    # for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
    #     interpreter.process_page(page)
    #
    # text = retstr.getvalue()
    #
    # fp.close()
    # device.close()
    # retstr.close()
    # print(text)
