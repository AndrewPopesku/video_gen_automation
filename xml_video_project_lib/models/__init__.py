# # Expose core classes directly from the package
from xml_video_project_lib.models.timecode import Timecode
from xml_video_project_lib.models.file import File
from xml_video_project_lib.models.clipitem import ClipItem
from xml_video_project_lib.models.track import Track
from xml_video_project_lib.models.audio import Audio
from xml_video_project_lib.models.video import Video
from xml_video_project_lib.models.media import Media
from xml_video_project_lib.models.logging_info import LoggingInfo
from xml_video_project_lib.models.project import Project
from xml_video_project_lib.models.sequence import Sequence
from xml_video_project_lib.models.additional import Filter, Parameter, Link

# # Expose serializers
# from .serializers.xml_serializer import XMLSerializer

# # Expose plugins
# from .plugins.color_correction import ColorCorrectionPlugin

# # Expose utilities
# from .utils.id_generator import IDGenerator
# from .utils.validator import XMLValidator

# # Expose custom exceptions
# from .exceptions.custom_exceptions import (
#     XMLGenerationError,
#     ValidationError,
#     PluginError
# )

__all__ = [
    "Project",
    "Sequence",
    "Media",
    "Video",
    "Audio",
    "Track",
    "ClipItem",
    "File",
    "Timecode",
    "Filter",
    "Parameter",
    "Link"
]
