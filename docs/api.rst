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

Select by status:

.. code-block:: none

    documents/{document_id}/findings?status=closed

Select optional pages:

.. code-block:: none

    documents/{document_id}/findings?pages=start:end

Select finding by **document_id** and **finding_id**:

.. code-block:: none

    documents/{document_id}/findings/{finding_id}

* See: :py:func:`viewo.api.findings.present.finding_get`

pages
-----

List of pages in document

.. code-block:: none

    documents/{document_id}/pages

List of a part of pages in document

.. code-block:: none

    documents/{document_id}/pages?range=start:end

user
----

userid
~~~~~~

0 - public

operation
~~~~~~~~~

List of documents owned by **user_id**:

.. code-block:: none

    users/{user_id}/documents
