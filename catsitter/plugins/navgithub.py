#! /usr/bin/python
# encoding: utf-8

import re
import sys
import urllib2
import json

from catsitter import register

ISSUE_URL = 'https://github.com/UNINETT/nav/issues/{bug_id}'

@register('(?P<bugline>.*#\d+.*)')
def handler(bugline=None):

    result = []

    for bug in re.findall('#(\d+)', bugline):
        url = ISSUE_URL.format(bug_id=bug)
        try:
            req = urllib2.Request(url, headers={
                'Accept': 'application/json'
            })
            page = urllib2.urlopen(req).read()
        except urllib2.HTTPError:
            continue

        data = json.loads(page)
        title = data.get('title')
        if title:
            output = '[{bug}] {title} ({url})'.format(
                bug=bug, title=title, url=url)
            result.append(output)

    return result
