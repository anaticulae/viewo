# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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


def curlpdf(url: str):
    try:
        with urllib.request.urlopen(
                url,
                timeout=FILE_READ_TIMEOUT,
        ) as webhandle:
            header = webhandle.read(HEADER_READ_SIZE)
            # %PDF-1.5 for example
            if not header[0:len(EXPECTED_PDFSTART)] == EXPECTED_PDFSTART:
                utila.error(f'no pdf file: {url}')
                return None
            todo = viewo.config.MAX_FILE_SIZE - HEADER_READ_SIZE
            content = webhandle.read(todo)
            if webhandle.read(1) != b'':
                # there are some bytes left
                utila.error(f'file too large: {url}')
                return None
    except (ValueError, urllib.error.URLError):
        utila.error(f'invalid url: {url}')
        return None
    filecontent = header + content

    class TmpFile:

        def __init__(self, content):
            self.content = content

        def save(self, path: str):
            utila.file_replace_binary(path, self.content)

    return TmpFile(filecontent)
