from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir

#from docutils.io import StringOutput
from docutils import frontend, io
from docutils.core import publish_from_doctree
from docutils.core import *
from docutils.core import Publisher
from docutils.writers.odf_odt import Writer, Reader
import docutils.readers.doctree

import codecs
from os import path

from ..writers.odfw import OdtWriter

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

#def publish_programmatically(source_class, source, source_path,
#                             destination_class, destination, destination_path,
#                             reader, reader_name,
#                             parser, parser_name,
#                             writer, writer_name,
#                             settings, settings_spec,
#                             settings_overrides, config_section,
#                             enable_exit_status):   

    source_class=io.DocTreeInput
    source=io.DocTreeInput(doctree)
    source_path=None
    destination_class=io.BinaryFileOutput
    destination=None
    destination_path=outfilename
    reader=None
    reader_name='standalone'
    parser=None
    parser_name='restructuredtext'
    writer = Writer()
    writer_name='pseudoxml'
    settings=None
    settings_spec=None
    settings_overrides={'output_encoding': 'unicode'}
    config_section=None
    enable_exit_status=False

    reader = docutils.readers.doctree.Reader(parser_name='null')
    pub = Publisher(reader, None, writer, settings=settings,
                    source=source,
                    destination_class=destination_class)
#    if not writer and writer_name:
#        pub.set_writer(writer_name)
#    pub.set_components(reader_name, parser_name, writer_name)
    pub.process_programmatic_settings(
        settings_spec, settings_overrides, config_section)
#    pub.set_source(source, source_path)
    pub.set_destination(destination, destination_path)
    output = pub.publish(enable_exit_status=enable_exit_status)



#    pub = Publisher(reader, None, self.writer, None,destination_class=io.BinaryFileOutput)
#    pub.set_components(reader_name, parser_name, writer_name)
#    output = pub.publish(
#        argv, usage, description, settings_spec, settings_overrides,
#        config_section=config_section, enable_exit_status=enable_exit_status)
#return output



#   publish_cmdline_to_binary(reader=reader,
#    pub = Publisher(reader, None, self.writer,
#                    source=io.DocTreeInput(doctree),
#                    destination_class=io.BinaryFileOutput, settings=None)
#    pub.process_programmatic_settings(None, None, None)
#    pub.set_destination(None, outfilename)
#    pub.publish(enable_exit_status=False)


#    output = publish_from_doctree(doctree,destination_path=outfilename,writer=self.writer,destination_class=io.BinaryFileOutput)
#    output = pub.publish()

#    destination = io.BinaryFileOutput(None,outfilename)
#    self.writer.write(doctree,destination)
#    self.writer.assemble_parts()
#    ensuredir(path.dirname(outfilename))
#    try:
#            f = codecs.open(outfilename, 'w', 'utf-8')
#            try:
#                f.write(output)
#            finally:
#                f.close()
#    except (IOError, OSError) as err:
#      self.warn("error writing file %s: %s" % (outfilename, err))
