from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir

from odf.opendocument import OpenDocumentText
from odf.text import P

from os import path

class OdfBuilder(Builder):
  name = 'odf'
  format = 'odf'
  file_suffix = '.odt'
  link_suffix = '' # defaults to file_suffix

  def get_outdated_docs(self):
        """
        Return an iterable of input files that are outdated.
        """
        # This method is taken from TextBuilder.get_outdated_docs()
        # with minor changes to support :confval:`rst_file_transform`.
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            sourcename = path.join(self.env.srcdir, docname +
                                   self.file_suffix)
            targetname = path.join(self.outdir, self.file_transform(docname))
            print (sourcename, targetname)

            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(sourcename)
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass


  def prepare_writing(self, docnames):
    pass

  def get_target_uri(self, docname, typ=None):
    return self.link_transform(docname)

  # Function to convert the docname to a relative URI.
  def link_transform(self,docname):
    return docname + self.link_suffix

  # Function to convert the docname to a reST file name.
  def file_transform(self,docname):
    return docname + self.file_suffix

  def write_doc(self, docname, doctree):
    outfilename = path.join(self.outdir, self.file_transform(docname))
    ensuredir(path.dirname(outfilename))
    textdoc = OpenDocumentText()
    p = P(text="Hello World!")
    textdoc.text.addElement(p)
    textdoc.save(outfilename, True)
