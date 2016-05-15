# The Simple Noteprogram

This is a simple note-taking program written in Python 3 with GTK+ 3 aimed at GNU/Linux users. It will display a note icon in the system tray. The tray icon can be clicked and new notes with a title and a description can be made. The notes are always saved automatically.

## Windows/OSX support

This application was designed for GNU/Linux users. I haven't made a Windows installer (yet) so following these instructions for installing the Windows dependencies will result in many useless programs. I've included some Windows instructions anyway just because it's possible to run this program in Windows.

OSX is not supported in these instructions. I don't have a mac so i can't test my applications on OSX. However, installing the dependencies should work the same way it works for Windows and running should work similarly to GNU operating systems.

## Downloading and dependencies

Downloading this application is easy. Just go to the top right of this page and click the "Download zip" button. Then extract the `install-root` folder from the zip.

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

This is easy after downloading the `install-root` directory. On Windows, open `install-root`, rename `the-simple-noteprogram` to `the-simple-noteprogram.pyw` and double-click it to run. On GNU/Linux, run these commands on a terminal window (`$` is the prompt, don't type it literally):

    $ cd /path/to/install-root
    $ chmod +x bin/the-simple-noteprogram
    $ bin/the-simple-noteprogram

## Installing and uninstalling

#### GNU operating systems

First run the program without installing to make sure it works.

The `install-root` directory's content is meant to be installed into a directory somewhere on your computer. Typical locations for it are `/usr/local` for a system-wide install, `~/.local` for a user-wide install (where `~` is the user's home directory) and `~/your/build/root/usr` for creating a distribution package, such as a Debian package or an rpm package. The program should appear in the desktop environment's menu after installation. In the example commands, replace `/path/to/local` with a path to the `install-root` directory you extracted.

You can use rsync to install the content of the install-root directory. For example, a system-wide installation can be done like this:

    $ cd /path/to/install-root
    $ sudo rsync -r * /usr/local

You can also install user-wide like this, the .desktop file is edited to make sure it will find the executable. Don't run this as root.

    $ cd /path/to/install-root
    $ rsync -r * ~/.local
    $ echo "Exec=$HOME/.local/bin/the-simple-noteprogram" >> ~/.local/share/applications/the-simple-noteprogram.desktop

Uninstalling is a bit more complicated. We need to find the installed files and then remove them. __Remember that `/path/to/install-root` is the path to the `install-root` you downloaded, *not* to the directory you installed to!__

This is for system-wide installations. In the last step you'll probably get a lot of warnings from rmdir saying that the directory is not empty, that's normal.

    $ cd /path/to/install-root
    $ find -type f -exec rm ~/.local/{} \;
    $ find -type d -exec rmdir ~/.local/{} \;

Here are similar commands for user-wide installations:

    $ cd /path/to/install-root
    $ find -type f -exec rm /usr/local/{} \;
    $ find -type d -exec rmdir /usr/local/{} \;

#### Other operating systems

Move the install-root directory somewhere. You can also rename it if you want to. Then make a clickable link to the executable (for example, `the-simple-noteprogram.pyw` on Windows).
