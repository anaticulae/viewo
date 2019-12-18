# Changelog

Every noteable change is logged here.

## v0.5.0

### Feature

* if one state failed, set global state to failed (9e7c262adce8)
* add verify step with negative result (f90540b46f1d)
* extend waiting room state machine (134133e1b83f)
* add method to load waiting status (32b6975b826f)
* deliver the status for selected document (11a63821e07c)
* link waiting view with document list view (c1014c5ad951)
* add waiters view and connect with status-web-service (6129b15cc0e5)
* add method to convert Status to JSON format (d6c256e14265)
* add general rest doc structure (6d0f092695ae)
* add prototype view for waiting room (ed3c6813294c)

### Fix

* pass process id of document correctly (6ab82de62e4e)
* reduce polling rate (bc6add43a6ea)
* make waiting view smaller to fit in homepage view (d8b8d703126e)

## v0.4.10

## v0.4.9

## v0.4.8

## v0.4.7

### Fix

* fix requirements of a unit test (4412b92eebaf)

## v0.4.6

## v0.4.5

### Documentation

* fix spelling error and format README (e4044cc82076)

## v0.4.4

### Fix

* fix spelling error (41851a272f0e)
* extend white list for right behavior (a17cb26416b4)

## v0.4.3

## v0.4.2

### Feature

* add percent sign to show grade of uploaded document (41e74d4a18e3)
* sort files in document view by upload date (7c19eefe23e3)

## v0.4.1

### Feature

* move code to link and configo (38de874407cb)

### Fix

* skip folder with wrong result pattern (7763da26b62f)

## v0.4.0

### Feature

* increase max-width to show more content (26c865878dc1)
* display index.html as result of feature (d3f0dc4d9962)
* add global error handler for 404 + test (675c3b9ad89e)

### Fix

* correct application name, find templates/static folder automatically (3a0510ddde83)

## v0.3.0

### Feature

* add result view to display result of analysation (bd10d719e036)
* add website-symbols (175cb2555174)

### Fix

* make links independent of current directory (efcf21dbbb4a)

## v0.2.0

### Feature

* add job to save meta data for uploaded documents (f19125193d59)
* extend documents view to show a list of all uploaded documents (85c3b66c5f3c)

### Fix

* rename blueprint to avoid naming collisions with upload (588f2d1b70fd)
* use environment vars instead of flask app to reduce despondencies to flaks app (76213e7931a8)

## v0.1.0

### Feature

* basic checkitweg implementation with uploading pdf's (22518a62e3cc)

### Fix

* fix bugs from baw init template (4c2363ed1318)

### Documentation

* basic description of running dev server (f9a8668e5b52)

## v0.0.0 Initial release

