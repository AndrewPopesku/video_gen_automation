from lxml import etree as ET
from xml_video_project_lib.models.base import XMElement

class Timecode(XMElement):
    def __init__(self, timebase=30, ntsc="TRUE", string="00;00;00;00", frame="0", displayformat="DF"):
        self.timebase = timebase
        self.ntsc = ntsc
        self.string = string
        self.frame = frame
        self.displayformat = displayformat

    def to_xml(self):
        timecode_el = ET.Element('timecode')
        rate_el = ET.SubElement(timecode_el, 'rate')
        timebase_el = ET.SubElement(rate_el, 'timebase')
        timebase_el.text = str(self.timebase)
        ntsc_el = ET.SubElement(rate_el, 'ntsc')
        ntsc_el.text = self.ntsc

        string_el = ET.SubElement(timecode_el, 'string')
        string_el.text = self.string
        frame_el = ET.SubElement(timecode_el, 'frame')
        frame_el.text = self.frame
        displayformat_el = ET.SubElement(timecode_el, 'displayformat')
        displayformat_el.text = self.displayformat

        return timecode_el
