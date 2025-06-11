AUTHOR = "Manuel Vázquez Acosta"
SITENAME = "Sofretería"
SITEURL = ""

PATH = "content"

TIMEZONE = "UTC"
DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Python.org", "https://www.python.org/"),
    ("Pelican", "https://getpelican.com/"),
)

# Social widget
SOCIAL = (("GitHub", "https://github.com/mvaled"),)

DEFAULT_PAGINATION = 10

# URL settings to match your current structure
ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}.html"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}.html"
PAGE_URL = "pages/{slug}.html"
PAGE_SAVE_AS = "pages/{slug}.html"

# Static paths - copy images from posts
STATIC_PATHS = ["images"]
EXTRA_PATH_METADATA = {}

# Plugin settings
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = []

# Theme settings
THEME = "theme"
THEME_STATIC_PATHS = ["static"]

# Keep original copyright
COPYRIGHT_YEAR = "2016-2025"
COPYRIGHT_NAME = AUTHOR


TYPOGRIFY = True


PYGMENTS_RST_OPTIONS = {"classprefix": "pygment-", "cssclass": "pygment-highlight"}
