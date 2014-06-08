#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import nose


def test_download():
    from u17_cartoon_download import main
    cartoon_url = 'http://www.u17.com/comic/70378.html'
    main(cartoon_url, 1)
    assert os.path.exists('Cartoon/')

if __name__ == '__main__':
    nose.runmodule()
