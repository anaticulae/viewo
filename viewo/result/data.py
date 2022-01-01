# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import os

import iamraw
import link
import protocol
import serializeraw
import utila

import viewo.result.loader
import viewo.waiting


def load_resultview_result(process: str) -> str:
    result = link.resultview(process)
    if not os.path.exists(result):
        result = link.resultview(process, done=True)
    if not os.path.exists(result):
        return None
    with utila.profile(f'load resultview: {process}'):
        loaded = load_resultview(result, process)
    return loaded


def load_resultview(path: str, process: str) -> 'viewo.waiting.ResultPageViews':
    """Load result view and findings.

    Args:
        path(str): path to result view: e.g: `ready/processid`
        process(str): number of analyzed `process`
    Returns:
        Loaded HTML Page View
    """
    assert os.path.exists(path), str(path)

    with utila.profile('load findings'):
        pagefindings = load_findings(path)

    with utila.profile('load html'):
        html = load_html(path)

    with utila.profile('render result view'):
        rendered = render_resultpage_view(html, pagefindings, process)
    return rendered


def render_resultpage_view(html, pagefindings, process):
    result = []
    # load all pages not only the erroneous
    for page in sync_pages(html, pagefindings):
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


def load_findings(path: str):
    pagefindings = findings_from_path(path)
    for item in pagefindings:
        # TODO: REMOVE AFTER FIXING
        # THIS STEP SHOULD NOT BE NECESSARY IF EVERY THING WORKS FINE IN
        # QUEUEMO.
        before = len(item.content)
        item.content = utila.make_unique(item.content)
        after = len(item.content)
        if after != before:
            # we copy results twice
            utila.debug(f'duplicated finding ids on page: {item.page}')
    return pagefindings


def load_html(path: str):
    htmlpath = os.path.join(path, 'view')
    html = HtmlLookup(htmlpath)
    return html


def patch_images(html: str, process: int) -> str:
    # TODO: REMOVE THIS HACK
    utila.debug('patch images')
    html = html.replace('src="', f'src="{process}/')
    return html


def sync_pages(html, pagefindings) -> list:
    collected = []
    # TODO: IMPROVE THIS TO SUPPORT SELECTIVE PAGES
    collected.extend(list(range(len(html))))
    collected.extend([item.page for item in pagefindings])
    result = set(collected)
    result = sorted(result)
    return result


def load_htmlview(path: str) -> list:
    # TODO: DANGEROUS?
    assert os.path.exists(path), str(path)
    # Sort html pages by number, sort 0, 1, 2, 3, ..., 10, 11, 12 correctly.
    # Example: 0.html, cut file extention and make file name int-sortable.
    files = utila.file_list(path, 'html')
    files = utila.files_sort(files)
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


def findings_from_path(path: str, worker: int = 10) -> iamraw.PageFindings:
    """Load Findings from `path` directory and group them by page as
    `PageFindings`."""
    assert os.path.isdir(path), str(path)
    files = utila.file_list(path, include='yaml', recursive=True)
    files = [item for item in files if utila.file_name(item).endswith('_user')]
    paths = [os.path.join(path, item) for item in files]

    # yaml parsing is cpu bound, therefore we need a process pool instead
    # of thread pool.
    executor = utila.select_executor()
    # select executor is required to run in pytest
    with executor(max_workers=worker) as executor:
        todo = {
            executor.submit(serializeraw.load_findings, path): path
            for path in paths
        }
        findings = []
        for job in concurrent.futures.as_completed(todo):
            data = job.result()
            findings.extend(data)
    result = protocol.bypage(findings)
    return result
