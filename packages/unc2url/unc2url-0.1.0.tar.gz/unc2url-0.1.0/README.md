# UNC2URL

A UNC to URL Converter.

[![Build Status](https://github.com/alexanderwillner/unc2url/workflows/Build-Test/badge.svg)](https://github.com/alexanderwillner/unc2url/actions)
[![Coverage Status](https://codecov.io/gh/alexanderwillner/unc2url/branch/master/graph/badge.svg?token=dJbdYWeg7d)](https://codecov.io/gh/alexanderwillner/unc2url)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/quality/g/alexanderwillner/unc2url)](https://scrutinizer-ci.com/g/alexanderwillner/unc2url/?branch=master)
[![GitHub Issues](https://img.shields.io/github/issues/alexanderwillner/unc2url)](https://github.com/alexanderwillner/unc2url/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub Release](https://img.shields.io/github/v/release/alexanderwillner/unc2url?sort=semver)](https://github.com/alexanderwillner/unc2url/releases)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/unc2url?label=pypi%20downloads)](https://pypi.org/project/unc2url/)
[![GitHub Download Count](https://img.shields.io/github/downloads/alexanderwillner/unc2url/total.svg)](https://github.com/alexanderwillner/unc2url/releases)

## Table of Contents

- [Install](#install)
- [Examples](#examples)
- [Screenshots](#screenshots)

## Install

```sh
$ pip3 install unc2url
# or
$ git clone https://github.com/alexanderwillner/unc2url && cd unc2url && make install
```

## Examples

```shell
% unc2url '\\example.org\foo\bar'
smb://example.org/foo/bar

% unc2url --file '\\example.org\foo\bar'
file://example.org/foo/bar

% unc2url --reverse 'file://example.org/foo/bar' 
\\example.org\foo\bar

% unc2url -h
usage: unc2url.py [-h] [-r] [-f] [--version] unc

Simple UNC to URL tool.

positional arguments:
  unc            An Uniform Naming Convention (UNC) link

optional arguments:
  -h, --help     show this help message and exit
  -r, --reverse  Reverse the conversation (url2unc)
  -f, --file     File URL (file://)
  --version, -v  show program's version number and exit
```

## Alfred Workflow

To activate this workflow use the default keyword ```unc2url``` and enter the UNC you want to get translated. You can also press ⌘+⇧+U to translate what is in your clipboard. Pressing Enter will copy the translations to the clipboard. Pressing ⇧+Enter will open the SMB link.

![Alfred](resources/alfred.png)