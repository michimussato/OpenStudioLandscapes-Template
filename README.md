# OpenStudioLandscapes Template Module

Template version: `1.0.0`

## Guide: How to use the template

1. Create your new Git repo on Github, 
   i.e. OpenStudioLandscapes-YourModule
2. Clone OpenStudioLandscapes-Template
   ```shell
   git clone https://github.com/michimussato/OpenStudioLandscapes-Template.git OpenStudioLandscapes-YourModule
   ```
3. Rename Git remote
   1. ```shell
      cd OpenStudioLandscapes-YourModule
      rm -rf .git && git init --initial-branch=main
      ```
   2. ```shell
      git remote add origin https://github.com/yourlogin/OpenStudioLandscapes-YourModule.git
      git branch -M main
      git push -u origin main
      ```
   3. Create initial commit
      ```shell
      git add --all
      git commit -m "initial commit"
      ```
   4. Initial Push
      ```shell
      git branch -M main
      git push -u origin main
      ```
4. Rename Template
   1. OpenStudioLandscapes-Template -> OpenStudioLandscapes-YourModule
   2. All occurrences of <Template> -> YourModule
   3. All occurrences of John Doe -> Your Name
   4. All occurrences of john.doe@adme.com -> your@email.com
