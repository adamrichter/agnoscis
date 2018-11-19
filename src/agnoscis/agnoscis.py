from subprocess import Popen, PIPE
#import xml.etree.ElementTree as ET
from lxml import etree
from lxml import isoschematron
from os import path
import tempfile
import shutil




class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class YangValidator:
    def __init__(self, relax_ng, schematron, dsrl, data_xslt):
        self._relax_ng = relax_ng
        self._schematron = schematron
        self._dsrl = dsrl
        self._data_xslt = data_xslt

    def valid(self, instance):
        instance_with_default = self._dsrl(instance) 
        return self._relax_ng(instance) & self._schematron(instance)

    def get_data(self, instance):
        if self.valid(instance):
            return self._data_xslt(instance)
        return False

class YangValidatorFactory:
    def __init__(self):
        self._xslt_dir = "/usr/local/share/yang/xslt"
        self._schema_dir = "/usr/local/share/yang/schema"
        self._dsdl_to_relaxng = self._create_transform('gen-relaxng.xsl')
        self._dsdl_to_schematron = self._create_transform('gen-schematron.xsl')
        self._dsdl_to_dsrl = self._create_transform('gen-dsrl.xsl') 
        self._dsrl_to_xslt = self._create_transform('dsrl2xslt.xsl')
        
    def create(self, yang_dir, yang):
        dsdl = self._get_dsdl(yang_dir, yang)
        relaxng = self._get_relaxng(dsdl)
        
        schematron_doc = self._dsdl_to_schematron(dsdl)
        schematron = isoschematron.Schematron(schematron_doc)

        dsrl_doc = self._dsdl_to_dsrl(dsdl)
        dsrl_xslt = self._dsrl_to_xslt(dsrl_doc)
        dsrl = etree.XSLT(dsrl_xslt)

        yin = self._get_yin(yang_dir, yang)
        extract_xslt_doc = etree.parse('./stylesheets/gen-paramiters.xsl')
        get_extract_xslt = etree.XSLT(extract_xslt_doc)
        print etree.tostring(get_extract_xslt(yin))
        extract_xslt = etree.XSLT(get_extract_xslt(yin))
        
        return YangValidator(relaxng, schematron, dsrl, extract_xslt)

    def _create_transform(self, file_name):
        xslt_doc = etree.parse(path.join(self._xslt_dir, file_name))
        return etree.XSLT(xslt_doc)


    def _get_yin(self, yang_dir, yang_file):
        parameters = ['pyang', '--format=yin',
                      '--path='+yang_dir, yang_dir+"/" + yang_file]
        return self._run_pyang(parameters)
       
        
    def _get_dsdl(self, yang_dir, yang_file):
        parameters = ['pyang', '--format=dsdl',
                      '--path='+yang_dir, yang_dir+"/" + yang_file]
        return self._run_pyang(parameters)

    def _run_pyang(self, parameters):
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
            
        shutil.copy(path.join(self._schema_dir, 'relaxng-lib.rng'), tempdir)
        relaxng = etree.RelaxNG(file = path.join(tempdir, 'schema.rng'))
        shutil.rmtree(tempdir)
        return relaxng

#    def _get_schematron(self, dsdl):
        

yang_files_dir= "/home/richtada/tmp/discovery/yang-modules"
a = YangValidatorFactory()
service = a.create(yang_files_dir, 'service.yang')

service_instance = etree.parse('/home/richtada/tmp/discovery/test/xml/service.xml')

k = service.get_data(service_instance)
