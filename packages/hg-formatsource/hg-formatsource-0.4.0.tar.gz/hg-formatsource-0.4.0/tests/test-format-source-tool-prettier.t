#require prettier

Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3

  $ hg init default-io-modes

  $ cd default-io-modes

  $ touch ROOT

  $ hg commit -Aq -m "Root"

Add js file
===========

  $ hg up -Cq 0

  $ cat << EOF >> prettier-test-file.js
  > var express = require('express');
  > var app = express();
  > 
  > app.get('/', function (req, res) { res.send('Hello World!'); });
  > 
  > app.listen(3000, function () { console.log('Example app listening on port 3000!'); });
  > EOF

  $ hg add prettier-test-file.js

  $ hg commit -q -m "Add prettier test file"

  $ hg format-source --date '0 0' prettier glob:prettier-test-file.js -m 'format using prettier'

  $ hg export . --git -T "{diff}"
  diff --git a/.hg-format-source b/.hg-format-source
  new file mode 100644
  --- /dev/null
  +++ b/.hg-format-source
  @@ -0,0 +1,1 @@
  +{"configpaths": [".prettierrc", "prettier.yaml", ".prettier.yml", ".prettier.json", ".prettier.toml", "prettier.config.js", ".prettierrc.js", "package.json"], "pattern": "glob:prettier-test-file.js", "tool": "prettier", "version": "*"} (glob)
  diff --git a/prettier-test-file.js b/prettier-test-file.js
  --- a/prettier-test-file.js
  +++ b/prettier-test-file.js
  @@ -1,6 +1,10 @@
  -var express = require('express');
  +var express = require("express");
   var app = express();
   
  -app.get('/', function (req, res) { res.send('Hello World!'); });
  +app.get("/", function(req, res) {
  +  res.send("Hello World!");
  +});
   
  -app.listen(3000, function () { console.log('Example app listening on port 3000!'); });
  +app.listen(3000, function() {
  +  console.log("Example app listening on port 3000!");
  +});

  $ cat prettier-test-file.js
  var express = require("express");
  var app = express();
  
  app.get("/", function(req, res) {
    res.send("Hello World!");
  });
  
  app.listen(3000, function() {
    console.log("Example app listening on port 3000!");
  });

Make some changes
=================

  $ cat << EOF > prettier-test-file.js
  > var express = require("express");
  > var app = express();
  > 
  > app.get("/", function(req, res) {
  >     res.send("Hello Foobar!");
  > });
  > 
  > app.listen(3000, function() {
  >   console.log("Example app listening on port 3000!");
  > });
  > EOF

  $ hg commit -q -m "Hello Foobar"

  $ hg export . --git -T "{diff}"
  diff --git a/prettier-test-file.js b/prettier-test-file.js
  --- a/prettier-test-file.js
  +++ b/prettier-test-file.js
  @@ -2,7 +2,7 @@
   var app = express();
   
   app.get("/", function(req, res) {
  -  res.send("Hello World!");
  +    res.send("Hello Foobar!");
   });
   
   app.listen(3000, function() {

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > prettier-test-file.js
  > var express = require("express");
  > var app = express();
  > 
  > app.get("/", function(req, res) {
  >     res.send("Hello World!");
  > });
  > app.get("/healthcheck", function(req, res) {
  >     res.send("OK!");
  > });
  > 
  > app.listen(3000, function() {
  >   console.log("Example app listening on port 3000!");
  > });
  > EOF

  $ hg commit -m "Add healthcheck"
  created new head

  $ hg export . --git -T "{diff}"
  diff --git a/prettier-test-file.js b/prettier-test-file.js
  --- a/prettier-test-file.js
  +++ b/prettier-test-file.js
  @@ -2,7 +2,10 @@
   var app = express();
   
   app.get("/", function(req, res) {
  -  res.send("Hello World!");
  +    res.send("Hello World!");
  +});
  +app.get("/healthcheck", function(req, res) {
  +    res.send("OK!");
   });
   
   app.listen(3000, function() {

Add a config file
=================

  $ cat << EOF > prettier.config.js
  > module.exports = {
  >   tabWidth: 2,
  >   singleQuote: true
  > };
  > EOF

  $ hg add prettier.config.js

  $ prettier --write prettier-test-file.js
  prettier-test-file.js *ms (glob)

  $ hg commit -m "Add prettier config file"

  $ hg export . --git -T "{diff}"
  diff --git a/prettier-test-file.js b/prettier-test-file.js
  --- a/prettier-test-file.js
  +++ b/prettier-test-file.js
  @@ -1,13 +1,13 @@
  -var express = require("express");
  +var express = require('express');
   var app = express();
   
  -app.get("/", function(req, res) {
  -    res.send("Hello World!");
  +app.get('/', function(req, res) {
  +  res.send('Hello World!');
   });
  -app.get("/healthcheck", function(req, res) {
  -    res.send("OK!");
  +app.get('/healthcheck', function(req, res) {
  +  res.send('OK!');
   });
   
   app.listen(3000, function() {
  -  console.log("Example app listening on port 3000!");
  +  console.log('Example app listening on port 3000!');
   });
  diff --git a/prettier.config.js b/prettier.config.js
  new file mode 100644
  --- /dev/null
  +++ b/prettier.config.js
  @@ -0,0 +1,4 @@
  +module.exports = {
  +  tabWidth: 2,
  +  singleQuote: true
  +};


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   *   1970-01-01 00:00 +0000   test (glob)
  |    Add prettier config file
  |
  o  4:2   *   1970-01-01 00:00 +0000   test (glob)
  |    Add healthcheck
  |
  | o  3   *   1970-01-01 00:00 +0000   test (glob)
  |/     Hello Foobar
  |
  o  2   *   1970-01-01 00:00 +0000   test (glob)
  |    format using prettier
  |
  o  1   602ac470e240   1970-01-01 00:00 +0000   test
  |    Add prettier test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  .prettier.json: No such file or directory
  .prettier.toml: No such file or directory
  .prettier.yml: No such file or directory
  .prettierrc: No such file or directory
  .prettierrc.js: No such file or directory
  package.json: No such file or directory
  prettier.yaml: No such file or directory
  merging prettier-test-file.js
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg diff --git
  diff --git a/prettier-test-file.js b/prettier-test-file.js
  --- a/prettier-test-file.js
  +++ b/prettier-test-file.js
  @@ -2,7 +2,7 @@
   var app = express();
   
   app.get('/', function(req, res) {
  -  res.send('Hello World!');
  +  res.send('Hello Foobar!');
   });
   app.get('/healthcheck', function(req, res) {
     res.send('OK!');

  $ hg commit -m "Merge"

  $ hg export . --git -T "{diff}"
  diff --git a/prettier-test-file.js b/prettier-test-file.js
  --- a/prettier-test-file.js
  +++ b/prettier-test-file.js
  @@ -2,7 +2,7 @@
   var app = express();
   
   app.get('/', function(req, res) {
  -  res.send('Hello World!');
  +  res.send('Hello Foobar!');
   });
   app.get('/healthcheck', function(req, res) {
     res.send('OK!');

  $ hg export . --git -T "{diff}" --switch-parent
  diff --git a/prettier-test-file.js b/prettier-test-file.js
  --- a/prettier-test-file.js
  +++ b/prettier-test-file.js
  @@ -1,10 +1,13 @@
  -var express = require("express");
  +var express = require('express');
   var app = express();
   
  -app.get("/", function(req, res) {
  -    res.send("Hello Foobar!");
  +app.get('/', function(req, res) {
  +  res.send('Hello Foobar!');
  +});
  +app.get('/healthcheck', function(req, res) {
  +  res.send('OK!');
   });
   
   app.listen(3000, function() {
  -  console.log("Example app listening on port 3000!");
  +  console.log('Example app listening on port 3000!');
   });
  diff --git a/prettier.config.js b/prettier.config.js
  new file mode 100644
  --- /dev/null
  +++ b/prettier.config.js
  @@ -0,0 +1,4 @@
  +module.exports = {
  +  tabWidth: 2,
  +  singleQuote: true
  +};
