from lxml import etree as ET
from xml_video_project_lib.models.audio import Audio
from xml_video_project_lib.models.base import XMElement
from xml_video_project_lib.models.video import Video

class Media(XMElement):
    def __init__(self):
        self.video = None
        self.audio = None

    def add_video(self, video: Video):
        self.video = video

    def add_audio(self, audio: Audio):
        self.audio = audio

    def to_xml(self):
        media_el = ET.Element('media')
        if self.video:
            media_el.append(self.video.to_xml())
        if self.audio:
            media_el.append(self.audio.to_xml())
        return media_el
