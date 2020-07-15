# Pycharm Tutorial

## Table of Contents
1. [Intro](#intro)
2. [Creating a New Project in Pycharm](#NewProject)
   1. [First Project Example](#FirstProject)
   2. [How to configure the Interpreter](#Interpreter)
   3. [Alternative ways to configure the Interpreter](#Interpreter2)
3. [Loading Scripts](#Scripts) 
   1. [Option 1. Use PyCharm terminal](#Option1)
   2. [Option 2. Load the scripts on the Configurations tool](#Option2)
4. [Debugging a Script](#Debug)
5. [Working with Git and PyCharm](#Git)


## Intro <a name="intro"></a>
Install PyCharm free Community Edition from here:

https://www.jetbrains.com/pycharm/download


## Creating a New Project in Pycharm <a name="NewProject"></a>

### First Project Example <a name="FirstProject"></a>
Create your first Python script in PyCharm:

•	Right click on the project’s title: 


<img src="pictures/pyCharm/1.png" width="400">

•	Give a name to the file, then click OK.


<img src="pictures/pyCharm/2.png" width="400">

This step will generate a file which is named to **test.py**

### How to configure the Interpreter <a name="Interpreter"></a>

Tutorials:

https://www.jetbrains.com/help/pycharm/creating-empty-project.html#

https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

The easiest way is to create a new project and set the environment from there
•	Click on “File” – “Create New Project”

<img src="pictures/pyCharm/3.png" width="400">

File-New Project – Existing interpreter – Select the Python interpreter corresponding to your project

The environments created by Conda is always located in 

  /Users/.../anaconda3/envs/

Alternatively, locate your environment using the following tutorial:

https://docs.anaconda.com/anaconda/user-guide/tasks/integration/python-path/

  •	Now, select the interpreter. Use the option **“Existing interpreter”**. 

<img src="pictures/pyCharm/4.png" width="600">

<img src="pictures/pyCharm/5.png" width="600">

Click OK, and then Create
If you want to manage packages and versions for your environment, you can follow this tutorial:

https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#

•	Now, VERY IMPORTANT: Wait for the “skeleton” to build

<img src="pictures/pyCharm/6.png" width="700">

•	Lastly, specify the location of your project, where the files will be saved.
•	Click on the **“Create“** button.


### Alternative ways to configure the Interpreter <a name="Interpreter2"></a>

Once the new project is created and you have assigned a folder to it:
***File-Settings – Project – Project Interpreter***

<img src="pictures/pyCharm/7.png" width="650">

<img src="pictures/pyCharm/8.png" width="650">


## Loading Scripts <a name="Scripts"></a>

We will load and run a script called: “multiagent_figure_eight”.


### Option 1. Use PyCharm terminal <a name="Option1"></a>
PyCharm has its own terminal where you could run your commands in command line:

<img src="pictures/pyCharm/9.png" width="700">


### Option 2. Load the scripts on the Configurations tool <a name="Option2"></a>
This option is the most convenient as it allows to run scripts with just one click. Additionally, you can run several scripts at the same time.

**Run – Edit-Configurations**

<img src="pictures/pyCharm/10.png" width="500">

The general configuration is:

<img src="pictures/pyCharm/11.png" width="650">

The below is the equivalent of the following command on the terminal:
     python train.py multiagent_figure_eight
     
<img src="pictures/pyCharm/12.png" width="650">   

To run the scripts select the configuration you want to run and hit the green “run” triangle

<img src="pictures/pyCharm/13.png" width="650">

## Debugging a Script <a name="Debug"></a>

Full information here:

https://www.jetbrains.com/help/pycharm/part-1-debugging-python-code.html#

Open the script you want to debug and place breakpoints
**Run - Debug**

<img src="pictures/pyCharm/14.png" width="650"> 

Click on **“Python Console”** below to see the values of your variables

<img src="pictures/pyCharm/15.png" width="900">


## Working with Git and PyCharm <a name="Git"></a>

Complete info can be found here:

https://www.jetbrains.com/help/pycharm/github.html#

https://waterprogramming.wordpress.com/2016/09/02/a-guide-to-using-git-in-pycharm-part-1/

### To add the project into version control

Go to the VCS menu, then  – Import into Version Control  - then do these 2 steps:
  1.	Create Git repository -  select the folder containing the project - done
  2.	Share project on Github – Add the Repo name 

<img src="pictures/pyCharm/16.png" width="650">

### To add my GitHub repo
Go to “Settings”
Either with ALT+CTRL +S
Or File – Settings 
Or Go to Settings here:

<img src="pictures/pyCharm/17.png" width="650">

Find the Version Control tab on the left pane
Click the **Add** button on the right. And add your GitHub repo and the Git configuration.

### Remote repo configuration
File - Settings

<img src="pictures/pyCharm/18.png" width="650">

Click on the refresh circle on the left, otherwise it won’t recognize the update. 

<img src="pictures/pyCharm/19.png" width="600">

Under Version Control you will find Git and GitHub

<img src="pictures/pyCharm/20.png" width="600">


### Rebasing local Git or Remote Repo

https://www.jetbrains.com/help/pycharm/sync-with-a-remote-repository.html#update

### Fetching /Pulling (i.e. get latest changes) local Git or Remote Repo

https://www.jetbrains.com/help/pycharm/sync-with-a-remote-repository.html#update

### Commit to Remote GitHub Repo
VSC – Git – Push –Force Push

<img src="pictures/pyCharm/21.png" width="650">

### Committing to Local Git

https://www.jetbrains.com/help/pycharm/commit-and-push-changes.html

Right click on a file –Git – Commit

<img src="pictures/pyCharm/22.png" width="850">

### Managing versions
After you have linked PyCharm to your Repo, you can manage the version control from the bottom panel (there is a same panel on the upper right)

Click were it says “Git” and the box will expand

<img src="pictures/pyCharm/23.png" width="650">

You can manage the remote and master Repos:

<img src="pictures/pyCharm/24.png" width="850">

Or here:

<img src="pictures/pyCharm/25.png" width="700">

### Change the GitHub Repo

https://stackoverflow.com/questions/23241509/how-to-change-github-repository-in-idea-intellij

Update or add Git repository URL in Intellij

  VCS - > Git - > Remotes

Popup will open with all repository URLs configured, you can simply edit them or add new one

