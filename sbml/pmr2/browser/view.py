import zope.component
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from paste.httpexceptions import HTTPNotFound
from plone.z3cform import layout

from plone.memoize.view import memoize

from pmr2.app.exposure.interfaces import IExposureSourceAdapter

from pmr2.app.exposure.browser.browser import ExposureFileViewBase
from pmr2.annotation.mathjax.browser import DeferredMathJaxNote


class SBMLNoteView(ExposureFileViewBase):
    """\
    SBML note.
    """

    template = ViewPageTemplateFile('sbml_note.pt')


class SBMLSpeciesView(ExposureFileViewBase):
    """\
    SBML species.
    """

    template = ViewPageTemplateFile('sbml_species.pt')

    keys = ('name', 'id', 'compartment', 'initialConcentration',
        'boundaryCondition',)

    @memoize
    def species(self):
        species = self.note.species
        result = []
        for name, id_, compartment, iC, bC in species:
            result.append(dict(zip(self.keys, 
                (name, id_, compartment, '%.2f' % iC, bC and u'\u2713' or '')
            )))
        return result


class SBMLReactionsView(DeferredMathJaxNote):
    """\
    SBML reactions.
    """

    template = ViewPageTemplateFile('sbml_reactions.pt')

    keys = ('name', 'reactants', 'reversible', 'products', 'modifiers',
        'math',)

    @memoize
    def reactions(self):
        reactions = self.note.reactions
        result = []
        for (name, reactants, reversible, products, modifiers,
                math) in reactions:
            result.append(dict(zip(self.keys, (
                name,
                ' + '.join(reactants),
                reversible and u'\u2194' or u'\u2492',
                ' + '.join(products),
                ', '.join(modifiers),
                math,
            ))))
        return result
