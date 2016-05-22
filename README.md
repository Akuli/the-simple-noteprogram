# The Simple Noteprogram

This is a simple note-taking program written in Python 3 with GTK+ 3 aimed at GNU/Linux users. It displays a note icon in the system tray. The tray icon can be clicked and notes with a title and a description can be easily made. The notes are always saved automatically.

## Windows/OSX support

This application was designed for GNU/Linux users. I haven't made a Windows installer yet, so if you happen to be using Windows this program is not for you just yet.

OSX is not supported in these instructions. I don't have a mac so I can't test my applications on OSX. However, after installing the dependencies, you should be able to install this program on OSX the same way it can be installed in GNU/Linux.

## Dependencies

You need to have these dependencies installed in order to install this program:

| Name                  | Debian/Ubuntu package             |
|-----------------------|-----------------------------------|
| Git                   | `git`                             |
| GNU Make              | `make`                            |
| Python 3.2 or newer   | `python3` (installed by default)  |
| Appdirs for Python 3  | `python3-appdirs`                 |
| psutil for Python 3   | `python3-psutil`                  |
| PyGI for Python 3     | `python3-gi`                      |
| GTK+3 for GI          | `gir1.2-gtk-3.0`                  |
| AppIndicator 3 for GI | `gir1.2-appindicator3-0.1`        |

Most GNU/Linux distributions come with many of these dependencies installed, and the rest of them are usually available in the distribution's package manager. For example, on Ubuntu/Debian based distributions you can simply run this command to install everything (`$` is the prompt, don't type it literally):

    $ sudo apt-get install git python3-appdirs python3-psutil python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1

## Installing and uninstalling

With the dependencies installed, you can download and install this program using these commands:

    $ git clone https://github.com/Akuli/the-simple-noteprogram
    $ cd the-simple-noteprogram
    $ sudo make install

The Simple Noteprogram should be in your desktop environment's menu after installing it.

To uninstall this program you need the Makefile that came with it when you downloaded it. You can easily uninstall this program with it like this, assuming the Makefile is in a directory called `the-simple-noteprogram`:

    $ cd the-simple-noteprogram
    $ sudo make uninstall

## Issues

If you have trouble using this program please help me to improve it by opening an issue [here](https://github.com/Akuli/the-simple-noteprogram/issues).
