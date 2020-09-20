<p align="center">
  <img src="https://github.com/PushpenderIndia/ragno/blob/master/img/ragno-logo.png" alt="Ragno Logo" />
</p>

<p align="center">
    <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.7-green.svg">
  </a>
  <a href="https://github.com/PushpenderIndia/ragno/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg">
  </a>
  <a href="https://github.com/PushpenderIndia/ragno/releases">
    <img src="https://img.shields.io/badge/Release-1.0-blue.svg">
  </a>
    <a href="https://github.com/PushpenderIndia/ragno">
    <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-brightgreen.svg">
  </a>
</p>

**Ragno** is a **Passive URL Crawler** | Written in **Python3** | Fetches URLs from the **Wayback Machine**, **AlienVault's Open Threat Exchange** & **Common Crawl**

## Disclaimer
<p align="center">
  :computer: This project was created only for good purposes and personal use.
</p>

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.

## Features
- [x] Works on Windows/Linux/MacOS
- [x] Passive Crawler (Does not intract with target directly)
- [x] Crawl URLs from 3 Sources i.e.

| Crawl URLs from |
| --------------- |
| Wayback Machine |
| Common Crawl    |
| AlienVault's OTX (Open Threat Exchange) |

- [x] DeepCrawl Feature (If Enabled, then Ragno try to fetch URLs from all **74+ CommonCrawl APIs**)
- [x] MultiThreading (Only Used When **DeepCrawl** Feature is Enabled)
- [x] Result of **Subdomains** could be excluded & included via CommandLine Argument (i.e. **-s**)
- [x] Save Result in TXT File
- [x] Quiet Mode

## Prerequisite
- [x] Python 3.X
- [x] Few External Modules

## How To Use in Linux
```bash
# Navigate to the /opt directory (optional)
$ cd /opt/

# Clone this repository
$ git clone https://github.com/PushpenderIndia/ragno.git

# Navigate to ragno folder
$ cd ragno

# Installing dependencies
$ apt-get update && apt-get install python3-pip
$ pip3 install numpy requests

# Giving Executable Permission
$ chmod +x ragno.py

# Checking Help Menu
$ python3 ragno.py --help

# Run Normal (Fast) Crawl
$ python3 ragno.py -d target.com 

# Run Normal (Fast) Crawl + Saving Result
$ python3 ragno.py -d target.com -o result.txt

# Run Normal (Fast) Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ python3 ragno.py -d target.com -o result.txt -q

# Run Deep Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ python3 ragno.py -d target.com -o result.txt -q --deepcrawl
```

## How To Use in Windows
```bash
# Install dependencies 
$ Install latest python 3.x from Official Site (https://www.python.org/downloads/)

# Clone this repository or Download Zip File
$ git clone https://github.com/PushpenderIndia/ragno.git

# Navigate to ragno folder
$ cd ragno

# Installing dependencies
$ python -m pip install numpy requests

# Checking Help Menu
$ python ragno.py --help

# Run Normal (Fast) Crawl
$ python ragno.py -d target.com 

# Run Normal (Fast) Crawl + Saving Result
$ python ragno.py -d target.com -o result.txt

# Run Normal (Fast) Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ python ragno.py -d target.com -o result.txt -q

# Run Deep Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ python ragno.py -d target.com -o result.txt -q --deepcrawl
```

## Available Arguments 
* Optional Arguments

| Short Hand  | Full Hand       | Description                     |
| ----------  | ---------       | -----------                     |
| -h          | --help          | show this help message and exit |
| -o OUTPUT   | --output OUTPUT | Save Result in TXT file         |
| -s          | --subs          | Include Result of Subdomains    |
| -q          | --quiet         | Run Scan Without printing URLs on screen |
|             | --deepcrawl     | Uses All Available APIs of CommonCrawl for Crawling URLs [Takes Time] |
| -t THREAD   | --thread THREAD | Number of Threads to Used. Default=50 [Use When deepcrawl is Enabled] |

* Required Arguments

| Short Hand  | Full Hand | Description |
| ----------  | --------- | ----------- |
| -d DOMAIN   | --domain DOMAIN | Target Domain Name, ex:- google.com |

## Use Cases

> After Finding URLs, you can filter them on the basics of your attack & can Mass Hunt Particular vulnerabilites such as XSS, LFI, Open redirect, SSRF, etc

* Example: One Liner for Hunting Mass Open Redirect
```
$ python3 ragno.py -d test.vulnweb.com -q -o test.vulnweb.txt | grep -a -i \=http | qsreplace "http://evil.com" | while read target_url do; do curl -s -L $target_url -I | grep "evil.com" && echo "[+] [Vulnerable] $target_url\n"; done
```

* You can Use GF Tool by Tomnonnom, to filter URLs with juice parameters, and then you can test them further.

## Contribute

* All Contributors are welcome, this repo needs contributors who will improve this tool to make it best.

## Contact

singhpushpender250@gmail.com 

## Buy Me A Coffee

* Support my Open Source projects by making Donation, It really motivates me to work on more projects
* PayPal Email: `shrisatender@gmail.com` [**Please Don't Send Emails to This Address**]

## More Features Coming Soon...
