from sphinx.builders import Builder

from docutils import io
from docutils.core import Publisher
from docutils.writers.odf_odt import Writer
import docutils.readers.doctree

from sphinx.util import logging, status_iterator
from sphinx.util.nodes import inline_all_toctrees

from os import path

from ..writers.odfw import OdtWriter

from sphinx.util.console import bold, darkgreen
logger = logging.getLogger(__name__)

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
        return 'all documents'
#        for docname in self.env.found_docs:
#            if docname not in self.env.all_docs:
#                yield docname
#                continue
#            sourcename = path.join(self.env.srcdir, docname +
#                                   self.file_suffix)
#            targetname = path.join(self.outdir, self.file_transform(docname))
#            print (sourcename, targetname)
#
#            try:
#                targetmtime = path.getmtime(targetname)
#            except Exception:
#                targetmtime = 0
#            try:
#                srcmtime = path.getmtime(sourcename)
#                if srcmtime > targetmtime:
#                    yield docname
#            except EnvironmentError:
#                # source doesn't exist anymore
#                pass


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

  def assemble_doctree(self):
    master = self.config.master_doc
    tree = self.env.get_doctree(master)
    tree = inline_all_toctrees(self, set(), master, tree, darkgreen,[master])
    tree['docname'] = master
    self.env.resolve_references(tree, master, self)
    return tree


  def write(self, *ignored):
    doctree=self.assemble_doctree()
    docname = "%s-%s" % (self.config.project, self.config.version)
    self.write_doc(docname, doctree)


#        if build_docnames is None or build_docnames == ['__all__']:
#            # build_all
#            build_docnames = self.env.found_docs
#        if method == 'update':
#            # build updated ones as well
#            docnames = set(build_docnames) | set(updated_docnames)
#        else:
#            docnames = set(build_docnames)
#        logger.debug('docnames to write: %s', ', '.join(sorted(docnames)))

#        # add all toctree-containing files that may have changed
#        for docname in list(docnames):
#            for tocdocname in self.env.files_to_rebuild.get(docname, set()):
#                if tocdocname in self.env.found_docs:
#                    docnames.add(tocdocname)
#        docnames.add(self.config.master_doc)

#        logger.info(bold('preparing documents... '), nonl=True)
#        self.prepare_writing(docnames)
#        logger.info('done')

#        with logging.pending_warnings():
#            for docname in status_iterator(docnames, 'writing output... ', "darkgreen",
#                                           len(docnames), self.app.verbosity):
#                logger.debug('path: %s, file: %s',self.outdir,docname)
#                doctree = self.env.get_and_resolve_doctree(docname, self)
#                self.write_doc_serialized(docname, doctree)
#                self.write_doc(docname, doctree)


  def write_doc(self, docname, doctree):
    outfilename = path.join(self.outdir, self.file_transform(docname))
    logger.debug(outfilename)


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


