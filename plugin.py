from tuneflow_py import TuneflowPlugin, Song, ParamDescriptor, WidgetType, TrackType, Track, AutomationTargetType, db_to_volume_value, TempoEvent
from typing import Dict, List
from typing_extensions import Any
from pathlib import PurePath
import os
import random
import librosa
import soundfile as sf
from io import BytesIO
from track_utils import TrackUtils
from sentiment.consts import Sentiment
from sentiment.utils import SentimentUtils
from gen_utils import GenUtils
from chord_bank import baseInventory
import math

presetsFolder = PurePath(__file__).parent.joinpath('presets')


class QuickLofi(TuneflowPlugin):
    @staticmethod
    def provider_id() -> str:
        return 'andantei'

    @staticmethod
    def plugin_id() -> str:
        return 'auto-lofi'

    @staticmethod
    def params(song: Song) -> Dict[str, ParamDescriptor]:
        return {
            "mood": {
                "displayName": {
                    "zh": '情绪',
                    "en": 'Mood',
                },
                "defaultValue": 5,
                "widget": {
                    "type": WidgetType.Slider.value,
                    "config": {
                        "minValue": 1,
                        "maxValue": 9,
                        "step": 1,
                        "markers": {
                            1: {
                                "zh": "伤感",
                                "en": "Sadness"
                            },
                            9: {
                                "zh": "愉悦",
                                "en": "Delight"
                            }
                        }
                    },
                },
            },
            "duration": {
                "displayName": {
                    "zh": '时长（秒）',
                    "en": 'Duration (Seconds)',
                },
                "defaultValue": 60,
                "widget": {
                    "type": WidgetType.InputNumber.value,
                    "config": {
                        "minValue": 5,
                        "maxValue": 120,
                        "step": 1,
                    },
                },
            },
            "bpm": {
                "displayName": {
                    "zh": 'BPM',
                    "en": 'BPM',
                },
                "defaultValue": 70,
                "widget": {
                    "type": WidgetType.InputNumber.value,
                    "config": {
                        "minValue": 50,
                        "maxValue": 85,
                        "step": 5,
                    },
                },
            },
        }

    @staticmethod
    def createEmptyMIDITrack(song: Song) -> Track:
        newTrack = song.create_track(type=TrackType.MIDI_TRACK, assign_default_sampler_plugin=True)  # type:ignore
        return newTrack

    @staticmethod
    def createSFXTrack(song: Song, songEndTick: int, ticksPerBar: int) -> Track:
        sfxFolder = PurePath(presetsFolder).joinpath('sfx')
        # List files in sfxFolder in Python
        sfxFiles = os.listdir(sfxFolder)
        # Choose one randomly from sfxFiles
        sfxName = random.choice(sfxFiles)
        sfxTrack = song.create_track(type=TrackType.AUDIO_TRACK)  # type:ignore
        sfxPath = str(PurePath(sfxFolder).joinpath(sfxName))
        y, sr = librosa.load(sfxPath)
        sfxData = QuickLofi.convertToMp3(y, sr)
        sfxData.seek(0)
        sfxClip = sfxTrack.create_audio_clip(clip_start_tick=0, clip_end_tick=songEndTick, audio_clip_data={
            'audio_data': {
                "format": "mp3",
                "data": sfxData.read()
            },
            'duration': librosa.get_duration(y=y, sr=sr),
            "start_tick": 0
        }, insert_clip=True)

        TrackUtils.fill_clip_till_tick(sfxTrack, sfxClip, songEndTick)
        TrackUtils.add_volume_or_pan_automation_points(sfxTrack, AutomationTargetType.VOLUME, [
            # Fading in
            {
                "id": 1,
                "tick": 0,
                "value": db_to_volume_value(-30),
            },
            {
                "id": 2,
                "tick": ticksPerBar * 2,
                "value": db_to_volume_value(0),
            },
            {
                "id": 3,
                "tick": ticksPerBar * 4,
                "value": db_to_volume_value(-20),
            },
            {
                "id": 4,
                "tick": songEndTick - ticksPerBar * 4,
                "value": db_to_volume_value(-20),
            },
            # Fading out
            {
                "id": 5,
                "tick": songEndTick - ticksPerBar * 2,
                "value": db_to_volume_value(-30),
            },
        ])
        return sfxTrack

    @staticmethod
    def convertToMp3(y, sr):
        # Convert audio to mp3
        output_file = BytesIO()
        sf.write(output_file, y, sr, format='mp3')
        return output_file

    @staticmethod
    def createDrumTrack(
        song: Song,
        bpm: float,
        songEndTick: int,
        ticksPerBar: int,
    ):
        drumFolder = str(PurePath(presetsFolder).joinpath('drum'))
        drumBPMFolder = str(PurePath(drumFolder).joinpath(str(bpm)))
        drumFileNames = os.listdir(drumBPMFolder)
        drumFileName = random.choice(drumFileNames)
        drumPath = str(PurePath(drumBPMFolder).joinpath(drumFileName))
        y, sr = librosa.load(drumPath)
        audioContent = QuickLofi.convertToMp3(y, sr)
        audioContent.seek(0)
        drumTrack = song.create_track(
            type=TrackType.AUDIO_TRACK,  # type: ignore
        )
        drumClip = drumTrack.create_audio_clip(
            clip_start_tick=0,
            clip_end_tick=songEndTick,
            audio_clip_data={
                "audio_data": {
                    "data": audioContent.read(),
                    "format": "mp3",
                },
                "duration": librosa.get_duration(y=y, sr=sr),
                "start_tick": 0,
            },
            insert_clip=True,
        )
        TrackUtils.fill_clip_till_tick(drumTrack, drumClip, songEndTick)
        TrackUtils.add_volume_or_pan_automation_points(drumTrack, AutomationTargetType.VOLUME, [
            # Fading in
            {
                "id": 1,
                "tick": 0,
                "value": db_to_volume_value(-15),
            },
            {
                "id": 2,
                "tick": ticksPerBar * 2,
                "value": db_to_volume_value(-4),
            },
            {
                "id": 3,
                "tick": songEndTick - ticksPerBar * 4,
                "value": db_to_volume_value(-4),
            },
            # Fading out
            {
                "id": 4,
                "tick": songEndTick - ticksPerBar * 2,
                "value": db_to_volume_value(-15),
            },
        ])

        return drumTrack

    @staticmethod
    def getChordLoopPattern(patternTrack: Track, chords: List[Any], ticksPerBar: int):
        chordProgression = []
        for chord in chords:
            # Duplicate chords to fill up 4 bars
            for i in range(math.ceil(4/chord['numBars'])):
                chordProgression.append(chord)

        patternClip = patternTrack.create_midi_clip(
            clip_start_tick=0,
            insert_clip=True,
        )
        tickOffset = 0
        for chord in chordProgression:
            for note in chord['notes']:
                patternClip.create_note(
                    pitch=note[0],
                    velocity=note[1],
                    start_tick=tickOffset + note[2],
                    end_tick=tickOffset + note[3],
                    update_clip_range=True,
                )
            tickOffset += ticksPerBar * chord['numBars']

        return patternClip

    @staticmethod
    def filterTrackBarsBySentiments(
        track: Track,
        barSentiments: List[Sentiment],
        trackSentiment: int,
        ticksPerBar: int,
    ):
        trackEndTick = track.get_track_end_tick()
        for index in range(len(barSentiments)):
            bar = barSentiments[index]
            barStartTick = index * ticksPerBar
            barEndTick = min(barStartTick + ticksPerBar, trackEndTick)
            if (bar.value != trackSentiment):
                TrackUtils.clear_track_range(track, barStartTick, barEndTick)

    @staticmethod
    def run(song: Song, params: Dict[str, Any]):
        # User Input
        mood: int = params['mood']
        duration: int = params['duration']
        bpm: float = params['bpm']

        # Clear song tracks
        for i in range(song.get_track_count()-1, -1, -1):
            song.remove_track(song.get_track_at(i).get_id())

        # Only supports 4/4
        ticksPerBeat = song.get_resolution()
        ticksPerBar = ticksPerBeat * 4
        numBeats = math.ceil((duration / 60) * bpm)
        numBars = math.ceil(numBeats / 4)
        numBeats = numBars * 4
        songEndTick = numBeats * ticksPerBeat

        song.overwrite_tempo_changes([
            TempoEvent(
                ticks=0,
                time=0,
                bpm=bpm,
            ),
        ])

        # Choose chords with similiar moods
        chordCandidates = baseInventory[mood]
        numChordCandidates = len(chordCandidates)
        if numChordCandidates < 2:
            raise Exception('A minimum of 2 chords required.')
        if (mood - 1) in baseInventory:
            chordCandidates.extend(baseInventory[mood - 1])
        if (mood + 1) in baseInventory:
            chordCandidates.extend(baseInventory[mood + 1])

        # Loop with only one or two chords.
        numChords = random.randint(1, 2)
        selectedChords = []
        if (numChords == 1):
            selectedChords = [random.choice(chordCandidates)]
        else:
            chordIndexA = random.randint(0, numChordCandidates - 1)
            chordIndexB = random.randint(0, numChordCandidates - 2)
            chordIndexB = numChordCandidates - 1 if chordIndexA == chordIndexB else chordIndexB
            selectedChords = [chordCandidates[chordIndexA], chordCandidates[chordIndexB]]

        # Generate the chord track with selected chords
        chordTrack = QuickLofi.createEmptyMIDITrack(song)
        chordLoopPattern = QuickLofi.getChordLoopPattern(chordTrack, selectedChords, ticksPerBar)
        TrackUtils.fill_clip_till_tick(chordTrack, chordLoopPattern, songEndTick)
        if (chordTrack.get_track_end_tick() > songEndTick):
            TrackUtils.clear_track_range(chordTrack, songEndTick, chordTrack.get_track_end_tick())

        # Transition to a new sentiment every 4 bars.
        numParagraphs = math.ceil(numBeats / 16 + 0.4)
        barSentiments = SentimentUtils.getBarSentiments(numBars, numParagraphs)
        climaxSentiment = max([sentiment.value for sentiment in barSentiments])

        # Arrange according to sentiment
        bassTrack = GenUtils.extractChords(song, chordTrack, 32, False, True, 36)
        if not bassTrack:
            return

        trebleTrack = chordTrack

        QuickLofi.createSFXTrack(song, songEndTick, ticksPerBar)
        QuickLofi.createDrumTrack(song, bpm, songEndTick, ticksPerBar)

        if (bassTrack.get_track_end_tick() > songEndTick):
            TrackUtils.clear_track_range(bassTrack, songEndTick, bassTrack.get_track_end_tick())

        # Split the treble track according to sentiments
        # sentimentTracks = {}
        # for i in range(Sentiment.S.value, climaxSentiment+1):
        #   sentimentTrack = song.clone_track(trebleTrack)
        #   # There is currently one track for each sentiment
        #   sentimentTracks[i] = [sentimentTrack]
        #   QuickLofi.filterTrackBarsBySentiments(sentimentTrack, barSentiments, i, ticksPerBar)

        # song.remove_track(trebleTrack.get_id())
