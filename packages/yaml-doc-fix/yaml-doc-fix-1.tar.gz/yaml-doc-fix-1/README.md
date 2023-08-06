# Ansible yamllint "document-start" warning fixer

Based on https://gist.github.com/danihodovic/94597709bf7e8bd89a4a82fcaee5c05e

Auto fixes the yamllint warning `document-start`. Walks all the files in the `ansible` directory and executes yamllint on every yaml file. If the document start error is found it prepends the file with `---\n`.

## Install with pip:
```
pip install yaml-doc-fix
```