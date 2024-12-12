from lxml import etree as ET
from xml_video_project_lib.models.base import XMElement
from xml_video_project_lib.models.file import File

class ClipItem(XMElement):
    def __init__(self, id, premiereChannelType, masterclipid, name, enabled, duration, rate_timebase,
                 rate_ntsc, start, end, in_point, out_point, pproTicksIn, pproTicksOut, file: File,
                 sourcetrack_mediatype, sourcetrack_trackindex, label2, alphatype="none", filters=None, links=None):
        self.id = id
        self.premiereChannelType = premiereChannelType
        self.masterclipid = masterclipid
        self.name = name
        self.enabled = enabled
        self.duration = duration
        self.rate_timebase = rate_timebase
        self.rate_ntsc = rate_ntsc
        self.start = start
        self.end = end
        self.in_point = in_point
        self.out_point = out_point
        self.pproTicksIn = pproTicksIn
        self.pproTicksOut = pproTicksOut
        self.file = file
        self.sourcetrack_mediatype = sourcetrack_mediatype  # "audio" or "video"
        self.sourcetrack_trackindex = sourcetrack_trackindex
        self.label2 = label2
        self.alphatype = alphatype
        self.filters = filters if filters else []  # List of Filter objects
        self.links = links if links else []      # List of Link objects

    def to_xml(self):
        clipitem_el = ET.Element('clipitem', id=self.id, premiereChannelType=self.premiereChannelType)
        masterclipid_el = ET.SubElement(clipitem_el, 'masterclipid')
        masterclipid_el.text = self.masterclipid

        name_el = ET.SubElement(clipitem_el, 'name')
        name_el.text = self.name

        enabled_el = ET.SubElement(clipitem_el, 'enabled')
        enabled_el.text = self.enabled

        duration_el = ET.SubElement(clipitem_el, 'duration')
        duration_el.text = str(self.duration)

        rate_el = ET.SubElement(clipitem_el, 'rate')
        timebase_el = ET.SubElement(rate_el, 'timebase')
        timebase_el.text = self.rate_timebase
        ntsc_el = ET.SubElement(rate_el, 'ntsc')
        ntsc_el.text = self.rate_ntsc

        start_el = ET.SubElement(clipitem_el, 'start')
        start_el.text = self.start
        end_el = ET.SubElement(clipitem_el, 'end')
        end_el.text = self.end
        in_el = ET.SubElement(clipitem_el, 'in')
        in_el.text = self.in_point
        out_el = ET.SubElement(clipitem_el, 'out')
        out_el.text = self.out_point

        pproTicksIn_el = ET.SubElement(clipitem_el, 'pproTicksIn')
        pproTicksIn_el.text = self.pproTicksIn
        pproTicksOut_el = ET.SubElement(clipitem_el, 'pproTicksOut')
        pproTicksOut_el.text = self.pproTicksOut

        # Add File
        clipitem_el.append(self.file.to_xml())

        # sourcetrack
        sourcetrack_el = ET.SubElement(clipitem_el, 'sourcetrack')
        mediatype_el = ET.SubElement(sourcetrack_el, 'mediatype')
        mediatype_el.text = self.sourcetrack_mediatype
        trackindex_el = ET.SubElement(sourcetrack_el, 'trackindex')
        trackindex_el.text = str(self.sourcetrack_trackindex)

        # alphatype
        alphatype_el = ET.SubElement(clipitem_el, 'alphatype')
        alphatype_el.text = self.alphatype

        # logginginfo
        logginginfo_el = ET.SubElement(clipitem_el, 'logginginfo')
        for field in ['description', 'scene', 'shottake', 'lognote', 'good', 'originalvideofilename', 'originalaudiofilename']:
            el = ET.SubElement(logginginfo_el, field)
            el.text = ""

        # colorinfo
        colorinfo_el = ET.SubElement(clipitem_el, 'colorinfo')
        for lut in ['lut', 'lut1', 'asc_sop', 'asc_sat', 'lut2']:
            el = ET.SubElement(colorinfo_el, lut)
            el.text = ""

        # labels
        labels_el = ET.SubElement(clipitem_el, 'labels')
        label2_el = ET.SubElement(labels_el, 'label2')
        label2_el.text = self.label2

        # filters
        for filter_obj in self.filters:
            clipitem_el.append(filter_obj.to_xml())

        # links
        for link_obj in self.links:
            clipitem_el.append(link_obj.to_xml())

        return clipitem_el