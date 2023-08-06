from .Exceptions import *


class Google:
    def __init__(self):
        self._speech = ""
        self._VALID_STRENGTH = ["x-weak", "weak", "medium", "strong", "x-strong"]
        self._VALID_INTERPRET = ["cardinal", "ordinal", "characters", "fraction", "expletive", "bleep", "unit", "verbatim", "spell-out", "date", "time", "telephone"]
        self._VALID_PROSODY_ATTRIBUTES = {
            'rate': ['x-slow', 'slow', 'medium', 'fast', 'x-fast'],
            'pitch': ['x-low', 'low', 'medium', 'high', 'x-high'],
            'volume': ['silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud']
        }
        self._VALID_EMPHASIS = ["strong", "moderate", "none", "reduced"]

    def add_text(self, text):
        """
        Add text to the SSML

        Args:
            text (str): A string to add to the SSML

        Returns:
            Speech
        """
        self._speech += text
        return self

    def speak(self):
        """
        The root element of the SSML response.
        Build the SSML string and return it

        Returns:
            str: An SSML string
        """
        return "<speak>{}</speak>".format(self._speech)

    def breakk(self, time=None, strength=None):
        """
        An empty element that controls pausing or other prosodic boundaries between words. Using `<break>` between any pair of tokens is optional. If this element is not present between words, the break is automatically determined based on the linguistic context.

        Args:
            time (str): Sets the length of the break by seconds or milliseconds (e.g. "3s" or "250ms").
            strength (str): Sets the strength of the output's prosodic break by relative terms. Valid values are: "x-weak", weak", "medium", "strong", and "x-strong". The value "none" indicates that no prosodic break boundary should be outputted, which can be used to prevent a prosodic break that the processor would otherwise produce. The other values indicate monotonically non-decreasing (conceptually increasing) break strength between tokens. The stronger boundaries are typically accompanied by pauses.

        Raises:
            InvalidTime: if time has no suffix unit
            InvalidAttribute: if the strength isn't recognized

        Returns:
            Speech
        """
        if time:
            if time.endswith("ms") or time.endswith("ms"):
                self._speech += f"<break time='{time}'/>"
            else:
                raise InvalidTime(time)
        elif strength:
            if strength in self._VALID_STRENGTH:
                self._speech += f"<break strength='{strength}'/>"
            else:
                raise InvalidAttribute("break", strength, _VALID_STRENGTH)
        else:
            self._speech += "<break/>"
        return self

    def say_as(self, text, interpret_as, format=None, detail="1"):
        """
        This element lets you indicate information about the type of text construct that is contained within the element. It also helps specify the level of detail for rendering the contained text.
        The <say‑as> element has the required attribute, interpret-as, which determines how the value is spoken. Optional attributes format and detail may be used depending on the particular interpret-as value.

        Args:
            text (str): text to interpret
            interpret_as (str): determines how the value is spoken.
            format (str):
            detail (str):

        Returns:

        """
        if interpret_as not in self._VALID_INTERPRET:
            raise InvalidAttribute("say-as", interpret_as, self._VALID_INTERPRET)

        if interpret_as in ["time", "date"]:
            if not format:
                raise MissingAttribute("say-as", "format")
            if interpret_as == "time":
                self._speech += f"<say-as interpret-as='{interpret_as}' format='{format}'>{text}</say-as>"
            else:
                self._speech += f"<say-as interpret-as='{interpret_as}' format='{format}' detail='{detail}'>{text}</say-as>"
        else:
            self._speech += f"<say-as interpret-as='{interpret_as}'>{text}</say-as>"
        return self

    def audio(self, src, alt, description=None, clip_begin=0, clip_end="infinity", speed="100%", repeat_count="1", repeat_dur="infinity", sound_level="+0dB"):
        """
        Supports the insertion of recorded audio files and the insertion of other audio formats in conjunction with synthesized speech output.

        Args:
            src (str): A URI referring to the audio media source. Supported protocol is https.
            alt (str):
            description (desc):
            clip_begin (str): A TimeDesignation that is the offset from the audio source's beginning to start playback from. If this value is greater than or equal to the audio source's actual duration, then no audio is inserted
            clip_end (str): A TimeDesignation that is the offset from the audio source's beginning to end playback at. If the audio source's actual duration is less than this value, then playback ends at that time. If clipBegin is greater than or equal to clipEnd, then no audio is inserted.
            speed (str): The ratio output playback rate relative to the normal input rate expressed as a percentage. The format is a positive Real Number followed by %. The currently supported range is [50% (slow - half speed), 200% (fast - double speed)]. Values outside that range may (or may not) be adjusted to be within it.
            repeat_count (str): A Real Number specifying how many times to insert the audio (after clipping, if any, by clipBegin and/or clipEnd). Fractional repetitions aren't supported, so the value will be rounded to the nearest integer. Zero is not a valid value and is therefore treated as being unspecified and has the default value in that case.
            repeat_dur (str): A TimeDesignation that is a limit on the duration of the inserted audio after the source is processed for clipBegin, clipEnd, repeatCount, and speed attributes (rather then the normal playback duration). If the duration of the processed audio is less than this value, then playback ends at that time.
            sound_level (str): Adjust the sound level of the audio by soundLeveldecibels. Maximum range is +/-40dB but actual range may be effectively less, and output quality may not yield good results over the entire range.

        Returns:

        """
        if repeat_dur:
            repeat_count = "10"

        self._speech += f"<audio src='{src}' clipBegin='{clip_begin}' clipEnd='{clip_end}' speed='{speed}'" \
                        f"repeatCount='{repeat_count}' repeatDur='{repeat_dur}' soundLevel='{sound_level}'>"
        if description:
            self._speech += f"<desc>{description}</desc>"

        self._speech += f"{alt}</audio>"
        return self

    def p(self, *sentences):
        paragraph = ''.join([f"<s>{sentence}</s>" for sentence in sentences])
        self._speech += f"<p>{paragraph}</p>"

    def sub(self, text, alias):
        """
        Indicate that the text in the alias attribute value replaces the contained text for pronunciation.
        You can also use the sub element to provide a simplified pronunciation of a difficult-to-read word.

        Args:
            text (str):
            alias (str):

        Returns:
            Speech
        """
        self._speech += f"<sub alias='{alias}'>{text}</sub>"

    def mark(self, name):
        """
        An empty element that places a marker into the text or tag sequence. It can be used to reference a specific location in the sequence or to insert a marker into an output stream for asynchronous notification.

        Args:
            name (str):

        Returns:
            Speech
        """
        self._speech += f"<mark name='{name}'/>"
        return self

    def prosody(self, text, rate="medium", pitch="medium", volume="medium"):
        """
        Used to customize the pitch, speaking rate, and volume of text contained by the element. Currently the rate, pitch, and volume attributes are supported.

        Args:
            text
            rate
            pitch
            volume

        Returns:

        """
        if rate not in self._VALID_PROSODY_ATTRIBUTES["rate"]:
            raise InvalidAttribute("prosody", rate, self._VALID_PROSODY_ATTRIBUTES["rate"])

        if pitch not in self._VALID_PROSODY_ATTRIBUTES["pitch"]:
            raise InvalidAttribute("prosody", pitch, self._VALID_PROSODY_ATTRIBUTES["pitch"])

        if volume not in self._VALID_PROSODY_ATTRIBUTES["volume"]:
            raise InvalidAttribute("prosody", volume, self._VALID_PROSODY_ATTRIBUTES["volume"])

        self._speech += f"<prosody rate='{rate}' pitch='{pitch}' volume='{volume}'>{text}</prosody>"
        return self

    def emphasis(self, text, level):
        """
        Used to add or remove emphasis from text contained by the element. The <emphasis> element modifies speech similarly to <prosody>, but without the need to set individual speech attributes.

        Args:
            text (str): text to emphasie
            level (str): level of emphasis

        Returns:

        """
        if level not in self._VALID_EMPHASIS:
            raise InvalidAttribute("emphasis", level, self._VALID_EMPHASIS)

        self._speech += f"<emphasis level='{level}'>{text}</emphasis>"
        return self

    # TODO: add par
    # TODO: add seq
    # TODO: add media
