# imgload
[![Build Status](https://travis-ci.org/frenos/imgload.svg?branch=master)](https://travis-ci.org/frenos/imgload)  [![Maintainability](https://api.codeclimate.com/v1/badges/d86a6992bc47e8e90d6f/maintainability)](https://codeclimate.com/github/frenos/imgload/maintainability)  [![Test Coverage](https://api.codeclimate.com/v1/badges/d86a6992bc47e8e90d6f/test_coverage)](https://codeclimate.com/github/frenos/imgload/test_coverage)  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/frenos/imgload.svg)  ![GitHub](https://img.shields.io/github/license/frenos/imgload.svg)
---
**imgload** is a python library to download images from several different hosters.
It's an ideal companion for writing web-crawlers, just feed the urls to imgload and get the raw bytes or a finished PIL 'Image' back.

---
## Supported Hosters:
Currently the following image hosters are supported.
* http://imgur.com/
* http://www.imagevenue.com/
* https://fastpic.ru/

Further planned hosts:
* http://www.imagebam.com/
* https://www.turboimagehost.com/

If you know other hosts that should be supported, create an Issue with a test file or send a pull request.
