# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses
import json
import re

import configo
import iamraw.caption
import utila
import writers


def tojson(
    items: 'viewo.waiting.ResultPageViews',
    pagesentences: dict = None,
    footnotes: list = None,
    doctextstyle=None,
    properties: dict = None,
    captions: list = None,
) -> str:
    pages = pages_tojson(items, pagesentences)
    footnotes = footnotes_tojson(footnotes)
    doctextstyle = doctextstyle_tojson(doctextstyle)
    properties = properties_tojson(properties)
    captions = iamraw.caption.pagecaptions_toraw(captions) if captions else []  # pylint:disable=E1101
    # result
    raw = {
        'status': 0,
        'content': pages,
        'captions': captions,
        'doctextstyle': doctextstyle,
        'footnotes': footnotes,
        'properties': properties,
    }
    dumped = json.dumps(raw)
    return dumped


def doctextstyle_tojson(item) -> dict:
    if not item:
        return {}
    result = dataclasses.asdict(item)
    return result


def properties_tojson(properties: dict) -> dict:
    keys = [
        'author', 'title', 'date', 'subject', 'keywords', 'password', 'outlines'
    ]
    if not properties:
        return {key: '' for key in keys}
    # TODO: USE SERIALIZERAW.data_parse
    result = {
        'title': properties['Title'],
        'author': properties['Author'],
        'date': {
            'year': 2020,
            'month': 12,
            'day': 10,
        },
        'subject': properties['Subject'],
        'keywords': ['Hier', 'Spricht', 'Helm'],
        'password': properties['Password'],
        'outlines': False,
    }
    return result


def pages_tojson(pages: list, pagesentences) -> list:
    result = []
    for item in pages:
        findings = [{
            'number': finding.number,
            'location': location_tojson(finding.location, pagesentences),
            'title': finding.solution.title,
            'message': message_replace(finding.solution.description),
            'status': finding.solution.status.value,
            'selectable': selectable(finding.location)
        } for finding in item.findings if finding.solution]
        pageraw = {
            'page': item.page,
            'html': item.html,
            'findings': findings,
        }
        result.append(pageraw)
    return result


def footnotes_tojson(footnotes: list) -> dict:
    footnotes = footnotes if footnotes else []
    # convert to raw
    footnotes = [[{
        'title': footnote.text,
        'number': footnote.number,
        'page': page,
        'error': '',
    } for footnote in content] for page, content in footnotes]
    footnotes = utila.flatten(footnotes)
    return footnotes


def location_tojson(location, pagesentences: dict = None) -> dict:
    result = {
        'page': location.page,
    }
    shortcut = ''
    with contextlib.suppress(AttributeError):
        # not every location type has a location shortcut
        shortcut = location.shortcut
    # sentence, convert to words
    if shortcut == 's':
        result['sentence'] = location.value
        if pagesentences is not None:
            words = word_index(pagesentences, location.page, location.value)
            if words is None:
                utila.error(f'no words on page: {location.page}'
                            f' sentence: {location.value}')
            else:
                result['words'] = words
        return result
    if shortcut == 'r':
        # ranged location
        line, linened = location.line, location.line_end
        linened = line if linened is None else linened
        lines = tuple(range(line, linened + 1))
        result['lines'] = lines
    return result


def message_replace(content: str) -> str:
    r"""Replace rst pattern with html syntax

    >>> message_replace('that is **?very 2.0!** important')
    'that is <strong>?very 2.0!</strong> important'
    >>> message_replace('that is **?very 2.0!** important. *More than this.*.')
    'that is <strong>?very 2.0!</strong> important. <em>More than this.</em>.'
    >>> message_replace('Heute: **Gibt es nicht genug Mitarbeiter*innen.**')
    'Heute: <strong>Gibt es nicht genug Mitarbeiter*innen.</strong>'
    >>> message_replace('**first**, **second**')
    '<strong>first</strong>, <strong>second</strong>'

    Ensure that newlines or spaces wich are introduces by long links are
    matched correctly.
    >>> message_replace('Hyperlink: ** http://www.statistik.at/\nservices/\n/5/'
    ... 'index.html?includePage=detailedView%C2%A** ist.')
    'Hyperlink: <strong> http://www.statistik.at/<br/>services/<br/>/5/...</strong> ist.'
    >>> message_replace('{{hn:4:nh}}')
    '<sup>4</sup>'
    """
    # TODO: INTRODUCE MARKDOWN PACKAGE
    url = configo.docs_url()
    content = writers.replace(content, url)
    # TODO: REMOVE VIEW HACK LATER
    # TODO: REPLACE WITH <<VDIST>>(vertical distance)
    # content = content.replace('<a href', '<br/><a href')
    # replace **[CONTENT]**-pattern with html `strong` pattern
    content = re.sub(r'\*\*((.|\s)+?)\*\*', r'<strong>\1</strong>', content)
    # emphasis lower important than strong content
    content = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', content)
    # highnotes
    content = re.sub(r'\{\{hn\:(\d{1,3})\:nh\}\}', r'<sup>\1</sup>', content)
    # replace newline
    content = content.replace('\n', '<br/>')
    return content


def selectable(location) -> int:
    """Page able only `location` is not selectable."""
    with contextlib.suppress(AttributeError):
        # TODO: REMOVE AFTER FIXING RANGED LOCATION IN PROTOCOL
        if location.value is None:
            return 0
    return 1


def word_index(pagesentences, page, sentence):
    try:
        current = pagesentences[page]
    except KeyError:
        utila.log(f'could not access page: {page}')
        return []

    generator = WordGenerator()
    for line in current[0:sentence]:
        list(generator.words(line))

    result = [index for index, _ in generator.words(current[sentence])]
    return result


# TODO: MOVE TO WORDS MODULE
def split_token(text: str, normalize: bool = True):
    # replace text division -
    text = text.replace('-\n', '')
    # support multi line text
    text = text.replace('\n', ' ')
    tokens = text.split(' ')
    if normalize:
        tokens = [token for token in tokens if token]
    return tokens


class WordGenerator:

    def __init__(self):
        self.index = 0

    def words(self, line):
        splitted = split_token(line, normalize=False)
        for item in splitted:
            if not item or not item.strip():
                continue
            yield self.index, item
            self.index += 1


def count_words(lines):
    generator = WordGenerator()
    result = []
    for line in lines:
        result.extend(list(generator.words(line)))
    return len(result)
