---
title: Installing Eric Zimmerman's CLI Tools On Linux
date: 2026-11-11 01:00:01 +/-0000
categories: [Education, Write Ups]
tags: [bash, linux, incident response, digital forensics, dotnet]
author: cblake
description: A demonstration on how to install and use Eric Zimmerman's CLI tools on Linux
comments: false
image:
  path: /assets/img/zimmermantools/logo.png
  alt: The logo for Eric Zimmerman's tools with the addition of a tux.

---


# Overview
Eric Zimmerman's tools are an essential addition for your DFIR toolbox. These tools support analysis for a vast range of Windows artifacts. These tools include MFTECmd for MFT files; LECmd for lnk files; EvtxECmd for Windows event log files, and more. You may already be familiar with these tools. Thanks to being open-source, they have grown to be very popular amongst digital forensic capture the flag communities.

There is one issue that Linux users may face if they decide to use these tools; they are *developed with .NET*, therefore *they are designed for Windows systems*. Thankfully, there is a work-around for Linux machines that will be demonstrated to you in this post.

# Walkthrough

## Installing .NET

Let's begin by installing the framework that was used to develop these tools, .NET.

There are two versions of .NET that Eric supports his tools with: .NET 4 and .NET 10. Before deciding on which version to install, Eric supports <u>all</u> of his tools with <u>.NET 10</u>, whilst .NET 4 is only supported by 14 of the tools.

That being said, for this walkthrough, we will move forward with installing **.NET 10**.

### Ensure your package manager is up to date first:

#### Debian, Ubuntu
```
sudo apt update && sudo apt upgrade
```

#### Arch
```
sudo pacman -Syu
```

#### Fedora
```
sudo dnf upgrade --refresh
```

### Afterwards, install the .NET 10 SDK package:

#### Ubuntu
```
sudo apt install -y dotnet-sdk-10.0
```

#### Debian
```
sudo apt-get install -y dotnet-sdk-10.0
```

#### Arch
```
sudo pacman -Syu dotnet-sdk
```

#### Fedora
```
sudo dnf install dotnet-sdk-10.0
```

## Downloading and installing the tool
Once we have installed the proper version of .NET, we can start downloading tools.

Navigate to [https://ericzimmerman.github.io/#forensic-tools](https://ericzimmerman.github.io/#forensic-tools) and download the tool that you want; **ensure that the version matches your .NET runtime's version!**

You choose the directory to store the tool in, however, I recommend storing it in **/opt/** as it is designed for storing add-on application packages.

You can follow this one liner template:
```
sudo mkdir <location>/<name> && sudo mv ~/Downloads/<tool.zip> <new dir> && sudo unzip <new dir>/<tool.zip>
```

To put it in practice, here is how it would be used to install `JLECmd`:

```
sudo mkdir /opt/JLECmd && sudo mv ~/Downloads/JLECmd.zip /opt/JLECmd/JLECmd.zip && sudo unzip /opt/JLECmd/JLECmd.zip -d /opt/JLECmd
```

You could follow this example by swapping `JLECmd` with the name of the tool you are installing!


Now that the tool is extracted, and placed in an appropriate directory, we can use it. To use these .NET tools, we will execute the runtime with the tool's `.dll` file.

```
dotnet <directory>/<tool.dll>
```

**JLECmd example:**

```
dotnet /opt/JLECmd/JLECmd.dll
```

## Creating an alias

Typing `dotnet` followed by the tool's directory will add additional mental-work during your analysis. Bear in mind, these tools use **many** parameters (files, output directories, output files, etc). Shortening our command will make our investigation more precise.

We can append an alias for our dotnet command to perform this concision!
```
echo 'alias <toolname>="dotnet <directory>/<tool.dll>"' >> ~/.bash_aliases
```

**JLECmd example:**
```
echo 'alias jlecmd="dotnet /opt/JLECmd/JLECmd.dll"' >> ~/.bash_aliases
```
Running this command will append a new alias to your aliases file.

Then we must source our newly modified aliases file:
```
source ~/.bash_aliases
```

Now we can simply execute the tool's name in our terminal to run it!

# Conclusion

This post went over how to install a .NET runtime for your Linux machine, the proper steps for downloading and storing Zimmerman CLI tools, and lastly, creating an alias for accessibility. Have fun with your investigations!
