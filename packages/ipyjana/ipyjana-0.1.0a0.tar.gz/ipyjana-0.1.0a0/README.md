ipyjana
===============================

Jana widget

Installation
------------

To install use pip:

    $ pip install ipyjana
    $ jupyter nbextension enable --py --sys-prefix ipyjana


For a development installation (requires npm),

    $ git clone https://github.com/epic/ipyjana.git
    $ cd ipyjana
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipyjana
    $ jupyter nbextension enable --py --sys-prefix ipyjana

## Development

This plugin initially created with:  
https://github.com/jupyter-widgets/widget-ts-cookiecutter

```bash
# First install the python package. This will also build the JS packages.
pip install -e .
```


When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:

```bash
jupyter labextension link .
#or 
jupyter labextension install ipyjana
```

Run 
```bash
jupyter lab --NotebookApp.token=''
```

For classic notebook, you can run:

```bash

jupyter nbextension install ipyjana --py --symlink --sys-prefix 
jupyter nbextension enable ipyjana --py --sys-prefix
```

