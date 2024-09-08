nfancurve
---------
## Features
- comes with a more aggressive fan curve than the nvidia default (lower temps, louder noise)
- uses `nvidia-settings` commands
- automatically enables/disables GPU fan control (but **not** `CoolBits`)
- very lightweight
- multiple GPU control with individual fan controller support
- makes use of a config file with explanations for each setting
- POSIX compliant

## Prerequisites
- a POSIX compliant shell; tested with recent versions of `bash` and `dash`
- `nvidia glx driver` version greater than 304
- `nvidia-settings` for controlling the GPU(s)
- `coreutils`
- `procps` - you can comment out the function `check_already_running` if you don't have it

## How to install
### GitHub
- Download the .zip file straight from the GitHubs
- Extract it somewhere, and open a terminal to that directory
- Make sure `CoolBits` is enabled (see [USAGE.md](USAGE.md))
- Run `sh temp.sh` (or any compatable shell) or `./temp.sh` for a foreground process. Run with the option `-D` (case sensitive) for a background process (i.e. `./temp.sh -D`). Note that using `sh` or `./` will automatically use your default shell.

### git
- Choose a folder you want to download/install the script in
- `git clone https://github.com/nan0s7/nfancurve`
- Follow the last two steps under the **GitHub** guide area

## Using the systemd service
Ensure the script and the config paths are correct.
Move or copy the nfancurve.service file to /etc/systemd/user/nfancurve.service then enable and start the service with:

    systemctl --user daemon-reload
    systemctl --user start nfancurve.service
    systemctl --user enable nfancurve.service

### Troubleshooting
On some Distro's which are further behind in updates, or if there's a slight misconfiguration with services, you may encounter issues with the service file.

To work around this, you may change the following lines in the `nfancurve.service` file:
1. Change `After=graphical-session.target` to `After=default.target`
2. Remove the line `Requires=graphical-session.target`
3. Change `WantedBy=graphical-session.target` to `WantedBy=default.target`
4. Under the `[Service]` heading, add the line `ExecStartPre=/bin/sleep 20`

Don't forget to reload and reenable the service:

    systemctl --user daemon-reload
    systemctl reenable --user nfancurve.service

### Using the python script
On headless servers or Wayland systems, it might be easier to use @AlexKordic's python script. Use an enviroment with pynvml installed to run `nfancurve.py`. This can also be automated with systemd.
