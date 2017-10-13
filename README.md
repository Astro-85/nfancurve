# nfancurve
A small and lightweight bash script for using a custom fan curve in Linux for those with an Nvidia GPU.

You are probably wondering why I have chosen to write this script in Bash. The reason is very simple; I wanted a script with the minimum number of dependencies possible. To get this script up-and-running you _technically_ only need the **temp.sh** file. If you don't have a certain dependency (ie git or procps) you can just remove the code that uses them.

The current version of the script is **version 14.**

This script is currently set up for Celsius. However, it can easily be modified for other temperature scales.

If you need any help configuring my script or don't know how to make it start automatically check the **USAGE.md** file.

## Features
- by default it has an aggressive fan curve profile (lower temps, louder noise)
- uses `nvidia-settings` commands
- automatically enables/disables GPU fan control (but **not** `CoolBits`)
- easy to read code, with plentiful comments (beginner friendly)
- "intelligently" adjusts the time between tempurature readings
- very lightweight; see stats section for more info
- easy-to-use update script that uses `git`
- supports multiple GPU control

## Prerequisites
- _Bash_ version 4 and above, or a bash-like shell with the same syntax
- _NVIDIA GLX Driver_ version greater than 304
- _procps_ in version 14 and greater - you can comment out the function `check_already_running` if you don't have it
- Update script requires _git_ (it'll check for it when it's run)

## How to install
**GitHub**
- Download the .zip file straight from the GitHubs
- Extract it somewhere, and open a terminal to that directory
- Make sure `CoolBits` is enabled (see **USAGE.md**)
- Run `./temp.sh` for a foreground process, or `./update.sh` for a background* one

**git**
- Choose a folder you want to download/install the script in
- `git clone https://github.com/nan0s7/nfancurve`
- See instructions for **GitHub** for the rest

## Stats
- **v4** over 4.5h up-time: 0:03.88 CPU time
- **v7** around 5h: 0:03.22 CPU time
- **v10** around 5h: 0:02.42 CPU time

I ended up catching the command I use to get the current temperature in action and these are the stats: 0:00.06 CPU time. I will say this is quite inaccurate at this scale, and on other times I've caught the command I've seen the statistics vary by a small bit. My current CPU for measuring these stats is an i7 6700K @ 4.4GHz.

**TODO:**
- ~~make sure that "CoolBits" is enabled~~ - _not really the scope of this script_
- ~~possibly check the currently installed driver version~~ - _earlier versions used the  GPUCurrentFanSpeed command_
- add in a **really** detailed guide of how the script works
- add nouveau support (once they fix Pascal)
- allow single GPU's other than GPU 0 to be used
- add support for GPU's that have more than one controllable fan (ie >1 fan controller)

*or just execute this command: `nohup ./temp.sh >/dev/null 2>&1 &`
