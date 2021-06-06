API
===

documents
---------

**document_id**: alpha-numeric-32-length

**finding_id**: plus/minus numeric

resources
~~~~~~~~~

* :py:class:`viewo.api.documents`

Document root:

* :py:class:`viewo.api.documents.present`

.. code-block:: none

    documents/{document_id}

* See: :py:func:`viewo.api.documents.present.document_get`

operation
~~~~~~~~~

**create**:

**delete**:

findings
--------

List findings of selected document:

.. code-block:: none

    documents/{document_id}/findings

* See: :py:func:`viewo.api.findings.present.findings`

Update status of finding via **PUT** status={0,1,2,4} request

.. code-block:: none

    documents/{document_id}/findings/{finding_id}

* See: :py:func:`viewo.api.findings.update.finding_put`

Select by status:

.. code-block:: none

    documents/{document_id}/findings?status=closed

Select optional pages:

.. code-block:: none

    documents/{document_id}/findings?pages={start|start:end}

* See: :py:func:`viewo.api.findings.present.findings`

Select finding by **document_id** and **finding_id**:

.. code-block:: none

    documents/{document_id}/findings/{finding_id}

* See: :py:func:`viewo.api.findings.present.finding_get`

pages
-----

List of pages in document

.. code-block:: none

    documents/{document_id}/pageviews

* See: :py:func:`viewo.api.pageviews.present`

List of a part of pages in document

.. code-block:: none

documents/{document_id}/pageviews?pages={start|start:end}

* See: :py:func:`viewo.api.pageviews.present`

user
----

userid
~~~~~~

'00000000' - public

operation
~~~~~~~~~

List of documents owned by **user_id**:

.. code-block:: none

    users/{user_id}/documents
