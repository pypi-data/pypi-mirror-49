test the logic to capture and store the version of the tool used for the test

Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > rebase =
  > strip =
  > [format-source]
  > json = python $TESTDIR/testlib/json-pretty.py
  > json:configpaths = .json-indent
  > [default]
  > format-source=--date '0 0'
  > EOF

  $ hg init test_repo
  $ cd test_repo

Commit various json file

  $ cat << EOF > file-1.json
  > {"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  > EOF
  $ hg add .
  adding file-1.json
  $ hg commit --message 'initial commit'

Test various scenarios around tool version configuration

No version command, no regex
  $ hg format-source --date '0 0' json glob:file-1.json -m 'format without version command'
  $ hg cat .hg-format-source
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}

Version command configured, no regex
  $ hg format-source --date '0 0' json glob:file-1.json -m 'format with version command' --config "format-source.json:version-command=echo 'version 1.2.3b4'"
  $ hg cat .hg-format-source
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}

Version command configured, regex matching
  $ hg format-source --date '0 0' json glob:file-1.json -m 'format with version command' --config "format-source.json:version-command=echo 'version 1.2.3b4'" --config "format-source.json:version-regex=(\\d.\\d.\\d)"
  $ hg cat .hg-format-source
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "1.2.3"}

Version command configured, regex not matching
  $ hg format-source --date '0 0' json glob:file-1.json -m 'format with version command' --config "format-source.json:version-command=echo 'version 1.2.3b4'" --config "format-source.json:version-regex=' (\\d.\\d) '"
  $ hg cat .hg-format-source
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "1.2.3"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}

Version command configured, regex matching, no capture group
  $ hg format-source --date '0 0' json glob:file-1.json -m 'format with version command' --config "format-source.json:version-command=echo 'version 1.2.3b4'" --config "format-source.json:version-regex=\\d.\\d"
  $ hg cat .hg-format-source
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "1.2.3"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}

Not existing version command, no regex
  $ hg format-source --date '0 0' json glob:file-1.json -m 'format without version command' --config "format-source.json:version-command=non_existing"
  Version command 'non_existing' for tool 'json' exited with 127
  $ hg cat .hg-format-source
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "1.2.3"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}

Failing version command, no regex
  $ hg format-source --date '0 0' json glob:file-1.json -m 'format without version command' --config "format-source.json:version-command=python -c 'import sys; sys.exit(23)'"
  Version command "python -c 'import sys; sys.exit(23)'" for tool 'json' exited with 23
  $ hg cat .hg-format-source
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "1.2.3"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json", "version": "version 1.2.3b4"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
  {"configpaths": [".json-indent"], "pattern": "glob:file-1.json", "tool": "json"}
