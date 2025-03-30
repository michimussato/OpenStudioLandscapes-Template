# OpenStudioLandscapes Template Module

Source template version: [`1.1.0`](https://github.com/michimussato/OpenStudioLandscapes-Template/tree/1.0.0)

## Guide: How to use the template

1. Create your new Git repo on Github, 
   i.e. OpenStudioLandscapes-YourModule
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
   3. Rename src directory
      ```shell
      mv src/OpenStudioLandscapes/Template src/OpenStudioLandscapes/Your_New_Module
      ```
   2. ```shell
      git remote add origin https://github.com/yourlogin/OpenStudioLandscapes-Your-New-Module.git
      git branch -M main
      ```
   3. Create initial commit
      ```shell
      git add --all
      git commit -m "initial commit"
      ```
   4. Initial Push
      ```shell
      git push -u origin main
      ```
4. Rename Template
   1. OpenStudioLandscapes-Template -> OpenStudioLandscapes-Your-New-Module
   2. All occurrences of `<Your-New-Module>` -> `Your-Module`
   3. All occurrences of `<Your_New_Module>` -> `Your_Module`
   4. All occurrences of `John Doe` -> `Your Name`
   5. All occurrences of `john.doe@acme.com` -> `your.name@email.com`

# Install

```shell
cd OpenStudioLandscapes-Your-New-Module
pip install -e .[dev]
```
