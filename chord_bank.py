import math
import os
from pathlib import Path
from miditoolkit import MidiFile
from tuneflow_py import Song


def mergeChordBanks(chordBanks):
    inventory = {}
    for bank in chordBanks:
        for key in bank:
            mood = math.floor(int(key) / 10)
            if mood not in inventory:
                inventory[mood] = []
            inventory[mood].extend(bank[key])
    return inventory


def build_from_directory(directory):
    inventory = {}
    item_count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            filename_parts = filename.split('_')
            mood = math.floor(int(filename_parts[0]) / 10)
            midi_obj = MidiFile(filename=full_path)
            song = Song.from_midi(midi_obj)
            ticks_per_bar = round(4 * song.get_resolution() / song.get_time_signature_event_at(0).get_denominator()
                                  * song.get_time_signature_event_at(0).get_numerator())
            num_bars = round(song.get_last_tick() / ticks_per_bar)
            first_clip = song.get_track_at(0).get_clip_at(0)
            inventory_item = {
                "numBars": num_bars,
                "beatsPerBar": song.get_time_signature_event_at(0).get_numerator(),
                "notes": [[note.get_pitch(), note.get_velocity(), note.get_start_tick(), note.get_end_tick()] for note in first_clip.get_raw_notes()]
            }
            if mood not in inventory:
                inventory[mood] = []
            inventory[mood].append(inventory_item)
            item_count += 1
    print(f'Loaded {item_count} chord bank items from {directory}.')
    return inventory


baseInventory = build_from_directory(str(Path(__file__).parent.joinpath(f'presets/chord_bank')))
