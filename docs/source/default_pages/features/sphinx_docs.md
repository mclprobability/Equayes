# Documentation
This documentation generator is based on a custom implementation using [sphinx](https://www.sphinx-doc.org/en/master/) and [jupyterbook](https://jupyterbook.org/en/stable/intro.html) toolstack.
It's main focus is to simplify the creation of professional documentation exportable as html and latex code by simply writing **jupyter notebooks** (+ markdown) and python [**docstrings**](https://peps.python.org/pep-0257/).


## How to write your own docs

There are two major parts of writing your documentation:

- **scientific narrative**  
  describes the whole context and results, basically the *"what"* and *"why"*
- **technical documentation**  
  describes your code and *"how"* to use e.g. functions/classes/modules

### Scientific narrative
You can express the context of each part of your codebase in simple markdown files and jupyter notebooks. The latter is especially useful when showcasing how results are produced.

Check out the `docs/source` folder.
The `index.md` the (html) documentations **entry point** with a **table of contents** section where you can embed other markdown files and/or jupyter notebooks into your doc.

```{Note}
Only files which are included into a table of content (toc) is available in the documentation.
By defining toc's including files with it's own tocs you can specify a hierarchy (expandable section in your main table of contents on the left side of the documentation website).
```


### Technical documentation
Simply write [python docstrings](https://peps.python.org/pep-0257/) in your code.  
If you are using **vscode** I recommend to use the extension *[autodocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)*.  

The docs build process scans all code inside equayes source folder for docstrings and renders them nicely in the final documentation under *Technical Documentation*.

## Local build process

To create your docs **locally** you need some python packages.  
*(I suggest to install them into your own "docs_creation" or "sphinx" virtual (conda/venv) environment.)*

- Install required packages:
    ```
    pip install sphinx "sphinx-autoapi>=3" sphinx-design sphinx-book-theme myst-nb graphviz setuptools_scm
    ```
- navigate into your docs folder
- create your docs with e.g.
    - **`make html`** to create html docs  

  You can even make other documentation formats like:  
    - **`make latex`** to create latex docs (usable in e.g. [overleaf](https://www.overleaf.com/))
    - **`make latexpdf`**  
      (this requires having latex installed locally)

      
