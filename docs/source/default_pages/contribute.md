# Contribute to this project

The Equayes tool is made to be applicable MCL project agnostic.  
If features are missing or you have suggestions to improve usage or this documentation, please share your thoughts!

```{margin} **@developers out there:**  
Let's work together via github issues to make this tool even better.  
Do never hesitate to write a message on teams if something is not clear!
```

(developer-installation)=
## Installation (developer mode)

```{margin}
```{admonition} pip -e mode
:class: tip
As soon as your package is pip installable, I'd recommend to always install you own packages like this during development.
```


```{include} ../../README.md
:start-after: "## Developer Installation"
:end-before: "## User Installation"
```



```{Note}
Directly pushing to the main branch is - by default - disabled (except for maintainers/owners of a repository).  
Feel free to use your own branch(es) or work on the `develop` branch.
E.g. `git checkout develop` and then create a merge request from your branch when your done.  
**Advantages are**  
- no "dirty" development code on main branch
- no "accidental" push to the main branch when it's protected  

But feel free to (ask your repo-maintainer to) unprotect the main branch, if you think it is not necessary.
```

## How to contribute
**Use [GitHub](https://github.com/mclprobability/Equayes.git) as the central platform to document (and discuss) problems/bugs/vulnerabilites/ideas/... <u>which are not solvable/implementable instantly</u>!**  
This way, issues are stored centrally for future investigation and colleagues can easily contribute without the need to necessarily deep-dive into the code - depending on how well an issue is written.

```{admonition} Dev-Setup is easy...
:class: dropdown
**...if one knows how.**  
This guide is surely not complete, so again:  
never hesitate to get in contact (or leave a GitHub issue ;), before you struggle around and lose your valuable time.
```
### Use GitHub issues
if you have improvements, suggestions, feature-requests, merge-requests or simply comments.
**<center>New issues are always very welcome!</center>**  

### Create merge requests
if you want to add your commits/branches with changed code/docs to this project.  
Merge requests then trigger a CI/CD pipeline with executing the unit-tests, so **don't be afraid to crash something!**  

```{Note}
If you just want to share code with other developers, push your own (or commits from the `develop` branch) to github.
```