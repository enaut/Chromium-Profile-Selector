This script launches a dialog to select a profile before launching chrome/chromium with the selected profile.

This script is in its early stages so it might break stuff. So please use with care ;). I'm not responsible for the damage you do with it!

usage:
    Launch the script, select a Profile or create a new one and hit execute.

relevant paths:

    * location of the profiles: ~/.config/ChromiumProfiles
        Note: that this is not really the same as ~/.config/chromium since this directory already is the profile.
              If you want to use this profile with the profile selector add a link to it from the ChromiumProfiles directory.
              On my system this looks like:
                $cd ~/.config/ChromiumProfiles
                $ln ../chromium OldChromiumProfile

    * Ausführbare Datei: /usr/bin/chromium-browser
        Ajust this if you use chrome.

License:
    This is free software, you can redistribute or modify it under the terms of the GNU General Public License Version 2 or any later Version (see http://www.gnu.org/copyleft/gpl.html for details). 

Please feel free to contact me (name: enaut.w host: googlemail.com).
