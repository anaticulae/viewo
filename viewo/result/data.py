# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import protocol
import utila

import viewo.result.loader
import viewo.utils
import viewo.waiting


def load_resultview_result(process: str) -> str:
    result = link.resultview(process)
    if not os.path.exists(result):
        return None
    return load_resultview(result, process)


def load_resultview(path: str, process: str) -> viewo.waiting.ResultPageViews:
    """Load result view and findings.

    Args:
        path(str): path to result view: e.g: `ready/processid`
        process(str): number of analyzed `process`
    Returns:
        Loaded HTML Page View
    """
    assert os.path.exists(path), str(path)
    pagefindings = protocol.findings_from_path(path)

    result = []
    htmlpath = os.path.join(path, 'view')
    html = HtmlLookup(htmlpath)
    # load all pages not only the erroneous
    for page in pages(html, pagefindings):
        # for page, rendered in enumerate(html):
        finding = utila.select_page(pagefindings, page, default=[])
        try:
            content = html[page]
        except IndexError:
            utila.error(f'non existing html page: {page}')
            content = ''
        # for group in grouped:
        # content = html[group.page]
        item = viewo.waiting.ResultPageView(
            page=page,
            html=patch_images(content, process),
            findings=finding,
        )
        result.append(item)
    return result


def patch_images(html: str, process: int) -> str:
    # TODO: REMOVE THIS HACK
    utila.error('patch images')
    html = html.replace('src="', f'src="{process}/')
    return html


def pages(html, pagefindings) -> list:
    collected = []
    # TODO: IMPROVE THIS TO SUPPORT SELECTIVE PAGES
    collected.extend(list(range(len(html))))
    collected.extend([item.page for item in pagefindings])
    result = set(collected)
    result = sorted(result)
    return result


def load_htmlview(path: str) -> list:
    # TODO: DANGEROUS
    assert os.path.exists(path), str(path)
    # Sort html pages by number, sort 0, 1, 2, 3, ..., 10, 11, 12 correctly.
    # Example: 0.html, cut file extention and make file name int-sortable.
    files = utila.file_list(path, 'html')
    try:
        # TODO: RELACE WITH UTILA CODE
        files = sorted(files, key=lambda x: int(str(x).split('.')[0]))
    except ValueError:
        # TODO: REMOVE LATER
        utila.error('error while sorting files')
        utila.error(files)
        return []
    content = [utila.file_read(os.path.join(path, item)) for item in files]
    return content


class HtmlLookup:

    def __init__(self, path):
        self.data = []
        if os.path.exists(path):
            self.data = load_htmlview(path)
        else:
            utila.error(f'html lookup: {path} does not exists.')

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)
