# Changelog

Every noteable change is logged here.

## v0.8.0

### Feature

* integrate writer html generation result (2c4bb8454ad3)
* add path to generated writers content (454207694af9)
* set focus on input box to toggle visibility via space (9bbc642e63a9)
* add option to hide/show linter findings (dd5f86a6d72f)
* add shortcuts to navigate though results (831d1d2a52dd)
* enable to navigate thru error border (a9f4cfa6544b)
* return failure if document does not exists (f28430da7655)
* use waiting result-view to represent result view (46fe0a5df1dc)
* make pages bar visible as default (6e8ecc1b3e5a)
* add next previous function change displayed page (44112ff64bab)
* add toggle button to toggle page number view (fe25053e46a5)
* deliver every page and decide via web view what error/page is presented (2ce33b607951)
* use Times as default font face (5d67473aaa70)

### Fix

* improve java script style (477473d17502)
* preserve page order (028bb780c9fc)
* avoid JavaScript error if data can not be loaded (205171e07034)

## v0.7.0

### Feature

* sort document by year, month, day, hour and second (172c87235e69)
* add warning that html result path does not exists (c9c23e958620)
* connect html page view to result delivery service (56185052e62f)

### Fix

* fix hard coded links (a4bd7d0bf1af)

### Documentation

* Happy New Year! (dd98cea6c8b0)

## v0.6.1

### Fix

* change style of error content box (122ad3282e3d)

## v0.6.0

### Feature

* harden result view against malformed folder structure (f1d936cbf3e2)
* connect web service and view of result view (502583c04ddf)
* add web service to deliver result view status (0ad6f9482de7)
* add result view and link to documents view (0e379d4c2e2a)
* use modern html syntax (35b652db0a8c)
* raise ValueError if creating illegal state (1adbe765dcd1)
* change document list item if analysis fails (ca3cfe072b75)
* extend loader to load linter result (63c314f9dbcb)
* update fast view on content change (b0799c08dfa2)
* filter non matching directory names (af099b3c4389)
* extend FastViewStatus with running status (0078c6bc2a49)
* connect view with web service data delivery (5d268b5a9038)
* add web service to deliver current FastViewStatus (73aca2acef91)
* add method to load FastViewStatus (9da81ff7ce33)
* add FastViewStatus to store status of FastView-Process (4538919c1362)
* link fast view into waiting room (d8a2044c7279)
* add draft for fastview (f95529e56854)
* extend status state machine of fast view and result view (3b47c1d6d682)
* enable link to visit fast view and result view (72bd280bc3c9)
* extend validation result view (8e611fa7dba9)
* enable validation result view after finishing validation (d22292039fa5)
* add validation result view (b93ce3540b67)

### Fix

* validate html output (2f5c5418db03)
* check only todo instead of both folder (666081bfc2b3)
* correct path to results to view (9187aac64110)
* fix link when being on sub page (f43a47c5369e)
* move method to solve cyclic imports (acacdaf4b18a)
* remove forbidden body statement (bc433138bd4c)
* rename Blueprints to avoid problems with importing (9f5712325e5c)

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

