import argparse
import sys
import logging
import uuid
from pathlib import Path

from xml_video_project_lib.utils import *
from xml_video_project_lib.models import *
from xml_video_project_lib.logging import logger
from docx import Document
import ffmpeg

def get_video_dimensions(video_path):
    """
    Extracts the width and height of a video file using ffmpeg.

    Args:
        video_path (str or Path): Path to the video file.

    Returns:
        tuple: (width, height) of the video.

    Raises:
        ffmpeg.Error: If ffprobe fails to retrieve metadata.
    """
    try:
        probe = ffmpeg.probe(str(video_path))
        video_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None
        )
        if video_stream is None:
            raise ValueError(f"No video stream found in file: {video_path}")

        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return width, height

    except ffmpeg.Error as e:
        print(f"An error occurred while probing video file: {video_path}")
        print(e.stderr.decode())
        raise
    except KeyError as e:
        print(f"Missing expected metadata in video file: {video_path}")
        raise

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate XML video project files based on provided assets.")
    parser.add_argument(
        'project_path',
        type=str,
        help='Path to the project directory containing footage, audio, and script files.'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='sequence_with_video_image_audio.xml',
        help='Output XML file name. Default is sequence_with_video_image_audio.xml'
    )
    return parser.parse_args()

def process_script(script_path, logger):
    try:
        doc = Document(script_path)
        script_text = '\n'.join([para.text for para in doc.paragraphs])
        logger.info(f"Extracted script from {script_path.name}")
        # Implement further processing as needed
        return script_text
    except Exception as e:
        logger.error(f"Failed to process script file: {e}")
        return ""

def main():
    args = parse_arguments()
    project_dir = Path(args.project_path).resolve()

    # Setup logger with DEBUG level to capture detailed logs
    # logger = setup_logger("XMLProjectLib", level=logging.DEBUG)

    try:
        # Validate project directory
        if not project_dir.exists() or not project_dir.is_dir():
            logger.error(f"The specified project path does not exist or is not a directory: {project_dir}")
            sys.exit(1)

        # Define paths
        footage_dir = project_dir / 'footage'
        audio_dir = project_dir / 'audio'
        script_file = project_dir / 'script.docx'

        # Validate presence of required directories and files
        if not footage_dir.exists() or not footage_dir.is_dir():
            logger.error(f"'footage' directory not found in the project path: {footage_dir}")
            sys.exit(1)

        if not audio_dir.exists() or not audio_dir.is_dir():
            logger.error(f"'audio' directory not found in the project path: {audio_dir}")
            sys.exit(1)

        if not script_file.exists() or not script_file.is_file():
            logger.error(f"'script.docx' file not found in the project path: {script_file}")
            sys.exit(1)

        # Proceed with project creation
        project = Project()

        # Create Sequence
        sequence = Sequence(
            id=IDGenerator.generate_id("sequence"),
            uuid=str(uuid.uuid4()),
            name="Sequence 01",
            duration=4526,  # You might want to make this dynamic based on content
        )
        project.add_sequence(sequence)
        logger.info("Added sequence to project.")

        # ---------------- AUDIO SECTION ----------------
        # Find the first mp3 file in the audio directory
        mp3_files = list(audio_dir.glob('*.mp3'))

        if not mp3_files:
            logger.warning(f"No mp3 files found in 'audio' directory: {audio_dir}")

        else:
            mp3_file_path = mp3_files[0]  # Assuming the first mp3 is the voiceover
            logger.info(f"Using MP3 file for audio: {mp3_file_path.name}")

            file_id = IDGenerator.generate_id("file")
            clipitem_id = IDGenerator.generate_id("clipitem")

            # Create File object for mp3
            file_obj = File(
                id=file_id,
                name=mp3_file_path.name,
                pathurl=f"file://localhost/{mp3_file_path.as_posix()}",
                samplerate=44100,
                channelcount=2,
                mediatype="audio"
            )
            logger.info(f"Created File object for audio: {mp3_file_path.name}")

            try:
                probe = ffmpeg.probe(str(mp3_file_path))
                video_stream = next(
                    (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None
                )
                duration = int(float(probe['format']['duration']))
                logger.debug(f"Extracted duration for video {mp3_file_path.name}: {duration} seconds")
            except Exception as e:
                logger.error(f"Failed to extract duration for video: {mp3_file_path.name}. Setting default duration.")
                duration = 4526  # Default duration if extraction fails


            # Create Audio ClipItem
            audio_clipitem = ClipItem(
                id=clipitem_id,
                premiereChannelType="stereo",
                masterclipid=f"masterclip-{file_id}",
                name=mp3_file_path.name,
                enabled="TRUE",
                duration=duration,  # Optionally, derive from audio metadata
                rate_timebase="30",
                rate_ntsc="TRUE",
                start="0",
                end=str(duration),
                in_point="0",
                out_point=str(duration),
                pproTicksIn="0",
                pproTicksOut="38360869747200",
                file=file_obj,
                sourcetrack_mediatype="audio",
                sourcetrack_trackindex=1,
                label2="Caribbean",
                alphatype="none",
                filters=[
                    Filter(
                        name="Audio Levels",
                        effectid="audiolevels",
                        effectcategory="audiolevels",
                        effecttype="audiolevels",
                        mediatype="audio",
                        pproBypass="false",
                        parameters=[
                            Parameter(parameterid="level", name="Level", valuemin="0", valuemax="3.98109", value="1")
                        ]
                    )
                ],
            )
            logger.info(f"Created Audio ClipItem: {clipitem_id}")

            # Add the audio clipitem to the first audio track
            atrack = Track(
                MZ_TrackTargeted="1",
                premiereTrackType="Stereo",
                outputchannelindex="1"
            )
            atrack.add_clipitem(audio_clipitem)
            logger.info(f"Added Audio ClipItem to audio track: {clipitem_id}")

            # Add the audio tracks to the audio section
            audio = Audio(numOutputChannels=2, depth=16, samplerate=48000)
            audio.add_track(atrack)
            logger.info("Added audio tracks to audio media.")

            # Add audio to the sequence
            sequence.add_audio(audio)
            logger.info("Added audio media to sequence.")

        # ---------------- VIDEO SECTION ----------------
        # video = Video()

        # # Create a video track targeted for video
        # vtrack = Track(
        #     MZ_TrackTargeted="1",
        #     premiereTrackType="Mono",
        #     outputchannelindex="1"
        # )
        # logger.info("Created video track.")

        # # Scan footage directory for video files
        # video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
        # video_files = list(footage_dir.glob('*'))
        # video_files = [f for f in video_files if f.suffix.lower() in video_extensions]

        # if not video_files:
        #     logger.warning(f"No video files found in 'footage' directory: {footage_dir}")

        # for video_file in video_files:
        #     file_id = IDGenerator.generate_id("file")
        #     clipitem_id = IDGenerator.generate_id("clipitem")

        #     width, height = get_video_dimensions(video_file)

        #     # Create File object for each video
        #     file_obj = File(
        #         id=file_id,
        #         name=video_file.name,
        #         pathurl=f"file://localhost/{video_file.as_posix()}",
        #         samplerate=48000,   # Typically irrelevant for video, but provided
        #         channelcount=2,
        #         mediatype="video",
        #         width=width,
        #         height=height
        #     )
        #     logger.info(f"Created File object for video: {video_file.name}")

        #     # Optionally, extract duration from video metadata
        #     try:
        #         probe = ffmpeg.probe(str(video_file))
        #         video_stream = next(
        #             (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None
        #         )
        #         duration = int(float(probe['format']['duration']))
        #         logger.debug(f"Extracted duration for video {video_file.name}: {duration} seconds")
        #     except Exception as e:
        #         logger.error(f"Failed to extract duration for video: {video_file.name}. Setting default duration.")
        #         duration = 4526  # Default duration if extraction fails

        #     # Create ClipItem for each video
        #     clipitem = ClipItem(
        #         id=clipitem_id,
        #         premiereChannelType="stereo",
        #         masterclipid=f"masterclip-{file_id}",
        #         name=video_file.name,
        #         enabled="TRUE",
        #         duration=duration,
        #         rate_timebase="30",
        #         rate_ntsc="TRUE",
        #         start="0",
        #         end="449",
        #         in_point="0",
        #         out_point="449",
        #         pproTicksIn="0",
        #         pproTicksOut="3805574572800",
        #         file=file_obj,
        #         sourcetrack_mediatype="video",
        #         sourcetrack_trackindex=1,
        #         label2="Iris",
        #         alphatype="none",
        #         filters=[
        #             Filter(
        #                 name="Basic Motion",
        #                 effectid="basic",
        #                 effectcategory="motion",
        #                 effecttype="motion",
        #                 mediatype="video",
        #                 pproBypass="false",
        #                 parameters=[
        #                     Parameter(parameterid="scale", name="Scale", valuemin="0", valuemax="1000", value="66.6667"),
        #                     Parameter(parameterid="rotation", name="Rotation", valuemin="-8640", valuemax="8640", value="0"),
        #                     Parameter(parameterid="center", name="Center", value=None),  # Will handle separately
        #                     Parameter(parameterid="centerOffset", name="Anchor Point", value=None),
        #                     Parameter(parameterid="antiflicker", name="Anti-flicker Filter", valuemin="0.0", valuemax="1.0", value="0")
        #                 ]
        #             )
        #         ]
        #     )
        #     logger.info(f"Created ClipItem for video: {video_file.name}")

        #     # Add the clipitem to the video track
        #     vtrack.add_clipitem(clipitem)
        #     logger.info(f"Added ClipItem to video track: {clipitem_id}")

        # # Similarly, handle image files in footage directory
        # image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        # image_files = list(footage_dir.glob('*'))
        # image_files = [f for f in image_files if f.suffix.lower() in image_extensions]

        # if not image_files:
        #     logger.warning(f"No image files found in 'footage' directory: {footage_dir}")


        # for image_file in image_files:
        #     file_id = IDGenerator.generate_id("file")
        #     clipitem_id = IDGenerator.generate_id("clipitem")

        #     width, height = get_video_dimensions(image_file)
        #     # Create File object for each image
        #     file_obj = File(
        #         id=file_id,
        #         name=image_file.name,
        #         pathurl=f"file://localhost/{image_file.as_posix()}",
        #         samplerate=48000,
        #         channelcount=2,
        #         mediatype="video",  # Images are treated as video media in editing software
        #         width=width,
        #         height=height
        #     )
        #     logger.info(f"Created File object for image: {image_file.name}")

        #     try:
        #         probe = ffmpeg.probe(str(video_file))
        #         video_stream = next(
        #             (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None
        #         )
        #         duration = int(float(probe['format']['duration']))
        #         logger.debug(f"Extracted duration for video {video_file.name}: {duration} seconds")
        #     except Exception as e:
        #         logger.error(f"Failed to extract duration for video: {video_file.name}. Setting default duration.")
        #         duration = 4526  # Default duration if extraction fails


        #     # Create ClipItem for each image
        #     clipitem = ClipItem(
        #         id=clipitem_id,
        #         premiereChannelType="stereo",
        #         masterclipid=f"masterclip-{file_id}",
        #         name=image_file.name,
        #         enabled="TRUE",
        #         duration=duration,  # Optionally, set based on project requirements
        #         rate_timebase="30",
        #         rate_ntsc="TRUE",
        #         start="449",
        #         end="598",
        #         in_point="107892",
        #         out_point="108041",
        #         pproTicksIn="914456685542400",
        #         pproTicksOut="915719559955200",
        #         file=file_obj,
        #         sourcetrack_mediatype="video",
        #         sourcetrack_trackindex=1,
        #         label2="Lavender",
        #         alphatype="straight",
        #         filters=[
        #             Filter(
        #                 name="Basic Motion",
        #                 effectid="basic",
        #                 effectcategory="motion",
        #                 effecttype="motion",
        #                 mediatype="video",
        #                 pproBypass="false",
        #                 parameters=[
        #                     Parameter(parameterid="scale", name="Scale", valuemin="0", valuemax="1000", value="140.625"),
        #                     Parameter(parameterid="rotation", name="Rotation", valuemin="-8640", valuemax="8640", value="0"),
        #                     Parameter(parameterid="center", name="Center", value=None),
        #                     Parameter(parameterid="centerOffset", name="Anchor Point", value=None),
        #                     Parameter(parameterid="antiflicker", name="Anti-flicker Filter", valuemin="0.0", valuemax="1.0", value="0")
        #                 ]
        #             )
        #         ]
        #     )
        #     logger.info(f"Created ClipItem for image: {image_file.name}")

        #     # Add the clipitem to the video track
        #     vtrack.add_clipitem(clipitem)
        #     logger.info(f"Added ClipItem to video track: {clipitem_id}")

        # # Add the video track to the video section
        # video.add_track(vtrack)
        # logger.info("Added video track to video media.")

        # # Add video to the sequence
        # sequence.add_video(video)
        # logger.info("Added video media to sequence.")

        # ---------------- SCRIPT SECTION ----------------
        # Process the script.docx file as needed
        # For example, extract text or integrate with voiceover timings
        # This part depends on your specific requirements
        # Here's a placeholder for handling the script
        # script_content = process_script(script_file, logger)

        # You might want to integrate script_content into the project metadata or elsewhere
        # For now, it's just extracted and logged
        logger.info("Processed script content.")

        # Serialize and Save XML
        project.save_to_file(args.output)
        logger.info(f"Project XML generated and saved successfully at {args.output}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

    logger.info("Video project generation completed successfully.")

if __name__ == "__main__":
    main()