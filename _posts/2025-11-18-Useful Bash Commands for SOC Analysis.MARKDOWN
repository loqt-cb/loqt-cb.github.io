---
title: Helpful Bash Commands for SOC Analysis
date: 2025-11-18 10:19:20 +/-0000
categories: [Education, Tutorials]
tags: [linux, bash, networking, network analysis]
author: cblake
description: Some basic Linux commands that would be helpful for (nearly) any SOC Analysis.
comments: false
image:
  path: /assets/img/bashsoccmds/logo.png
  alt: Tux showing us some important information!

---
# test
Linux has numerous commands that make it the best operating system for anyone in Cybersecurity. These commands have various purposes and functions, but are all ultimately important to learn in order to save time on simple tasks as opposed to manually performing these functions yourself.

<h2> File Searching and Analysis </h2>
<strong>grep</strong> - To start, grep is one of the most frequently used commands in Linux. Grep can search for certain strings to appear in either a file or another command's output. A fundamental way to explain its purpose is to get only what you need out of a file.
`grep <filename> <pattern>`  or `cat <filename> | grep <pattern>`

<strong>strings</strong> - A command that finds strings from binary files, and outputs them. Very helpful to find items that are human-readable, whether they were left that way intentionally or not.
`strings <filename>`

<strong>find</strong> - A very efficient command for finding the location of a file, especially if you know a couple of attributes about that file. It also has the option to execute a command after finding said file. Try combining it with `-exec cat {} +` at the end for it to output any file it finds!

Example use for finding a file with the name of "script". (`/` means root directory, `2>/dev/null` makes output cleaner by not outputting any "Permission Denied Messages"):
`find / -type f -name script 2>dev/null`

<strong>md5sum/sha256sum</strong> - Commands that calculates the hashes of any sort of file or string that you give it. Useful for verifying file integrity, but also file identification, which is very helpful for malware analysis.
`md5sum <filename>` or `echo "something" | sha256sum`

<strong>base64</strong> - The `base64` command can be used for encoding and decoding various things such as commands, payloads, and information. Being able to detect base64 is crucial for anyone in Cybersecurity, and to decode it in one command is very beneficial.
`echo "hello world" | base64` and `echo "aGVsbG8gd29ybGQK" | base64 -d`

<h2>Network Information</h2>
<strong>ip</strong> - The most well known network related command in Bash. Has various functions, such as assigning or removing IP addresses, viewing ip addresses, enabling/disabling interfaces, and more. An important command to become knowledgeable of for it's adaptability. `ip a`, `ip link set eth0 up`

<strong>tcpdump</strong> - A widely used packet capturing tool. It has versatility for whatever kind of traffic you're looking to capture on your network. In addition to this, it's very lightweight, and not overly complicated.

<strong>ping</strong> - The essential command for testing and analyzing your device's network connection. It provides feedback of your connection by sending ICMP packets to a specified address or domain. Incredibly simple and straightforward. `ping <ip address>`

<strong>traceroute</strong> - Similar to ping, however it shows the user the path that packets take from the computer it's sent off of towards it's destination. A great way to diagnose network problems but also could be used to identify Man in the Middle Attacks. `traceroute <domain name>`

<h2>Other helpful commands</h2>
<strong>tr</strong> - This command stands for translate, which takes any string and can replace or delete characters based on the parameters you set. Has various purposes and capabilities for any investigation or analysis

<strong>wc</strong> - Counts certain patterns in text, such as bytes, characters, lines, and words. This can be useful for various purposes and is often needed under uncommon conditions. Normal usage will print out the lines, words, and character counts `echo "hello world " | wc`

<strong>#/dev/null</strong> - This is for redirecting output, which is great for when you do not receive the output you want, or want to make it more clean. There are 3 values you can insert for this:
* 0 - Ignores STDIN, which means any input that is normally read from STDIN is discarded
* 1 - Removes STDOUT, which discards any normal messages
* 2 - Removes STDERR, removing any error messages from the output.
All of which have various uses, however most commonly you'd use `2>/dev/null` .
