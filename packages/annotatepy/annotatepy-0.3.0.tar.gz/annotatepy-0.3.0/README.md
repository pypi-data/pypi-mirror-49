annotatepy
==========

Scans Python source code and emits an annotation graph for
[git.sr.ht](https://git.sr.ht/)'s code [annotations
feature](https://man.sr.ht/git.sr.ht/annotations.md).

**This project is in early stages of development, so things may change and break
without warning.**

Resources
---------

* Homepage: https://git.sr.ht/~ihabunek/annotatepy/
* Issues: https://todo.sr.ht/~ihabunek/annotatepy/
* Package: https://pypi.org/project/annotatepy/

Usage
-----

```
annotatepy [-h] [-o OUTPUT] [-r ROOT] [source_paths [source_paths ...]]

Generate sourcehut annotations

positional arguments:
  source_paths          one or more paths within the project containing the
                        code to be annotated (defaults to project root)

optional arguments:
  -h, --help            show this help message and exit
  -r ROOT, --root ROOT  project root (defaults to working dir)
  -v, --verbose         enable verbose logging
  -q, --quiet           disable logging

https://git.sr.ht/~ihabunek/annotatepy/
```

Example
-------

To annotate the code in the `src` and `test` dirs within your project and
upload the annotations to sourcehut, from the project root run:

```
annotatepy src test > annotations.json
```

See docs on uploading the generated annotations to your sourcehut project
[here](https://man.sr.ht/git.sr.ht/annotations.md).
