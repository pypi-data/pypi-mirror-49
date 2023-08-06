import os
import sys
import re
from pprint import pprint

from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

class FileSelector(BasePlugin):

    config_scheme = (
        ('param', config_options.Type(mkdocs_utils.string_types, default='')),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
        path = re.search('(\'.*\')',)
       #path = path.group(0)
        pprint( config['docs_dir'])
        return markdown
