from sphinx.builders import Builder

def setup(app):
  app.add_builder(OdfBuilder)
