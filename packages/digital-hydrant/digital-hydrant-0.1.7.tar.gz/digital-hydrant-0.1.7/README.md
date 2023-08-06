<a href="http://outsideopen.com"><img src="https://www.zinkwazi.com/wp-content/uploads/2015/04/a2014-05-11-16.29.43-2.jpg" title="Outside Open" alt="Outside Open"></a>

# Digital Hydrant Collectors

> Open Source network information collector, developed for the Digital Hydrant project

## Installation

### System Requirements

- Python >= 3.6
- [arp-scan](https://github.com/royhills/arp-scan)
- [dhcpcd](https://wiki.archlinux.org/index.php/Dhcpcd)
- [iw](https://wireless.wiki.kernel.org/en/users/documentation/iw)
- [lldpd](https://lldpd.github.io/lldpd/installation.html)
- [net-tools](https://wiki.linuxfoundation.org/networking/net-tools)
- [nmap](https://nmap.org/)
- [hydra](https://github.com/vanhauser-thc/thc-hydra)
- [tshark](https://www.wireshark.org/docs/man-pages/tshark.html)
- [wpasupplicant](https://wiki.archlinux.org/index.php/wpa_supplicant)
- [yersinia](https://github.com/tomac/yersinia)

### Install with Pip

```bash
$ sudo pip install digital-hydrant
```

### Install from source

Clone this repository

```shell
$ git clone https://github.com/outsideopen/digital-hydrant-collectors.git
$ cd ~/digital-hydrant-collectors
$ sudo ./setup.py install
```

## Usage

### Configuration

- Create a new Hydrant on the Digital Hydrant [website](https://app.digitalhydrant.com/hydrants)
- Run the hydrant init script with your api token
  - \*You should delete this command from `.bash_history` as it poses a potential security risk
    - If you have `$HISTCONTROL` set to "ignorespace" or "ignoreboth" then you can add a space before running the command
    - OR you can execute the command with your token and then run `history -d $((HISTCMD-2))` to delete the command from your history

```shell
$ sudo hydrant --init <MY_TOKEN>
```

- OR manually copy the api token to your configuration file at `/etc/digital-hydrant/config.ini`
  - \*If your config file does not yet exist you can run `sudo hydrant --init` to initialize the default config file

```
[api]
token = $MY_TOKEN
```

### Run it

```shell
$ sudo hydrant
```

### Options

```
usage: hydrant [-h] [--init [TOKEN]] [--systemd [LOCATION]] [-c] [-u] [-cq] [-v] [-f]

Run Digital-Hydrant data collectors

optional arguments:
  -h, --help            show this help message and exit
  --init [TOKEN]        setup local config file and database. optionally accepts a hydrant's api token
  --systemd [LOCATION]  move the digital-hydrant service file to it's system location (defaults to
                        /usr/lib/systemd/system/)
  -c, --collect         dictates that data collection should be run
  -u, --upload          dictates that stored data should be uploaded
  -cq, --clear-queue    delete all entries from local database
  -v, --version         show program's version number and exit
  -f, --force           runs Digital Hydrant without checking for system dependencies(this may cause
                        errors)

By default, both collection and upload will execute unless otherwise specified
```

### DH_cron

###### In order to schedule collector execution, Digital Hydrant uses a cron-like string with the following structure

- \<day of week(1-7)> \<days> \<hours> \<minutes> \<seconds>
- whichever value is populated first will be read as "every \<value> \<interval>" and the remaining values will be combined and read as "at \<values>"
  - examples:
    - \* 4 18 30 0 = "every 4 days at 18:30:00"
    - 5 \* \* 30 45 = "every thursday at 0:30:45"
- day of the week values start on Sunday (i.e. 1 = Sun... 7 = Sat)
- for DH_cron strings with the day of the week populated, the days value will be ignored
- if no schedule string is provided then the default value of \* \* \* \* \* will be used, indicating that the process should only be run once

---

## Features

- Easily add new collectors
- Build off existing network scanning tools
- Integrated logging
- Very flexible and configurable

## Contributing

### Step 1

- **Option 1**

  - 🍴 Fork this repo!

- **Option 2**
  - 👯 Clone this repo to your local machine using `https://github.com/outsideopen/digital-hydrant-collectors`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull [request](https://github.com/outsideopen/digital-hydrant-collectors/compare)

---

## FAQ

- What is Outside Open?
  - Outside Open is a team of smart, passionate artists, photographers, cyclists, hikers, soccer players, parents, beekeepers, blacksmiths and tinkerers. What unites this disparate team is a love for building and integrating amazing technology to help their clients succeed. They think outside the “singular technical solution” box. They embrace solutions from both the standard corporate software/hardware world and the open source community. This sets them apart and enables them to provide highly customized and scaleable solutions. Outside Open was founded in 2012 by Trevor Young and Greg Lawler, two technology leaders with a love for technology and a desire to help others succeed.

---

## Support

Reach out at one of the following places!

- Website at <a href="http://outsideopen.com" target="_blank">`outsideopen.com`</a>
- Email: <developers@outsideopen.com>

---
