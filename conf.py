# -*- coding: utf-8 -*-

import tinkerer
import tinkerer.paths

# **************************************************************
# TODO: Edit the lines below
# **************************************************************

# Change this to the name of your blog
project = 'Manuel on Software - Reloaded'

# Change this to the tagline of your blog
tagline = ''

# Change this to the description of your blog
description = 'Blog mostly about software.'

# Change this to your name
author = u'Manuel Vázquez Acosta'

# Change this to your copyright string
copyright = '2014, ' + author

# Generated language
language = 'en'

# Change this to your blog root URL (required for RSS feed)
website = 'http://mvaled.github.io/blog/html/'


# **************************************************************
# More tweaks you can do
# **************************************************************

# Add your Disqus shortname to enable comments powered by Disqus
disqus_shortname = None

# Change your favicon (new favicon goes in _static directory)
# html_favicon = 'tinkerer.ico'

# Pick another Tinkerer theme or use your own
html_theme = "mva"

# Theme-specific options, see docs
html_theme_options = {}

# Link to RSS service like FeedBurner if any, otherwise feed is
# linked directly
rss_service = None

# Generate full posts for RSS feed even when using "read more"
rss_generate_full_posts = False

# Number of blog posts per page
posts_per_page = 10

# Character use to replace non-alphanumeric characters in slug
slug_word_separator = '-'

# **************************************************************
# Edit lines below to further customize Sphinx build
# **************************************************************

# Add other Sphinx extensions here
extensions = ['tinkerer.ext.blog',
              'tinkerer.ext.disqus',
              'sphinx.ext.intersphinx']

# Add other template paths here
templates_path = ['_templates']

# Add other static paths here
html_static_path = ['_static', tinkerer.paths.static]

# Add other theme paths here
html_theme_path = ['_themes', tinkerer.paths.themes]

# Add file patterns to exclude from build
exclude_patterns = ["_templates/*"]

# Add templates to be rendered in sidebar here
html_sidebars = {
    #   "**": ["recent.html", "searchbox.html"]
}


intersphinx_mapping = {
    'py': ('http://docs.python.org/3.4/', None),
    'sphinx': ('http://sphinx-doc.org/', None),
    'xotlql': ('http://xotl-ql.readthedocs.org/en/latest/', None),
}


# Maintain the cache forever.
intersphinx_cache_limit = 365

pygments_style = 'sphinx'

# **************************************************************
# Do not modify below lines as the values are required by
# Tinkerer to play nice with Sphinx
# **************************************************************

source_suffix = tinkerer.source_suffix
master_doc = tinkerer.master_doc
version = tinkerer.__version__
release = tinkerer.__version__
html_title = project
html_use_index = False
html_show_sourcelink = False
html_add_permalinks = None
