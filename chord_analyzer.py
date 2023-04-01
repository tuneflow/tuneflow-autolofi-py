from __future__ import annotations
from tuneflow_py import Song, TrackType, Note
from typing import List
from typing_extensions import TypedDict
from chorder import Chord, Dechorder
from miditoolkit import MidiFile


class ChordWithRange(TypedDict):
    chord: Chord
    startTick: int
    endTick: int


class ChordAnalyzer:
    @staticmethod
    def raw_notes_to_midi_obj(raw_notes: List[Note]):
        song = Song()
        track = song.create_track(type=TrackType.MIDI_TRACK)  # type: ignore
        clip = track.create_midi_clip(clip_start_tick=0)
        for note in raw_notes:
            clip.create_note(
                pitch=note.get_pitch(),
                velocity=note.get_velocity(),
                start_tick=note.get_start_tick(),
                end_tick=note.get_end_tick())
        midi_obj = song.to_midi()
        midi_obj.max_tick = song.get_last_tick()
        return midi_obj

    @staticmethod
    def extract_chords(raw_notes: List[Note], resolution: int):
        result: List[ChordWithRange] = []
        midi_obj = ChordAnalyzer.raw_notes_to_midi_obj(raw_notes)
        rawChords = Dechorder.dechord(midi_obj)
        prevChord: None | Chord = None
        prevChordStart: None | int = None
        beat = 0
        for beat in range(len(rawChords)):
            currentChord = rawChords[beat]
            if ((currentChord and not prevChord) or
                    (not currentChord and prevChord) or
                    (currentChord and prevChord and currentChord != prevChord)
                ):
                # Chord changed.
                if (prevChord):
                    result.append({
                        "chord": prevChord,
                        "startTick": prevChordStart,  # type: ignore
                        "endTick": beat * resolution,
                    })

                prevChord = currentChord
                prevChordStart = beat * resolution

        if (prevChord):
            result.append({
                "chord": prevChord,
                "startTick": prevChordStart,  # type: ignore
                "endTick": beat * resolution,
            })

        # Extend the last chord's end tick to the end of the last note.
        if len(result) > 0:
            noteEnd = max([note.get_end_tick() for note in raw_notes])
            result[len(result) - 1]['endTick'] = noteEnd

        # Trim leading and trailing invalid chords.
        while (len(result) > 0 and not result[0]['chord'].is_complete()):
            result.pop(0)

        while (len(result) > 0 and not result[len(result) - 1]['chord'].is_complete()):
            result.pop()
        return result

    @staticmethod
    def chord_to_pitch_offsets(chord: Chord):
        '''
        Convert a chord into pitch offsets relative to C.

        @param chord
        @returns In the format of `{bass: number | undefined, root: number[]}`, where bass is the bass pitch offset relative to
        C for the bass note and root is an array of pitch offsets relative to C for treble notes.
        '''
        rootPc = chord.root_pc
        bassPc = chord.bass_pc

        result = {
            "bass": None,
            "root": [],
        }
        if isinstance(bassPc, int):
            result['bass'] = bassPc

        if isinstance(rootPc, int) and isinstance(chord.quality, str):
            if chord.quality in Dechorder.chord_maps:
                chord_map = Dechorder.chord_maps[chord.quality]
                for step in chord_map:
                    result['root'].append(rootPc + step)

        return result
