from sphinx.builders import Builder

from docutils import io
from docutils.core import Publisher
from docutils.writers.odf_odt import Writer
import docutils.readers.doctree

from os import path

from ..writers.odfw import OdtWriter

class OdfBuilder(Builder):
  name = 'odt'
  format = 'odt'
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
    self.writer = OdtWriter(self)

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


    reader = docutils.readers.doctree.Reader(parser_name='null')
    #Note, want to use our OdtWriter class here - but it doesn't work yet
    writer = Writer()
    
    pub = Publisher(reader, None, writer, settings=None,
                    source=io.DocTreeInput(doctree),
                    destination_class=io.BinaryFileOutput)

    settings_spec=None
    settings_overrides={'output_encoding': 'unicode'}
    config_section=None
    pub.process_programmatic_settings(
        settings_spec, settings_overrides, config_section)
    destination=None
    destination_path=outfilename
    pub.set_destination(destination, destination_path)
    output = pub.publish(enable_exit_status=False)


