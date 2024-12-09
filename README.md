# YkxRecon

![Screenshot from 2024-12-09 21-40-05](https://github.com/user-attachments/assets/9f7e0f5c-60b6-4952-abb9-997171b28beb)

Take list of domains to find subdomains for

## Table of content 

[instalation](#instalation)


[basic usage](#usage)


[options](#options)

## Instalation

```bash
git clone https://github.com/Ykxx999/YkxRecon.git
cd YkxRecon/YkxRecon
chmod +x ykxrecon
```
## Basic Usage

```bash
./ykxrecon.py -d glassdoor.com tiktok.com hackerone.com --stdout
```

## options

```bash
-h, --help            show this help message and exit
  -d DOMAINS [DOMAINS ...], --domains DOMAINS [DOMAINS ...]
                        List of domains to add. Separate multiple domains with spaces.
  -f FILE, --file FILE  Path to a file containing domains (one per line).
  -v, --version         Display the script version and exit.
  --stdout              Display the subdomain enumeration result directly in the terminal.
```
