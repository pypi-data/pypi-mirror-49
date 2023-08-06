
# epic-widgets

[![Build Status](https://travis-ci.org/DraTeots/epic-widgets.svg?branch=master)](https://travis-ci.org/DraTeots/epic_widgets)
[![codecov](https://codecov.io/gh/DraTeots/epic-widgets/branch/master/graph/badge.svg)](https://codecov.io/gh/DraTeots/epic-widgets)


EIC EPIC widgets collection

## Installation

You can install using `pip`:

```bash
pip install epic_widgets
```

Or if you use jupyterlab:

```bash
pip install epic_widgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] epic_widgets
```

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

```
jupyter labextension link .
```

For classic notebook, you can run:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter nbextension install --sys-prefix --symlink --overwrite --py @electronioncollider/epic-widgets
jupyter nbextension enable --sys-prefix --py @electronioncollider/epic-widgets
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
  
  twine upload dist/epic-widgets
  ```
- Tag the release commit (`git tag <python package version identifier>`)
- Update the version in `_version.py`, and put it back to dev (e.g. 0.1.0 -> 0.2.0.dev).
  Update the versions of the npm packages (without publishing).
- Commit the changes.
- `git push` and `git push --tags`.
