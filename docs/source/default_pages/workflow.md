This document outlines the cornerstones of this project's
(sw_dev_workflow)=
# Software Development Workflow
**Jupyter Notebooks should <ins>use</ins> functions**, while  
**python files <ins>implement</ins> functions**!

(how-to-implementing-a-feature)=
## How-To: implement a feature
To achieve a robust, tested and reusable codebase, SW Developers should follow these steps:
0. checkout your favourite branch, which is **not** the main branch
1. **prototype in a jupyter notebook**
   - if you are more familiar with notebook scripting, keep performing your own best-practice.
   - Tip: try to limit yourself to "one unit of logic" (e.g. "sanity checks") and complete points 2, 3 & 4 before proceeding prototyping
2. refactor your logic into functions in a corresponding .py file
   - a good place to store them is Equayes/equayes/core/<my_unit_of_logic>.py
   - don't forget to [write docstrings](how-to-write-docstrings)
3. write unittest(s) for that function
   - write your unittest in Equayes/tests/
   - you can have multiple files there, just start their filename with "test_<whatever>.py"
   - help yourself by dowing that directly after your function to test is placed in <my_unit_of_logic>.py
   - check out [how to write unit tests](how-to-write-unittests) section for more infos
4. use that function in your Notebook
   - in your notebook, `import equayes` to **use** your fresh function for further prototyping
   - depending on your __init__.py file(s), also something like `from equayes import my_perfect_function`
  
Now - with point 4 done - you should realize one advantage of doing steps 2 and 3 frequently:  
**Notebook content can focus on interpretation of results and is not overloaded with implementation details.**  
Many more advantages of doing so will stand out soon.  

5. if you're happy with your results, merge your changes into the main branch as stated in our *[branching strategy section](branching-strategy)*.



---
## More Tips:

### Initial Setup <br/> (for first time users/developers of this repo)
To work on this repository locally, clone it with `git clone https://github.com/mclprobability/Equayes.git`.  
To develop according to [our development workflow](how-to-implementing-a-feature) install this package in editable mode by  
- navigate to eh cloned folder
- and `pip install -e .`

(branching-strategy)=
### Branching Strategy

First things first: get comfortable with working with [git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)! It can help you and is not difficult. Try [tools like this](https://learngitbranching.js.org) get an intuition.

0. **Don't use the main branch** while prototyping
1. Use whatever branching you prefer (single develop branch, or own branch for each feature/logic_unit,...)
2. Merge working things (which follow [our workflow](how-to-implementing-a-feature)) into main branch
3. **Only what is committed to the main branch is relevant repo content!**

Let's see in the future, if protecting the main branch and working with merge-requests is a good idea.  
But for now let's keep it simple.

(how-to-write-unittests)=
### How-To: write unittests
- write your tests in that folder: `Equayes/tests/`
- [get more infos on unittests](https://docs.python.org/3/library/unittest.html)

(how-to-write-docstrings)=
### How-To: write docstrings
- if you code in visual studio code, let you help by [autoDocstring extension](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- Let's be consistent with docstring format. I suggest google style format.