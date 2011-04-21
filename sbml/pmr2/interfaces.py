import zope.interface
import zope.schema


class ISBMLSpeciesNote(zope.interface.Interface):
    """\
    SBML Species
    """

    species = zope.schema.List(
        title=u'Species',
        description=u'List of Species',
        default=[],
        required=False,
    )


class ISBMLReaction(zope.interface.Interface):
    # XXX implement this later.
    pass


class ISBMLReactionsNote(zope.interface.Interface):
    """\
    SBML Reactions
    """

    reactions = zope.schema.List(
        title=u'Reactions',
        description=u'List of Reactions',
        default=[],
        required=False,
    )
