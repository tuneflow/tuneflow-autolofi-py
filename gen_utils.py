from tuneflow_py import Song, Track, Note, ClipType, TrackType
from typing import List
from chord_analyzer import ChordAnalyzer


class GenUtils:
    @staticmethod
    def extractChords(
        song: Song,
        track: Track,
        minimumNoteLengthDenomitor: int,
        extractTreble: bool,
        extractBass: bool,
        bassPitchOffset=48,
        treblePitchOffset=60,
    ):
        minimumNoteLengthInTicks = (4 / minimumNoteLengthDenomitor) * song.get_resolution()
        notes: List[Note] = []
        for clip in track.get_clips():
            if (clip.get_type() != ClipType.MIDI_CLIP):  # type: ignore
                continue

            for note in clip.get_notes():
                if (note.get_end_tick() - note.get_start_tick() < minimumNoteLengthInTicks):
                    continue

                notes.append(note)

        notes.sort(key=lambda x: x.get_start_tick())
        chordsWithRange = ChordAnalyzer.extract_chords(notes, song.get_resolution())
        if (len(chordsWithRange) == 0):
            return None

        newTrack = song.create_track(
            type=TrackType.MIDI_TRACK,  # type: ignore
            index=song.get_track_index(track.get_id()),
            assign_default_sampler_plugin=True,
        )
        newClip = newTrack.create_midi_clip(
            clip_start_tick=chordsWithRange[0]['startTick'],
        )
        for chordWithRange in chordsWithRange:
            startTick = chordWithRange['startTick']
            endTick = chordWithRange['endTick']
            chord = chordWithRange['chord']
            pitchOffsets = ChordAnalyzer.chord_to_pitch_offsets(chord)
            if not pitchOffsets:
                continue
            # Add bass note.
            if extractBass and isinstance(pitchOffsets['bass'], int):
                newClip.create_note(
                    pitch=pitchOffsets['bass'] + bassPitchOffset, velocity=60, start_tick=startTick, end_tick=endTick,
                    update_clip_range=True, resolve_clip_conflict=False)

            # Add treble notes.
            if (extractTreble):
                for i in range(len(pitchOffsets['root'])):
                    pitch = pitchOffsets['root'][i]
                    newClip.create_note(
                        pitch=pitch + treblePitchOffset,
                        velocity=24,
                        start_tick=startTick,
                        end_tick=endTick,
                        update_clip_range=True,
                        resolve_clip_conflict=False,
                    )

        return newTrack
