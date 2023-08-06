#!/usr/bin/env python
# _____  _              _       _____       _    _  _
#|   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
#|__   || ||     || . || || | ||__   || | || . || || ||     || -_|
#|_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|

import yaml
from getpass import getuser
from os import path
from subprocess import run


import click
import pyperclip

from haste import Post
from screen import screenShot
from shorten import Link
from upload import File

########## Config ##########
u = getuser()
configFile = "/home/" + u + "/.subshare.yaml"



"""
add in the ability to select screenshot quality
make nextcloud togglable
make nextcloud automatically add folders if they dont exist
add imgur as a upload target
"""


def createConfig():
    createConfig = {
        "DefaultFileUploader": "nextcloud",
        "DefaultImageUploader": "nextcloud",
        "DefaultUrlShortener": "polr",
        "screenshots": {
            "savedir": "/home/USERNAME/screenshots",
            "quality": 100,
        },
        "nextcloud": {
            "activated": True,
            "url": "https://cloud.yourdomain.com",
            "username": "admin",
            "password": "supersecretpassword",
            "screenshot_directory": "subshare/screenshots",
            "uploads_directory": "subshare/share",
        },
        "polr": {
            "activated": False,
            "url": "https://polr.yourdomain.com",
            "apikey": "123456789abcdefgh",
        },
        "hastebin": {
            "url": "https://hastebin.com",
        },
    }

    with open(configFile, "w") as f:
        yaml.dump(createConfig, f, default_flow_style=False, sort_keys=False)


if not path.isfile(configFile):
    createConfig()
    print("Config file created at: ~/.subshare.yaml")

else:
    with open(configFile, 'r', encoding="utf8") as f:
        config = yaml.load(f)

    userNextcloud = config["nextcloud"]["activated"]
    nextcloud_url = config["nextcloud"]["url"]
    nextcloud_uploads_directory = config["nextcloud"]["uploads_directory"]
    nextcloud_screenshots_directory = config["nextcloud"]["screenshot_directory"]
    nextcloud_username = config["nextcloud"]["username"]
    nextcloud_password = config["nextcloud"]["password"]
    use_polr = config["polr"]["activated"]
    polr_url = config["polr"]["url"]
    polr_api_key = config["polr"]["apikey"]
    hastebin_url = config["hastebin"]["url"]
    screenshot_save_dir = config["screenshots"]["savedir"]
    screenshot_qualirt = config["screenshots"]["quality"]


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


#####################################
#              Files                #
#####################################
@main.command(help="Uploads a file to Nextcloud.")
@click.argument("file_to_upload")
def file(file_to_upload):
    if use_polr is True:
        pyperclip.copy(Link(File(file_to_upload, nextcloud_username, nextcloud_password,
                                 nextcloud_url, nextcloud_uploads_directory), polr_url, polr_api_key))
        click.echo("File uploaded to NextCloud\n" + pyperclip.paste())
    else:
        pyperclip.copy(File(file_to_upload, nextcloud_username,
                            nextcloud_password, nextcloud_url, nextcloud_uploads_directory))
        click.echo("File uploaded to NextCloud\n" + pyperclip.paste())


#####################################
#           Screenshots             #
#####################################
@main.command(help="Takes a screenshot: Use 'select' for selection mode.")
@click.argument("mode", required=False, default="selection")
def screen(mode):
    if mode is "select":
        if use_polr is True:
            pyperclip.copy(Link(File(screenShot(mode, screenshot_save_dir), nextcloud_username,
                                     nextcloud_password, nextcloud_url, nextcloud_uploads_directory) + "/preview", polr_url, polr_api_key))
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot region captured: Copied to clipboard\n" + pyperclip.paste())
        else:
            pyperclip.copy(File(screenShot(mode, screenshot_save_dir), nextcloud_username,
                                nextcloud_password, nextcloud_url, nextcloud_uploads_directory) + "/preview")
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot region captured: Copied to clipboard\n" + pyperclip.paste())
    else:
        if use_polr is True:
            pyperclip.copy(Link(File(screenShot(mode, screenshot_save_dir), nextcloud_username,
                                     nextcloud_password, nextcloud_url, nextcloud_uploads_directory) + "/preview", polr_url, polr_api_key))
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot captured: Copied to clipboard\n" + pyperclip.paste())
        else:
            pyperclip.copy(File(screenShot(mode, screenshot_save_dir), nextcloud_username,
                                nextcloud_password, nextcloud_url, nextcloud_uploads_directory) + "/preview")
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot captured: Copied to clipboard\n" + pyperclip.paste())


#####################################
#              Text                 #
#####################################
@main.command(help="Posts contents of file to Hastebin")
@click.argument("text_file_to_upload")
def text(text_file_to_upload):
    if use_polr is True:
        pyperclip.copy(Link(Post(text_file_to_upload, hastebin_url), polr_url, polr_api_key))
        click.echo("Text uploaded to hastebin\n" + pyperclip.paste())
    else:
        pyperclip.copy(Post(text_file_to_upload, hastebin_url))
        click.echo("Text uploaded to hastebin\n" + pyperclip.paste())


#####################################
#              Links                #
#####################################
@main.command(help="Shotens link via Polr.")
@click.argument("link_to_shorten")
def link(link_to_shorten):
    if use_polr is True:
        pyperclip.copy(Link(link_to_shorten, polr_url, polr_api_key))
        click.echo("Link shortened\n" + pyperclip.paste())
    else:
        click.echo("Enable Polr from ~/.subshare.json to use Link Shortening")


if __name__ == '__main__':
    main()
