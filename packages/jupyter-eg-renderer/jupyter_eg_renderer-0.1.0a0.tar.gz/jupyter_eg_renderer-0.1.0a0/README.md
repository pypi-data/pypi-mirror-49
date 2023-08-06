jupyter-eg-renderer
===============================

Easy graph renderer for Jupyter Notebook

Installation
------------

To install use pip:

    $ pip install jupyter_eg_renderer
    $ jupyter nbextension enable --py --sys-prefix jupyter_eg_renderer


For a development installation (requires npm),

    $ git clone https://github.com//jupyter-eg-renderer.git
    $ cd jupyter-eg-renderer
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix jupyter_eg_renderer
    $ jupyter nbextension enable --py --sys-prefix jupyter_eg_renderer
