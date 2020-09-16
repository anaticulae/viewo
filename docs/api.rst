API
===

documents
---------

**document_id**: alpha-numeric-32-length

**finding_id**: plus/minus numeric

resources
~~~~~~~~~

Document root:

.. code-block:: none

    documents/{document_id}

List findings of selected document:

.. code-block:: none

    documents/{document_id}/findings

Select optional pages:

.. code-block:: none

    documents/{document_id}/findings?pages=start:end

Select finding by **document_id** and **finding_id**:

.. code-block:: none

    documents/{document_id}/findings/{finding_id}

operation
~~~~~~~~~

**create**:

**delete**:


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
