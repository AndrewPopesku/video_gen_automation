import uuid
from xml_video_project_lib.logging import logger

class IDGenerator:
    """
    A utility class for generating unique IDs for various elements in the xml_video_project_lib.
    """

    PREFIXES = {
        'project': 'project',
        'sequence': 'sequence',
        'track': 'track',
        'clipitem': 'clipitem',
        'file': 'file',
        'effect': 'effect',
        'media': 'media',
        # Add more prefixes as needed
    }

    @staticmethod
    def generate_id(element_type: str) -> str:
        """
        Generates a unique ID for the given element type.

        Args:
            element_type (str): The type of the element (e.g., 'project', 'sequence', 'track').

        Returns:
            str: A unique ID string with the appropriate prefix.

        Raises:
            ValueError: If the element_type is not recognized.
        """
        prefix = IDGenerator.PREFIXES.get(element_type.lower())
        if not prefix:
            logger.error(f"Unknown element type for ID generation: '{element_type}'")
            raise ValueError(f"Unknown element type for ID generation: '{element_type}'")
        
        unique_id = f"{prefix}-{uuid.uuid4()}"
        logger.debug(f"Generated ID '{unique_id}' for element type '{element_type}'")
        return unique_id

    @staticmethod
    def generate_sequential_id(element_type: str, counter: int) -> str:
        """
        Generates a sequential ID for the given element type.

        Args:
            element_type (str): The type of the element (e.g., 'clipitem', 'file').
            counter (int): The sequential number to append.

        Returns:
            str: A sequential ID string with the appropriate prefix.

        Raises:
            ValueError: If the element_type is not recognized.
        """
        prefix = IDGenerator.PREFIXES.get(element_type.lower())
        if not prefix:
            logger.error(f"Unknown element type for sequential ID generation: '{element_type}'")
            raise ValueError(f"Unknown element type for sequential ID generation: '{element_type}'")
        
        sequential_id = f"{prefix}-{counter}"
        logger.debug(f"Generated Sequential ID '{sequential_id}' for element type '{element_type}'")
        return sequential_id
