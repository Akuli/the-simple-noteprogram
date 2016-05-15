# the-simple-noteprogram
This is a simple note-taking program written in Python 3 with GTK+ 3 aimed at GNU/Linux users. It will display a note icon in the system tray. The tray icon can be clicked and new notes can be added. The notes are always saved automatically.

### Windows and OSX support
This application was designed for GNU/Linux users. I haven't made a Windows installer (yet) so following these instructions for installing the Windows dependencies will result in many useless programs. I've included Windows instructions anyway just because it's possible to run this program in Windows.

OSX is not supported in these instructions. I don't have a mac so i can't test my program on one. However, installing the dependencies and running this program without installing should work the same way it does for Windows.

### Downloading and dependencies
Downloading this application is easy. Just go to the top right of this page and click the "Download zip" option. Then extract the `local` folder from the zip.

These dependencies are needed to run this program:
| Name | Debian/Ubuntu package | Windows download |
| - | - | - |
| Python 3.2 or newer | `python3` (installed by default) | [python.org/downloads](https://www.python.org/downloads/)
| Appdirs for Python 3 | `python3-appdirs` | `py -m pip install appdirs` __[\*]__ |
| PyGI for Python 3 | `python3-gi` | [sourceforge.net/projects/pygobjectwin32](https://sourceforge.net/projects/pygobjectwin32/) |
| GTK+ 3 for GI | `gir1.2-gtk-3.0` | Same as for PyGI, make sure it installs GTK+ 3 |
| Appindicator 3 for GI | `gir1.2-appindicator3-0.1` | Same as for PyGI, make sure it installs AppIndicator 3 |

__[\*]__ *Install Python first, then right-click command prompt in Start menu or Start screen, open it as administrator, type the command there and press Enter.*

#### Running without installing
This is easy after downloading the `local` directory. On Windows, open the `local` directory, rename `the-simple-noteprogram` to `the-simple-noteprogram.pyw` and double-click it to run. On GNU/Linux, run these commands on a terminal window:
```
cd /path/to/local
chmod +x bin/the-simple-noteprogram
bin/the-simple-noteprogram
```

#### Installing on GNU/Linux and GNU/Linux-like operating systems
The `local` directory's content is meant to be installed into a directory somewhere on your computer. Typical locations for it are `~/.local` for a user-wide install (where `~` is the user's home directory), `/usr/local` for a system-wide install and `/usr` for creating a distribution package, such as a Debian package or an .rpm package. The program should appear in the desktop environment's menu after installation. In the example commands, replace `/path/to/local` with a path to the `local` folder you extracted, __not with the directory you installed to__.

One way to install the content of a directory is with `rsync`. For example, a user-wide installation can be done like this:
```
cd /path/to/local
rsync -r * ~/.local
```

After the installation the program should appear in your desktop environment's menu. It usually doesn't work on user-wide installations, so you need to edit its `.desktop` file:
```
echo "Exec=$HOME/.local/bin/the-simple-noteprogram" >> ~/.local/share/applications/the-simple-noteprogram.desktop
```

Uninstalling is a bit more complicated. We need to first list the installed files, then remove them. Again, this is for user-wide installations.
```
for file in $(find -type f)
do rm "$HOME/.local$i"
done
```
