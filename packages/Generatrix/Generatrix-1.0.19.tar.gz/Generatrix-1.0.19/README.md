# Generatrix Py
A utility script that generates a list of branches/tags as url markdown.
Useful when making tutorials, and creating branches per each video or step of the tutorial. This gives the ability to the learner to go to the branch and download the branch as zip as needed. Also it keeps some sort of sanity for the creator to avoid having to track down zip files and what not, just let git and generatrix do the work.

# Dependencies
Not much is needed for this to run, most is installed by default on unix based systems. For windows you might need to install dependencies, but if you work with python and git you might have them already.
- Python
- Pip
- git
- git username configured or else give it as an argument

# Install
```
pip install Generatrix
```

# Usage
cd into your git repo folder that has remote branches/tags, and the command would be:
To return all branches and tags markdown:
```
gtrix
```
```
gtrix -u "username"
```

If you'd rather like to work with tags only:
```
gtrix -t
```

# Contributions
Open to suggestions, and contributions.
