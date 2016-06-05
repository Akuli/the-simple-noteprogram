# The Simple Noteprogram

#### NOTE: This program is still being developed. This notice will be removed when this program is ready.

This is a simple note-taking program written in Python with GTK+. It displays a note icon in the system tray. The tray icon can be clicked and notes with a title and a description can be easily made. The notes are always saved automatically.

## Windows/OSX support

This application was designed for GNU/Linux users. I haven't made a Windows installer yet, so if you happen to be using Windows this program is not ready for you just yet.

OSX is not supported in these instructions. I don't have a mac so I can't test my applications on OSX. However, after installing the dependencies, you should be able to install this program on OSX the same way as on GNU/Linux.

## Dependencies

You need to have these dependencies installed in order to install this program:

| Name                              | Debian/Ubuntu package             |
|-----------------------------------|-----------------------------------|
| Git                               | `git`                             |
| GNU Make                          | `make`                            |
| Python 3.2 or newer               | `python3` (installed by default)  |
| Appdirs for Python 3              | `python3-appdirs`                 |
| psutil for Python 3               | `python3-psutil`                  |
| PyGI for Python 3                 | `python3-gi`                      |
| GTK+3 for GI                      | `gir1.2-gtk-3.0`                  |
| AppIndicator 3 for GI (optional)  | `gir1.2-appindicator3-0.1`        |

Most GNU/Linux distributions come with many of these dependencies installed, and the rest of them are usually available in the distribution's package manager. For example, on Ubuntu/Debian based distributions you can simply run this command to install everything (`$` is the prompt, don't type it literally):

    $ sudo apt-get install git make python3-appdirs python3-psutil python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1

## Downloading and running without installing

If you installed all the dependencies succesfully you should be able to download this program and try it out without installing it, like this:

    $ git clone https://github.com/Akuli/the-simple-noteprogram
    $ cd the-simple-noteprogram
    $ make run

## Installing and uninstalling

After a test run, you can install this program easily.

    $ sudo make install

By default, the program will be installed to `/usr/local`. You can install to a custom location like this:

    $ make select-prefix
    $ sudo make install

The program should be in your desktop environment's menu after installing it.

To uninstall this program, you need the directory you used for installing. Uninstalling is simple:

    $ sudo make uninstall

## Issues

If you have trouble using this program please help me improve it by opening an issue [here](https://github.com/Akuli/the-simple-noteprogram/issues).
