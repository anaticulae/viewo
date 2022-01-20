# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests


def test_contact_call(client):
    response = client.get('/contact', follow_redirects=True)
    content = tests.decode(response)
    assert '<h2>Kontakt</h2>' in content
    assert len(content) > 2000, content


def test_contact_message_send(client):
    result = tests.post(
        client,
        '/contact',
        dict(
            title='Ich habe eine Frage',
            email='manfred@gmail.com',
            message='This is a very very secret message',
        ),
    )
    assert 'Ihre Nachricht wurde erfolgreich übermittelt' in result, result


def test_contact_message_send_error(client):
    result = tests.post(
        client,
        '/contact',
        dict(
            title='Ich habe eine Frage',
            message='This is a very very secret message',
        ),
    )
    assert 'Nachricht konnte nicht übermittelt werden.' in result
