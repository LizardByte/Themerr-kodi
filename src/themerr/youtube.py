# standard imports
from typing import Optional

# lib imports
import youtube_dl

# local imports
from . import logger

log = logger.log


def process_youtube(url: str) -> Optional[str]:
    """
    Get URL using `youtube_dl`.

    The function will try to get a playable URL from the YouTube video.

    Parameters
    ----------
    url : str
       The URL of the YouTube video.

    Returns
    -------
    Optional[str]
       The URL of the audio object.

    Examples
    --------
    >>> process_youtube(url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    ...
    """
    youtube_dl_params = dict(
        logger=logger.log,
        socket_timeout=10,
        youtube_include_dash_manifest=False,
    )

    ydl = youtube_dl.YoutubeDL(params=youtube_dl_params)

    with ydl:
        try:
            result = ydl.extract_info(
                url=url,
                download=False  # We just want to extract the info
            )
        except Exception as exc:
            if isinstance(exc, youtube_dl.utils.ExtractorError) and exc.expected:
                log.error('YDL returned YT error while downloading {}: {}'.format(url, exc))
            else:
                log.error('YDL returned an unexpected error while downloading {}: {}'.format(url, exc))
            return None

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video_data = result['entries'][0]
        else:
            # Just a video
            video_data = result

    selected = {
        'opus': {
            'size': 0,
            'audio_url': None
        },
        'mp4a': {
            'size': 0,
            'audio_url': None
        },
    }
    if video_data:
        for fmt in video_data['formats']:  # loop through formats, select largest audio size for better quality
            if 'audio only' in fmt['format']:
                if 'opus' == fmt['acodec']:
                    temp_codec = 'opus'
                elif 'mp4a' == fmt['acodec'].split('.')[0]:
                    temp_codec = 'mp4a'
                else:
                    log.debug('Unknown codec: %s' % fmt['acodec'])
                    continue  # unknown codec
                filesize = int(fmt['filesize'])
                if filesize > selected[temp_codec]['size']:
                    selected[temp_codec]['size'] = filesize
                    selected[temp_codec]['audio_url'] = fmt['url']

    audio_url = None

    if 0 < selected['opus']['size'] > selected['mp4a']['size']:
        audio_url = selected['opus']['audio_url']
    elif 0 < selected['mp4a']['size'] > selected['opus']['size']:
        audio_url = selected['mp4a']['audio_url']

    if audio_url:  # mp4a codec is preferred
        if selected['mp4a']['audio_url']:  # mp4a codec is available
            audio_url = selected['mp4a']['audio_url']
        elif selected['opus']['audio_url']:  # fallback to opus :(
            audio_url = selected['opus']['audio_url']

    return audio_url  # return None or url found
