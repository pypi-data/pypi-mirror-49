#require yapf

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

Add python file
===============

  $ hg up -Cq 0

  $ cat << EOF >> yapf-test-file.py
  > 
  > l = [1,
  >      2,
  >      3,
  > ]
  > EOF

  $ hg add yapf-test-file.py

  $ hg commit -q -m "Add yapf test file"

  $ hg format-source --date '0 0' yapf glob:yapf-test-file.py -m 'format using yapf'

  $ hg export . --git -T "{diff}"
  diff --git a/.hg-format-source b/.hg-format-source
  new file mode 100644
  --- /dev/null
  +++ b/.hg-format-source
  @@ -0,0 +1,1 @@
  +{"configpaths": [".style.yapf", "setup.cfg"], "pattern": "glob:yapf-test-file.py", "tool": "yapf", "version": "*"} (glob)
  diff --git a/yapf-test-file.py b/yapf-test-file.py
  --- a/yapf-test-file.py
  +++ b/yapf-test-file.py
  @@ -1,5 +1,5 @@
  -
  -l = [1,
  -     2,
  -     3,
  +l = [
  +    1,
  +    2,
  +    3,
   ]

Make some changes
=================

  $ cat << EOF > yapf-test-file.py
  > l = [1, 2, 3, 4,5,6,7,8,9,10]
  > EOF

  $ hg commit -q -m "Update yapf test file"

  $ hg export . --git -T "{diff}"
  diff --git a/yapf-test-file.py b/yapf-test-file.py
  --- a/yapf-test-file.py
  +++ b/yapf-test-file.py
  @@ -1,5 +1,1 @@
  -l = [
  -    1,
  -    2,
  -    3,
  -]
  +l = [1, 2, 3, 4,5,6,7,8,9,10]

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > yapf-test-file.py
  > l = [
  >     1,
  >     2,
  >     3,
  > ]
  > 
  > d = {"key": "value"}
  > EOF

  $ hg commit -m "Add dict"
  created new head

  $ hg export . --git -T "{diff}"
  diff --git a/yapf-test-file.py b/yapf-test-file.py
  --- a/yapf-test-file.py
  +++ b/yapf-test-file.py
  @@ -3,3 +3,5 @@
       2,
       3,
   ]
  +
  +d = {"key": "value"}

Add a config file
=================

  $ cat << EOF >> .style.yapf
  > [style]
  > based_on_style = pep8
  > column_limit = 10
  > EOF

  $ hg add .style.yapf

  $ yapf yapf-test-file.py
  l = [
      1,
      2,
      3,
  ]
  
  d = {
      "key":
      "value"
  }

  $ hg commit -m "Add yapf config file"

  $ hg export . --git -T "{diff}"
  diff --git a/.style.yapf b/.style.yapf
  new file mode 100644
  --- /dev/null
  +++ b/.style.yapf
  @@ -0,0 +1,3 @@
  +[style]
  +based_on_style = pep8
  +column_limit = 10


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   *   1970-01-01 00:00 +0000   test (glob)
  |    Add yapf config file
  |
  o  4:2   *   1970-01-01 00:00 +0000   test (glob)
  |    Add dict
  |
  | o  3   *   1970-01-01 00:00 +0000   test (glob)
  |/     Update yapf test file
  |
  o  2   *   1970-01-01 00:00 +0000   test (glob)
  |    format using yapf
  |
  o  1   2f19add4f218   1970-01-01 00:00 +0000   test
  |    Add yapf test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  setup.cfg: No such file or directory
  merging yapf-test-file.py
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg diff --git
  diff --git a/yapf-test-file.py b/yapf-test-file.py
  --- a/yapf-test-file.py
  +++ b/yapf-test-file.py
  @@ -1,7 +1,9 @@
   l = [
  -    1,
  -    2,
  -    3,
  +    1, 2,
  +    3, 4,
  +    5, 6,
  +    7, 8,
  +    9, 10
   ]
   
   d = {"key": "value"}

  $ hg commit -m "Merge"

  $ hg export . --git -T "{diff}"
  diff --git a/yapf-test-file.py b/yapf-test-file.py
  --- a/yapf-test-file.py
  +++ b/yapf-test-file.py
  @@ -1,7 +1,9 @@
   l = [
  -    1,
  -    2,
  -    3,
  +    1, 2,
  +    3, 4,
  +    5, 6,
  +    7, 8,
  +    9, 10
   ]
   
   d = {"key": "value"}

  $ hg export . --git -T "{diff}" --switch-parent
  diff --git a/.style.yapf b/.style.yapf
  new file mode 100644
  --- /dev/null
  +++ b/.style.yapf
  @@ -0,0 +1,3 @@
  +[style]
  +based_on_style = pep8
  +column_limit = 10
  diff --git a/yapf-test-file.py b/yapf-test-file.py
  --- a/yapf-test-file.py
  +++ b/yapf-test-file.py
  @@ -1,1 +1,9 @@
  -l = [1, 2, 3, 4,5,6,7,8,9,10]
  +l = [
  +    1, 2,
  +    3, 4,
  +    5, 6,
  +    7, 8,
  +    9, 10
  +]
  +
  +d = {"key": "value"}
