from lxml import etree as ET
from xml_video_project_lib.models.base import XMElement

class LoggingInfo(XMElement):
    def __init__(self):
        self.description = ""
        self.scene = ""
        self.shottake = ""
        self.lognote = ""
        self.good = ""
        self.originalvideofilename = ""
        self.originalaudiofilename = ""

    def to_xml(self):
        logginginfo_el = ET.Element('logginginfo')
        for field in ['description', 'scene', 'shottake', 'lognote', 'good', 'originalvideofilename', 'originalaudiofilename']:
            el = ET.SubElement(logginginfo_el, field)
            el.text = getattr(self, field)
        return logginginfo_el