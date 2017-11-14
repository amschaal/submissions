# ./bioproject.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2017-11-13 11:34:49.327762 by PyXB version 1.2.6 using Python 2.7.6.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:b64dde30-c8a9-11e7-9ba6-c03fd56d5244')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 54, 24)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.eUnchanged = STD_ANON._CF_enumeration.addEnumeration(unicode_value='eUnchanged', tag='eUnchanged')
STD_ANON.eUpdated = STD_ANON._CF_enumeration.addEnumeration(unicode_value='eUpdated', tag='eUpdated')
STD_ANON.eAdded = STD_ANON._CF_enumeration.addEnumeration(unicode_value='eAdded', tag='eAdded')
STD_ANON.eDeleted = STD_ANON._CF_enumeration.addEnumeration(unicode_value='eDeleted', tag='eDeleted')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 346, 40)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.eDisease = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='eDisease', tag='eDisease')
STD_ANON_.eComparativeGenomics = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='eComparativeGenomics', tag='eComparativeGenomics')
STD_ANON_.eMetagenome = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='eMetagenome', tag='eMetagenome')
STD_ANON_.eSingleOrganismDiscovery = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='eSingleOrganismDiscovery', tag='eSingleOrganismDiscovery')
STD_ANON_.eFundingInitiative = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='eFundingInitiative', tag='eFundingInitiative')
STD_ANON_.eOther = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 406, 52)
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.eMonoisolate = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='eMonoisolate', tag='eMonoisolate')
STD_ANON_2.eMultiisolate = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='eMultiisolate', tag='eMultiisolate')
STD_ANON_2.eMultispecies = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='eMultispecies', tag='eMultispecies')
STD_ANON_2.eEnvironment = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='eEnvironment', tag='eEnvironment')
STD_ANON_2.eSynthetic = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='eSynthetic', tag='eSynthetic')
STD_ANON_2.eOther = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 447, 52)
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.eGenome = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='eGenome', tag='eGenome')
STD_ANON_3.ePartialGenome = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='ePartialGenome', tag='ePartialGenome')
STD_ANON_3.eTranscriptome = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='eTranscriptome', tag='eTranscriptome')
STD_ANON_3.eReagent = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='eReagent', tag='eReagent')
STD_ANON_3.eProteome = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='eProteome', tag='eProteome')
STD_ANON_3.ePhenotype = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='ePhenotype', tag='ePhenotype')
STD_ANON_3.eOther = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 493, 52)
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.eWhole = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='eWhole', tag='eWhole')
STD_ANON_4.eCloneEnds = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='eCloneEnds', tag='eCloneEnds')
STD_ANON_4.eExome = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='eExome', tag='eExome')
STD_ANON_4.eTargetedLocusLoci = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='eTargetedLocusLoci', tag='eTargetedLocusLoci')
STD_ANON_4.eRandomSurvey = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='eRandomSurvey', tag='eRandomSurvey')
STD_ANON_4.eOther = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 555, 50)
    _Documentation = None
STD_ANON_5._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_5, enum_prefix=None)
STD_ANON_5.eSequencing = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='eSequencing', tag='eSequencing')
STD_ANON_5.eArray = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='eArray', tag='eArray')
STD_ANON_5.eMassSpectrometry = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='eMassSpectrometry', tag='eMassSpectrometry')
STD_ANON_5.eOther = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_enumeration)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 598, 50)
    _Documentation = None
STD_ANON_6._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_6, enum_prefix=None)
STD_ANON_6.eRawSequenceReads = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eRawSequenceReads', tag='eRawSequenceReads')
STD_ANON_6.eSequence = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eSequence', tag='eSequence')
STD_ANON_6.eAnalysis = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eAnalysis', tag='eAnalysis')
STD_ANON_6.eAssembly = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eAssembly', tag='eAssembly')
STD_ANON_6.eAnnotation = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eAnnotation', tag='eAnnotation')
STD_ANON_6.eVariation = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eVariation', tag='eVariation')
STD_ANON_6.eEpigeneticMarkers = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eEpigeneticMarkers', tag='eEpigeneticMarkers')
STD_ANON_6.eExpression = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eExpression', tag='eExpression')
STD_ANON_6.eMaps = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eMaps', tag='eMaps')
STD_ANON_6.ePhenotype = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='ePhenotype', tag='ePhenotype')
STD_ANON_6.eOther = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_enumeration)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Atomic simple type: [anonymous]
class STD_ANON_7 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 723, 16)
    _Documentation = None
STD_ANON_7._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_7, enum_prefix=None)
STD_ANON_7.ePMC = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value='ePMC', tag='ePMC')
STD_ANON_7.ePubmed = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value='ePubmed', tag='ePubmed')
STD_ANON_7.eDOI = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value='eDOI', tag='eDOI')
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_enumeration)
_module_typeBindings.STD_ANON_7 = STD_ANON_7

# Atomic simple type: [anonymous]
class STD_ANON_8 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 796, 16)
    _Documentation = None
STD_ANON_8._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_8, enum_prefix=None)
STD_ANON_8.eEukaryotes = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value='eEukaryotes', tag='eEukaryotes')
STD_ANON_8.eArchaea = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value='eArchaea', tag='eArchaea')
STD_ANON_8.eBacteria = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value='eBacteria', tag='eBacteria')
STD_ANON_8.eViruses = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value='eViruses', tag='eViruses')
STD_ANON_8.eOther = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_enumeration)
_module_typeBindings.STD_ANON_8 = STD_ANON_8

# Atomic simple type: [anonymous]
class STD_ANON_9 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 821, 40)
    _Documentation = None
STD_ANON_9._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_9, enum_prefix=None)
STD_ANON_9.eNegative = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='eNegative', tag='eNegative')
STD_ANON_9.ePositive = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='ePositive', tag='ePositive')
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_enumeration)
_module_typeBindings.STD_ANON_9 = STD_ANON_9

# Atomic simple type: [anonymous]
class STD_ANON_10 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 829, 40)
    _Documentation = None
STD_ANON_10._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_10, enum_prefix=None)
STD_ANON_10.eNo = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='eNo', tag='eNo')
STD_ANON_10.eYes = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='eYes', tag='eYes')
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_enumeration)
_module_typeBindings.STD_ANON_10 = STD_ANON_10

# Atomic simple type: [anonymous]
class STD_ANON_11 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 837, 40)
    _Documentation = None
STD_ANON_11._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_11, enum_prefix=None)
STD_ANON_11.eBacilli = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eBacilli', tag='eBacilli')
STD_ANON_11.eCocci = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eCocci', tag='eCocci')
STD_ANON_11.eSpirilla = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eSpirilla', tag='eSpirilla')
STD_ANON_11.eCoccobacilli = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eCoccobacilli', tag='eCoccobacilli')
STD_ANON_11.eFilamentous = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eFilamentous', tag='eFilamentous')
STD_ANON_11.eVibrios = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eVibrios', tag='eVibrios')
STD_ANON_11.eFusobacteria = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eFusobacteria', tag='eFusobacteria')
STD_ANON_11.eSquareShaped = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eSquareShaped', tag='eSquareShaped')
STD_ANON_11.eCurvedShaped = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eCurvedShaped', tag='eCurvedShaped')
STD_ANON_11.eTailed = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='eTailed', tag='eTailed')
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_enumeration)
_module_typeBindings.STD_ANON_11 = STD_ANON_11

# Atomic simple type: [anonymous]
class STD_ANON_12 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 895, 40)
    _Documentation = None
STD_ANON_12._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_12, enum_prefix=None)
STD_ANON_12.eNo = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value='eNo', tag='eNo')
STD_ANON_12.eYes = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value='eYes', tag='eYes')
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_enumeration)
_module_typeBindings.STD_ANON_12 = STD_ANON_12

# Atomic simple type: [anonymous]
class STD_ANON_13 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 903, 40)
    _Documentation = None
STD_ANON_13._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_13, enum_prefix=None)
STD_ANON_13.eNo = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value='eNo', tag='eNo')
STD_ANON_13.eYes = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value='eYes', tag='eYes')
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_enumeration)
_module_typeBindings.STD_ANON_13 = STD_ANON_13

# Atomic simple type: [anonymous]
class STD_ANON_14 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 917, 40)
    _Documentation = None
STD_ANON_14._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_14, enum_prefix=None)
STD_ANON_14.ePureCulture = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value='ePureCulture', tag='ePureCulture')
STD_ANON_14.eMixedCulture = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value='eMixedCulture', tag='eMixedCulture')
STD_ANON_14.eUncultered = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value='eUncultered', tag='eUncultered')
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_enumeration)
_module_typeBindings.STD_ANON_14 = STD_ANON_14

# Atomic simple type: [anonymous]
class STD_ANON_15 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 926, 40)
    _Documentation = None
STD_ANON_15._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_15, enum_prefix=None)
STD_ANON_15.eIsolated = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value='eIsolated', tag='eIsolated')
STD_ANON_15.eNonisolated = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value='eNonisolated', tag='eNonisolated')
STD_ANON_15._InitializeFacetMap(STD_ANON_15._CF_enumeration)
_module_typeBindings.STD_ANON_15 = STD_ANON_15

# Atomic simple type: [anonymous]
class STD_ANON_16 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 943, 40)
    _Documentation = None
STD_ANON_16._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_16, enum_prefix=None)
STD_ANON_16.eUnknown = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value='eUnknown', tag='eUnknown')
STD_ANON_16.eNonHalophilic = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value='eNonHalophilic', tag='eNonHalophilic')
STD_ANON_16.eMesophilic = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value='eMesophilic', tag='eMesophilic')
STD_ANON_16.eModerateHalophilic = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value='eModerateHalophilic', tag='eModerateHalophilic')
STD_ANON_16.eExtremeHalophilic = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value='eExtremeHalophilic', tag='eExtremeHalophilic')
STD_ANON_16._InitializeFacetMap(STD_ANON_16._CF_enumeration)
_module_typeBindings.STD_ANON_16 = STD_ANON_16

# Atomic simple type: [anonymous]
class STD_ANON_17 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 954, 40)
    _Documentation = None
STD_ANON_17._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_17, enum_prefix=None)
STD_ANON_17.eUnknown = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value='eUnknown', tag='eUnknown')
STD_ANON_17.eAerobic = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value='eAerobic', tag='eAerobic')
STD_ANON_17.eMicroaerophilic = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value='eMicroaerophilic', tag='eMicroaerophilic')
STD_ANON_17.eFacultative = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value='eFacultative', tag='eFacultative')
STD_ANON_17.eAnaerobic = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value='eAnaerobic', tag='eAnaerobic')
STD_ANON_17._InitializeFacetMap(STD_ANON_17._CF_enumeration)
_module_typeBindings.STD_ANON_17 = STD_ANON_17

# Atomic simple type: [anonymous]
class STD_ANON_18 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 967, 40)
    _Documentation = None
STD_ANON_18._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_18, enum_prefix=None)
STD_ANON_18.eUnknown = STD_ANON_18._CF_enumeration.addEnumeration(unicode_value='eUnknown', tag='eUnknown')
STD_ANON_18.eCryophilic = STD_ANON_18._CF_enumeration.addEnumeration(unicode_value='eCryophilic', tag='eCryophilic')
STD_ANON_18.ePsychrophilic = STD_ANON_18._CF_enumeration.addEnumeration(unicode_value='ePsychrophilic', tag='ePsychrophilic')
STD_ANON_18.eMesophilic = STD_ANON_18._CF_enumeration.addEnumeration(unicode_value='eMesophilic', tag='eMesophilic')
STD_ANON_18.eThermophilic = STD_ANON_18._CF_enumeration.addEnumeration(unicode_value='eThermophilic', tag='eThermophilic')
STD_ANON_18.eHyperthermophilic = STD_ANON_18._CF_enumeration.addEnumeration(unicode_value='eHyperthermophilic', tag='eHyperthermophilic')
STD_ANON_18._InitializeFacetMap(STD_ANON_18._CF_enumeration)
_module_typeBindings.STD_ANON_18 = STD_ANON_18

# Atomic simple type: [anonymous]
class STD_ANON_19 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 979, 40)
    _Documentation = None
STD_ANON_19._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_19, enum_prefix=None)
STD_ANON_19.eUnknown = STD_ANON_19._CF_enumeration.addEnumeration(unicode_value='eUnknown', tag='eUnknown')
STD_ANON_19.eHostAssociated = STD_ANON_19._CF_enumeration.addEnumeration(unicode_value='eHostAssociated', tag='eHostAssociated')
STD_ANON_19.eAquatic = STD_ANON_19._CF_enumeration.addEnumeration(unicode_value='eAquatic', tag='eAquatic')
STD_ANON_19.eTerrestrial = STD_ANON_19._CF_enumeration.addEnumeration(unicode_value='eTerrestrial', tag='eTerrestrial')
STD_ANON_19.eSpecialized = STD_ANON_19._CF_enumeration.addEnumeration(unicode_value='eSpecialized', tag='eSpecialized')
STD_ANON_19.eMultiple = STD_ANON_19._CF_enumeration.addEnumeration(unicode_value='eMultiple', tag='eMultiple')
STD_ANON_19._InitializeFacetMap(STD_ANON_19._CF_enumeration)
_module_typeBindings.STD_ANON_19 = STD_ANON_19

# Atomic simple type: [anonymous]
class STD_ANON_20 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 998, 40)
    _Documentation = None
STD_ANON_20._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_20, enum_prefix=None)
STD_ANON_20.eFreeLiving = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eFreeLiving', tag='eFreeLiving')
STD_ANON_20.eCommensal = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eCommensal', tag='eCommensal')
STD_ANON_20.eSymbiont = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eSymbiont', tag='eSymbiont')
STD_ANON_20.eEpisymbiont = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eEpisymbiont', tag='eEpisymbiont')
STD_ANON_20.eIntracellular = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eIntracellular', tag='eIntracellular')
STD_ANON_20.eParasite = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eParasite', tag='eParasite')
STD_ANON_20.eHost = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eHost', tag='eHost')
STD_ANON_20.eEndosymbiont = STD_ANON_20._CF_enumeration.addEnumeration(unicode_value='eEndosymbiont', tag='eEndosymbiont')
STD_ANON_20._InitializeFacetMap(STD_ANON_20._CF_enumeration)
_module_typeBindings.STD_ANON_20 = STD_ANON_20

# Atomic simple type: [anonymous]
class STD_ANON_21 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1012, 40)
    _Documentation = None
STD_ANON_21._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_21, enum_prefix=None)
STD_ANON_21.eAutotroph = STD_ANON_21._CF_enumeration.addEnumeration(unicode_value='eAutotroph', tag='eAutotroph')
STD_ANON_21.eHeterotroph = STD_ANON_21._CF_enumeration.addEnumeration(unicode_value='eHeterotroph', tag='eHeterotroph')
STD_ANON_21.eMixotroph = STD_ANON_21._CF_enumeration.addEnumeration(unicode_value='eMixotroph', tag='eMixotroph')
STD_ANON_21._InitializeFacetMap(STD_ANON_21._CF_enumeration)
_module_typeBindings.STD_ANON_21 = STD_ANON_21

# Atomic simple type: [anonymous]
class STD_ANON_22 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1029, 16)
    _Documentation = None
STD_ANON_22._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_22, enum_prefix=None)
STD_ANON_22.eUnicellular = STD_ANON_22._CF_enumeration.addEnumeration(unicode_value='eUnicellular', tag='eUnicellular')
STD_ANON_22.eMulticellular = STD_ANON_22._CF_enumeration.addEnumeration(unicode_value='eMulticellular', tag='eMulticellular')
STD_ANON_22.eColonial = STD_ANON_22._CF_enumeration.addEnumeration(unicode_value='eColonial', tag='eColonial')
STD_ANON_22._InitializeFacetMap(STD_ANON_22._CF_enumeration)
_module_typeBindings.STD_ANON_22 = STD_ANON_22

# Atomic simple type: [anonymous]
class STD_ANON_23 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1038, 16)
    _Documentation = None
STD_ANON_23._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_23, enum_prefix=None)
STD_ANON_23.eSexual = STD_ANON_23._CF_enumeration.addEnumeration(unicode_value='eSexual', tag='eSexual')
STD_ANON_23.eAsexual = STD_ANON_23._CF_enumeration.addEnumeration(unicode_value='eAsexual', tag='eAsexual')
STD_ANON_23._InitializeFacetMap(STD_ANON_23._CF_enumeration)
_module_typeBindings.STD_ANON_23 = STD_ANON_23

# Atomic simple type: [anonymous]
class STD_ANON_24 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1055, 44)
    _Documentation = None
STD_ANON_24._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_24, enum_prefix=None)
STD_ANON_24.eHaploid = STD_ANON_24._CF_enumeration.addEnumeration(unicode_value='eHaploid', tag='eHaploid')
STD_ANON_24.eDiploid = STD_ANON_24._CF_enumeration.addEnumeration(unicode_value='eDiploid', tag='eDiploid')
STD_ANON_24.ePolyploid = STD_ANON_24._CF_enumeration.addEnumeration(unicode_value='ePolyploid', tag='ePolyploid')
STD_ANON_24.eAllopolyploid = STD_ANON_24._CF_enumeration.addEnumeration(unicode_value='eAllopolyploid', tag='eAllopolyploid')
STD_ANON_24._InitializeFacetMap(STD_ANON_24._CF_enumeration)
_module_typeBindings.STD_ANON_24 = STD_ANON_24

# Atomic simple type: typeRepresentation
class typeRepresentation (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeRepresentation')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1092, 4)
    _Documentation = None
typeRepresentation._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeRepresentation, enum_prefix=None)
typeRepresentation.eReference = typeRepresentation._CF_enumeration.addEnumeration(unicode_value='eReference', tag='eReference')
typeRepresentation.eAlternate = typeRepresentation._CF_enumeration.addEnumeration(unicode_value='eAlternate', tag='eAlternate')
typeRepresentation.eOther = typeRepresentation._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
typeRepresentation._InitializeFacetMap(typeRepresentation._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeRepresentation', typeRepresentation)
_module_typeBindings.typeRepresentation = typeRepresentation

# Atomic simple type: typeDecimalPositive
class typeDecimalPositive (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeDecimalPositive')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1099, 4)
    _Documentation = None
typeDecimalPositive._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=typeDecimalPositive, value=pyxb.binding.datatypes.decimal('0.0'))
typeDecimalPositive._InitializeFacetMap(typeDecimalPositive._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'typeDecimalPositive', typeDecimalPositive)
_module_typeBindings.typeDecimalPositive = typeDecimalPositive

# Atomic simple type: [anonymous]
class STD_ANON_25 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1108, 20)
    _Documentation = None
STD_ANON_25._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_25, enum_prefix=None)
STD_ANON_25.Mb = STD_ANON_25._CF_enumeration.addEnumeration(unicode_value='Mb', tag='Mb')
STD_ANON_25.Kb = STD_ANON_25._CF_enumeration.addEnumeration(unicode_value='Kb', tag='Kb')
STD_ANON_25.cM = STD_ANON_25._CF_enumeration.addEnumeration(unicode_value='cM', tag='cM')
STD_ANON_25._InitializeFacetMap(STD_ANON_25._CF_enumeration)
_module_typeBindings.STD_ANON_25 = STD_ANON_25

# Atomic simple type: typeArchive
class typeArchive (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeArchive')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1123, 4)
    _Documentation = None
typeArchive._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeArchive, enum_prefix=None)
typeArchive.NCBI = typeArchive._CF_enumeration.addEnumeration(unicode_value='NCBI', tag='NCBI')
typeArchive.EBI = typeArchive._CF_enumeration.addEnumeration(unicode_value='EBI', tag='EBI')
typeArchive.DDBJ = typeArchive._CF_enumeration.addEnumeration(unicode_value='DDBJ', tag='DDBJ')
typeArchive._InitializeFacetMap(typeArchive._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeArchive', typeArchive)
_module_typeBindings.typeArchive = typeArchive

# Atomic simple type: typeRepliconMolType
class typeRepliconMolType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeRepliconMolType')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1187, 4)
    _Documentation = None
typeRepliconMolType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeRepliconMolType, enum_prefix=None)
typeRepliconMolType.eChromosome = typeRepliconMolType._CF_enumeration.addEnumeration(unicode_value='eChromosome', tag='eChromosome')
typeRepliconMolType.ePlasmid = typeRepliconMolType._CF_enumeration.addEnumeration(unicode_value='ePlasmid', tag='ePlasmid')
typeRepliconMolType.eLinkageGroup = typeRepliconMolType._CF_enumeration.addEnumeration(unicode_value='eLinkageGroup', tag='eLinkageGroup')
typeRepliconMolType.eSegment = typeRepliconMolType._CF_enumeration.addEnumeration(unicode_value='eSegment', tag='eSegment')
typeRepliconMolType.eOther = typeRepliconMolType._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
typeRepliconMolType._InitializeFacetMap(typeRepliconMolType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeRepliconMolType', typeRepliconMolType)
_module_typeBindings.typeRepliconMolType = typeRepliconMolType

# Atomic simple type: [anonymous]
class STD_ANON_26 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1205, 20)
    _Documentation = None
STD_ANON_26._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_26, enum_prefix=None)
STD_ANON_26.eNuclearProkaryote = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eNuclearProkaryote', tag='eNuclearProkaryote')
STD_ANON_26.eMacronuclear = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eMacronuclear', tag='eMacronuclear')
STD_ANON_26.eNucleomorph = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eNucleomorph', tag='eNucleomorph')
STD_ANON_26.eMitochondrion = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eMitochondrion', tag='eMitochondrion')
STD_ANON_26.eKinetoplast = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eKinetoplast', tag='eKinetoplast')
STD_ANON_26.eChloroplast = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eChloroplast', tag='eChloroplast')
STD_ANON_26.eChromoplast = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eChromoplast', tag='eChromoplast')
STD_ANON_26.ePlastid = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='ePlastid', tag='ePlastid')
STD_ANON_26.eVirionPhage = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eVirionPhage', tag='eVirionPhage')
STD_ANON_26.eProviralProphage = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eProviralProphage', tag='eProviralProphage')
STD_ANON_26.eViroid = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eViroid', tag='eViroid')
STD_ANON_26.eExtrachrom = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eExtrachrom', tag='eExtrachrom')
STD_ANON_26.eCyanelle = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eCyanelle', tag='eCyanelle')
STD_ANON_26.eApicoplast = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eApicoplast', tag='eApicoplast')
STD_ANON_26.eLeucoplast = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eLeucoplast', tag='eLeucoplast')
STD_ANON_26.eProplastid = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eProplastid', tag='eProplastid')
STD_ANON_26.eHydrogenosome = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eHydrogenosome', tag='eHydrogenosome')
STD_ANON_26.eChromatophore = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eChromatophore', tag='eChromatophore')
STD_ANON_26.eOther = STD_ANON_26._CF_enumeration.addEnumeration(unicode_value='eOther', tag='eOther')
STD_ANON_26._InitializeFacetMap(STD_ANON_26._CF_enumeration)
_module_typeBindings.STD_ANON_26 = STD_ANON_26

# Atomic simple type: typeLocusTagPrefix
class typeLocusTagPrefix (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeLocusTagPrefix')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1258, 4)
    _Documentation = None
typeLocusTagPrefix._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
typeLocusTagPrefix._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
typeLocusTagPrefix._InitializeFacetMap(typeLocusTagPrefix._CF_minLength,
   typeLocusTagPrefix._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'typeLocusTagPrefix', typeLocusTagPrefix)
_module_typeBindings.typeLocusTagPrefix = typeLocusTagPrefix

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """
                Set of packages. 
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 11, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Package uses Python identifier Package
    __Package = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Package'), 'Package', '__AbsentNamespace0_CTD_ANON_Package', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 13, 16), )

    
    Package = property(__Package.value, __Package.set, None, None)

    _ElementMap.update({
        __Package.name() : __Package
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type typePackage with content type ELEMENT_ONLY
class typePackage (pyxb.binding.basis.complexTypeDefinition):
    """
                A container for project information that may be exchanged.
                May contain one or more single elements (i.e. one Project and one Submission)
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typePackage')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 18, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Processing uses Python identifier Processing
    __Processing = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Processing'), 'Processing', '__AbsentNamespace0_typePackage_Processing', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 26, 12), )

    
    Processing = property(__Processing.value, __Processing.set, None, '\n                        Information about owner and what to do with the package\n                    ')

    
    # Element Project uses Python identifier Project
    __Project = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Project'), 'Project', '__AbsentNamespace0_typePackage_Project', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 69, 12), )

    
    Project = property(__Project.value, __Project.set, None, '\n                        Project core XML (see corresponding schema)\n                    ')

    
    # Element ProjectAssembly uses Python identifier ProjectAssembly
    __ProjectAssembly = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectAssembly'), 'ProjectAssembly', '__AbsentNamespace0_typePackage_ProjectAssembly', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 682, 12), )

    
    ProjectAssembly = property(__ProjectAssembly.value, __ProjectAssembly.set, None, None)

    
    # Element ProjectSubmission uses Python identifier ProjectSubmission
    __ProjectSubmission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectSubmission'), 'ProjectSubmission', '__AbsentNamespace0_typePackage_ProjectSubmission', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 685, 12), )

    
    ProjectSubmission = property(__ProjectSubmission.value, __ProjectSubmission.set, None, '\n                        Unique for BioProject submission information, that is indicated in element Path in the main submission XML. \n                        For instance comments for DB staff in web submission form, etc.\n                    ')

    
    # Element ProjectLinks uses Python identifier ProjectLinks
    __ProjectLinks = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectLinks'), 'ProjectLinks', '__AbsentNamespace0_typePackage_ProjectLinks', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 693, 12), )

    
    ProjectLinks = property(__ProjectLinks.value, __ProjectLinks.set, None, '\n                        Project links XML (see corresponding schema)\n                    ')

    
    # Element ProjectPresentation uses Python identifier ProjectPresentation
    __ProjectPresentation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectPresentation'), 'ProjectPresentation', '__AbsentNamespace0_typePackage_ProjectPresentation', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 700, 12), )

    
    ProjectPresentation = property(__ProjectPresentation.value, __ProjectPresentation.set, None, '\n                        Project core XML. Currenty not used.\n                    ')

    _ElementMap.update({
        __Processing.name() : __Processing,
        __Project.name() : __Project,
        __ProjectAssembly.name() : __ProjectAssembly,
        __ProjectSubmission.name() : __ProjectSubmission,
        __ProjectLinks.name() : __ProjectLinks,
        __ProjectPresentation.name() : __ProjectPresentation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.typePackage = typePackage
Namespace.addCategoryObject('typeBinding', 'typePackage', typePackage)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """
                        Project core XML (see corresponding schema)
                    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 75, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Project uses Python identifier Project
    __Project = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Project'), 'Project', '__AbsentNamespace0_CTD_ANON__Project', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 76, 0), )

    
    Project = property(__Project.value, __Project.set, None, None)

    _ElementMap.update({
        __Project.name() : __Project
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 77, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ProjectID uses Python identifier ProjectID
    __ProjectID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectID'), 'ProjectID', '__AbsentNamespace0_CTD_ANON_2_ProjectID', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 79, 16), )

    
    ProjectID = property(__ProjectID.value, __ProjectID.set, None, '\n                        List of all project ids: submitter asigned, archive assigned, ....\n                    ')

    
    # Element ProjectDescr uses Python identifier ProjectDescr
    __ProjectDescr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectDescr'), 'ProjectDescr', '__AbsentNamespace0_CTD_ANON_2_ProjectDescr', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 115, 16), )

    
    ProjectDescr = property(__ProjectDescr.value, __ProjectDescr.set, None, '\n                            Common description of a project : title, publication, etc...\n                        ')

    
    # Element ProjectType uses Python identifier ProjectType
    __ProjectType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectType'), 'ProjectType', '__AbsentNamespace0_CTD_ANON_2_ProjectType', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 289, 16), )

    
    ProjectType = property(__ProjectType.value, __ProjectType.set, None, '\n                           Project type specific fields. Created as "choice" - for future expansion.\n                       ')

    _ElementMap.update({
        __ProjectID.name() : __ProjectID,
        __ProjectDescr.name() : __ProjectDescr,
        __ProjectType.name() : __ProjectType
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """
                        List of all project ids: submitter asigned, archive assigned, ....
                    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 85, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ArchiveID uses Python identifier ArchiveID
    __ArchiveID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ArchiveID'), 'ArchiveID', '__AbsentNamespace0_CTD_ANON_3_ArchiveID', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 92, 28), )

    
    ArchiveID = property(__ArchiveID.value, __ArchiveID.set, None, ' \n                                        Unique project identifier across all archives.\n                                        Contains host archive name, unique NCBI database ID (assigned only by NCBI DB staff) and unique accession (see accession description). \n                                        Element is optional since it will be created on submission. However it is required in the DB.\n                                    ')

    
    # Element CenterID uses Python identifier CenterID
    __CenterID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CenterID'), 'CenterID', '__AbsentNamespace0_CTD_ANON_3_CenterID', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 102, 28), )

    
    CenterID = property(__CenterID.value, __CenterID.set, None, ' \n                                    List of center-specific internal tracking IDs for the project.\n                                ')

    
    # Element LocalID uses Python identifier LocalID
    __LocalID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'LocalID'), 'LocalID', '__AbsentNamespace0_CTD_ANON_3_LocalID', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 110, 28), )

    
    LocalID = property(__LocalID.value, __LocalID.set, None, None)

    _ElementMap.update({
        __ArchiveID.name() : __ArchiveID,
        __CenterID.name() : __CenterID,
        __LocalID.name() : __LocalID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """
                            Common description of a project : title, publication, etc...
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 121, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Name'), 'Name', '__AbsentNamespace0_CTD_ANON_4_Name', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 123, 28), )

    
    Name = property(__Name.value, __Name.set, None, '\n                                    Very short descriptive name of the project  for caption, labels, etc.  For example:  1000 Genomes Project\n                                ')

    
    # Element Title uses Python identifier Title
    __Title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Title'), 'Title', '__AbsentNamespace0_CTD_ANON_4_Title', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 130, 28), )

    
    Title = property(__Title.value, __Title.set, None, '\n                                    Short, but informative title of the projects, single phrase, single line. For example: \n                                    Sequencing the southern Chinese HAN population from the 1000 Genomes Project.\n                                ')

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Description'), 'Description', '__AbsentNamespace0_CTD_ANON_4_Description', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 138, 28), )

    
    Description = property(__Description.value, __Description.set, None, 'Informative paragraph')

    
    # Element ExternalLink uses Python identifier ExternalLink
    __ExternalLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ExternalLink'), 'ExternalLink', '__AbsentNamespace0_CTD_ANON_4_ExternalLink', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 143, 28), )

    
    ExternalLink = property(__ExternalLink.value, __ExternalLink.set, None, '\n                                        Link to external resources (as an URL) or to external databases (DB name, ID). \n                                        This is not a project-to-project relation.  \n                                        May be an URL to any external web resource or link to specified by name database. \n                                    ')

    
    # Element Grant uses Python identifier Grant
    __Grant = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Grant'), 'Grant', '__AbsentNamespace0_CTD_ANON_4_Grant', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 153, 28), )

    
    Grant = property(__Grant.value, __Grant.set, None, '\n                                    Funding information for a project. \n                                ')

    
    # Element Publication uses Python identifier Publication
    __Publication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Publication'), 'Publication', '__AbsentNamespace0_CTD_ANON_4_Publication', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 176, 28), )

    
    Publication = property(__Publication.value, __Publication.set, None, None)

    
    # Element ProjectReleaseDate uses Python identifier ProjectReleaseDate
    __ProjectReleaseDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectReleaseDate'), 'ProjectReleaseDate', '__AbsentNamespace0_CTD_ANON_4_ProjectReleaseDate', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 178, 28), )

    
    ProjectReleaseDate = property(__ProjectReleaseDate.value, __ProjectReleaseDate.set, None, 'Date of public release.')

    
    # Element Keyword uses Python identifier Keyword
    __Keyword = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Keyword'), 'Keyword', '__AbsentNamespace0_CTD_ANON_4_Keyword', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 183, 28), )

    
    Keyword = property(__Keyword.value, __Keyword.set, None, 'Intended to be used in support of queries')

    
    # Element Relevance uses Python identifier Relevance
    __Relevance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Relevance'), 'Relevance', '__AbsentNamespace0_CTD_ANON_4_Relevance', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 189, 28), )

    
    Relevance = property(__Relevance.value, __Relevance.set, None, 'Major impact categories for the project.')

    
    # Element LocusTagPrefix uses Python identifier LocusTagPrefix
    __LocusTagPrefix = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'LocusTagPrefix'), 'LocusTagPrefix', '__AbsentNamespace0_CTD_ANON_4_LocusTagPrefix', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 217, 28), )

    
    LocusTagPrefix = property(__LocusTagPrefix.value, __LocusTagPrefix.set, None, None)

    
    # Element UserTerm uses Python identifier UserTerm
    __UserTerm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'UserTerm'), 'UserTerm', '__AbsentNamespace0_CTD_ANON_4_UserTerm', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 219, 28), )

    
    UserTerm = property(__UserTerm.value, __UserTerm.set, None, '\n                                        Attribute represents a key ; element text() represents a value\n                                    ')

    
    # Element RefSeq uses Python identifier RefSeq
    __RefSeq = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RefSeq'), 'RefSeq', '__AbsentNamespace0_CTD_ANON_4_RefSeq', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 256, 28), )

    
    RefSeq = property(__RefSeq.value, __RefSeq.set, None, '\n                                        If element with "RefSeq" tag present, the project is a refseq project.  To be created by NCBI only.\n                                    ')

    _ElementMap.update({
        __Name.name() : __Name,
        __Title.name() : __Title,
        __Description.name() : __Description,
        __ExternalLink.name() : __ExternalLink,
        __Grant.name() : __Grant,
        __Publication.name() : __Publication,
        __ProjectReleaseDate.name() : __ProjectReleaseDate,
        __Keyword.name() : __Keyword,
        __Relevance.name() : __Relevance,
        __LocusTagPrefix.name() : __LocusTagPrefix,
        __UserTerm.name() : __UserTerm,
        __RefSeq.name() : __RefSeq
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """
                                    Funding information for a project. 
                                """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 159, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Title uses Python identifier Title
    __Title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Title'), 'Title', '__AbsentNamespace0_CTD_ANON_5_Title', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 161, 40), )

    
    Title = property(__Title.value, __Title.set, None, None)

    
    # Element Agency uses Python identifier Agency
    __Agency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Agency'), 'Agency', '__AbsentNamespace0_CTD_ANON_5_Agency', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 163, 40), )

    
    Agency = property(__Agency.value, __Agency.set, None, None)

    
    # Attribute GrantId uses Python identifier GrantId
    __GrantId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'GrantId'), 'GrantId', '__AbsentNamespace0_CTD_ANON_5_GrantId', pyxb.binding.datatypes.string, required=True)
    __GrantId._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 173, 36)
    __GrantId._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 173, 36)
    
    GrantId = property(__GrantId.value, __GrantId.set, None, None)

    _ElementMap.update({
        __Title.name() : __Title,
        __Agency.name() : __Agency
    })
    _AttributeMap.update({
        __GrantId.name() : __GrantId
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 164, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute abbr uses Python identifier abbr
    __abbr = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'abbr'), 'abbr', '__AbsentNamespace0_CTD_ANON_6_abbr', pyxb.binding.datatypes.string)
    __abbr._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 167, 50)
    __abbr._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 167, 50)
    
    abbr = property(__abbr.value, __abbr.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __abbr.name() : __abbr
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Major impact categories for the project."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 193, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Agricultural uses Python identifier Agricultural
    __Agricultural = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Agricultural'), 'Agricultural', '__AbsentNamespace0_CTD_ANON_7_Agricultural', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 195, 40), )

    
    Agricultural = property(__Agricultural.value, __Agricultural.set, None, None)

    
    # Element Medical uses Python identifier Medical
    __Medical = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Medical'), 'Medical', '__AbsentNamespace0_CTD_ANON_7_Medical', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 197, 40), )

    
    Medical = property(__Medical.value, __Medical.set, None, None)

    
    # Element Industrial uses Python identifier Industrial
    __Industrial = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Industrial'), 'Industrial', '__AbsentNamespace0_CTD_ANON_7_Industrial', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 198, 40), )

    
    Industrial = property(__Industrial.value, __Industrial.set, None, 'Could include bio-remediation, bio-fuels and other areas of research where there are areas of\n                                            mass production')

    
    # Element Environmental uses Python identifier Environmental
    __Environmental = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Environmental'), 'Environmental', '__AbsentNamespace0_CTD_ANON_7_Environmental', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 204, 40), )

    
    Environmental = property(__Environmental.value, __Environmental.set, None, None)

    
    # Element Evolution uses Python identifier Evolution
    __Evolution = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Evolution'), 'Evolution', '__AbsentNamespace0_CTD_ANON_7_Evolution', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 206, 40), )

    
    Evolution = property(__Evolution.value, __Evolution.set, None, None)

    
    # Element ModelOrganism uses Python identifier ModelOrganism
    __ModelOrganism = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ModelOrganism'), 'ModelOrganism', '__AbsentNamespace0_CTD_ANON_7_ModelOrganism', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 207, 40), )

    
    ModelOrganism = property(__ModelOrganism.value, __ModelOrganism.set, None, None)

    
    # Element Other uses Python identifier Other
    __Other = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Other'), 'Other', '__AbsentNamespace0_CTD_ANON_7_Other', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 209, 40), )

    
    Other = property(__Other.value, __Other.set, None, 'Unspecified major impact categories to be defined here.')

    _ElementMap.update({
        __Agricultural.name() : __Agricultural,
        __Medical.name() : __Medical,
        __Industrial.name() : __Industrial,
        __Environmental.name() : __Environmental,
        __Evolution.name() : __Evolution,
        __ModelOrganism.name() : __ModelOrganism,
        __Other.name() : __Other
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_7 = CTD_ANON_7


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """
                                        Attribute represents a key ; element text() represents a value
                                    """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 225, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute term uses Python identifier term
    __term = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'term'), 'term', '__AbsentNamespace0_CTD_ANON_8_term', pyxb.binding.datatypes.string, required=True)
    __term._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 228, 44)
    __term._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 228, 44)
    
    term = property(__term.value, __term.set, None, '\n                                                        Attribute represents a term\n                                                    ')

    
    # Attribute category uses Python identifier category
    __category = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'category'), 'category', '__AbsentNamespace0_CTD_ANON_8_category', pyxb.binding.datatypes.string)
    __category._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 236, 44)
    __category._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 236, 44)
    
    category = property(__category.value, __category.set, None, '\n                                                        Category to group the terms\n                                                    ')

    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'units'), 'units', '__AbsentNamespace0_CTD_ANON_8_units', pyxb.binding.datatypes.string)
    __units._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 244, 44)
    __units._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 244, 44)
    
    units = property(__units.value, __units.set, None, '\n                                                        Units - when value represent a measurement\n                                                    ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __term.name() : __term,
        __category.name() : __category,
        __units.name() : __units
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """
                           Project type specific fields. Created as "choice" - for future expansion.
                       """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 295, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ProjectTypeTopSingleOrganism uses Python identifier ProjectTypeTopSingleOrganism
    __ProjectTypeTopSingleOrganism = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectTypeTopSingleOrganism'), 'ProjectTypeTopSingleOrganism', '__AbsentNamespace0_CTD_ANON_9_ProjectTypeTopSingleOrganism', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 297, 28), )

    
    ProjectTypeTopSingleOrganism = property(__ProjectTypeTopSingleOrganism.value, __ProjectTypeTopSingleOrganism.set, None, '\n                                An administrative project with the following attributes:\n                                a.\tUnique tax_id is required.  This will generally be at the single species-level, but could be at sub-species or a level higher than species.  For example, with Canis lupus, dog is a sub-species of gray wolf.\n                                b.\tOnly one top single project for a tax_id\n                                c.\tOnly created by archive database collaborators (NCBI/EBI/DDBJ)\n                                d.\tTop-single includes a description of the organism \n                                e.\tIt may include structured descriptors; for instance, information about habitat, chromosomes (how many, what are they named), genome size etc. These descriptors are extendable.\n                                f.\tMay have 1 to many submitter-level project types attached\n                                g.\tAttached projects likely are not related by collaboration or funding (e.g. independent groups A, B, and C generate independent marker maps or transcriptome projects etc.)\n                            ')

    
    # Element ProjectTypeTopAdmin uses Python identifier ProjectTypeTopAdmin
    __ProjectTypeTopAdmin = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectTypeTopAdmin'), 'ProjectTypeTopAdmin', '__AbsentNamespace0_CTD_ANON_9_ProjectTypeTopAdmin', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 317, 28), )

    
    ProjectTypeTopAdmin = property(__ProjectTypeTopAdmin.value, __ProjectTypeTopAdmin.set, None, '\n                                An administrative project with the following attributes:\n                                a.\tTax_id is optional; may be a species- or higher-level tax_id (e.g., \u2018primates\u2019)\n                                b.\tPrimarily created by archive database collaborators (NCBI/EBI/DDBJ)\n                                c.\tSubmitters can request creation\n                                d.\tMay reflect a large multi-disciplinary project initiated by a funding agency \n                                e.\tOr, Arbitrary grouping; e.g. all sequences (from a grant) submitted by different process flows; any grouping that does not cleanly fit into the first two classes.\n                                f.\tMay have subtypes, e.g. a controlled vocabulary of descriptors including:\n                                            i.\tComparative genomics\n                                            ii.\tDisease\n                                            iii.\tMetagenome\n                            ')

    
    # Element ProjectTypeSubmission uses Python identifier ProjectTypeSubmission
    __ProjectTypeSubmission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProjectTypeSubmission'), 'ProjectTypeSubmission', '__AbsentNamespace0_CTD_ANON_9_ProjectTypeSubmission', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 363, 28), )

    
    ProjectTypeSubmission = property(__ProjectTypeSubmission.value, __ProjectTypeSubmission.set, None, '\n                                       A submitter level project based on actual experiment whose intent is to produce and submit data to one or more archives.                                         \n                                   ')

    _ElementMap.update({
        __ProjectTypeTopSingleOrganism.name() : __ProjectTypeTopSingleOrganism,
        __ProjectTypeTopAdmin.name() : __ProjectTypeTopAdmin,
        __ProjectTypeSubmission.name() : __ProjectTypeSubmission
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """
                                An administrative project with the following attributes:
                                a.	Unique tax_id is required.  This will generally be at the single species-level, but could be at sub-species or a level higher than species.  For example, with Canis lupus, dog is a sub-species of gray wolf.
                                b.	Only one top single project for a tax_id
                                c.	Only created by archive database collaborators (NCBI/EBI/DDBJ)
                                d.	Top-single includes a description of the organism 
                                e.	It may include structured descriptors; for instance, information about habitat, chromosomes (how many, what are they named), genome size etc. These descriptors are extendable.
                                f.	May have 1 to many submitter-level project types attached
                                g.	Attached projects likely are not related by collaboration or funding (e.g. independent groups A, B, and C generate independent marker maps or transcriptome projects etc.)
                            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 310, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Organism uses Python identifier Organism
    __Organism = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Organism'), 'Organism', '__AbsentNamespace0_CTD_ANON_10_Organism', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 312, 40), )

    
    Organism = property(__Organism.value, __Organism.set, None, None)

    _ElementMap.update({
        __Organism.name() : __Organism
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """
                                       A submitter level project based on actual experiment whose intent is to produce and submit data to one or more archives.                                         
                                   """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 369, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Target uses Python identifier Target
    __Target = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Target'), 'Target', '__AbsentNamespace0_CTD_ANON_11_Target', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 372, 40), )

    
    Target = property(__Target.value, __Target.set, None, '\n                                                   Target of the experiment. See @target_type for possible choices\n                                               ')

    
    # Element TargetBioSampleSet uses Python identifier TargetBioSampleSet
    __TargetBioSampleSet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TargetBioSampleSet'), 'TargetBioSampleSet', '__AbsentNamespace0_CTD_ANON_11_TargetBioSampleSet', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 536, 41), )

    
    TargetBioSampleSet = property(__TargetBioSampleSet.value, __TargetBioSampleSet.set, None, 'Set of Targets references to BioSamples')

    
    # Element Method uses Python identifier Method
    __Method = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Method'), 'Method', '__AbsentNamespace0_CTD_ANON_11_Method', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 545, 40), )

    
    Method = property(__Method.value, __Method.set, None, '\n                                                    The core experimental approach used to obtain the data that is submitted to archival databases\n                                               ')

    
    # Element Objectives uses Python identifier Objectives
    __Objectives = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Objectives'), 'Objectives', '__AbsentNamespace0_CTD_ANON_11_Objectives', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 584, 40), )

    
    Objectives = property(__Objectives.value, __Objectives.set, None, '\n                                                    The type of data that results from the experimental study; e.g., the type of data that will be submitted to archival databases\n                                                ')

    _ElementMap.update({
        __Target.name() : __Target,
        __TargetBioSampleSet.name() : __TargetBioSampleSet,
        __Method.name() : __Method,
        __Objectives.name() : __Objectives
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Set of Targets references to BioSamples"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 538, 45)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__AbsentNamespace0_CTD_ANON_12_ID', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 540, 0), )

    
    ID = property(__ID.value, __ID.set, None, None)

    _ElementMap.update({
        __ID.name() : __ID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_12 = CTD_ANON_12


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """
                                                    The type of data that results from the experimental study; e.g., the type of data that will be submitted to archival databases
                                                """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 590, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Data'), 'Data', '__AbsentNamespace0_CTD_ANON_13_Data', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 592, 50), )

    
    Data = property(__Data.value, __Data.set, None, None)

    _ElementMap.update({
        __Data.name() : __Data
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_13 = CTD_ANON_13


# Complex type typeRefSeqSource with content type ELEMENT_ONLY
class typeRefSeqSource (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typeRefSeqSource with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeRefSeqSource')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 709, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Name'), 'Name', '__AbsentNamespace0_typeRefSeqSource_Name', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 711, 12), )

    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Element Url uses Python identifier Url
    __Url = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Url'), 'Url', '__AbsentNamespace0_typeRefSeqSource_Url', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 712, 12), )

    
    Url = property(__Url.value, __Url.set, None, None)

    _ElementMap.update({
        __Name.name() : __Name,
        __Url.name() : __Url
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.typeRefSeqSource = typeRefSeqSource
Namespace.addCategoryObject('typeBinding', 'typeRefSeqSource', typeRefSeqSource)


# Complex type typePublication with content type ELEMENT_ONLY
class typePublication (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typePublication with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typePublication')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 715, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Reference uses Python identifier Reference
    __Reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Reference'), 'Reference', '__AbsentNamespace0_typePublication_Reference', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 717, 12), )

    
    Reference = property(__Reference.value, __Reference.set, None, 'Free form citation.')

    
    # Element DbType uses Python identifier DbType
    __DbType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DbType'), 'DbType', '__AbsentNamespace0_typePublication_DbType', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 722, 12), )

    
    DbType = property(__DbType.value, __DbType.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__AbsentNamespace0_typePublication_id', pyxb.binding.datatypes.int)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 732, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 732, 8)
    
    id = property(__id.value, __id.set, None, '\n                    Unique publication identifier in the specified database that is specific to the project.\n                ')

    
    # Attribute date uses Python identifier date
    __date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'date'), 'date', '__AbsentNamespace0_typePublication_date', pyxb.binding.datatypes.dateTime)
    __date._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 739, 8)
    __date._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 739, 8)
    
    date = property(__date.value, __date.set, None, 'Publication date.')

    _ElementMap.update({
        __Reference.name() : __Reference,
        __DbType.name() : __DbType
    })
    _AttributeMap.update({
        __id.name() : __id,
        __date.name() : __date
    })
_module_typeBindings.typePublication = typePublication
Namespace.addCategoryObject('typeBinding', 'typePublication', typePublication)


# Complex type typeExternalLink with content type ELEMENT_ONLY
class typeExternalLink (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typeExternalLink with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeExternalLink')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 745, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'URL'), 'URL', '__AbsentNamespace0_typeExternalLink_URL', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 747, 12), )

    
    URL = property(__URL.value, __URL.set, None, None)

    
    # Element dbXREF uses Python identifier dbXREF
    __dbXREF = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dbXREF'), 'dbXREF', '__AbsentNamespace0_typeExternalLink_dbXREF', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 748, 12), )

    
    dbXREF = property(__dbXREF.value, __dbXREF.set, None, None)

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label', '__AbsentNamespace0_typeExternalLink_label', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 767, 8)
    __label._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 767, 8)
    
    label = property(__label.value, __label.set, None, '\n                    Text which shown on the project presentation page for this link.\n                    \n                  \n                ')

    
    # Attribute category uses Python identifier category
    __category = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'category'), 'category', '__AbsentNamespace0_typeExternalLink_category', pyxb.binding.datatypes.string)
    __category._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 776, 8)
    __category._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 776, 8)
    
    category = property(__category.value, __category.set, None, None)

    _ElementMap.update({
        __URL.name() : __URL,
        __dbXREF.name() : __dbXREF
    })
    _AttributeMap.update({
        __label.name() : __label,
        __category.name() : __category
    })
_module_typeBindings.typeExternalLink = typeExternalLink
Namespace.addCategoryObject('typeBinding', 'typeExternalLink', typeExternalLink)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 749, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__AbsentNamespace0_CTD_ANON_14_ID', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 751, 24), )

    
    ID = property(__ID.value, __ID.set, None, '\n                                    Unique identifier in the specified database.  \n                                ')

    
    # Attribute db uses Python identifier db
    __db = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'db'), 'db', '__AbsentNamespace0_CTD_ANON_14_db', pyxb.binding.datatypes.string)
    __db._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 759, 20)
    __db._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 759, 20)
    
    db = property(__db.value, __db.set, None, 'The external database to which the ID is referring.')

    _ElementMap.update({
        __ID.name() : __ID
    })
    _AttributeMap.update({
        __db.name() : __db
    })
_module_typeBindings.CTD_ANON_14 = CTD_ANON_14


# Complex type typeOrganism with content type ELEMENT_ONLY
class typeOrganism (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typeOrganism with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeOrganism')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 778, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element OrganismName uses Python identifier OrganismName
    __OrganismName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'OrganismName'), 'OrganismName', '__AbsentNamespace0_typeOrganism_OrganismName', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 780, 12), )

    
    OrganismName = property(__OrganismName.value, __OrganismName.set, None, None)

    
    # Element Label uses Python identifier Label
    __Label = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Label'), 'Label', '__AbsentNamespace0_typeOrganism_Label', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 781, 12), )

    
    Label = property(__Label.value, __Label.set, None, '\n                        Used in situations to distinguish a project that is not a strain, breed or cultivar.  For example,\n                        this could be a common library name or a known sample name, such as Coco the gorilla.\n                    ')

    
    # Element Strain uses Python identifier Strain
    __Strain = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Strain'), 'Strain', '__AbsentNamespace0_typeOrganism_Strain', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 789, 12), )

    
    Strain = property(__Strain.value, __Strain.set, None, 'A strain, breed or cultivar.\n                    ')

    
    # Element Supergroup uses Python identifier Supergroup
    __Supergroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Supergroup'), 'Supergroup', '__AbsentNamespace0_typeOrganism_Supergroup', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 795, 12), )

    
    Supergroup = property(__Supergroup.value, __Supergroup.set, None, None)

    
    # Element BiologicalProperties uses Python identifier BiologicalProperties
    __BiologicalProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'BiologicalProperties'), 'BiologicalProperties', '__AbsentNamespace0_typeOrganism_BiologicalProperties', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 806, 12), )

    
    BiologicalProperties = property(__BiologicalProperties.value, __BiologicalProperties.set, None, '\n                        New items: Organism, Morphology, Environment, Phenotype, Relevance\n                    ')

    
    # Element Organization uses Python identifier Organization
    __Organization = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Organization'), 'Organization', '__AbsentNamespace0_typeOrganism_Organization', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1028, 12), )

    
    Organization = property(__Organization.value, __Organization.set, None, None)

    
    # Element Reproduction uses Python identifier Reproduction
    __Reproduction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Reproduction'), 'Reproduction', '__AbsentNamespace0_typeOrganism_Reproduction', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1037, 12), )

    
    Reproduction = property(__Reproduction.value, __Reproduction.set, None, None)

    
    # Element RepliconSet uses Python identifier RepliconSet
    __RepliconSet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RepliconSet'), 'RepliconSet', '__AbsentNamespace0_typeOrganism_RepliconSet', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1045, 12), )

    
    RepliconSet = property(__RepliconSet.value, __RepliconSet.set, None, None)

    
    # Element GenomeSize uses Python identifier GenomeSize
    __GenomeSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'GenomeSize'), 'GenomeSize', '__AbsentNamespace0_typeOrganism_GenomeSize', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1087, 12), )

    
    GenomeSize = property(__GenomeSize.value, __GenomeSize.set, None, None)

    
    # Attribute taxID uses Python identifier taxID
    __taxID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'taxID'), 'taxID', '__AbsentNamespace0_typeOrganism_taxID', pyxb.binding.datatypes.int)
    __taxID._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1089, 8)
    __taxID._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1089, 8)
    
    taxID = property(__taxID.value, __taxID.set, None, None)

    
    # Attribute species uses Python identifier species
    __species = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'species'), 'species', '__AbsentNamespace0_typeOrganism_species', pyxb.binding.datatypes.int)
    __species._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1090, 8)
    __species._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1090, 8)
    
    species = property(__species.value, __species.set, None, None)

    _ElementMap.update({
        __OrganismName.name() : __OrganismName,
        __Label.name() : __Label,
        __Strain.name() : __Strain,
        __Supergroup.name() : __Supergroup,
        __BiologicalProperties.name() : __BiologicalProperties,
        __Organization.name() : __Organization,
        __Reproduction.name() : __Reproduction,
        __RepliconSet.name() : __RepliconSet,
        __GenomeSize.name() : __GenomeSize
    })
    _AttributeMap.update({
        __taxID.name() : __taxID,
        __species.name() : __species
    })
_module_typeBindings.typeOrganism = typeOrganism
Namespace.addCategoryObject('typeBinding', 'typeOrganism', typeOrganism)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    """
                        New items: Organism, Morphology, Environment, Phenotype, Relevance
                    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 812, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Morphology uses Python identifier Morphology
    __Morphology = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Morphology'), 'Morphology', '__AbsentNamespace0_CTD_ANON_15_Morphology', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 814, 24), )

    
    Morphology = property(__Morphology.value, __Morphology.set, None, 'Physical attributes of the organism')

    
    # Element BiologicalSample uses Python identifier BiologicalSample
    __BiologicalSample = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'BiologicalSample'), 'BiologicalSample', '__AbsentNamespace0_CTD_ANON_15_BiologicalSample', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 913, 24), )

    
    BiologicalSample = property(__BiologicalSample.value, __BiologicalSample.set, None, None)

    
    # Element Environment uses Python identifier Environment
    __Environment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Environment'), 'Environment', '__AbsentNamespace0_CTD_ANON_15_Environment', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 939, 24), )

    
    Environment = property(__Environment.value, __Environment.set, None, None)

    
    # Element Phenotype uses Python identifier Phenotype
    __Phenotype = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Phenotype'), 'Phenotype', '__AbsentNamespace0_CTD_ANON_15_Phenotype', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 993, 24), )

    
    Phenotype = property(__Phenotype.value, __Phenotype.set, None, None)

    _ElementMap.update({
        __Morphology.name() : __Morphology,
        __BiologicalSample.name() : __BiologicalSample,
        __Environment.name() : __Environment,
        __Phenotype.name() : __Phenotype
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_15 = CTD_ANON_15


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    """Physical attributes of the organism"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 818, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Gram uses Python identifier Gram
    __Gram = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Gram'), 'Gram', '__AbsentNamespace0_CTD_ANON_16_Gram', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 820, 36), )

    
    Gram = property(__Gram.value, __Gram.set, None, None)

    
    # Element Enveloped uses Python identifier Enveloped
    __Enveloped = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Enveloped'), 'Enveloped', '__AbsentNamespace0_CTD_ANON_16_Enveloped', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 828, 36), )

    
    Enveloped = property(__Enveloped.value, __Enveloped.set, None, None)

    
    # Element Shape uses Python identifier Shape
    __Shape = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Shape'), 'Shape', '__AbsentNamespace0_CTD_ANON_16_Shape', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 836, 36), )

    
    Shape = property(__Shape.value, __Shape.set, None, None)

    
    # Element Endospores uses Python identifier Endospores
    __Endospores = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Endospores'), 'Endospores', '__AbsentNamespace0_CTD_ANON_16_Endospores', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 894, 36), )

    
    Endospores = property(__Endospores.value, __Endospores.set, None, None)

    
    # Element Motility uses Python identifier Motility
    __Motility = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Motility'), 'Motility', '__AbsentNamespace0_CTD_ANON_16_Motility', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 902, 36), )

    
    Motility = property(__Motility.value, __Motility.set, None, None)

    _ElementMap.update({
        __Gram.name() : __Gram,
        __Enveloped.name() : __Enveloped,
        __Shape.name() : __Shape,
        __Endospores.name() : __Endospores,
        __Motility.name() : __Motility
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_16 = CTD_ANON_16


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 914, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CultureSample uses Python identifier CultureSample
    __CultureSample = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CultureSample'), 'CultureSample', '__AbsentNamespace0_CTD_ANON_17_CultureSample', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 916, 36), )

    
    CultureSample = property(__CultureSample.value, __CultureSample.set, None, None)

    
    # Element CellSample uses Python identifier CellSample
    __CellSample = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CellSample'), 'CellSample', '__AbsentNamespace0_CTD_ANON_17_CellSample', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 925, 36), )

    
    CellSample = property(__CellSample.value, __CellSample.set, None, None)

    
    # Element TissueSample uses Python identifier TissueSample
    __TissueSample = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TissueSample'), 'TissueSample', '__AbsentNamespace0_CTD_ANON_17_TissueSample', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 934, 36), )

    
    TissueSample = property(__TissueSample.value, __TissueSample.set, None, None)

    _ElementMap.update({
        __CultureSample.name() : __CultureSample,
        __CellSample.name() : __CellSample,
        __TissueSample.name() : __TissueSample
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_17 = CTD_ANON_17


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 940, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Salinity uses Python identifier Salinity
    __Salinity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Salinity'), 'Salinity', '__AbsentNamespace0_CTD_ANON_18_Salinity', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 942, 36), )

    
    Salinity = property(__Salinity.value, __Salinity.set, None, None)

    
    # Element OxygenReq uses Python identifier OxygenReq
    __OxygenReq = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'OxygenReq'), 'OxygenReq', '__AbsentNamespace0_CTD_ANON_18_OxygenReq', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 953, 36), )

    
    OxygenReq = property(__OxygenReq.value, __OxygenReq.set, None, None)

    
    # Element OptimumTemperature uses Python identifier OptimumTemperature
    __OptimumTemperature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'OptimumTemperature'), 'OptimumTemperature', '__AbsentNamespace0_CTD_ANON_18_OptimumTemperature', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 964, 36), )

    
    OptimumTemperature = property(__OptimumTemperature.value, __OptimumTemperature.set, None, None)

    
    # Element TemperatureRange uses Python identifier TemperatureRange
    __TemperatureRange = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TemperatureRange'), 'TemperatureRange', '__AbsentNamespace0_CTD_ANON_18_TemperatureRange', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 966, 36), )

    
    TemperatureRange = property(__TemperatureRange.value, __TemperatureRange.set, None, None)

    
    # Element Habitat uses Python identifier Habitat
    __Habitat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Habitat'), 'Habitat', '__AbsentNamespace0_CTD_ANON_18_Habitat', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 978, 36), )

    
    Habitat = property(__Habitat.value, __Habitat.set, None, None)

    _ElementMap.update({
        __Salinity.name() : __Salinity,
        __OxygenReq.name() : __OxygenReq,
        __OptimumTemperature.name() : __OptimumTemperature,
        __TemperatureRange.name() : __TemperatureRange,
        __Habitat.name() : __Habitat
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_18 = CTD_ANON_18


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 994, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element BioticRelationship uses Python identifier BioticRelationship
    __BioticRelationship = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'BioticRelationship'), 'BioticRelationship', '__AbsentNamespace0_CTD_ANON_19_BioticRelationship', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 996, 36), )

    
    BioticRelationship = property(__BioticRelationship.value, __BioticRelationship.set, None, None)

    
    # Element TrophicLevel uses Python identifier TrophicLevel
    __TrophicLevel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TrophicLevel'), 'TrophicLevel', '__AbsentNamespace0_CTD_ANON_19_TrophicLevel', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1011, 36), )

    
    TrophicLevel = property(__TrophicLevel.value, __TrophicLevel.set, None, None)

    
    # Element Disease uses Python identifier Disease
    __Disease = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Disease'), 'Disease', '__AbsentNamespace0_CTD_ANON_19_Disease', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1020, 36), )

    
    Disease = property(__Disease.value, __Disease.set, None, None)

    _ElementMap.update({
        __BioticRelationship.name() : __BioticRelationship,
        __TrophicLevel.name() : __TrophicLevel,
        __Disease.name() : __Disease
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_19 = CTD_ANON_19


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1046, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Replicon uses Python identifier Replicon
    __Replicon = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Replicon'), 'Replicon', '__AbsentNamespace0_CTD_ANON_20_Replicon', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1048, 24), )

    
    Replicon = property(__Replicon.value, __Replicon.set, None, None)

    
    # Element Ploidy uses Python identifier Ploidy
    __Ploidy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Ploidy'), 'Ploidy', '__AbsentNamespace0_CTD_ANON_20_Ploidy', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1050, 24), )

    
    Ploidy = property(__Ploidy.value, __Ploidy.set, None, None)

    
    # Element Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Count'), 'Count', '__AbsentNamespace0_CTD_ANON_20_Count', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1068, 24), )

    
    Count = property(__Count.value, __Count.set, None, '\n                                    Number ot chromosomes for the project or organism per replicon type\n                                ')

    _ElementMap.update({
        __Replicon.name() : __Replicon,
        __Ploidy.name() : __Ploidy,
        __Count.name() : __Count
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_20 = CTD_ANON_20


# Complex type typeCenterID with content type SIMPLE
class typeCenterID (pyxb.binding.basis.complexTypeDefinition):
    """ 
                    Center-specific project IDs, assumed to be unique for a center. 
                """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeCenterID')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1153, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute center uses Python identifier center
    __center = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'center'), 'center', '__AbsentNamespace0_typeCenterID_center', pyxb.binding.datatypes.string, required=True)
    __center._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1161, 16)
    __center._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1161, 16)
    
    center = property(__center.value, __center.set, None, ' \n                                Center internal abbreviation for the project. \n                            ')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__AbsentNamespace0_typeCenterID_id', pyxb.binding.datatypes.integer)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1168, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1168, 16)
    
    id = property(__id.value, __id.set, None, ' \n                                Can have an integer synonym if needed.\n                            ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __center.name() : __center,
        __id.name() : __id
    })
_module_typeBindings.typeCenterID = typeCenterID
Namespace.addCategoryObject('typeBinding', 'typeCenterID', typeCenterID)


# Complex type typeLocalID with content type SIMPLE
class typeLocalID (pyxb.binding.basis.complexTypeDefinition):
    """Alternative internal IDs that may be optionally provided within a submission stream.
                For example, there may be a localID from the Center and a different localID from the submitting DAC."""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeLocalID')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1178, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.typeLocalID = typeLocalID
Namespace.addCategoryObject('typeBinding', 'typeLocalID', typeLocalID)


# Complex type typeReplicon with content type ELEMENT_ONLY
class typeReplicon (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typeReplicon with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeReplicon')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1236, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Type uses Python identifier Type
    __Type = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Type'), 'Type', '__AbsentNamespace0_typeReplicon_Type', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1238, 12), )

    
    Type = property(__Type.value, __Type.set, None, None)

    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Name'), 'Name', '__AbsentNamespace0_typeReplicon_Name', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1239, 12), )

    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Element Size uses Python identifier Size
    __Size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Size'), 'Size', '__AbsentNamespace0_typeReplicon_Size', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1240, 12), )

    
    Size = property(__Size.value, __Size.set, None, None)

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Description'), 'Description', '__AbsentNamespace0_typeReplicon_Description', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1241, 12), )

    
    Description = property(__Description.value, __Description.set, None, 'Explanation of an unusual chromosome features')

    
    # Element Synonym uses Python identifier Synonym
    __Synonym = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Synonym'), 'Synonym', '__AbsentNamespace0_typeReplicon_Synonym', True, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1246, 12), )

    
    Synonym = property(__Synonym.value, __Synonym.set, None, 'Optionally: List all accepted synonyms for this chromosome')

    
    # Attribute order uses Python identifier order
    __order = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'order'), 'order', '__AbsentNamespace0_typeReplicon_order', pyxb.binding.datatypes.token)
    __order._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1252, 8)
    __order._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1252, 8)
    
    order = property(__order.value, __order.set, None, 'Chromosome number for organisms whith established numbering system :1,2,3,X,Y')

    _ElementMap.update({
        __Type.name() : __Type,
        __Name.name() : __Name,
        __Size.name() : __Size,
        __Description.name() : __Description,
        __Synonym.name() : __Synonym
    })
    _AttributeMap.update({
        __order.name() : __order
    })
_module_typeBindings.typeReplicon = typeReplicon
Namespace.addCategoryObject('typeBinding', 'typeReplicon', typeReplicon)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    """
                        Information about owner and what to do with the package
                    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 32, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute owner uses Python identifier owner
    __owner = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'owner'), 'owner', '__AbsentNamespace0_CTD_ANON_21_owner', _module_typeBindings.typeArchive, required=True)
    __owner._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 33, 20)
    __owner._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 33, 20)
    
    owner = property(__owner.value, __owner.set, None, ' \n                                Owner of the package (host archive): NCBI, EMBL, DDBJ, .....\n                            ')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__AbsentNamespace0_CTD_ANON_21_id', pyxb.binding.datatypes.positiveInteger)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 40, 20)
    __id._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 40, 20)
    
    id = property(__id.value, __id.set, None, '\n                                Package ID; Optional\n                            ')

    
    # Attribute action uses Python identifier action
    __action = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'action'), 'action', '__AbsentNamespace0_CTD_ANON_21_action', _module_typeBindings.STD_ANON, required=True)
    __action._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 47, 20)
    __action._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 47, 20)
    
    action = property(__action.value, __action.set, None, '\n                                What to do with the package. \n                                Is it just info (eUnchanged), new data (eAdded), update of the existing data (eUpdated) or data to be deleted (eDeleted)\n                            ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __owner.name() : __owner,
        __id.name() : __id,
        __action.name() : __action
    })
_module_typeBindings.CTD_ANON_21 = CTD_ANON_21


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    """
                                        If element with "RefSeq" tag present, the project is a refseq project.  To be created by NCBI only.
                                    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 262, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element AnnotationSource uses Python identifier AnnotationSource
    __AnnotationSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AnnotationSource'), 'AnnotationSource', '__AbsentNamespace0_CTD_ANON_22_AnnotationSource', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 264, 40), )

    
    AnnotationSource = property(__AnnotationSource.value, __AnnotationSource.set, None, 'The source of the annotation.  For example, propogated from INSDC, RefSeq curation, etc.')

    
    # Element SequenceSource uses Python identifier SequenceSource
    __SequenceSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SequenceSource'), 'SequenceSource', '__AbsentNamespace0_CTD_ANON_22_SequenceSource', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 269, 40), )

    
    SequenceSource = property(__SequenceSource.value, __SequenceSource.set, None, 'Used sequence source')

    
    # Element NomenclatureSource uses Python identifier NomenclatureSource
    __NomenclatureSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NomenclatureSource'), 'NomenclatureSource', '__AbsentNamespace0_CTD_ANON_22_NomenclatureSource', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 275, 40), )

    
    NomenclatureSource = property(__NomenclatureSource.value, __NomenclatureSource.set, None, 'External authority (if one exists)')

    
    # Attribute representation uses Python identifier representation
    __representation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'representation'), 'representation', '__AbsentNamespace0_CTD_ANON_22_representation', _module_typeBindings.typeRepresentation)
    __representation._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 282, 36)
    __representation._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 282, 36)
    
    representation = property(__representation.value, __representation.set, None, None)

    _ElementMap.update({
        __AnnotationSource.name() : __AnnotationSource,
        __SequenceSource.name() : __SequenceSource,
        __NomenclatureSource.name() : __NomenclatureSource
    })
    _AttributeMap.update({
        __representation.name() : __representation
    })
_module_typeBindings.CTD_ANON_22 = CTD_ANON_22


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_23 (pyxb.binding.basis.complexTypeDefinition):
    """
                                An administrative project with the following attributes:
                                a.	Tax_id is optional; may be a species- or higher-level tax_id (e.g., ‘primates’)
                                b.	Primarily created by archive database collaborators (NCBI/EBI/DDBJ)
                                c.	Submitters can request creation
                                d.	May reflect a large multi-disciplinary project initiated by a funding agency 
                                e.	Or, Arbitrary grouping; e.g. all sequences (from a grant) submitted by different process flows; any grouping that does not cleanly fit into the first two classes.
                                f.	May have subtypes, e.g. a controlled vocabulary of descriptors including:
                                            i.	Comparative genomics
                                            ii.	Disease
                                            iii.	Metagenome
                            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 332, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Organism uses Python identifier Organism
    __Organism = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Organism'), 'Organism', '__AbsentNamespace0_CTD_ANON_23_Organism', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 334, 40), )

    
    Organism = property(__Organism.value, __Organism.set, None, None)

    
    # Element DescriptionSubtypeOther uses Python identifier DescriptionSubtypeOther
    __DescriptionSubtypeOther = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DescriptionSubtypeOther'), 'DescriptionSubtypeOther', '__AbsentNamespace0_CTD_ANON_23_DescriptionSubtypeOther', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 336, 40), )

    
    DescriptionSubtypeOther = property(__DescriptionSubtypeOther.value, __DescriptionSubtypeOther.set, None, '\n                                                    If subtype eOther is chosen, explain details here\n                                                ')

    
    # Attribute subtype uses Python identifier subtype
    __subtype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'subtype'), 'subtype', '__AbsentNamespace0_CTD_ANON_23_subtype', _module_typeBindings.STD_ANON_, required=True)
    __subtype._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 345, 36)
    __subtype._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 345, 36)
    
    subtype = property(__subtype.value, __subtype.set, None, None)

    _ElementMap.update({
        __Organism.name() : __Organism,
        __DescriptionSubtypeOther.name() : __DescriptionSubtypeOther
    })
    _AttributeMap.update({
        __subtype.name() : __subtype
    })
_module_typeBindings.CTD_ANON_23 = CTD_ANON_23


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_24 (pyxb.binding.basis.complexTypeDefinition):
    """
                                                   Target of the experiment. See @target_type for possible choices
                                               """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 378, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Organism uses Python identifier Organism
    __Organism = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Organism'), 'Organism', '__AbsentNamespace0_CTD_ANON_24_Organism', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 380, 50), )

    
    Organism = property(__Organism.value, __Organism.set, None, None)

    
    # Element Provider uses Python identifier Provider
    __Provider = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Provider'), 'Provider', '__AbsentNamespace0_CTD_ANON_24_Provider', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 382, 50), )

    
    Provider = property(__Provider.value, __Provider.set, None, '\n                                                               Source of biomaterial used as target for this data project\n                                                           ')

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Description'), 'Description', '__AbsentNamespace0_CTD_ANON_24_Description', False, pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 391, 50), )

    
    Description = property(__Description.value, __Description.set, None, '\n                                                               Optionally provide description especially when "eOther" is selected\n                                                           ')

    
    # Attribute sample_scope uses Python identifier sample_scope
    __sample_scope = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sample_scope'), 'sample_scope', '__AbsentNamespace0_CTD_ANON_24_sample_scope', _module_typeBindings.STD_ANON_2, required=True)
    __sample_scope._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 400, 48)
    __sample_scope._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 400, 48)
    
    sample_scope = property(__sample_scope.value, __sample_scope.set, None, '\n                                                            The scope and purity of the biological sample used for the study\n                                                        ')

    
    # Attribute material uses Python identifier material
    __material = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'material'), 'material', '__AbsentNamespace0_CTD_ANON_24_material', _module_typeBindings.STD_ANON_3, required=True)
    __material._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 441, 48)
    __material._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 441, 48)
    
    material = property(__material.value, __material.set, None, '\n                                                            The type of material that is isolated from the sample for the experimental study\n                                                        ')

    
    # Attribute capture uses Python identifier capture
    __capture = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'capture'), 'capture', '__AbsentNamespace0_CTD_ANON_24_capture', _module_typeBindings.STD_ANON_4, required=True)
    __capture._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 487, 48)
    __capture._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 487, 48)
    
    capture = property(__capture.value, __capture.set, None, '\n                                                            The scope of results that the experimental study is capturing, e.g. the focus of the study\n                                                        ')

    
    # Attribute biosample_id uses Python identifier biosample_id
    __biosample_id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'biosample_id'), 'biosample_id', '__AbsentNamespace0_CTD_ANON_24_biosample_id', pyxb.binding.datatypes.token)
    __biosample_id._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 526, 48)
    __biosample_id._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 526, 48)
    
    biosample_id = property(__biosample_id.value, __biosample_id.set, None, '\n                                                           Identifier of the BioSample when known\n                                                       ')

    _ElementMap.update({
        __Organism.name() : __Organism,
        __Provider.name() : __Provider,
        __Description.name() : __Description
    })
    _AttributeMap.update({
        __sample_scope.name() : __sample_scope,
        __material.name() : __material,
        __capture.name() : __capture,
        __biosample_id.name() : __biosample_id
    })
_module_typeBindings.CTD_ANON_24 = CTD_ANON_24


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_25 (pyxb.binding.basis.complexTypeDefinition):
    """
                                                    The core experimental approach used to obtain the data that is submitted to archival databases
                                               """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 551, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute method_type uses Python identifier method_type
    __method_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'method_type'), 'method_type', '__AbsentNamespace0_CTD_ANON_25_method_type', _module_typeBindings.STD_ANON_5, required=True)
    __method_type._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 554, 50)
    __method_type._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 554, 50)
    
    method_type = property(__method_type.value, __method_type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __method_type.name() : __method_type
    })
_module_typeBindings.CTD_ANON_25 = CTD_ANON_25


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_26 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 594, 50)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute data_type uses Python identifier data_type
    __data_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'data_type'), 'data_type', '__AbsentNamespace0_CTD_ANON_26_data_type', _module_typeBindings.STD_ANON_6)
    __data_type._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 597, 50)
    __data_type._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 597, 50)
    
    data_type = property(__data_type.value, __data_type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __data_type.name() : __data_type
    })
_module_typeBindings.CTD_ANON_26 = CTD_ANON_26


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_27 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1051, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_27_type', _module_typeBindings.STD_ANON_24, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1054, 40)
    __type._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1054, 40)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type
    })
_module_typeBindings.CTD_ANON_27 = CTD_ANON_27


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_28 (pyxb.binding.basis.complexTypeDefinition):
    """
                                    Number ot chromosomes for the project or organism per replicon type
                                """
    _TypeDefinition = pyxb.binding.datatypes.positiveInteger
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1074, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.positiveInteger
    
    # Attribute repliconType uses Python identifier repliconType
    __repliconType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'repliconType'), 'repliconType', '__AbsentNamespace0_CTD_ANON_28_repliconType', _module_typeBindings.typeRepliconMolType, required=True)
    __repliconType._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1077, 40)
    __repliconType._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1077, 40)
    
    repliconType = property(__repliconType.value, __repliconType.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __repliconType.name() : __repliconType
    })
_module_typeBindings.CTD_ANON_28 = CTD_ANON_28


# Complex type typeGSize with content type SIMPLE
class typeGSize (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typeGSize with content type SIMPLE"""
    _TypeDefinition = typeDecimalPositive
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeGSize')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1104, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is typeDecimalPositive
    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'units'), 'units', '__AbsentNamespace0_typeGSize_units', _module_typeBindings.STD_ANON_25)
    __units._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1107, 16)
    __units._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1107, 16)
    
    units = property(__units.value, __units.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __units.name() : __units
    })
_module_typeBindings.typeGSize = typeGSize
Namespace.addCategoryObject('typeBinding', 'typeGSize', typeGSize)


# Complex type typeArchiveID with content type EMPTY
class typeArchiveID (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typeArchiveID with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeArchiveID')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1130, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute archive uses Python identifier archive
    __archive = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'archive'), 'archive', '__AbsentNamespace0_typeArchiveID_archive', _module_typeBindings.typeArchive, required=True)
    __archive._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1131, 8)
    __archive._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1131, 8)
    
    archive = property(__archive.value, __archive.set, None, ' \n                    Host archive: NCBI, EMBL, DDBJ, .....\n                ')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__AbsentNamespace0_typeArchiveID_id', pyxb.binding.datatypes.integer)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1138, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1138, 8)
    
    id = property(__id.value, __id.set, None, ' \n                    Host archive integer id (projectID for NCBI), optional. May be assigned only by NCBI. Should be omitted when created by other archive and reassigned later by NCBI.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_typeArchiveID_accession', pyxb.binding.datatypes.string, required=True)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1145, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1145, 8)
    
    accession = property(__accession.value, __accession.set, None, '\n                    Required unique accession. For NCBI: PRJNA12345, for EMBL: PRJEA12345, for DDBJ: PRJDA12345, where 12345 is an archive-unique internal number\n                ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __archive.name() : __archive,
        __id.name() : __id,
        __accession.name() : __accession
    })
_module_typeBindings.typeArchiveID = typeArchiveID
Namespace.addCategoryObject('typeBinding', 'typeArchiveID', typeArchiveID)


# Complex type typeRepliconType with content type SIMPLE
class typeRepliconType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type typeRepliconType with content type SIMPLE"""
    _TypeDefinition = typeRepliconMolType
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeRepliconType')
    _XSDLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1196, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is typeRepliconMolType
    
    # Attribute location uses Python identifier location
    __location = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'location'), 'location', '__AbsentNamespace0_typeRepliconType_location', _module_typeBindings.STD_ANON_26, required=True)
    __location._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1204, 16)
    __location._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1204, 16)
    
    location = property(__location.value, __location.set, None, None)

    
    # Attribute isSingle uses Python identifier isSingle
    __isSingle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isSingle'), 'isSingle', '__AbsentNamespace0_typeRepliconType_isSingle', pyxb.binding.datatypes.boolean, required=True)
    __isSingle._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1229, 16)
    __isSingle._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1229, 16)
    
    isSingle = property(__isSingle.value, __isSingle.set, None, None)

    
    # Attribute typeOtherDescr uses Python identifier typeOtherDescr
    __typeOtherDescr = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'typeOtherDescr'), 'typeOtherDescr', '__AbsentNamespace0_typeRepliconType_typeOtherDescr', pyxb.binding.datatypes.string)
    __typeOtherDescr._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1230, 16)
    __typeOtherDescr._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1230, 16)
    
    typeOtherDescr = property(__typeOtherDescr.value, __typeOtherDescr.set, None, None)

    
    # Attribute locationOtherDescr uses Python identifier locationOtherDescr
    __locationOtherDescr = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'locationOtherDescr'), 'locationOtherDescr', '__AbsentNamespace0_typeRepliconType_locationOtherDescr', pyxb.binding.datatypes.string)
    __locationOtherDescr._DeclarationLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1231, 16)
    __locationOtherDescr._UseLocation = pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1231, 16)
    
    locationOtherDescr = property(__locationOtherDescr.value, __locationOtherDescr.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __location.name() : __location,
        __isSingle.name() : __isSingle,
        __typeOtherDescr.name() : __typeOtherDescr,
        __locationOtherDescr.name() : __locationOtherDescr
    })
_module_typeBindings.typeRepliconType = typeRepliconType
Namespace.addCategoryObject('typeBinding', 'typeRepliconType', typeRepliconType)


PackageSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PackageSet'), CTD_ANON, documentation='\n                Set of packages. \n            ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 5, 4))
Namespace.addCategoryObject('elementBinding', PackageSet.name().localName(), PackageSet)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Package'), typePackage, scope=CTD_ANON, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 13, 16)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'Package')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 13, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




typePackage._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Processing'), CTD_ANON_21, scope=typePackage, documentation='\n                        Information about owner and what to do with the package\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 26, 12)))

typePackage._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Project'), CTD_ANON_, scope=typePackage, documentation='\n                        Project core XML (see corresponding schema)\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 69, 12)))

typePackage._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectAssembly'), pyxb.binding.datatypes.anyType, scope=typePackage, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 682, 12)))

typePackage._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectSubmission'), pyxb.binding.datatypes.anyType, scope=typePackage, documentation='\n                        Unique for BioProject submission information, that is indicated in element Path in the main submission XML. \n                        For instance comments for DB staff in web submission form, etc.\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 685, 12)))

typePackage._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectLinks'), pyxb.binding.datatypes.anyType, scope=typePackage, documentation='\n                        Project links XML (see corresponding schema)\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 693, 12)))

typePackage._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectPresentation'), pyxb.binding.datatypes.anyType, scope=typePackage, documentation='\n                        Project core XML. Currenty not used.\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 700, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 26, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 69, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 682, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 685, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 693, 12))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 700, 12))
    counters.add(cc_5)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(typePackage._UseForTag(pyxb.namespace.ExpandedName(None, 'Processing')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 26, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(typePackage._UseForTag(pyxb.namespace.ExpandedName(None, 'Project')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 69, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(typePackage._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectAssembly')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 682, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(typePackage._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectSubmission')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 685, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(typePackage._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectLinks')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 693, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(typePackage._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectPresentation')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 700, 12))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
typePackage._Automaton = _BuildAutomaton_()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Project'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 76, 0)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'Project')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 76, 0))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_2()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectID'), CTD_ANON_3, scope=CTD_ANON_2, documentation='\n                        List of all project ids: submitter asigned, archive assigned, ....\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 79, 16)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectDescr'), CTD_ANON_4, scope=CTD_ANON_2, documentation='\n                            Common description of a project : title, publication, etc...\n                        ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 115, 16)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectType'), CTD_ANON_9, scope=CTD_ANON_2, documentation='\n                           Project type specific fields. Created as "choice" - for future expansion.\n                       ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 289, 16)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectID')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 79, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectDescr')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 115, 16))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectType')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 289, 16))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_3()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ArchiveID'), typeArchiveID, scope=CTD_ANON_3, documentation=' \n                                        Unique project identifier across all archives.\n                                        Contains host archive name, unique NCBI database ID (assigned only by NCBI DB staff) and unique accession (see accession description). \n                                        Element is optional since it will be created on submission. However it is required in the DB.\n                                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 92, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CenterID'), typeCenterID, scope=CTD_ANON_3, documentation=' \n                                    List of center-specific internal tracking IDs for the project.\n                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 102, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'LocalID'), typeLocalID, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 110, 28)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 92, 28))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 102, 28))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 110, 28))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'ArchiveID')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 92, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'CenterID')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 102, 28))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'LocalID')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 110, 28))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_4()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Name'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, documentation='\n                                    Very short descriptive name of the project  for caption, labels, etc.  For example:  1000 Genomes Project\n                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 123, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Title'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, documentation='\n                                    Short, but informative title of the projects, single phrase, single line. For example: \n                                    Sequencing the southern Chinese HAN population from the 1000 Genomes Project.\n                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 130, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Description'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, documentation='Informative paragraph', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 138, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ExternalLink'), typeExternalLink, scope=CTD_ANON_4, documentation='\n                                        Link to external resources (as an URL) or to external databases (DB name, ID). \n                                        This is not a project-to-project relation.  \n                                        May be an URL to any external web resource or link to specified by name database. \n                                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 143, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Grant'), CTD_ANON_5, scope=CTD_ANON_4, documentation='\n                                    Funding information for a project. \n                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 153, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Publication'), typePublication, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 176, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectReleaseDate'), pyxb.binding.datatypes.dateTime, scope=CTD_ANON_4, documentation='Date of public release.', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 178, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Keyword'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, documentation='Intended to be used in support of queries', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 183, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Relevance'), CTD_ANON_7, scope=CTD_ANON_4, documentation='Major impact categories for the project.', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 189, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'LocusTagPrefix'), typeLocusTagPrefix, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 217, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'UserTerm'), CTD_ANON_8, scope=CTD_ANON_4, documentation='\n                                        Attribute represents a key ; element text() represents a value\n                                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 219, 28)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RefSeq'), CTD_ANON_22, scope=CTD_ANON_4, documentation='\n                                        If element with "RefSeq" tag present, the project is a refseq project.  To be created by NCBI only.\n                                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 256, 28)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 123, 28))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 138, 28))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 143, 28))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 153, 28))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 176, 28))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 178, 28))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 183, 28))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 189, 28))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 217, 28))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 219, 28))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 256, 28))
    counters.add(cc_10)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'Name')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 123, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'Title')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 130, 28))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'Description')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 138, 28))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'ExternalLink')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 143, 28))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'Grant')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 153, 28))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'Publication')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 176, 28))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectReleaseDate')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 178, 28))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'Keyword')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 183, 28))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'Relevance')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 189, 28))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'LocusTagPrefix')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 217, 28))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'UserTerm')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 219, 28))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'RefSeq')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 256, 28))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, True) ]))
    st_11._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_5()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Title'), pyxb.binding.datatypes.string, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 161, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Agency'), CTD_ANON_6, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 163, 40)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 161, 40))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'Title')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 161, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'Agency')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 163, 40))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_6()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Agricultural'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 195, 40)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Medical'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 197, 40)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Industrial'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, documentation='Could include bio-remediation, bio-fuels and other areas of research where there are areas of\n                                            mass production', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 198, 40)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Environmental'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 204, 40)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Evolution'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 206, 40)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ModelOrganism'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 207, 40)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Other'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, documentation='Unspecified major impact categories to be defined here.', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 209, 40)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 195, 40))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 197, 40))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 198, 40))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 204, 40))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 206, 40))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 207, 40))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 209, 40))
    counters.add(cc_6)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'Agricultural')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 195, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'Medical')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 197, 40))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'Industrial')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 198, 40))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'Environmental')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 204, 40))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'Evolution')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 206, 40))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'ModelOrganism')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 207, 40))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'Other')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 209, 40))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_7()




CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectTypeTopSingleOrganism'), CTD_ANON_10, scope=CTD_ANON_9, documentation='\n                                An administrative project with the following attributes:\n                                a.\tUnique tax_id is required.  This will generally be at the single species-level, but could be at sub-species or a level higher than species.  For example, with Canis lupus, dog is a sub-species of gray wolf.\n                                b.\tOnly one top single project for a tax_id\n                                c.\tOnly created by archive database collaborators (NCBI/EBI/DDBJ)\n                                d.\tTop-single includes a description of the organism \n                                e.\tIt may include structured descriptors; for instance, information about habitat, chromosomes (how many, what are they named), genome size etc. These descriptors are extendable.\n                                f.\tMay have 1 to many submitter-level project types attached\n                                g.\tAttached projects likely are not related by collaboration or funding (e.g. independent groups A, B, and C generate independent marker maps or transcriptome projects etc.)\n                            ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 297, 28)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectTypeTopAdmin'), CTD_ANON_23, scope=CTD_ANON_9, documentation='\n                                An administrative project with the following attributes:\n                                a.\tTax_id is optional; may be a species- or higher-level tax_id (e.g., \u2018primates\u2019)\n                                b.\tPrimarily created by archive database collaborators (NCBI/EBI/DDBJ)\n                                c.\tSubmitters can request creation\n                                d.\tMay reflect a large multi-disciplinary project initiated by a funding agency \n                                e.\tOr, Arbitrary grouping; e.g. all sequences (from a grant) submitted by different process flows; any grouping that does not cleanly fit into the first two classes.\n                                f.\tMay have subtypes, e.g. a controlled vocabulary of descriptors including:\n                                            i.\tComparative genomics\n                                            ii.\tDisease\n                                            iii.\tMetagenome\n                            ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 317, 28)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProjectTypeSubmission'), CTD_ANON_11, scope=CTD_ANON_9, documentation='\n                                       A submitter level project based on actual experiment whose intent is to produce and submit data to one or more archives.                                         \n                                   ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 363, 28)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectTypeTopSingleOrganism')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 297, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectTypeTopAdmin')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 317, 28))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'ProjectTypeSubmission')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 363, 28))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_9._Automaton = _BuildAutomaton_8()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Organism'), typeOrganism, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 312, 40)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'Organism')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 312, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_9()




CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Target'), CTD_ANON_24, scope=CTD_ANON_11, documentation='\n                                                   Target of the experiment. See @target_type for possible choices\n                                               ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 372, 40)))

CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TargetBioSampleSet'), CTD_ANON_12, scope=CTD_ANON_11, documentation='Set of Targets references to BioSamples', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 536, 41)))

CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Method'), CTD_ANON_25, scope=CTD_ANON_11, documentation='\n                                                    The core experimental approach used to obtain the data that is submitted to archival databases\n                                               ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 545, 40)))

CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Objectives'), CTD_ANON_13, scope=CTD_ANON_11, documentation='\n                                                    The type of data that results from the experimental study; e.g., the type of data that will be submitted to archival databases\n                                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 584, 40)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'Target')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 372, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'TargetBioSampleSet')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 536, 41))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'Method')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 545, 40))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'Objectives')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 584, 40))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_11._Automaton = _BuildAutomaton_10()




CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ID'), pyxb.binding.datatypes.token, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 540, 0)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'ID')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 540, 0))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_12._Automaton = _BuildAutomaton_11()




CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Data'), CTD_ANON_26, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 592, 50)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'Data')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 592, 50))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_13._Automaton = _BuildAutomaton_12()




typeRefSeqSource._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Name'), pyxb.binding.datatypes.string, scope=typeRefSeqSource, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 711, 12)))

typeRefSeqSource._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Url'), pyxb.binding.datatypes.anyURI, scope=typeRefSeqSource, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 712, 12)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 712, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(typeRefSeqSource._UseForTag(pyxb.namespace.ExpandedName(None, 'Name')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 711, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(typeRefSeqSource._UseForTag(pyxb.namespace.ExpandedName(None, 'Url')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 712, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
typeRefSeqSource._Automaton = _BuildAutomaton_13()




typePublication._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Reference'), pyxb.binding.datatypes.string, scope=typePublication, documentation='Free form citation.', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 717, 12)))

typePublication._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DbType'), STD_ANON_7, scope=typePublication, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 722, 12)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(typePublication._UseForTag(pyxb.namespace.ExpandedName(None, 'Reference')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 717, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(typePublication._UseForTag(pyxb.namespace.ExpandedName(None, 'DbType')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 722, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
typePublication._Automaton = _BuildAutomaton_14()




typeExternalLink._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'URL'), pyxb.binding.datatypes.anyURI, scope=typeExternalLink, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 747, 12)))

typeExternalLink._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dbXREF'), CTD_ANON_14, scope=typeExternalLink, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 748, 12)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(typeExternalLink._UseForTag(pyxb.namespace.ExpandedName(None, 'URL')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 747, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(typeExternalLink._UseForTag(pyxb.namespace.ExpandedName(None, 'dbXREF')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 748, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
typeExternalLink._Automaton = _BuildAutomaton_15()




CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ID'), pyxb.binding.datatypes.string, scope=CTD_ANON_14, documentation='\n                                    Unique identifier in the specified database.  \n                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 751, 24)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, 'ID')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 751, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_14._Automaton = _BuildAutomaton_16()




typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'OrganismName'), pyxb.binding.datatypes.string, scope=typeOrganism, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 780, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Label'), pyxb.binding.datatypes.string, scope=typeOrganism, documentation='\n                        Used in situations to distinguish a project that is not a strain, breed or cultivar.  For example,\n                        this could be a common library name or a known sample name, such as Coco the gorilla.\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 781, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Strain'), pyxb.binding.datatypes.string, scope=typeOrganism, documentation='A strain, breed or cultivar.\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 789, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Supergroup'), STD_ANON_8, scope=typeOrganism, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 795, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'BiologicalProperties'), CTD_ANON_15, scope=typeOrganism, documentation='\n                        New items: Organism, Morphology, Environment, Phenotype, Relevance\n                    ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 806, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Organization'), STD_ANON_22, scope=typeOrganism, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1028, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Reproduction'), STD_ANON_23, scope=typeOrganism, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1037, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RepliconSet'), CTD_ANON_20, scope=typeOrganism, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1045, 12)))

typeOrganism._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'GenomeSize'), typeGSize, scope=typeOrganism, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1087, 12)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 781, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 789, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 795, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 806, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1028, 12))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1037, 12))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1045, 12))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1087, 12))
    counters.add(cc_7)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'OrganismName')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 780, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'Label')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 781, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'Strain')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 789, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'Supergroup')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 795, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'BiologicalProperties')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 806, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'Organization')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1028, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'Reproduction')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1037, 12))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'RepliconSet')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1045, 12))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(typeOrganism._UseForTag(pyxb.namespace.ExpandedName(None, 'GenomeSize')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1087, 12))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
typeOrganism._Automaton = _BuildAutomaton_17()




CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Morphology'), CTD_ANON_16, scope=CTD_ANON_15, documentation='Physical attributes of the organism', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 814, 24)))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'BiologicalSample'), CTD_ANON_17, scope=CTD_ANON_15, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 913, 24)))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Environment'), CTD_ANON_18, scope=CTD_ANON_15, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 939, 24)))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Phenotype'), CTD_ANON_19, scope=CTD_ANON_15, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 993, 24)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 814, 24))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 913, 24))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 939, 24))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 993, 24))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, 'Morphology')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 814, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, 'BiologicalSample')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 913, 24))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, 'Environment')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 939, 24))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, 'Phenotype')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 993, 24))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_15._Automaton = _BuildAutomaton_18()




CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Gram'), STD_ANON_9, scope=CTD_ANON_16, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 820, 36)))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Enveloped'), STD_ANON_10, scope=CTD_ANON_16, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 828, 36)))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Shape'), STD_ANON_11, scope=CTD_ANON_16, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 836, 36)))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Endospores'), STD_ANON_12, scope=CTD_ANON_16, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 894, 36)))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Motility'), STD_ANON_13, scope=CTD_ANON_16, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 902, 36)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 820, 36))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 828, 36))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 836, 36))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 894, 36))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 902, 36))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(None, 'Gram')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 820, 36))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(None, 'Enveloped')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 828, 36))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(None, 'Shape')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 836, 36))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(None, 'Endospores')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 894, 36))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(None, 'Motility')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 902, 36))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_16._Automaton = _BuildAutomaton_19()




CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CultureSample'), STD_ANON_14, scope=CTD_ANON_17, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 916, 36)))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CellSample'), STD_ANON_15, scope=CTD_ANON_17, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 925, 36)))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TissueSample'), pyxb.binding.datatypes.string, scope=CTD_ANON_17, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 934, 36)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 916, 36))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 925, 36))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 934, 36))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(None, 'CultureSample')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 916, 36))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(None, 'CellSample')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 925, 36))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(None, 'TissueSample')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 934, 36))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_17._Automaton = _BuildAutomaton_20()




CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Salinity'), STD_ANON_16, scope=CTD_ANON_18, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 942, 36)))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'OxygenReq'), STD_ANON_17, scope=CTD_ANON_18, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 953, 36)))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'OptimumTemperature'), pyxb.binding.datatypes.string, scope=CTD_ANON_18, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 964, 36)))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TemperatureRange'), STD_ANON_18, scope=CTD_ANON_18, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 966, 36)))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Habitat'), STD_ANON_19, scope=CTD_ANON_18, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 978, 36)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 942, 36))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 953, 36))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 964, 36))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 966, 36))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 978, 36))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(None, 'Salinity')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 942, 36))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(None, 'OxygenReq')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 953, 36))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(None, 'OptimumTemperature')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 964, 36))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(None, 'TemperatureRange')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 966, 36))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(None, 'Habitat')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 978, 36))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_18._Automaton = _BuildAutomaton_21()




CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'BioticRelationship'), STD_ANON_20, scope=CTD_ANON_19, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 996, 36)))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TrophicLevel'), STD_ANON_21, scope=CTD_ANON_19, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1011, 36)))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Disease'), pyxb.binding.datatypes.string, scope=CTD_ANON_19, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1020, 36)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 996, 36))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1011, 36))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1020, 36))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(None, 'BioticRelationship')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 996, 36))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(None, 'TrophicLevel')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1011, 36))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(None, 'Disease')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1020, 36))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_19._Automaton = _BuildAutomaton_22()




CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Replicon'), typeReplicon, scope=CTD_ANON_20, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1048, 24)))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Ploidy'), CTD_ANON_27, scope=CTD_ANON_20, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1050, 24)))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Count'), CTD_ANON_28, scope=CTD_ANON_20, documentation='\n                                    Number ot chromosomes for the project or organism per replicon type\n                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1068, 24)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1048, 24))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1050, 24))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1068, 24))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, 'Replicon')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1048, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, 'Ploidy')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1050, 24))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, 'Count')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1068, 24))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_20._Automaton = _BuildAutomaton_23()




typeReplicon._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Type'), typeRepliconType, scope=typeReplicon, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1238, 12)))

typeReplicon._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Name'), pyxb.binding.datatypes.string, scope=typeReplicon, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1239, 12)))

typeReplicon._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Size'), typeGSize, scope=typeReplicon, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1240, 12)))

typeReplicon._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Description'), pyxb.binding.datatypes.string, scope=typeReplicon, documentation='Explanation of an unusual chromosome features', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1241, 12)))

typeReplicon._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Synonym'), pyxb.binding.datatypes.string, scope=typeReplicon, documentation='Optionally: List all accepted synonyms for this chromosome', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1246, 12)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1240, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1241, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1246, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(typeReplicon._UseForTag(pyxb.namespace.ExpandedName(None, 'Type')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1238, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(typeReplicon._UseForTag(pyxb.namespace.ExpandedName(None, 'Name')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1239, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(typeReplicon._UseForTag(pyxb.namespace.ExpandedName(None, 'Size')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1240, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(typeReplicon._UseForTag(pyxb.namespace.ExpandedName(None, 'Description')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1241, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(typeReplicon._UseForTag(pyxb.namespace.ExpandedName(None, 'Synonym')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 1246, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
typeReplicon._Automaton = _BuildAutomaton_24()




CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AnnotationSource'), typeRefSeqSource, scope=CTD_ANON_22, documentation='The source of the annotation.  For example, propogated from INSDC, RefSeq curation, etc.', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 264, 40)))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SequenceSource'), typeRefSeqSource, scope=CTD_ANON_22, documentation='Used sequence source', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 269, 40)))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NomenclatureSource'), typeRefSeqSource, scope=CTD_ANON_22, documentation='External authority (if one exists)', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 275, 40)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 269, 40))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 275, 40))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(None, 'AnnotationSource')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 264, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(None, 'SequenceSource')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 269, 40))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(None, 'NomenclatureSource')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 275, 40))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_22._Automaton = _BuildAutomaton_25()




CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Organism'), typeOrganism, scope=CTD_ANON_23, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 334, 40)))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DescriptionSubtypeOther'), pyxb.binding.datatypes.string, scope=CTD_ANON_23, documentation='\n                                                    If subtype eOther is chosen, explain details here\n                                                ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 336, 40)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 334, 40))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 336, 40))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(None, 'Organism')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 334, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(None, 'DescriptionSubtypeOther')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 336, 40))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_23._Automaton = _BuildAutomaton_26()




CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Organism'), typeOrganism, scope=CTD_ANON_24, location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 380, 50)))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Provider'), pyxb.binding.datatypes.string, scope=CTD_ANON_24, documentation='\n                                                               Source of biomaterial used as target for this data project\n                                                           ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 382, 50)))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Description'), pyxb.binding.datatypes.string, scope=CTD_ANON_24, documentation='\n                                                               Optionally provide description especially when "eOther" is selected\n                                                           ', location=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 391, 50)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 380, 50))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 382, 50))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 391, 50))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(None, 'Organism')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 380, 50))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(None, 'Provider')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 382, 50))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(None, 'Description')), pyxb.utils.utility.Location('/virtualenvs/dnaorder/include/dnaorder/dnaorder/core_bioproject.xsd', 391, 50))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_24._Automaton = _BuildAutomaton_27()

