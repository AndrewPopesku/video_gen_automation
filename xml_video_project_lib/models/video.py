from lxml import etree as ET
from xml_video_project_lib.config import config
from xml_video_project_lib.models import Track
from xml_video_project_lib.models.base import XMElement

class Video(XMElement):
    def __init__(
            self, 
            name=config.get('Video', 'name'), 
            width=config.get('Video', 'width', type_cast=int), 
            height=config.get('Video', 'height', type_cast=int)
        ):
        self.name = name
        self.width = width
        self.height = height
        self.format_details = {}
        self.tracks = []
        self.set_format(
            {
                "rate_timebase": config.get('Sequence Rate', "rate_timebase"),
                "rate_ntsc": config.get('Sequence Rate', "rate_ntsc")
            }
        )

    def set_format(self, sample_characteristics):
        self.format_details = sample_characteristics

    def add_track(self, track: Track):
        self.tracks.append(track)

    def to_xml(self):
        video_el = ET.Element('video')

        # format
        format_el = ET.SubElement(video_el, 'format')
        sample_characteristics_el = ET.SubElement(format_el, 'samplecharacteristics')

        # rate
        rate_el = ET.SubElement(sample_characteristics_el, 'rate')
        timebase_el = ET.SubElement(rate_el, 'timebase')
        timebase_el.text = self.format_details.get('rate_timebase', "30")
        ntsc_el = ET.SubElement(rate_el, 'ntsc')
        ntsc_el.text = self.format_details.get('rate_ntsc', "TRUE")

        # codec
        codec_el = ET.SubElement(sample_characteristics_el, 'codec')
        codec_name_el = ET.SubElement(codec_el, 'name')
        codec_name_el.text = self.name

        # appspecificdata
        appspecificdata_el = ET.SubElement(codec_el, 'appspecificdata')
        appname_el = ET.SubElement(appspecificdata_el, 'appname')
        appname_el.text = "Final Cut Pro"
        appmanufacturer_el = ET.SubElement(appspecificdata_el, 'appmanufacturer')
        appmanufacturer_el.text = "Apple Inc."
        appversion_el = ET.SubElement(appspecificdata_el, 'appversion')
        appversion_el.text = "7.0"

        # data -> qtcodec
        data_el = ET.SubElement(appspecificdata_el, 'data')
        qtcodec_el = ET.SubElement(data_el, 'qtcodec')
        codecname_el = ET.SubElement(qtcodec_el, 'codecname')
        codecname_el.text = self.name
        codectypename_el = ET.SubElement(qtcodec_el, 'codectypename')
        codectypename_el.text = self.name
        codectypecode_el = ET.SubElement(qtcodec_el, 'codectypecode')
        codectypecode_el.text = "apcn"
        codecvendorcode_el = ET.SubElement(qtcodec_el, 'codecvendorcode')
        codecvendorcode_el.text = "appl"
        spatialquality_el = ET.SubElement(qtcodec_el, 'spatialquality')
        spatialquality_el.text = "1024"
        temporalquality_el = ET.SubElement(qtcodec_el, 'temporalquality')
        temporalquality_el.text = "0"
        keyframerate_el = ET.SubElement(qtcodec_el, 'keyframerate')
        keyframerate_el.text = "0"
        datarate_el = ET.SubElement(qtcodec_el, 'datarate')
        datarate_el.text = "0"

        # Additional video format details
        width_el = ET.SubElement(sample_characteristics_el, 'width')
        width_el.text = str(self.width)
        height_el = ET.SubElement(sample_characteristics_el, 'height')
        height_el.text = str(self.height)
        anamorphic_el = ET.SubElement(sample_characteristics_el, 'anamorphic')
        anamorphic_el.text = "FALSE"
        pixelaspectratio_el = ET.SubElement(sample_characteristics_el, 'pixelaspectratio')
        pixelaspectratio_el.text = "square"
        fielddominance_el = ET.SubElement(sample_characteristics_el, 'fielddominance')
        fielddominance_el.text = "none"
        colordepth_el = ET.SubElement(sample_characteristics_el, 'colordepth')
        colordepth_el.text = "24"

        # tracks
        for track in self.tracks:
            video_el.append(track.to_xml())

        return video_el
