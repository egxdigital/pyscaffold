# pyscaffold
> I started it way before that other guy did

# TODO
[x] Test arg_parser.py
[x] Test fragments.py
[x] Test pyscaffold.py

# TODO: Merge
[ ] Add _version.py and update setup.py
[ ] Tag master branch before creation of refactor-branch as version 0.1.0
[ ] Merge refactor-branch with master
[ ] Tag master branch as version 1.0.0

```bash
# Clone the repository and fetch all branches
git clone git@github.com:yourusername/yourproject.git
cd yourproject
git fetch --all

# Check out the refactor-branch
git checkout refactor-branch

# Update setup.py on master and tag it
git checkout master
# Update setup.py to version 0.1.0 using a text editor
git add setup.py
git commit -m "Set version to 0.1.0 in development"
git tag v0.1.0
git push origin master --tags

# Switch to refactor-branch (if not already)
git checkout refactor-branch

# Merge refactor-branch into master with strategy to overwrite completely
git checkout master
git merge --strategy=ours refactor-branch -m "Merge refactor-branch replacing master completely"

# Update setup.py to version 1.0.0 and tag it
# Update setup.py to version 1.0.0 using a text editor
git add setup.py
git commit -m "Set version to 1.0.0 for stable release"
git tag v1.0.0
git push origin master --tags

```