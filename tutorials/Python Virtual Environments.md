# Python Virtual Environments

## Table of Contents

## What is a Virtual Environment?

A virtual environment is a tool that helps us to work in multiple python projects while keeping their packages and dependencies separate. Basically, it is a best practice tool that allows us to cut unwanted dependencies between projects by creating isolated python virtual environments for them.

For example, by default, every project on your system will use the same directories to store and retrieve site packages. Say that we have two projects and they both rely on the same package, but with a different version. If we upgrade this package globally for all our projects, it can break some of them.

This is where virtual environments come into play. To solve this problem, we just need to create two separate virtual environments for both the projects.
In an isolated environment, each project has only the dependencies and the packages that they need, with the specic versions that they need.

## When Should I use a Virtual Environment?
Virtual Environment should be used whenever you work on any Python based project. It is generally good to have one new virtual environment for every Python based project you work on. So the dependencies of every project are isolated from the system and each other.

Each environment will be its own virtual space. All packages installed within that space would not interfere with packages outside the environment and will be contained only inside this space.

## How do I create a Virtual Environment?
Follow these simple steps:

1.To build the different environments, we will use a library called VirtualEnv. Install this package using the package installer called pip.

2.To test that Pip is installed open a command prompt and try 

    ```pip help```
   
3.Use pip to install 'virtualenv' by typing:

    ```$ pip install virtualenv``` (if you are using Linux)

or alternatively:

```pip3 install virtualenv ```(if you are using pip3 and Windows)

4.Test your installation:
```$ virtualenv {version (Linux)```

5.Create a virtual environment for a project:
```$ cd project folder (Linux)```
```$ virtualenv venv (Linux)```

Note that the command virtualenv venv will create a folder in the current directory which will contain the Python executable les, and a copy of the pip library which you can use to install other packages. The name of the virtual environment (in this case, it was venv) can be anything; omitting the name will place the les in the current directory instead.

6.To begin using the virtual environment, it needs to be     activated. When the environment is set up, a le called activate is created inside the bin folder in the environment. We set this le as the source and we are now inside the environment.
   
```$ source venv/bin/activate```

Remember to activate the relevant virtual environment every time you work on the project.

7.Once you are done with the work, you can deactivate the virtual environment by the following command:

```(virtualenv name)$ deactivate```

# How Do I Use the Virtual Environment?
Now we need to install all the required packages and dependencies to run a project.

1.If you want to specify Python interpreter of your choice, for example Python 3, it can be done using the following command:

```$ virtualenv -p /usr/bin/python3 virtualenv name```

To create a Python 2.7 virtual environment, use the following command:

```$ virtualenv -p /usr/bin/python2.7 virtualenv name```

2.Now you can install dependencies related to the project in this virtual
environment. For example if you are using Django 1.9 for a project, you can install it like you install other packages.

```(virtualenv name)$ pip install Django==1.9```

The Django 1.9 package will be placed in virtualenv name folder and will be isolated from the complete system.

## virtualenvwrapper
virtualenvwrapper provides a set of commands which makes working with virtual environments much more pleasant. It also places all your virtual environments in one place. It really helps when you have a lot of environments and have trouble remembering their names.

Further installation instructions and commands can be found here:

https://virtualenvwrapper.readthedocs.io/en/latest/install.html

* To install (make sure virtualenv is already installed):
    ```$ pip install virtualenvwrapper```
    ```$ export WORKON HOME=~/Envs```
    ```$ source /usr/local/bin/virtualenvwrapper.sh```

* In Windows: `pip install virtualenvwrapper-win' (for Windows)
In Windows, the default path for WORKON HOME is 

%USERPRO-FILE%Envs

* Now, anytime you want to start a new project, you just have to do this:
```$ mkvirtualenv my-new-project```

* If you have many environments to choose from, you can list them all with the workon function:

    ```$ workon```
    ```my-new-project```
    ```my-django-project```
    ```web-scraper```

* Finally, here's how to activate:
    ```$ workon web-scraper```
    ```(web-scraper) $```

## Other useful commands
* lsvirtualenv
List all of the environments.

* cdvirtualenv
Navigate into the directory of the currently activated virtual environment, so you can browse its site-packages, for example.

* cdsitepackages
Like the above, but directly into site-packages directory.

* lssitepackages
Shows contents of site-packages directory.

## Where Can I Learn More?
https://www.geeksforgeeks.org/python-virtual-environment/

https://docs.python-guide.org/dev/virtualenvs/

http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/
