#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITEURL = 'http://jackon.me'

SITENAME = u'Jackon.me'
SITE_SUBTEXT = u'Source code, project demo and narcissism of a coder.'

AUTHOR = u'Jackon Yang'
AUTHOR_IMG = '/theme/img/user-image.jpg'
AUTHOR_BIO = u'Jackon Yang, Web Developer. Passionate by Spider, Data Modeling and Visualization'


SLUGIFY_SOURCE = 'basename'
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'


TEMPLATE_PAGES = {
    'about.html': 'about/index.html',
    'resume.html': 'resume/index.html',
    }


PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

THEME = "Gorgeous-Flat"
POST_LIMIT = 10
ARTICLES_HOME_PAGE = True

DEFAULT_PAGINATION = False

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('GitHub', 'https://github.com/JackonYang'),
          ('LinkedIn', 'http://www.linkedin.com/in/jiekunyang'),
          ('Facebook', 'https://www.facebook.com/jackon.yang'),
          )

CONTACT_INFO = {'email': 'i@jackon.me',
                'home': u'陕西, 西安',
                }

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
