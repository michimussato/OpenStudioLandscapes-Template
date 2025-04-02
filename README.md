# OpenStudioLandscapes Template Module

Source template version: [`1.6.0`](https://github.com/michimussato/OpenStudioLandscapes-Template/tree/1.6.0)

## Guide: How to use the template

1. Create your new Git repo on Github, 
   i.e. yourlogin/OpenStudioLandscapes-YourModule
2. Clone OpenStudioLandscapes-Template
   ```shell
   git clone https://github.com/michimussato/OpenStudioLandscapes-Template.git OpenStudioLandscapes-Your-New-Module
   ```
3. Rename Git remote
   1. ```shell
      cd OpenStudioLandscapes-Your-New-Module
      rm -rf .venv
      rm -rf .idea
      rm -rf .git && git init --initial-branch=main
      ```
   2. Rename src directory
      ```shell
      mv src/OpenStudioLandscapes/Template src/OpenStudioLandscapes/Your_New_Module
      ```
   3. ```shell
      git remote add origin https://github.com/yourlogin/OpenStudioLandscapes-Your-New-Module.git
      git branch -M main
      ```
   4. Create initial commit
      ```shell
      git add --all
      git commit -m "initial commit"
      ```
   5. Initial Push
      ```shell
      git push -u origin main
      ```
4. Rename Template
   1. OpenStudioLandscapes-Template -> OpenStudioLandscapes-Your-New-Module
      - `mv OpenStudioTemplates-Temkplate OpenStudioLandscapes-Your-New-Module`
   2. All occurrences of `<Your-New-Module>` -> `Your-Module`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/<Your-New-Module>/Your-Module/g'`
   3. All occurrences of `<Your_New_Module>` -> `Your_Module`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/<Your_New_Module>/Your_Module/g'`
   4. All occurrences of `John Doe` -> `Your Name`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/John Doe/Your Name/g'`
   5. All occurrences of `john.doe@acme.com` -> `your.name@email.com`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/john.doe@acme.com/your.name@email.com/g'`
   6. All occurrences of `20XX` -> `2025`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/20XX/2025/g'`
   7. All occurrences of `YourLogin` -> `your_github_login`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/YourLogin/your_github_login/g'`
   8. All occurrences of `<USERNAME>` -> `your_github_login`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/<USERNAME>/your_github_login/g'`
   9. Revert `README.md`
      - `git checkout -f README.md`
   10. Commit changes
      ```shell
      git add --all
      git commit -m "Initial Changes"
      ```
   11. Initial Push
      ```shell
      git push -u origin main
      ```

# Install

## Create venv

```shell
cd OpenStudioLandscapes-Your-New-Module
python3.11 -m venv .venv
pip install -U setuptools
```

## Install OpenStudioLandscapes-Your-New-Module into venv

```shell
cd OpenStudioLandscapes-Your-New-Module
pip install -e .[dev]
```

## Install OpenStudioLandscapes-Your-New-Module into OpenStudioLandscapes venv

```shell
cd OpenStudioLandscapes
pip install -e ../OpenStudioLandscapes-Your-New-Module[dev]
```
