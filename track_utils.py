from tuneflow_py import Track, Clip, AutomationTarget
import math
from typing import List
from typing_extensions import Any


class TrackUtils:
    @staticmethod
    def fill_clip_till_tick(track: Track, clip: Clip, end_fill_tick: int):
        clip_duration = clip.get_clip_end_tick() - clip.get_clip_start_tick()
        if (clip_duration > 0 and clip.get_clip_end_tick() < end_fill_tick):
            clips_to_clone = math.ceil((end_fill_tick - clip.get_clip_end_tick()) / clip_duration)
            for i in range(clips_to_clone):
                duplicated_clip = track.clone_clip(clip)
                duplicated_clip.move_clip(
                    clip_duration * (i + 1),
                    move_associated_track_automation_points=True,
                )
                if (duplicated_clip.get_clip_end_tick() > end_fill_tick):
                    duplicated_clip.adjust_clip_right(end_fill_tick, resolve_conflict=False)

                track.insert_clip(duplicated_clip)

    @staticmethod
    def add_volume_or_pan_automation_points(
        track: Track,
        type: int,
        points: List[Any],
    ):
        target = AutomationTarget(type)
        track.get_automation().add_automation(target)
        for point in points:
            automation_value = track.get_automation().get_automation_value_by_target(target)
            if automation_value:
                automation_value.add_point(point['tick'], point['value'], overwrite=False)

    @staticmethod
    def clear_track_range(track: Track, start_tick: int, end_tick: int):
        clip = track.create_midi_clip(
            clip_start_tick=start_tick,
            clip_end_tick=end_tick - 1,
        )
        clip.delete_from_parent(delete_associated_track_automation=False)
