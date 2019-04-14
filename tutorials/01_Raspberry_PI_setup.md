# How to Setup a Raspberry PI With No Keyboard, No Mouse and No Ethernet Cable
## Intro
This tutorial explains how to setup a Raspberry PI using only command line (usually called “a headless setup”). The headless setup has the advantage that it can be done without needing a monitor and keyboard, as opposed to other types of setup. In a headless setup, the operating system (OS) is installed and configured entirely by command line.

The Raspberry PI runs under Linux, but comes out of the package without any operating system installed.  In this tutorial we show how to install Raspbian (a version of Debian Linux), which is the most common OS for the Raspberry Pi, and we will also show how to setup additional features.

Basically the steps required are as follows:

1. To install Raspbian (OS) we first need to download it to our computer to then transfer it to the Raspberry PI using the micro SD card.
2.	To transfer Raspbian from our computer to the Raspberry PI, we will use a micro SD car. The idea is to copy the OS from our computer to the SD card and from there to the Raspberry PI.
3.	After installing the OS in the Raspberry PI, we will update it and all the associated packages, plus any additional application we want.
4.	The last step will be to install the VCN application to manage the Raspberry PI remotely from our computer.

We explain how to achieve these steps in more detail below.

## Materials
*	A Raspberry Pi with WiFi on-board 
*	A micro SD card with SD adapter. We recommend at least 8GB of storage capacity.
*	A power supply for your Pi.
*	A computer connected to the same network you wish to connect your Pi to.
*	Download Raspbian from the RPi foundation. You can also download NoobS which is an Operating System installer / chooser.
*	PuTTY, a free SSH program. If you're on OSx or Linux, you can already SSH from your terminal.


## Burning the Operating System on the Mini SD Card
Unless you have bought a bundle with the OS already installed on your PI, you will need to install it. We recommend using Raspbian as the OS. For this, you will need to download Raspbian’s image to your computer and from there to the PI using the mini SD card. Note that the OS cannot be copied directly to the SD card, it needs to be burned into the SD card with a proper software.

Below we will provide the basic steps; additional information can be found on the link [2] under the “References” section below.

1.	The first step is to download Raspbian from the official site. This will usually be a zip file that then extracts to a file of type .img an image file.

Download “Raspbian Stretch with desktop and recommended software” from:
https://www.raspberrypi.org/downloads/

2.	We need to prepare the SD card to receive the OS image. For this, we will use a program called Etcher to format the SD card. Do not use Window’s formatting option.

Download Etcher from the link below. be sure to install the full version with Desktop, not the lite version.
 https://etcher.io/

3.	Before running the installer, eject any external storage devices such as USB flash drives and backup hard disks. This makes it easier to identify the SD card. Then insert the SD card reader into the slot on your computer or into the reader.

<img src="pictures/pic1.png" width="300">

4.	To write the OS image to the SD card, run Etcher and select the Zip file with the OS image. Click on “Flash” and the image will be now on our SD card. On windows 10 various pop ups many emerge, just ignore them and wait until it will say Flash Complete.

Note that you don't need to extract the image or format the card prior to writing.

<img src="pictures/pic2.png" width="500">

## References and Additional Resources.

1.	How to setup the PI with keyboard and monitor:

https://www.imore.com/how-get-started-using-raspberry-pi

https://lifehacker.com/the-always-up-to-date-guide-to-setting-up-your-raspberr-1781419054

2.	How to use Etcher:

Windows:

https://learn.adafruit.com/adafruit-raspberry-pi-lesson-1-preparing-and-sd-card-for-your-raspberry-pi/making-an-sd-card-using-a-windows-vista-slash-7

Mac:

https://learn.adafruit.com/adafruit-raspberry-pi-lesson-1-preparing-and-sd-card-for-your-raspberry-pi/making-an-sd-card-using-a-mac

3.	Tutorial on SSHing via Mac Terminal:

https://learn.adafruit.com/adafruits-raspberry-pi-lesson-6-using-ssh/using-ssh-on-a-mac-or-linux#

4.	List of WIFI configuration files for different Raspbian versions:

https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet

https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md



