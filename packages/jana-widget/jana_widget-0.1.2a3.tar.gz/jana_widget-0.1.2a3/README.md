jana-widget
===============================

JANA2 control widget

Installation
------------

To install use pip:

    $ pip install jana_widget
    $ jupyter nbextension enable --py --sys-prefix jana_widget


For a development installation (requires npm),

    $ git clone https://github.com/JeffersonLab/jana-widget.git
    $ cd jana-widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix jana_widget
    $ jupyter nbextension enable --py --sys-prefix jana_widget


## Development

This plugin initially created with:  
https://github.com/jupyter-widgets/widget-ts-cookiecutter

```bash
# First install the python package. This will also build the JS packages.
pip install -e ".[test, examples]"

# Run the python tests. This should not give you a few sucessful example tests
py.test

# Run the JS tests. This should again, only give TODO errors (Expected 'Value' to equal 'Expected value'):
npm test
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:

```bash
jupyter labextension install .
#or 
jupyter labextension install @electronioncollider/epic-widgets
```

For classic notebook, you can run:

```bash

jupyter nbextension install epic_widgets --py --symlink --sys-prefix 
jupyter nbextension enable epic_widgets --py --sys-prefix
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.


## Releasing your initial packages:

Prepare publishing tools for the first time:

```bash
pip install --upgrade pip
pip install setuptools wheel twine
```

- Add tests
- Ensure tests pass locally and on CI. Check that the coverage is reasonable.
- Make a release commit, where you remove the `, 'dev'` entry in `_version.py`.
- Update the version in `package.json`
- Relase the npm packages:
  ```bash
  npm login
  npm publish --access=public
  ```
- Bundle the python package: 
  ```bash
  python setup.py sdist bdist_wheel
  ```
- Publish the package to PyPI:
  ```bash
  
  twine upload dist/epic_widgets*
  ```
- Tag the release commit (`git tag <python package version identifier>`)
- Update the version in `_version.py`, and put it back to dev (e.g. 0.1.0 -> 0.2.0.dev).
  Update the versions of the npm packages (without publishing).
- Commit the changes.
- `git push` and `git push --tags`.
