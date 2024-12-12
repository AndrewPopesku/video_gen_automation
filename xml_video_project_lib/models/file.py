from lxml import etree as ET
from xml_video_project_lib.models.base import XMElement

class File(XMElement):
    def __init__(self, id, name, pathurl, samplerate, channelcount, mediatype="audio", width=None, height=None):
        self.id = id
        self.name = name
        self.pathurl = pathurl
        self.samplerate = samplerate
        self.channelcount = channelcount
        self.mediatype = mediatype  # "audio" or "video"
        self.width = width
        self.height = height

    def to_xml(self):
        file_el = ET.Element('file', id=self.id)
        name_el = ET.SubElement(file_el, 'name')
        name_el.text = self.name

        pathurl_el = ET.SubElement(file_el, 'pathurl')
        pathurl_el.text = self.pathurl

        media_el = ET.SubElement(file_el, 'media')
        if self.mediatype == "audio":
            audio_el = ET.SubElement(media_el, 'audio')
            sample_characteristics = ET.SubElement(audio_el, 'samplecharacteristics')
            depth_el = ET.SubElement(sample_characteristics, 'depth')
            depth_el.text = "16"
            samplerate_el = ET.SubElement(sample_characteristics, 'samplerate')
            samplerate_el.text = str(self.samplerate)
            channelcount_el = ET.SubElement(audio_el, 'channelcount')
            channelcount_el.text = str(self.channelcount)
        elif self.mediatype == "video":
            video_el = ET.SubElement(media_el, 'video')
            sample_characteristics = ET.SubElement(video_el, 'samplecharacteristics')
            rate_el = ET.SubElement(sample_characteristics, 'rate')
            timebase_el = ET.SubElement(rate_el, 'timebase')
            timebase_el.text = "30"
            ntsc_el = ET.SubElement(rate_el, 'ntsc')
            ntsc_el.text = "FALSE"  # Adjust as needed

            width_el = ET.SubElement(sample_characteristics, 'width')
            width_el.text = str(self.width if self.width else 1280)
            height_el = ET.SubElement(sample_characteristics, 'height')
            height_el.text = str(self.height if self.height else 720)
            anamorphic_el = ET.SubElement(sample_characteristics, 'anamorphic')
            anamorphic_el.text = "FALSE"
            pixelaspectratio_el = ET.SubElement(sample_characteristics, 'pixelaspectratio')
            pixelaspectratio_el.text = "square"
            fielddominance_el = ET.SubElement(sample_characteristics, 'fielddominance')
            fielddominance_el.text = "none"
            colordepth_el = ET.SubElement(sample_characteristics, 'colordepth')
            colordepth_el.text = "24"

        return file_el