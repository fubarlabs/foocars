# **Markdown Files in GitHub**

## Table of contents
1. [How To Create a Markdown File In GitHub](#HowToCreateAMarkdownFileInGitHub)

2. [How To Create Folders In GitHub](#HowToCreateFoldersInGitHub)
  
3. [How To Upload Pictures Into a Folder](#HowToUploadPicturesIntoAFolder)

4. [How To Add Pictures into Markdown Files Using Relative Paths](#HowToAddPicturesIntoMarkdownFilesUsingRelativePaths)

5. [How To Resize Pictures](#HowToResizePictures)


## How To Create a Markdown File In GitHub <a name="HowToCreateAMarkdownFileInGitHub"></a>

Press “Create new file” on the right corner of your Github repo.

<img src="pictures/mkdGitHub/1.png" width="500">

Give it a name and press “Enter”

<img src="pictures/mkdGitHub/2.png" width="500">


Now you can start editing it. 

To add pictures into Markdown files basically we will create a folder to store our pictures and then point to that folder from our file.

## How To Create Folders In GitHub <a name="HowToCreateFoldersInGitHub"></a>
Reference:
https://stackoverflow.com/questions/18773598/creating-folders-inside-github-com-repo-without-using-git

It is possible to create a new folder from the web interface, but it would require you to have at least one file within the folder when creating it. GitHub has a limitation that there should be at least one file in a folder.  

1.	From GitHub, click on your Branch or Main and then click on “Create new file" on the lower right corner

<img src="pictures/mkdGitHub/3.png" width="500">

2.	The location of the new file will appear on the left. There create a new sub folder called “Pictures/” and a directory will be created.

<img src="pictures/mkdGitHub/4.png" width="500">

3.	As GitHub does not allow for empty folders add any file to that folder.

<img src="pictures/mkdGitHub/5.png" width="500">

Click “Enter” then commit the file to the Repo and the folder with the new file will appear.

More info:

<img src="pictures/mkdGitHub/6.png" width="500">



## How To Upload Pictures Into a Folder. <a name="HowToUploadPicturesIntoAFolder"></a>

Steps:
1.	Create an images folder in your GitHub repo (see section on how to create a subfolder)

2.	Add your pictures to the dedicated folder created on GitHub. Click on “Upload files” on the right corner.

<img src="pictures/mkdGitHub/7.png" width="500">

3.	Drag your pictures or upload them into the website.

4.	After uploading all your pictures. Click on “Commit” at the bottom.
The picture will appear on your folder:

<img src="pictures/mkdGitHub/8.png" width="500">


### How to add pictures into Markdown files using relative paths
References:

https://www.youtube.com/watch?v=hHbWF1Bvgf4

https://www.youtube.com/watch?v=R6euByfGaN4

Steps:
1.	Go to the markdown file where you want your picture.  Put the cursor on the location you want to insert the picture.

2.	The markdown syntax to add a picture is as follows:

In markdown language:

``` ![<alt text>] (<path>/<pictureName.extension>)```

In html language:

``` <img src="imagesFolder/you-picture.png" width="100" >```

Note 1:

If your picture name has a space, the above won’t work. You can either remove the space:

From “my picture.gif” to “my_picture.gif”

Or you can do this trick:
From “my picture.gif” to “my%20picture.gif”
This is how the picture path with a space will be stored.

Note 2:

If  you ever want to change the picture, just save the new picture with the same file name and delete the previous one. In this way, you won’t have to change the original markdown file, but only the picture file.


## How To Resize Pictures
Github’s markdown language won’t recognize size code, while some other markdown editors do. 

The trick is to use HTML code to insert the picture and that will allow us to size the image.

```<img src="imagesFolder/you-picture.png"> ```

Then you can add width and height attributes 

```<img src="imagesFolder/you-picture.png" width="100" >```

 -Only specify 1 attribute to maintain the aspect ratio

Don't forget to commit your changes!!!

