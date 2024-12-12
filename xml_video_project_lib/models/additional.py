from lxml import etree as ET

class Filter:
    def __init__(self, name, effectid, effectcategory, effecttype, mediatype, pproBypass, parameters):
        self.name = name
        self.effectid = effectid
        self.effectcategory = effectcategory
        self.effecttype = effecttype
        self.mediatype = mediatype
        self.pproBypass = pproBypass
        self.parameters = parameters  # List of Parameter objects

    def to_xml(self):
        filter_el = ET.Element('filter')
        effect_el = ET.SubElement(filter_el, 'effect')
        name_el = ET.SubElement(effect_el, 'name')
        name_el.text = self.name

        effectid_el = ET.SubElement(effect_el, 'effectid')
        effectid_el.text = self.effectid

        effectcategory_el = ET.SubElement(effect_el, 'effectcategory')
        effectcategory_el.text = self.effectcategory

        effecttype_el = ET.SubElement(effect_el, 'effecttype')
        effecttype_el.text = self.effecttype

        mediatype_el = ET.SubElement(effect_el, 'mediatype')
        mediatype_el.text = self.mediatype

        pproBypass_el = ET.SubElement(effect_el, 'pproBypass')
        pproBypass_el.text = self.pproBypass

        for param in self.parameters:
            effect_el.append(param.to_xml())

        return filter_el


class Parameter:
    def __init__(self, parameterid, name, valuemin=None, valuemax=None, value=None, authoringApp="PremierePro"):
        self.parameterid = parameterid
        self.name = name
        self.valuemin = valuemin
        self.valuemax = valuemax
        self.value = value
        self.authoringApp = authoringApp

    def to_xml(self):
        parameter_el = ET.Element('parameter', authoringApp=self.authoringApp)
        parameterid_el = ET.SubElement(parameter_el, 'parameterid')
        parameterid_el.text = self.parameterid

        name_el = ET.SubElement(parameter_el, 'name')
        name_el.text = self.name

        if self.valuemin is not None:
            valuemin_el = ET.SubElement(parameter_el, 'valuemin')
            valuemin_el.text = str(self.valuemin)

        if self.valuemax is not None:
            valuemax_el = ET.SubElement(parameter_el, 'valuemax')
            valuemax_el.text = str(self.valuemax)

        if self.value is not None:
            value_el = ET.SubElement(parameter_el, 'value')
            value_el.text = str(self.value)

        return parameter_el


class Link:
    def __init__(self, linkclipref, mediatype, trackindex, clipindex, groupindex):
        self.linkclipref = linkclipref
        self.mediatype = mediatype
        self.trackindex = trackindex
        self.clipindex = clipindex
        self.groupindex = groupindex

    def to_xml(self):
        link_el = ET.Element('link')
        linkclipref_el = ET.SubElement(link_el, 'linkclipref')
        linkclipref_el.text = self.linkclipref

        mediatype_el = ET.SubElement(link_el, 'mediatype')
        mediatype_el.text = self.mediatype

        trackindex_el = ET.SubElement(link_el, 'trackindex')
        trackindex_el.text = str(self.trackindex)

        clipindex_el = ET.SubElement(link_el, 'clipindex')
        clipindex_el.text = str(self.clipindex)

        groupindex_el = ET.SubElement(link_el, 'groupindex')
        groupindex_el.text = str(self.groupindex)

        return link_el