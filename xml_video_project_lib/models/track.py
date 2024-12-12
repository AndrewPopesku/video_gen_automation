from lxml import etree as ET
from xml_video_project_lib.config import config
from xml_video_project_lib.models.base import XMElement
from xml_video_project_lib.models import ClipItem

class Track(XMElement):
    def __init__(
            self, 
            MZ_TrackTargeted, 
            premiereTrackType,
            outputchannelindex
        ):
        self.attributes = config.get_all('Track Attributes')
        self.MZ_TrackTargeted = MZ_TrackTargeted, 
        self.premiereTrackType = premiereTrackType,
        self.outputchannelindex = outputchannelindex
        self.clipitems = []  # List of ClipItems

    def add_clipitem(self, clipitem: ClipItem):
        self.clipitems.append(clipitem)

    def to_xml(self):
        track_el = ET.Element('track', **self.attributes)
        for clipitem in self.clipitems:
            track_el.append(clipitem.to_xml())
        enabled_el = ET.SubElement(track_el, 'enabled')
        enabled_el.text = "TRUE"
        locked_el = ET.SubElement(track_el, 'locked')
        locked_el.text = "FALSE"
        outputchannelindex_el = ET.SubElement(track_el, 'outputchannelindex')
        outputchannelindex_el.text = self.outputchannelindex
        return track_el