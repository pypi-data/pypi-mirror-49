#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ytu` package."""
import ytu


def test_video_id():
    # All these URLs occurred in the reddit submission corpus.
    tests = [
        ('http://youtu.be/zoLVUxKCWhY', 'zoLVUxKCWhY'),
        ('http://www.youtube.com/watch?v=VvRC0wxM-yM', 'VvRC0wxM-yM'),
        ('http://www.youtube.com/watch?v=thsc60UTUIE&amp;feature=youtu.be', 'thsc60UTUIE'),
        ('http://www.youtube.com/watch?v=a3asbkY0tTE?', 'a3asbkY0tTE'),
        ('http://www.youtube.com/watch?v=oHg5SJYRHA0???', 'oHg5SJYRHA0'),
        ('http://www.youtube.com/watch?v=55jUNNPT1eMads/4/NaQOUKyR9CY', '55jUNNPT1eM'),
        ('https://www.youtube.com/verify_age?next_url=http%3A//www.youtube.com/watch%3Fv%3DGqj1N9qeWXI%26feature%3Dmfu_in_order%26list%3DUL', 'Gqj1N9qeWXI'),
        ('https://www.youtube.com//watch?v=PQGrIsYUm4c', 'PQGrIsYUm4c'),  # 2 leading slashes in path
        ('https://www.youtube.com/v/j4FNGsNY3nI&amp;amp;rel=0&amp;amp;egm=0&amp;amp;showinfo=0&amp;amp;fs=1', 'j4FNGsNY3nI'),
        ('https://www.youtube.com/embed/mGnyH-SCZpM?autoplay=1&amp;hd=1&amp;KeepThis=true&amp;TB_iframe=true&amp;height=370&amp;width=640?autoplay=1&amp;hd=1', 'mGnyH-SCZpM'),
        ('https://www.youtube.com/verify_age?&amp;next_url=/watch%3Fv%3DsTPsFIsxM3w', 'sTPsFIsxM3w'),
        ('https://www.youtube.com/attribution_link?a=qbb_5VvcvY8&amp;u=%2Fwatch%3Fv%3DFgFeVlw2Ywg%26feature%3Dshare', 'FgFeVlw2Ywg'),
        ('https://www.youtube.com/attribution_link?a=ar77oUQIEOcNs-Wdao4XJw&amp;u=%2Fwatch%3Fv%3D0eXS1NI6Q6Y%26feature%3Dshare', '0eXS1NI6Q6Y'),
        ('https://www.youtube.com/?v=_RSaYVgd7yk', None),
        ('https://www.youtube.com/watch?v=U3M8pXZusQ', None)
    ]

    for t in tests:
        assert ytu.video_id(t[0]) == t[1]