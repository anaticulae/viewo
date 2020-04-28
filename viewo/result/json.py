# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json

import configo
import utila
import writers

import viewo.waiting


def tojson(
        items: viewo.waiting.ResultPageViews,
        pagesentences: dict = None,
) -> str:
    result = []
    for item in items:
        findings = [{
            'number': finding.number,
            'location': location_tojson(finding.location, pagesentences),
            'title': finding.solution.title,
            'message': message_replace(finding.solution.description),
            'status': finding.solution.status.value,
            'selectable': selectable(finding.location)
        } for finding in item.findings if finding.solution]
        result.append({
            'page': item.page,
            'html': item.html,
            'findings': findings,
        })
    raw = {
        'status': 0,
        'content': result,
    }
    dumped = json.dumps(raw)
    return dumped


def location_tojson(location, pagesentences: dict = None) -> dict:
    result = {
        'page': location.page,
    }
    # sentence, convert to words
    if location.shortcut == 's':
        result['sentence'] = location.value
        if pagesentences is not None:
            words = word_index(pagesentences, location.page, location.value)
            if words is None:
                utila.error(f'no words on page: {location.page}'
                            f' sentence: {location.value}')
            else:
                result['words'] = words
    return result


def message_replace(content: str) -> str:
    url = configo.docs_url()
    content = writers.replace(content, url)
    # TODO: REMOVE VIEW HACK LATER
    content = content.replace('<a href', '<br/><br/><a href')
    return content


def selectable(location) -> int:
    """Page able only `location` is not selectable."""
    if location.value is None:
        return 0
    return 1


def word_index(pagesentences, page, sentence):
    result = []
    try:
        current = pagesentences[page]
    except KeyError:
        utila.log(f'could not access page: {page}')
        return result

    start = sum([len(items) for items in current[current:sentence]], start=0)

    for index, _ in enumerate(current[sentence], start=start):
        result.append(index)
    return result
