from docutils.writers import odf_odt


class OdtWriter(odf_odt.Writer):

    output = None

    def __init__(self, builder):
        odf_odt.Writer.__init__(self)
        self.builder = builder
#        self.translator_class = OdtTranslator

    def translate(self):
        self.document.settings.odf_config_file=None
        self.document.settings.create_links=None
        self.document.settings.create_sections=None
        visitor = OdtTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

class OdtTranslator(odf_odt.ODFTranslator):

    def __init__(self, document):
      odf_odt.ODFTranslator.__init__(self, document)

    def log_unknown(self, type, node):
        logger = logging.getLogger("sphinxcontrib.writers.rst")
        if len(logger.handlers) == 0:
            # Logging is not yet configured. Configure it.
            logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(levelname)-8s %(message)s')
            logger = logging.getLogger("sphinxcontrib.writers.rst")
        logger.warning("%s(%s) unsupported formatting" % (type, node))
