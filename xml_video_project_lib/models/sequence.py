from lxml import etree as ET
from xml_video_project_lib.config import config
from xml_video_project_lib.models.base import XMElement
from xml_video_project_lib.models import Media, Timecode, Audio, Video, LoggingInfo

class Sequence(XMElement):
    def __init__(
            self, 
            id, 
            uuid,
            name, 
            duration, 
            rate_timebase=config.get('Sequence Rate', 'rate_timebase', type_cast=int),
            rate_ntsc=config.get('Sequence Rate', 'rate_ntsc'),
            attributes=config.get_all('Sequence Attributes')
        ):
        # attributes dict can contain additional keys like the TL.* and MZ.* attributes
        self.id = id
        self.uuid = uuid
        self.duration = duration
        self.rate_timebase = rate_timebase
        self.rate_ntsc = rate_ntsc
        self.name = name
        self.media = Media()
        self.timecode = Timecode(timebase=rate_timebase, ntsc=rate_ntsc)
        self.logginginfo = LoggingInfo()
        self.attributes = attributes

    def add_video(self, video: Video):
        self.media.add_video(video)

    def add_audio(self, audio: Audio):
        self.media.add_audio(audio)

    def to_xml(self):
        sequence_el = ET.Element('sequence', id=self.id, **self.attributes)

        uuid_el = ET.SubElement(sequence_el, 'uuid')
        uuid_el.text = str(self.uuid)

        duration_el = ET.SubElement(sequence_el, 'duration')
        duration_el.text = str(self.duration)

        rate_el = ET.SubElement(sequence_el, 'rate')
        timebase_el = ET.SubElement(rate_el, 'timebase')
        timebase_el.text = str(self.rate_timebase)
        ntsc_el = ET.SubElement(rate_el, 'ntsc')
        ntsc_el.text = self.rate_ntsc

        name_el = ET.SubElement(sequence_el, 'name')
        name_el.text = self.name

        # Media
        sequence_el.append(self.media.to_xml())

        # Timecode
        sequence_el.append(self.timecode.to_xml())

        # Logging Info
        sequence_el.append(self.logginginfo.to_xml())

        return sequence_el

