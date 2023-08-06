import os
import typing
import random
import numpy as np
import cv2
import uuid
from loguru import logger

from stagesepx import toolbox


class VideoCutRange(object):
    def __init__(self, video_path: str, start: int, end: int, ssim: float):
        self.video_path = video_path
        self.start = start
        self.end = end
        self.ssim = ssim

    def can_merge(self, another: 'VideoCutRange'):
        return (self.end == another.start) and self.video_path == another.video_path

    def merge(self, another: 'VideoCutRange') -> 'VideoCutRange':
        assert self.can_merge(another)
        return __class__(
            self.video_path,
            self.start,
            another.end,
            (self.ssim + another.ssim) / 2,
        )

    def pick(self, frame_count: int, is_random: bool = None):
        result = list()
        if is_random:
            return random.sample(range(self.start, self.end), frame_count)
        length = self.get_length()
        for _ in range(1, frame_count + 1):
            cur = int(self.start + length / frame_count * _)
            result.append(cur)
        return result

    def get_length(self):
        return self.end - self.start

    def is_stable(self, threshold: float = None):
        if not threshold:
            threshold = 0.95
        # TODO if range is too large? ( > 10)
        return self.ssim > threshold

    def __str__(self):
        return f'<VideoCutRange [{self.start}-{self.end}] ssim={self.ssim}>'

    __repr__ = __str__


class VideoCutResult(object):
    def __init__(self,
                 video_path: str,
                 ssim_list: typing.List[VideoCutRange]):
        self.video_path = video_path
        self.ssim_list = ssim_list

    @staticmethod
    def _length_filter(range_list: typing.List[VideoCutRange], limit: int) -> typing.List[VideoCutRange]:
        after = list()
        for each in range_list:
            if each.get_length() >= limit:
                after.append(each)
        return after

    def get_unstable_range(self, limit: int = None) -> typing.List[VideoCutRange]:
        change_range_list = sorted(
            [i for i in self.ssim_list if not i.is_stable()],
            key=lambda x: x.start)

        # merge
        i = 0
        merged_change_range_list = list()
        while i < len(change_range_list) - 1:
            cur = change_range_list[i]
            while cur.can_merge(change_range_list[i + 1]):
                # can be merged
                i += 1
                cur = cur.merge(change_range_list[i])

                # out of range
                if i + 1 >= len(change_range_list):
                    break
            merged_change_range_list.append(cur)
            i += 1
        if limit:
            merged_change_range_list = self._length_filter(merged_change_range_list, limit)
        logger.debug(f'unstable range of [{self.video_path}]: {merged_change_range_list}')
        return merged_change_range_list

    def get_stable_range(self, limit: int = None) -> typing.List[VideoCutRange]:
        total_range = [self.ssim_list[0].start, self.ssim_list[-1].end]
        unstable_range_list = self.get_unstable_range(limit)
        range_list = [
            VideoCutRange(self.video_path, total_range[0], unstable_range_list[0].start, 0),
            VideoCutRange(self.video_path, unstable_range_list[-1].end, total_range[-1], 0),
        ]
        for i in range(len(unstable_range_list) - 1):
            range_list.append(
                VideoCutRange(
                    self.video_path,
                    unstable_range_list[i].end,
                    unstable_range_list[i + 1].start,
                    0,
                )
            )
        if limit:
            range_list = self._length_filter(range_list, limit)
        logger.debug(f'stable range of [{self.video_path}]: {range_list}')
        return sorted(range_list, key=lambda x: x.start)

    def pick_and_save(self,
                      range_list: typing.List[VideoCutRange],
                      frame_count: int,
                      to_dir: str = None,
                      *args, **kwargs) -> str:
        stage_list = list()
        for index, each_range in enumerate(range_list):
            picked = each_range.pick(frame_count, *args, **kwargs)
            logger.info(f'pick {picked} in range {each_range}')
            stage_list.append((index, picked))

        # create parent dir
        if not to_dir:
            to_dir = toolbox.get_timestamp_str()
        os.makedirs(to_dir, exist_ok=True)

        for each_stage_id, each_frame_list in stage_list:
            # create sub dir
            each_stage_dir = os.path.join(to_dir, str(each_stage_id))
            os.makedirs(each_stage_dir, exist_ok=True)

            with toolbox.video_capture(self.video_path) as cap:
                for each_frame_id in each_frame_list:
                    each_frame_path = os.path.join(each_stage_dir, f'{uuid.uuid4()}.png')
                    each_frame = toolbox.get_frame(cap, each_frame_id)
                    cv2.imwrite(each_frame_path, each_frame)
                    logger.debug(f'frame [{each_frame_id}] saved to {each_frame_path}')

        return to_dir


class VideoCutter(object):
    def __init__(self, period: int = None, compress_rate: float = None):
        if not period:
            period = 5
        if not compress_rate:
            compress_rate = 0.2

        self.period = period
        self.compress_rate = compress_rate

    def convert_video_into_ssim_list(self, video_path: str) -> typing.List[VideoCutRange]:
        ssim_list = list()
        with toolbox.video_capture(video_path) as cap:
            # get video info
            frame_count = toolbox.get_frame_count(cap)
            frame_size = toolbox.get_frame_size(cap)
            logger.debug(f'total frame count: {frame_count}, size: {frame_size}')

            # load the first two frames
            _, start = cap.read()
            start_frame_id = toolbox.get_current_frame_id(cap)

            toolbox.video_jump(cap, self.period)
            ret, end = cap.read()
            end_frame_id = toolbox.get_current_frame_id(cap)

            # compress
            start = toolbox.compress_frame(start, compress_rate=self.compress_rate)

            while ret:
                end = toolbox.compress_frame(end, compress_rate=self.compress_rate)
                ssim = toolbox.compare_ssim(start, end)
                logger.debug(f'ssim between {start_frame_id} & {end_frame_id}: {ssim}')

                ssim_list.append(
                    VideoCutRange(
                        video_path,
                        start=start_frame_id,
                        end=end_frame_id,
                        ssim=ssim,
                    )
                )

                # load the next one
                start = end
                start_frame_id, end_frame_id = end_frame_id, end_frame_id + self.period
                toolbox.video_jump(cap, end_frame_id)
                ret, end = cap.read()

        return ssim_list

    def cut(self, video_path: str) -> VideoCutResult:
        logger.info(f'start cutting: {video_path}')
        assert os.path.isfile(video_path), f'video [{video_path}] not existed'
        ssim_list = self.convert_video_into_ssim_list(video_path)
        logger.info(f'cut finished: {video_path}')
        return VideoCutResult(
            video_path,
            ssim_list,
        )
