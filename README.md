# The Simple Noteprogram

#### __Note:__ This program is still being developed, it may be buggy.

This is a simple note-taking program written in Python 3 with GTK+ 3 aimed at GNU/Linux users. It will display a note icon in the system tray. The tray icon can be clicked and new notes with a title and a description can be made. The notes are always saved automatically.

## Windows/OSX support

This application was designed for GNU/Linux users. I haven't made a Windows installer (yet) so following these instructions for installing the Windows dependencies will result in many useless programs. I've included some Windows instructions anyway just because it's possible to run this program in Windows.

OSX is not supported in these instructions. I don't have a mac so i can't test my applications on OSX. However, installing the dependencies should work the same way it works for Windows and running should work similarly to GNU operating systems.

## Downloading and dependencies

Downloading this application is easy. Just go to the top right of this page and click the "Download zip" button. Then extract the `install-prefix` folder from the zip.

You need to have these dependencies installed in order to run this program:

| Name                  | Debian/Ubuntu package             | Windows download                                                                              |
|-----------------------|-----------------------------------|-----------------------------------------------------------------------------------------------|
| Python 3.2 or newer   | `python3` (installed by default)  | [python.org/downloads](https://www.python.org/downloads/)                                     |
| Appdirs for Python 3  | `python3-appdirs`                 | `py -m pip install appdirs` __[\*]__                                                          |
| PyGI for Python 3     | `python3-gi`                      | [sourceforge.net/projects/pygobjectwin32](https://sourceforge.net/projects/pygobjectwin32/)   |
| GTK+ 3 for GI         | `gir1.2-gtk-3.0`                  | Same as for PyGI, make sure it installs GTK+ 3                                                |
| AppIndicator 3 for GI | `gir1.2-appindicator3-0.1`        | Same as for PyGI, make sure it installs AppIndicator 3                                        |

__[\*]__ *Install Python first, then right-click command prompt in Start menu or Start screen, open it as administrator, type the command there and press Enter.*

## Running without installing

This is easy after downloading the `install-prefix` directory. On Windows, open `install-prefix`, go to `bin`, rename `the-simple-noteprogram` to `the-simple-noteprogram.pyw` and double-click it to run. On GNU/Linux, give the file executable permissions and run it. You can do it by running these commands on a terminal window (`$` is the prompt, don't type it literally):

    $ cd /path/to/install-prefix
    $ chmod +x bin/the-simple-noteprogram
    $ bin/the-simple-noteprogram

## Installing and uninstalling

#### GNU operating systems

First run the program without installing to make sure it works.

The `install-prefix` directory's content is meant to be installed into a directory somewhere on your computer. A typical location for it is `/usr/local`. The program should appear in the desktop environment's menu after installation. In the example commands, replace `/path/to/install-prefix` with the path to the `install-prefix` directory you extracted.

You can use rsync to install the content of the install-prefix directory, like this:

    $ cd /path/to/install-prefix
    $ sudo rsync -r * /usr/local

Uninstalling is a bit more complicated. We need to find the installed files and then remove them. You'll probably get some warnings from the last command saying that the directory is not empty, it's normal. Remember that `/path/to/install-prefix` is the path to the `install-prefix` you downloaded, __*not*__ to the directory you installed to!

    $ cd /path/to/install-prefix
    $ find -type f -exec sudo rm /usr/local/{} \;
    $ find -type d -exec sudo rmdir /usr/local/{} \;

#### Other operating systems

You can move the `install-prefix` directory anywhere you want and rename it to anything you want. You can also make a clickable link to the executable in `install-prefix/bin`.
