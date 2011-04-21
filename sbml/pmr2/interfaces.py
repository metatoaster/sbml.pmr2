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
