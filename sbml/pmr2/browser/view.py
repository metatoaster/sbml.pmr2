import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from paste.httpexceptions import HTTPNotFound
from plone.z3cform import layout

from pmr2.app.interfaces import IExposureSourceAdapter
from pmr2.app.browser.layout import PlainLayoutWrapper

from pmr2.app.exposure.browser.browser import ExposureFileViewBase


class SBMLNote(ExposureFileViewBase):
    """\
    SBML note.
    """

    template = ViewPageTemplateFile('sbml_note.pt')

SBMLNoteView = layout.wrap_form(SBMLNote, __wrapper_class=PlainLayoutWrapper)


class SBMLSpecies(ExposureFileViewBase):
    """\
    SBML species.
    """

    template = ViewPageTemplateFile('sbml_species.pt')

    keys = ('name', 'id', 'compartment', 'initialConcentration',
        'boundaryCondition',)

    @property
    def species(self):
        species = self.note.species
        result = []
        for name, id_, compartment, iC, bC in species:
            result.append(dict(zip(self.keys, 
                (name, id_, compartment, '%.2f' % iC, bC and u'\u2713' or '')
            )))
        return result

SBMLSpeciesView = layout.wrap_form(SBMLSpecies,
    __wrapper_class=PlainLayoutWrapper)
