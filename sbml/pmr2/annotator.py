from shutil import rmtree
from lxml import etree
import re
import tempfile
import os
import time
from os import listdir
from os.path import join, dirname, splitext
from cStringIO import StringIO
import cPickle as pickle

import zope.interface
import zope.component

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.data import datastream

from pmr2.app.interfaces import IExposureSourceAdapter
from pmr2.app.factory import named_factory
from pmr2.app.annotation.interfaces import *
from pmr2.app.annotation.annotator import ExposureFileAnnotatorBase
from pmr2.app.annotation.annotator import PortalTransformAnnotatorBase

import libsbml

from sbml.pmr2.interfaces import *

#XSLT_SOURCE = join(dirname(__file__), 'xslt')
#xsltpath = lambda x: join(XSLT_SOURCE, x)
#mathmlc2p_xslt = etree.parse(xsltpath('mathmlc2p.xsl'))


class SBMLNoteAnnotator(ExposureFileAnnotatorBase):
    zope.interface.implements(IExposureFileAnnotator)
    title = u'SBML Notes'
    label = u'Model Notes'
    description = u''
    for_interface = IRawTextNote

    def generate(self):
        reader = libsbml.SBMLReader()
        doc = reader.readSBMLFromString(self.input)
        model = doc.getModel()

        pt = getToolByName(self.context, 'portal_transforms', None)
        if pt:
            stream = datastream('license_description')
            pt.convert('safe_html', model.getNotesString(), stream)
            text = stream.getData().decode('utf8', 'ignore')
        else:
            # XXX should warn unsafe
            text = model.getNotesString()

        return (
            ('text', text,),
        )

SBMLNoteAnnotatorFactory = named_factory(SBMLNoteAnnotator)


class SBMLSpeciesAnnotator(ExposureFileAnnotatorBase):
    zope.interface.implements(IExposureFileAnnotator)
    title = u'SBML Species'
    label = u'Species'
    description = u''
    for_interface = ISBMLSpeciesNote

    def generate(self):
        reader = libsbml.SBMLReader()
        doc = reader.readSBMLFromString(self.input)
        model = doc.getModel()
        result = [
            (
                i.getName(),
                i.getId(),
                i.getCompartment(),
                i.getInitialConcentration(),
                i.getBoundaryCondition(),
            )
            for i in model.getListOfSpecies()
        ]
        return (
            ('species', result,),
        )

SBMLSpeciesAnnotatorFactory = named_factory(SBMLSpeciesAnnotator)


class SBMLReactionAnnotator(ExposureFileAnnotatorBase):
    zope.interface.implements(IExposureFileAnnotator)
    title = u'SBML Reactions'
    label = u'Reactions'
    description = u''
    for_interface = IRawTextNote # XXX fix

    def generate(self):
        def mathc2p(s):
            r = StringIO()
            t = etree.parse(StringIO(s))
            t.xslt(mathmlc2p_xslt).write(r)
            return r.getvalue()
        maths = self.maths()
        maths = [(k, [mathc2p(m) for m in v]) for k, v in maths]
        return (
            ('maths', maths),
        )

SBMLReactionAnnotatorFactory = named_factory(SBMLReactionAnnotator)

