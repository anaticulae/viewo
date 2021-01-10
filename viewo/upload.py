# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import urllib.error
import urllib.request

import utila

import viewo.config

HEADER_READ_SIZE = 1024
FILE_READ_TIMEOUT = 10
EXPECTED_PDFSTART = b'%PDF-1.'


class CurlError(ValueError):

    def __init__(self, url):
        super().__init__()
        self.url = url


class FileTooLarge(CurlError):
    pass


class InvalidResource(CurlError):
    pass


class InvalidUrl(CurlError):
    pass


class TmpFile:

    def __init__(self, content):
        self.content = content

    def save(self, path: str):
        utila.file_replace_binary(path, self.content)


def curlpdf(url: str) -> TmpFile:
    try:
        with urllib.request.urlopen(url, timeout=FILE_READ_TIMEOUT) as webfile:
            header = webfile.read(HEADER_READ_SIZE)
            # %PDF-1.5 for example
            if not header[0:len(EXPECTED_PDFSTART)] == EXPECTED_PDFSTART:
                utila.error(f'no pdf file: {url}')
                raise InvalidResource(url)
            todo = viewo.config.MAX_FILE_SIZE - HEADER_READ_SIZE
            content = webfile.read(todo)
            if webfile.read(1) != b'':
                # there are some bytes left
                utila.error(f'file too large: {url}')
                raise FileTooLarge(url)
    except urllib.error.URLError as error:
        utila.error(f'invalid url: {url}')
        raise InvalidUrl(url) from error

    filecontent = header + content
    return TmpFile(filecontent)


def valid_pdf(data):
    typedef = data[0:len(EXPECTED_PDFSTART)]
    return typedef == EXPECTED_PDFSTART
