import zope.interface
import zope.component
from zope.schema import fieldproperty

from pmr2.app.interfaces import *
from pmr2.app.annotation.note import ExposureFileNoteBase
from pmr2.app.annotation.note import ExposureFileEditableNoteBase

from sbml.pmr2.interfaces import *


class SBMLSpeciesNote(ExposureFileNoteBase):

    zope.interface.implements(ISBMLSpeciesNote)

    species = fieldproperty.FieldProperty(ISBMLSpeciesNote['species'])
