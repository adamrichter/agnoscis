from subprocess import Popen, PIPE
#import xml.etree.ElementTree as ET
from lxml import etree
from lxml import isoschematron
from os import path
import tempfile
import shutil

pyang_opts= "--dsdl-no-documentation --dsdl-no-dublin-core"
yang_files_dir= "/home/richtada/tmp/discovery/yang-modules"

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class YangValidator:
    def __init__(self, relax_ng, schematron):
        self._relax_ng = relax_ng
        self._schematron = schematron

    def valid(self, instance):
        return self._relax_ng(instance) & self._schematron(instance)


class YangValidatorFactory:
    def __init__(self):
        self._xslt_dir = "/usr/local/share/yang/xslt"
        self._schema_dir = "/usr/local/share/yang/schema"
        self._dsdl_to_relaxng = self._create_transform('gen-relaxng.xsl')
        self._dsdl_to_schematron = self._create_transform('gen-schematron.xsl')
        self._dsld_to_dsrl = self._create_transform('gen-dsrl.xsl') 
        
    def create(self, yang_dir, yang):
        dsdl = self._get_dsdl(yang_dir, yang)
        relaxng = self._get_relaxng(dsdl)
        
        schematron_doc = self._dsdl_to_schematron(dsdl)
        schematron = isoschematron.Schematron(schematron_doc)
        
        return YangValidator(relaxng, schematron)

    def _create_transform(self, file_name):
        xslt_doc = etree.parse(path.join(xslt_dir, file_name))
        return etree.XSLT(xslt_doc)

    def _get_dsdl(self, yang_dir, yang_file):
        parameters = ['pyang', '--format=dsdl',
                      '--path='+yang_dir, yang_dir+"/" + yang_file]
        process = Popen(parameters, stdout=PIPE, stderr=PIPE)
        stdout , stderr = process.communicate()
        if stderr:
            raise Exception('Pyang error:\n' + stderr)
        return etree.fromstring(stdout)

    def _get_relaxng(self, dsdl):
        relaxng_doc = self._dsdl_to_relaxng(dsdl)
        
        tempdir = tempfile.mkdtemp()
        with open(path.join(tempdir, 'schema.rng'), "w") as f:
            f.write(str(relaxng_doc))
            
        shutil.copy(path.join(schema_dir, 'relaxng-lib.rng'), tempdir)
        relaxng = etree.RelaxNG(file = path.join(tempdir, 'schema.rng'))
        shutil.rmtree(tempdir)
        return relaxng

#    def _get_schematron(self, dsdl):
        


a = YangValidatorFactory()
service = a.create(yang_files_dir, 'service.yang')

service_instance = etree.parse('/home/richtada/tmp/discovery/test/xml/service.xml')

