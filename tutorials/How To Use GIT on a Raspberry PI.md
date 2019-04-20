# How To Use GIT on a Raspberry PI
## Table of Contents

1. [Checking whether GIT is already installed](#checking)
2. [Cloning a Repo from GitHub to your Pi](#cloning)
2. [How to Run Code](#running)
## Checking whether GIT is already installed <a name="checking"></a>
First we need to check whether GIT is installed on our PI
Type:

```git ```

or alternatively:

```git –version```

after the command prompt and see if it loads:

<img src="pictures/GitPI/1.png" width="500">
 

Otherwise, we can install  git as follows:

```sudo apt-get install git```

You'll need to configure it with 

```git config --global user.name "Your Name"```
```git config --global user.email email@example.com```



## Cloning a Repo from GitHub to your Pi <a name="cloning"></a>

We will download a copy of the Repository on our PI.  For this, first you might want to make a Fork (copy on your own GitHub of the original Repo) of the Repo and create your own Branch (playground area on your own Forked version). Both things should be done on GitHub’s website.

After we have the Fork or Branch we want, we need to copy the location of the Repo on GitHub, from where we’ll pull the Repo. 


To copy the address of a Repo:
Go to your Forked Repo on GitHub and click on “Clone or download” 

<img src="pictures/GitPI/2.png" width="500">

 
After clicking on the green button, the address of our Forked version of the original Repo will show. We will clone this Fork to our own local computer.

<img src="pictures/GitPI/3.png" width="500">
 

Click on the arrow next to the URL to copy the address.
On the Raspberry PI:

If you want to place it on your desktop:

```cd Desktop```
```git clone <the Repo adress>```

The cloning process will start

<img src="pictures/GitPI/4.png" width="500">

 

The folder will appear on your Desktop:

<img src="pictures/GitPI/5.png" width="500">

 

You can click on it to see its content.

## How to run code <a name="running"></a>
Navigate to the directory where the code is: 
```cd Desktop```
```cd foocars```
```python monitor.py```

or

```python3 monitor.py```


Reference:
https://www.raspberrypi.org/forums/viewtopic.php?t=159990








