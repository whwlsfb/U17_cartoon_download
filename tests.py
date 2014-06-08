#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import nose


def test_download():
    from u17_cartoon_download import download_url
    cartoon_url = 'http://www.u17.com/comic/5553.html'
    download_url(cartoon_url, 1)
    assert os.path.exists('Cartoon/')

if __name__ == '__main__':
    nose.runmodule()
