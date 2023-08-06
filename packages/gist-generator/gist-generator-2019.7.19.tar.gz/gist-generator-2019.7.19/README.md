<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install gist-generator
```

#### How it works
+   description as folder name. or `description.txt` if exist
+   `gitignore` supported
+   clones `.git` after gist creation
+   skip if `.git` exists

#### Config
```bash
$ export GITHUB_TOKEN="<GITHUB_TOKEN>"
```

#### Scripts usage
command|`usage`
-|-
`gist-generator` |`usage: gist-generator [-p|--private] path`

#### Examples
```bash
$ gist-generator .
```

private gist
```bash
$ gist-generator -p .
```

create multiple gists
```bash
$ find ~/git/gists -type d -mindepth 1 -maxdepth 1 -exec gist-generator {} \;
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>