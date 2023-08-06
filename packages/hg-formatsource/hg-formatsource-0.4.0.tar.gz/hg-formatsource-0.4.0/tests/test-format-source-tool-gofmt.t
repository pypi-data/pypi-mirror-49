#require gofmt

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

Add go file
===========

  $ hg up -Cq 0

  $ cat << EOF >> gofmt-test-file.go
  > package main
  > 
  > 
  > import "fmt"
  > func main() {
  > fmt.Println("hello world")
  > }
  > EOF

  $ hg add gofmt-test-file.go

  $ hg commit -q -m "Add gofmt test file"

  $ hg format-source --date '0 0' gofmt glob:gofmt-test-file.go -m 'format using gofmt'

  $ hg export . --git -T "{diff}"
  diff --git a/.hg-format-source b/.hg-format-source
  new file mode 100644
  --- /dev/null
  +++ b/.hg-format-source
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:gofmt-test-file.go", "tool": "gofmt", "version": "*"} (glob)
  diff --git a/gofmt-test-file.go b/gofmt-test-file.go
  --- a/gofmt-test-file.go
  +++ b/gofmt-test-file.go
  @@ -1,7 +1,7 @@
   package main
   
  -
   import "fmt"
  +
   func main() {
  -fmt.Println("hello world")
  +	fmt.Println("hello world")
   }

