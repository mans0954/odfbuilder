from sphinx.builders import Builder
from .builders.odf import OdfBuilder


def setup(app):
  app.require_sphinx('1.0')
  app.add_builder(OdfBuilder)
