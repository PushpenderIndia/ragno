<p align="center">
  <img src="https://github.com/PushpenderIndia/ragno/blob/master/img/ragno-logo.png" alt="Ragno Logo" />
</p>

<p align="center">
    <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.9-green.svg">
  </a>
  <a href="https://github.com/PushpenderIndia/ragno/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg">
  </a>
  <a href="https://github.com/PushpenderIndia/ragno/releases">
    <img src="https://img.shields.io/badge/Release-1.5-blue.svg">
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

## How To Use in Linux
```bash
# Installing using pip
$ pip3 install Ragno

# Checking Help Menu
$ ragno --help

# Run Normal (Fast) Crawl
$ ragno -d target.com 

# Run Normal (Fast) Crawl + Saving Result
$ ragno -d target.com -o result.txt

# Run Normal (Fast) Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ ragno -d target.com -o result.txt -q

# Run Deep Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ ragno -d target.com -o result.txt -q --deepcrawl
```

## How To Use in Windows
```bash
# Install dependencies 
$ Install latest python 3.x from Official Site (https://www.python.org/downloads/)

# Installing ragno using pip
$ pip install Ragno

# Checking Help Menu
$ ragno --help

# Run Normal (Fast) Crawl
$ ragno -d target.com 

# Run Normal (Fast) Crawl + Saving Result
$ ragno -d target.com -o result.txt

# Run Normal (Fast) Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ ragno -d target.com -o result.txt -q

# Run Deep Crawl + Saving Result + Quiet Mode (Without Showing URLs on screen)
$ ragno -d target.com -o result.txt -q --deepcrawl
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

### Example 1: One Liner for Hunting Open Redirect
- Install qsreplace:
```
sudo wget https://github.com/tomnomnom/qsreplace/releases/download/v0.0.3/qsreplace-linux-amd64-0.0.3.tgz && sudo tar zvfx qsreplace-linux-amd64-0.0.3.tgz && sudo rm qsreplace-linux-amd64-0.0.3.tgz && sudo mv qsreplace /usr/bin/ && sudo chmod +x /usr/bin/qsreplace
```

- Run One Liner
```
ragno -d testphp.vulnweb.com -q -o ragno_urls.txt && cat ragno_urls.txt | grep -a -i \=http | qsreplace "http://evil.com" | while read target_url do; do curl -s -L $target_url -I | grep "evil.com" && echo "[+] [Vulnerable] $target_url \n"; done
```

* You can Use GF Tool by Tomnonnom, to filter URLs with juice parameters, and then you can test them further.

## Contribute

* All Contributors are welcome, this repo needs contributors who will improve this tool to make it best.
