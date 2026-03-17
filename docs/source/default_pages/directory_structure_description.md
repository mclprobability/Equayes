# Project Structure

Here you learn about this projects file and folder structure, to get a feeling for the purpose of each file and directory + it's nesting decisions.


## Data-Science-Project-Template

The git repository created with this template may seem overwhelming in terms of so many folders and files.  

```{dropdown} See the full repository tree
    **`Equayes\   `> &nbsp; your repository root**\
`├── `**`.ecml\   `> &nbsp; used to store template-related code+info** (automatable workflow and service related)\
`│   ├── `**`.badges\badges\   `> &nbsp; badges will be stored here** via CI service pipeline\
`│   ├── `**`.githooks\   `> &nbsp; template-related githooks are stored here** (git-configured but not in use yet)\
`│   │   └── pre-commit   `> &nbsp; may implement pre-commit code formatting (not active yet)\
`│   └── .creation_info.yml   `> &nbsp; stores basic info about template version\
`├── `**`.git\   `> &nbsp; git folder as it is**\
`├── `**`.vscode\   `> &nbsp; optional vscode (IDE) folder**, helps if you use vscode\
`│   ├── extensions.json   `> &nbsp; recommended extensions (creates notification but are not installed automatically)\
`│   └── settings.json   `> &nbsp; recommended minimal vscode settings\     
`├── `**`data\   `> &nbsp; store your local (gitignored) data here,** subfolders are suggestions only, organise as you wish\
`│   ├── `**`0_raw\   `> &nbsp; store your untouched raw data here**\
`│   ├── `**`1_processed\   `> &nbsp; place to store intermediate/final, processed data**\
`│   ├── `**`2_models\   `> &nbsp; place to store binary models** (e.g. pickles, tensorflow, sklearn, onnnx,...)\
`│   └── `**`dummy_test_data\   `> &nbsp; a (random) test subset may be useful to have**, if data is very large\
`├── `**`docs\   `> &nbsp; your sphinx docs gets written here**\
`│   │         `> &nbsp; with jupyter notebooks and markdown, organize your own subfolders\
`│   ├── `**`source\  `> &nbsp; sphinx docs source files are in here**\
`│   │   ├── `**`_ecml\  `> &nbsp; place to store template-related metadata**\
`│   │   │   └── .creation_info.yml  `> &nbsp; stores basic info about template version\
`│   │   ├── `**`_references\  `> &nbsp; description**\ put non-notebook generated media sources for docs here\
`│   │   │   └── mcl_logo_ohnetext_v_small.jpg  `> &nbsp; MCL logo used in pages docs\
`│   │   ├── `**`_static\  `> &nbsp; hook folder for sphinx to store custom static code like .css files**\
`│   │   ├── `**`_templates\  `> &nbsp; hook folder to store custom sphinx templating code**\
`│   │   ├── `**`default_content\  `> &nbsp; place to store docs pages which are pre-written and applicable generically**\
`│   │   │   ├── contribute.md  `> &nbsp; docs page to describe installation/contribution\
`│   │   │   ├── useful_links.md  `> &nbsp; docs page with potential useful web-resources (currently not used)\
`│   │   │   └── workflow.md  `> &nbsp; description of the development-workflow recommendation\
`│   │   ├── `**`notebooks\  `> &nbsp; all your jupyter notebooks you want to put into the docs**\
`│   │   │   ├── Example_Notebook.ipynb  `> &nbsp; see the power of jupyter-book features\
`│   │   │   └── toc_notebooks.md  `> &nbsp; notebooks' table of content, decide which notebook appears where\
`│   │   ├── conf.py  `> &nbsp; sphinx related configuration file, pre-configured\
`│   │   ├── index.md  `> &nbsp; landing page for gitlab pages docs website, define your table of contents here\
`│   │   └── start.md  `> &nbsp; getting started section, embeds installation section of the top-level README.md file\
`│   ├── Makefile  `> &nbsp; used for docs creation on Linux systems\
`│   └── make.bat  `> &nbsp; used for docs creation on Windows systems\
`├── `**`etc\   `> &nbsp; place to store files which do not fit in other folders**\
`│   └── `**`envs\   `> &nbsp; python environment files are stored here (creation not automated yet)**\
`│       └── equayes.yml   `> &nbsp; conda environment yaml file, not automatically generated\
`├── `**`equayes\   `> &nbsp; YOUR SOURCE CODE FOLDER** (equivalent with "src", do  not change the name)\
`│   │                       `> &nbsp; organise it your own way, just keep the `utils`, `config` and `log` folder\
`│   ├── `**`config\   `> &nbsp; put all your configuration & parameters here**; always separate configuration from code!\
`│   │   ├── `**`base\   `> &nbsp; define global configuration here**; it will land on git\
`│   │   │   ├── globals.yml   `> &nbsp; define "global" configurations like **paths** or **constants** here,\
`│   │   │   │                 `> &nbsp; use it in code with `equayes.CONFIG`\
`│   │   │   ├── logging_config.yml   `> &nbsp; boilerplate configuration for the python logging implementation\
`│   │   │   └── parameters.yml   `> &nbsp; define parameters here, available in code with `equayes.PARAMETERS`\
`│   │   └── `**`local\   `> &nbsp; define local configuration here, identical config (to base config) is prioritized from here**\
`│   │       └── globals.yml   `> &nbsp; all "global" configuration like **paths** are defined here\
`│   ├── `**`core\   `> &nbsp; put core code here**; e.g. abstract base classes or functions gluing code from other modules\
`│   │   ├── __init__.py   `> &nbsp; makes this folder a python package\
`│   │   └── core.py   `> &nbsp; example core implementation, can be deleted\
`│   ├── `**`features\   `> &nbsp; scripts to turn raw data into features for modeling.**\
`│   │   └── __init__.py   `> &nbsp; makes all future .py files importable\
`│   ├── `**`io\   `> &nbsp; collect scripts to read and write files here**\
`│   │   ├── __init__.py   `> &nbsp; makes all future .py files importable\
`│   │   ├── reader.py   `> &nbsp; empty example file which may collect data read functions\
`│   │   └── writer.py   `> &nbsp; empty example file which may collect data write functions\
`│   ├── `**`logs\   `> &nbsp; collects log files, no code in here, do not delete**\
`│   │   └── .gitkeep   `> &nbsp; just to make the empty folder git-trackable\
`│   ├── `**`models\   `> &nbsp; scripts to train models and then use trained models to make predictions**\
`│   │   └── __init__.py   `> &nbsp; makes all future .py files importable\
`│   ├── `**`utils\   `> &nbsp; scripts to help with common tasks, provides config import**\
`│   │   ├── __init__.py   `> &nbsp; provides importable constants `PROJECT_ROOT`, `CONFIG` & `PARAMETERS`\
`│   │   ├── configuration.py   `> &nbsp; implements base/local configuration mechanism\
`│   │   ├── helper_functions.py   `> &nbsp; place to implement generic helper functions like `timeit` and `isnotebook`\
`│   │   └── log.py   `> &nbsp; implements the python logging boilerplate code\
`│   ├── `**`visualisation\   `> &nbsp; scripts to create exploratory and results oriented visualizations**\
`│   │   └── __init__.py   `> &nbsp; makes all future .py files importable\
`│   ├── __init__.py   `> &nbsp; top-level package definition\
`│   └── __main__.py   `> &nbsp; entry-point for CLI usage like `python -m equayes`\
`├── `**`notebooks\   `> &nbsp; store all your jupyter notebooks here**, organize in subfolders as you wish\
`├── `**`reports\   `> &nbsp; store final results, images, visualisations, etc.** in your local repo folder\
`│   ├── `**`figures\   `> &nbsp; folder suggestion to store plots/figures**\
`│   │   └── .gitignore   `> &nbsp; do not delete, the content of this folder gets gitignored\
`│   └── .gitignore   `> &nbsp; do not delete, the content of this folder gets gitignored\
`├── `**`tests\   `> &nbsp; write unittests here**\
`│   ├── test_unittest.py   `> &nbsp; an example unittest to help you get started\
`│   └── test_utils.py   `> &nbsp; tests the features shipped with the utilites folder\
`├── .gitignore   `> &nbsp; defines which folders and files should be ignored\
`├── .gitlab-ci.yml   `> &nbsp; gitlab CI/CD is defined here, already includes hybrid20 CI service pipelines\
`├── LICENSE   `> &nbsp; License will be defined here (here for future use)\
`├── MANIFEST.in   `> &nbsp; defines which non-python folders folders/files should be included in python packaging\
`├── README.md   `> &nbsp; Main (high-level) entry to describe your project, do not delete the installation section\
`└── pyproject.toml   `> &nbsp; configuration for python pip packaging; define dependencies here
```

But **don't worry**!  
Beside the full descriptive directory tree below, we strip it down to the essentials files and folders relevant for you.

```{dropdown} relevant repository tree
:open:
**`Equayes\   `> &nbsp; your repository root**\
`├── `**`data\   `> &nbsp; store your local (gitignored) data here,** subfolders are suggestions only, organise as you wish\
`│   └── `**`...\   `> &nbsp; organise your data in subfolders as you wish**; the current folders are just a suggestion\
`├── `**`docs\   `> &nbsp; your sphinx docs gets written here**\
`│   │         `> &nbsp; with jupyter notebooks and markdown, organize your own subfolders\
`│   └── `**`source\   `> &nbsp; sphinx docs source files are in here**\
`│       ├── `**`notebooks\   `> &nbsp; all your jupyter notebooks you want to put into the docs**\
`│       │   └── toc_notebooks.md   `> &nbsp; notebooks' table of content, decide which notebook appears where\
`│       ├── index.md   `> &nbsp; landing page for gitlab pages docs website, define your table of contents here\
`│       └── start.md   `> &nbsp; getting started section, embeds installation section of the top-level README.md file\

`├── `**`equayes\   `> &nbsp; YOUR SOURCE CODE FOLDER** (equivalent with "src", do  not change the name)\
`│   │                       `> &nbsp; organise it your own way, just keep the `utils`, `config` and `log` folder\
`│   ├── `**`config\   `> &nbsp; put all your configuration & parameters here**; always separate configuration from code!\
`│   │   ├── `**`base\   `> &nbsp; define global configuration here**; it will land on git\
`│   │   │   └── ...   `> &nbsp; maintain your config variables like paths and parameters\
`│   │   └── `**`local\   `> &nbsp; define local configuration here**, identical config (to base config) is prioritized from here\
`│   │       └── ...   `> &nbsp; maintain your config variables like paths and parameters\
`│   ├── `**`core\   `> &nbsp; put core code here**; e.g. abstract base classes or functions gluing code from other modules\
`│   ├── `**`features\   `> &nbsp; scripts to turn raw data into features for modeling.**\
`│   ├── `**`io\   `> &nbsp; collect scripts to read and write files here**\
`│   ├── `**`models\   `> &nbsp; scripts to train models and then use trained models to make predictions**\
`│   └── `**`visualisation\   `> &nbsp; scripts to create exploratory and results oriented visualizations**\
`├── `**`notebooks\   `>all your jupyter notebooks, organize in subfolders as you wish**\
`├── `**`reports\   `> &nbsp; store final results, images, visualisations, etc.** in your local repo folder\
`├── `**`tests\   `> &nbsp; write unittests here**\
`├── .gitignore   `> &nbsp; defines which folders and files should be ignored\
`├── README.md   `> &nbsp; Main (high-level) entry to describe your project, do not delete the installation section\
`└── pyproject.toml   `> &nbsp; configuration for python pip packaging; define dependencies here
```
