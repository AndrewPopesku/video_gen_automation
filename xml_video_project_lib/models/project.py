from lxml import etree as ET
from xml_video_project_lib.models.base import XMElement
from xml_video_project_lib.models.sequence import Sequence

class Project(XMElement):
    def __init__(self, version="4", doctype="<!DOCTYPE xmeml>"):
        self.version = version
        self.doctype = doctype
        self.sequences = []

    def add_sequence(self, sequence: Sequence):
        self.sequences.append(sequence)

    def to_xml(self):
        xmeml_el = ET.Element('xmeml', version=self.version)
        for sequence in self.sequences:
            xmeml_el.append(sequence.to_xml())
        return xmeml_el

    def save_to_file(self, filename):
        # Create XML tree
        xml_tree = self.to_xml()

        # Convert to string with pretty print
        xml_bytes = ET.tostring(xml_tree, pretty_print=True, encoding='UTF-8', xml_declaration=False)

        # Insert DOCTYPE
        xml_str = xml_bytes.decode('utf-8')
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        # Remove existing XML declaration if present
        if xml_str.startswith(xml_declaration):
            xml_content = xml_str[len(xml_declaration):]
        else:
            xml_content = xml_str

        final_xml = xml_declaration + self.doctype + '\n' + xml_content

        # Write to file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(final_xml)

        print(f"XML project file '{filename}' generated successfully.")


