# subShare - ShareX linux alternative.

[![PyPI version](https://badge.fury.io/py/subshare.svg)](https://badge.fury.io/py/subshare)

## Features:

- Quickly upload and share files, text documents, screenshots and shorten links.
- Configurable to use your own Nextcloud instance for uploads.
- Uploading file contents to Hastebin.
- Shortening links via Polr. (selfhosted/public)

## Examples:

> Sharing a file:  
![Alt text](/img/file.png?raw=true "Optional Title")  
https://s.atriox.io/vImLV # links are shortened via Polr :D  

> Sharing a text file:  
![Alt text](/img/text.png?raw=true "Optional Title")  
https://s.atriox.io/noVEi  

Skip down to usage for more example commands.

## Summary:

I made Subshare since I couldn't find a suitable linux alternative for ShareX, which I used on Windows to capture my screenshots, share text and files after it would upload them to the respective servies. Eg: Nextcloud/Hastebin. So I made something to fit my needs. If there are issues feel free to open up a issue and I'll try to get it fixed. Better yet write some come and help a brotha out? :D

## Installation:
Subshare is available on PyPi and can be installed with ```pip```

https://pypi.org/project/subshare/

```pip3 install --user subshare```

## Requirements
Linux: ```escrotum```
- Scrot displayed artifacts when using selection mode. Escrotum fixed this.

## Configuration
The default config file is created on the first run on ```subshare``` at ```~/.subshare.yaml``` and concaints the following.

```
DefaultFileUploader: nextcloud
DefaultImageUploader: nextcloud
DefaultUrlShortener: polr
screenshots:
  savedir: /home/user/screenshots/
  quality: 100
nextcloud:
  activated: true
  url: https://cloud.yourwebsite.com
  username: youruser
  password: supersecretpassword
  screenshot_directory: subshare/screenshots
  uploads_directory: subshare/share
polr:
  activated: true
  url: https://polr.yourwebsite.com
  apikey: 123127234982c34c2943c223c4
hastebin:
  url: https://paste.yourwebsite.com

```
Enter all your respective details and a true or false for if you want to use Polr to shorten the links or not.


## Usage
Note: All commands will automatically copy the link to your clipboard.

- Sharing screenshots:
```subshare screen``` captures a regular screenshot.
``` subshare screen select``` lets you drag out a selection.

- Sharing text:
```subshare text /path/to/file``` will post the contents of the file to Hastebin.

- Sharing files:
```subshare file /path/to/file``` upload the file to your nextcloud instance.

- Shortening links:
```subshare link "LINK TO SHORTEN"``` will shorten the link you specify. Dont forget the quotes around it.


## To-do:

[x] Make Polr optional.
[] Add alternative providers for uploading and sharing links...
[] idk it pretty much does what I wanted rn. Feel free to make a pull request or open up an issue if you'd like anything added and we'll see what we can do.
