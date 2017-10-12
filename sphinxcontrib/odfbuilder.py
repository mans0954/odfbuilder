from sphinx.builders import Builder
from .builders.odfb import OdfBuilder


def setup(app):
  app.require_sphinx('1.0')
  app.add_builder(OdfBuilder)
