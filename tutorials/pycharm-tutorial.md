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

PIC1 HERE ================================================================

•	Give a name to the file, then click OK.


PIC2 HERE ================================================================================

This step will generate a file which is named to **test.py**

### How to configure the Interpreter <a name="Interpreter"></a>

Tutorials:

https://www.jetbrains.com/help/pycharm/creating-empty-project.html#

https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

The easiest way is to create a new project and set the environment from there
•	Click on “File” – “Create New Project”

PIC3 HERE =====================================================================================

File-New Project – Existing interpreter – Select the Python interpreter corresponding to your project

The environments created by Conda is always located in 

  /Users/.../anaconda3/envs/

Alternatively, locate your environment using the following tutorial:

https://docs.anaconda.com/anaconda/user-guide/tasks/integration/python-path/

  •	Now, select the interpreter. Use the option **“Existing interpreter”**. 

PIC4 HERE =====================================================================================

PIC5 HERE =====================================================================================

Click OK, and then Create
If you want to manage packages and versions for your environment, you can follow this tutorial:

https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#

•	Now, VERY IMPORTANT: Wait for the “skeleton” to build

PIC6 HERE =====================================================================================

•	Lastly, specify the location of your project, where the files will be saved.
•	Click on the **“Create“** button.


### Alternative ways to configure the Interpreter <a name="Interpreter2"></a>

Once the new project is created and you have assigned a folder to it:
***File-Settings – Project – Project Interpreter***

PIC7 HERE =====================================================================================

PIC8 HERE =====================================================================================


## Loading Scripts <a name="Scripts"></a>

We will load and run a script called: “multiagent_figure_eight”.


### Option 1. Use PyCharm terminal <a name="Option1"></a>
PyCharm has its own terminal where you could run your commands in command line:

PIC9 HERE =====================================================================================


### Option 2. Load the scripts on the Configurations tool <a name="Option2"></a>
This option is the most convenient as it allows to run scripts with just one click. Additionally, you can run several scripts at the same time.

**Run – Edit-Configurations**

PIC10 HERE =====================================================================================

The general configuration is:

PIC11 HERE =====================================================================================

The below is the equivalent of the following command on the terminal:
     python train.py multiagent_figure_eight
     
PIC12 HERE =====================================================================================     

To run the scripts select the configuration you want to run and hit the green “run” triangle

PIC13 HERE =====================================================================================   

## Debugging a Script <a name="Debug"></a>

Full information here:

https://www.jetbrains.com/help/pycharm/part-1-debugging-python-code.html#

Open the script you want to debug and place breakpoints
**Run - Debug**

PIC14 HERE =====================================================================================   

Click on **“Python Console”** below to see the values of your variables

PIC15 HERE =====================================================================================   


## Working with Git and PyCharm <a name="Git"></a>

Complete info can be found here:

https://www.jetbrains.com/help/pycharm/github.html#

https://waterprogramming.wordpress.com/2016/09/02/a-guide-to-using-git-in-pycharm-part-1/

### To add the project into version control

Go to the VCS menu, then  – Import into Version Control  - then do these 2 steps:
  1.	Create Git repository -  select the folder containing the project - done
  2.	Share project on Github – Add the Repo name 

PIC16 HERE =====================================================================================  

### To add my GitHub repo
Go to “Settings”
Either with ALT+CTRL +S
Or File – Settings 
Or Go to Settings here:

PIC17 HERE =====================================================================================

Find the Version Control tab on the left pane
Click the **Add** button on the right. And add your GitHub repo and the Git configuration.

### Remote repo configuration
File - Settings

PIC18 HERE =====================================================================================

Click on the refresh circle on the left, otherwise it won’t recognize the update. 

PIC19 HERE =====================================================================================

Under Version Control you will find Git and GitHub


PIC20 HERE =====================================================================================

### Rebasing local Git or Remote Repo

https://www.jetbrains.com/help/pycharm/sync-with-a-remote-repository.html#update

### Fetching /Pulling (i.e. get latest changes) local Git or Remote Repo

https://www.jetbrains.com/help/pycharm/sync-with-a-remote-repository.html#update

### Commit to Remote GitHub Repo
VSC – Git – Push –Force Push

PIC21 HERE =====================================================================================

### Committing to Local Git

https://www.jetbrains.com/help/pycharm/commit-and-push-changes.html

Right click on a file –Git – Commit

PIC22 HERE =====================================================================================

### Managing versions
After you have linked PyCharm to your Repo, you can manage the version control from the bottom panel (there is a same panel on the upper right)

Click were it says “Git” and the box will expand

PIC23 HERE =====================================================================================

You can manage the remote and master Repos:

PIC24 HERE =====================================================================================

Or here:

PIC25 HERE =====================================================================================

### Change the GitHub Repo

https://stackoverflow.com/questions/23241509/how-to-change-github-repository-in-idea-intellij

Update or add Git repository URL in Intellij

  VCS - > Git - > Remotes

Popup will open with all repository URLs configured, you can simply edit them or add new one

