# -*- coding: utf-8 -*-
from urllib.parse import parse_qs, urlparse, unquote


def get_param_value(purl, name):
    """Get the first value of the given URL parameter from a urllib.parse.ParseResult object.

    Values in dictionary returned by parse_qs are lists."""
    if purl.query:
        return parse_qs(purl.query).get(name, [None]).pop()


def video_id(url, recursion_depth=0, max_recursion_depth=10):
    """Extract and return youtube video ID.

    Assumption: a YouTube video ID is 11 characters long. All manually tested
    video IDs that were shorter resulted in an error. See these discussions:
    http://stackoverflow.com/a/6250619/291931
    https://groups.google.com/forum/?fromgroups=#!topic/youtube-api-gdata/oAztQ3f1tcM
    """

    if recursion_depth > max_recursion_depth:
        return

    vid = None
    purl = urlparse(url)
    path = purl.path.lstrip('/')  # strip leading slash(es)

    if purl.netloc.endswith('youtu.be'):
        vid = path

    elif purl.netloc.endswith('youtube.com'):
        # Check for verify age URLs.
        if path.startswith('verify_age'):
            next_url = get_param_value(purl, 'next_url')
            if next_url:
                # Next URL doesn't contain the host.
                if next_url.startswith('/'):
                    vid = get_param_value(urlparse(unquote(next_url)), 'v')
                # Next URL is an absolute URL.
                else:
                    vid = video_id(unquote(next_url), recursion_depth=recursion_depth + 1)
        # Check for full screen URLs.
        elif path.startswith(('v/', 'embed/')):
            vid = path.split('/')[1]
        # Check for standard watch URLs.
        elif path.startswith('watch'):
            vid = get_param_value(purl, 'v')
        # Check for attribution links.
        elif path.startswith('attribution_link'):
            watch_path = get_param_value(purl, 'u')
            if watch_path:
                vid = get_param_value(urlparse(watch_path), 'v')

    if vid and len(vid) >= 11:
        # Cut off extraneous characters after the ID.
        return vid[:11]