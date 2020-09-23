# Changelog

Every noteable change is logged here.

## v1.1.0

### Feature

* add allgemeine geschaeftsbedingungen (affdb8fcb2c2)
* replace resource selector with bootstrap components (bd94577db9ed)
* add flashed message area to inform user (971d5ef2698b)
* add bootstrap 3.4.1 dependency (26e70e673ea0)
* use new upload mechanism (9d3126f0df5d)
* use new delete API (102240957ec1)
* use new API to change finding status (e2c9e35fa620)

### Fix

* check pdf header to ensure correct file type (be95e5d83dbb)
* remove non required type cast (a687caa08201)
* fix finding id test data (9fe73afc7cb7)
* convert finding to required int (dcdb56f86d88)

## v1.0.0

### Feature

* add document properties provider (3f147a14a5d8)
* add captions data provider (6deca45f3ce2)
* add docstyle data provider (7e5cd1eda71b)
* add footnotes provider (4e2700ab91c1)
* add html pages provider (40f5759eab10)
* add html pages provider (56ee454cb6ed)
* add put request to update solution status (d43efc2cbe12)
* add option to select findings by id (223fffa88d11)
* add method to simplify objects (848f0b367670)
* add method to get finding by document and finding id (3f15b0e4f0c1)
* introduce decorator to check existence of document (66a87a3eda98)
* add central findings entree point (1c8581acbafb)
* introduce option to create documents via posting url (4d20713fe776)
* introduce different exceptions to increase reporting ability (7232c04cef8e)
* add methods to create and delete documents (2cebe014d7aa)
* access document status by documentid (39d0b62ba66d)
* patch link accessing deleted document state (0aedceb706e7)
* add separate data API (b8b4b6c6bbe2)

### Fix

* use finding number instead of new hashing (bacb0ceb8ac3)
* ensure to start app correctly (e50c5090627e)

### Documentation

* add option to select findings by status (bf5714e34440)
* sort paragraph into new categories (4ec0f78b99f5)
* add REST documentation for pages representation (acb92690393e)
* add general API documentation overview (2915552a136d)
* add REST basic developer information (fbdbe5af072c)
* extend solution of state question (8945142f033b)

## v0.20.3

### Fix

* remove outdated import (3cf9ca2c2cdf)
* hide solved findings in overview (8b040faf78a7)

## v0.20.2

### Fix

* adjust error overview to the start of document (2d306f739087)

## v0.20.1

## v0.20.0

### Feature

* add view to display list of extract captions (add6b9c29ff1)
* extend interface to deliver extracted captions (4f2e2029a87a)

## v0.19.0

### Feature

* add upper pdf file limit (c6e36842757d)
* extend interface to download pdf from external web resource (c3a91f82aa4d)
* add option to upload file via web link (91359ccfa495)

## v0.18.0

### Feature

* enable clicking on additional non pdf pages (d4ca38d4d158)
* move finding menu from left to right (733a3d0f204d)
* add Enter key to solve current finding (e4d8747d559f)
* add operation menu to decider findings (e15c99b2b84a)
* update bookkeeping for every status update (8f92111e5b5d)
* hide solved items in error todo view (b65a2cc07b65)

### Fix

* display waiting status in documents view correctly (3dd89b612ea8)
* ensure that indexing works properly (e7e202bfaa67)
* adjust selecting first visible element (76d730f0904e)
* adjust back end and view data structure (1a3373a0fbc3)
* fix outdated import (81b1586fbe8a)

## v0.17.1

### Feature

* replace newlines with html line break (66533d0822cf)

### Fix

* enable document view after finishing document extraction (6536db95d182)

## v0.17.0

### Feature

* adjust highlighted text (8aece1fbe8ba)

### Fix

* highlight multiple id identifier (fcef11cf3151)

## v0.16.3

### Fix

* adjust to new data format (5f393774031f)

## v0.16.2

## v0.16.1

## v0.16.0

### Feature

* delete line after changing finding status (03ab02112146)
* improve loading performance due multi processing (edff24a9d1fb)
* reduce fade out time (fd3bc84b473e)
* highlight selected finding on selecting (6639fc253f83)
* add method to temporary highlight an finding in view (f560a613f84b)
* highlight ranged location in pdfview (b2b16dbaa6e1)
* add ranged location to result view data provider (6412a1fe285b)

### Fix

* reduce logging level of duplicated finding (9663974f5247)
* reduce log level (a5ae0dcb6fcb)
* fix status update handler (d2fbd7ce99f4)
* do not highlight removed items (8ba5fad7b239)

## v0.15.3

## v0.15.2

### Feature

* add first draft of example view (04436246620a)

## v0.15.1

### Feature

* disable footnote view if no footnotes are given (204f5bb2bda2)
* link page dimension data to view (5a266f13cae3)
* disable view item if not data is given (317655487ae0)
* replace points with centimeter as distance unit (7699c7faa32d)
* add profiling step to render result view (f99b76fbecf0)

## v0.15.0

### Feature

* properties, convert font id to user friendly font name (09fef391bcf9)
* add **-pattern to mark chars in message as <strong> (f21cd0844302)
* add font face converter to properties view (e58e13777462)
* link page content border to page output (75be7467a9f6)
* link docstyle data to docstyle view (e07c65fa0b5f)
* store doctextstyle data (772512b952a0)
* add doctextstyle loader (5a0a266a8ac6)
* link date to user input (29f53f05fc65)
* disable page selection toggle in app view (b28a457d230d)
* add fixed page selection button size (0214ed4df49a)
* link protocol data to user interface (aa442d00ca5f)
* add pdf document meta data to result view data protocol (102e698e7d43)
* add pdf properties view (52d647e49329)
* disable bottom scroll bar (8b8804755018)
* add option to open footnote page directly (60dc4ad979d6)
* add separator between different footnote pages (6f0d54f513ba)
* use send footer data to display in footer view (ad4dae295019)
* add footnotes loader (767620d99c7c)
* add empty footnotes to result data service protocol (6cdad2518dc9)
* improve app view (9d15257da20a)
* add footnote view to display overview of detected footnotes (fe9b2a393202)
* add optional title property to finding protocol (1b9821eeca3f)
* add view document style overview (e47a7671c815)

### Fix

* adjust pdf style properties view (afe6ffb27a09)
* fix problems with importing order when running dev server (cabb60627310)
* remove duplicated findings which are a result of bad scheduling (3cec7209e2eb)
* add logger to investigate a raw occurring problem (ad7cef7b20e2)
* catch problems in incomplete `Ranged Location` definition (e770fe0ec4bd)
* fix relation of error list to pdf view (892ea3ccf315)
* remove distance between page selection and page content (f150d53ef086)
* disable shortcuts on textual input (b1aa914d3451)
* adjust pdf finding buttons (3ef49ac258d4)
* minimize white space in app mode (65c83031cfff)
* fix pdfview error view position (aef1013023cc)
* do not update findings if not required (8604245e73c7)
* adjust table size data (e71583ad453c)

## v0.14.0

### Feature

* do not shrink minimal items on small displays (f1c6f79a91ad)
* improve mobile navigation (e9449a9027e2)
* enable deleting items of page zero (073fb35c978a)
* add app view for small displays (9011559b0b1d)
* use double instead of triple layout for small displays (e3fae8d160fa)
* add pdf error overview to display non page bound lintings (6236e9ae6430)
* add pdf overview page (6975b016d721)
* add function to share, delete and lock link (df7bf1062c7b)
* modernize style (43605dccd7e3)
* add option to delete document by remove button (456370e51e44)
* hidden removed documents (231881eed265)
* sum open, closed and excluded todos in table (05059b450160)
* add icons to prepare new functionality (a40b36a6b2a6)

### Fix

* ensure to handle closed/deleted items correctly (473cbf9453ca)
* highlight non ascending pages (6d948ac47c18)
* make order consistent with progress view (799f524004fb)
* fix main view to adjust right border (0026b876e226)
* do not add the todo entry of finished document (aed56dd88720)
* do not display document in done and progress state (3ac2cdf68976)
* reduce hack a little bit (a24dd438cabc)

## v0.13.0

### Feature

* animate changing of todo counter (53338d5c6382)
* change pages in reduces page view correctly (7b5188ef1868)
* start with error mode first (29a39a88e953)
* move findings to separate module (1cf9d9ded641)
* remove button to reduce complexity (9600a268cf89)
* add action listener to delete and restore buttons (2bac2109f2bb)
* jump to open, closed and reject depending on clicked item (42625808ba17)
* add content of open, done and closed findings (a28cc4014657)
* add parameter page to select page to open in pdfview (a0d52843fdd9)
* add method to remove content of DOM object (53de61f7b31f)
* add useful basic style (b66a5804bacd)
* change to pdfview on finding status click (6792a03c71fb)
* introduce `todolistview` to show manage findings (6b4e9ccce328)
* serialize user decision on linting (3b0dae222ec9)
* do not remove items just hide them (df6deddd3257)
* count solved, rejected and open findings in result view (14efeab7f9c3)
* add finding status counter to display open and solved todos (7b009d81d2bf)
* add method to create image button (59f89f622ff2)

### Fix

* ensure to start on valid page if first page contain no error (8e5981c63b37)
* fix constructor of result view (1053e37d7a6c)
* start with pdf view (c0da7211f5a9)
* fix goto todo view in result view (d0d664284d9e)
* do not use Number, cause it is limited by 16-bits (52cf23f6e341)
* remove highlight in view when removing finding (feac0a5d7eaa)

### Documentation

* add document to store design decisions (2742cc457c77)

## v0.12.0

### Feature

* highlight sentences which contain finding (dc113ec58392)
* add words to sentence findings (b24ab5ca2243)
* add hint of non existing html file (96c12966e86d)
* add word indexes to `sentence` findings (ca8d968f3d87)
* disable finding navigator for less then 2 findings (cccf950d5229)
* remove current finding and signal to server (fad2eadf7def)
* add method to remove index out of array (889e62f2723c)
* add operation bar to hide and remove findings (2f01e6434f10)
* add REST API to sync document finding state (00cdc49ffa7e)
* save selected findings over page changes (39c52d16b998)
* disable selection for non select able linting events (601e764842eb)

### Fix

* disable deleting finding on empty findings (2ee9974a15fa)
* fix spelling error (723a02730657)
* change background color of finding list to white (5537394dad8a)
* add missing reference to library (4046fd058f17)
* enable selecting finding by clicking on line (10bf03a0625b)
* run done only when open view at first (e6c73ecddddd)

## v0.11.0

### Feature

* use new waiting approach to handle process communication (6de7e71f0ee3)
* introduce general waiting/short/error approach (6636db94d28f)
* minimize area of page selection view (b3bf8c3a6565)
* add more explicit waiting room error handling (496bba176503)
* use jquery as js bib (8040d67b4a73)
* increase copyright date (a286fc35eacc)

### Fix

* ensure to handle empty linter pages correctly (eb676f904cf4)
* fix error message box (621298969e0b)
* fix documents table view (c402b5e6cb78)
* fix spelling error (1d6695f26a44)
* fix spelling errors (77335d47b119)

## v0.10.0

### Feature

* add description of hand-factor and BIG5 use cases (7bfda7a84b67)

### Fix

* fix link in fastview (c10e658609d5)

## v0.9.0

### Feature

* add images loader and provider for html content (f608b700c302)
* increase width of main view (697bc96df8b1)
* replace link template with static checkitweg url (abae851f9ae9)
* add method to replace ref links in generated content (2091aa65aa4a)

### Fix

* ensure to load html files only (37ce8c154c45)
* forward to error page if page does not exists (8421c5089991)
* fix search option (79d928c5c267)
* fix rst directive (01e72c0d36ee)
* fix spelling error (ccc6b977a000)

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

