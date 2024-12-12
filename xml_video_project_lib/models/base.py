from abc import ABC, abstractmethod
from lxml import etree as ET

class XMElement(ABC):
    def __init__(self, **attributes):
        self.attributes = attributes
        self.children = []

    def add_child(self, child: 'XMElement'):
        self.children.append(child)

    @abstractmethod
    def to_xml(self) -> ET.Element:
        pass