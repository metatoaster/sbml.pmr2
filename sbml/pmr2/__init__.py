from pmr2.app.annotation import note_factory as factory
from pmr2.app.annotation.note import RawTextNote

from note import *

SBMLNoteFactory = factory(RawTextNote, 'sbml_note')
SBMLSpeciesNoteFactory = factory(SBMLSpeciesNote, 'sbml_species')
