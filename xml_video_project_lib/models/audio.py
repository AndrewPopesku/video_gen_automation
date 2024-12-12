from lxml import etree as ET
from xml_video_project_lib.models.base import XMElement
from xml_video_project_lib.models.track import Track

class Audio(XMElement):
    def __init__(self, numOutputChannels=2, depth=16, samplerate=48000):
        self.numOutputChannels = numOutputChannels
        self.depth = depth
        self.samplerate = samplerate
        self.outputs = []
        self.tracks = []

    def add_output_group(self, index, numchannels, downmix, channel_index):
        self.outputs.append({
            'index': str(index),
            'numchannels': str(numchannels),
            'downmix': str(downmix),
            'channel': {
                'index': str(channel_index)
            }
        })

    def add_track(self, track: Track):
        self.tracks.append(track)

    def to_xml(self):
        audio_el = ET.Element('audio')
        numOutputChannels_el = ET.SubElement(audio_el, 'numOutputChannels')
        numOutputChannels_el.text = str(self.numOutputChannels)

        # format
        format_el = ET.SubElement(audio_el, 'format')
        sample_characteristics = ET.SubElement(format_el, 'samplecharacteristics')
        depth_el = ET.SubElement(sample_characteristics, 'depth')
        depth_el.text = str(self.depth)
        samplerate_el = ET.SubElement(sample_characteristics, 'samplerate')
        samplerate_el.text = str(self.samplerate)

        # outputs
        outputs_el = ET.SubElement(audio_el, 'outputs')
        for group in self.outputs:
            group_el = ET.SubElement(outputs_el, 'group')
            index_el = ET.SubElement(group_el, 'index')
            index_el.text = group['index']
            numchannels_el = ET.SubElement(group_el, 'numchannels')
            numchannels_el.text = group['numchannels']
            downmix_el = ET.SubElement(group_el, 'downmix')
            downmix_el.text = group['downmix']
            channel_el = ET.SubElement(group_el, 'channel')
            channel_index_el = ET.SubElement(channel_el, 'index')
            channel_index_el.text = group['channel']['index']

        # tracks
        for track in self.tracks:
            audio_el.append(track.to_xml())

        return audio_el