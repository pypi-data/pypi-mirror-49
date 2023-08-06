<h3 align="center"><img src="https://i.imgur.com/Tyi3Bq5.png" width="200px"></h3>
<p align="center">Tag your anime photos effortlessly</p>

<p align="center">
<a href="https://github.com/mananapr/akari/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
<a href="https://github.com/mananapr/akari/releases"><img src="https://img.shields.io/github/release/mananapr/akari/all.svg"></a>
<a href="https://pypi.python.org/pypi/akari/"><img src="https://img.shields.io/pypi/v/akari.svg"></a>
</p>

akari is a work in progress python program to manage anime artwork. currently it uses [iqdb](https://iqdb.org) to reverse-search images and fetch appropriate tags.

<p align="center">
<img src="https://i.imgur.com/AP4JLSt.png" alt="img" width="600px">
</p>

## Requirements
 - requests
 - BeautifulSoup 4
 - PyQt5

## Installation
For user installation, simply run:

    pip3 install --user akari
    
Then add `$HOME/.local/bin` to your `$PATH`:

    echo PATH=\"\$PATH:\$HOME/.local/bin\" >> $HOME/.bashrc
    source $HOME/.bashrc

Alternatively, you can do a system wide installation:

    sudo pip3 install akari

## Usage
    usage: akari [-h] [-s /path/to/dir] [-g]

    optional arguments:
      -h, --help            show this help message and exit
      -s /path/to/dir, --scan /path/to/dir
                            Scan directory for new images
      -g, --gui             Start the GUI
      -v, --version         Displays the version

[TODO](https://github.com/mananapr/akari/issues/1)
