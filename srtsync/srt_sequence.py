'''
default
'''

import re
from datetime import timedelta
from typing import Tuple


class SRTSequence:
    '''
    default
    '''

    def __init__(
            self,
            seq_number: int = None,
            seq_time: Tuple[timedelta, timedelta] = None
    ):
        self.seq_number = seq_number
        self.time = seq_time
        self.caption_text = []

    def __str__(self) -> str:
        seq_str = (
            f'{self.seq_number}\n'
            f'{self.strf_seq_time()}\n'
        )

        for caption_line in self.caption_text:
            seq_str = (f'{seq_str}{caption_line}\n')

        return f'{seq_str}\n'

    @staticmethod
    def strp_seq_time(str_seq_time: str) -> (timedelta, timedelta):
        '''
        default
        '''

        def parse_time(str_time: str) -> timedelta:
            time_arr = [
                int(str_time_section)
                for str_time_section
                in re.compile(r'\d+').findall(str_time)
            ]

            return timedelta(
                hours=time_arr[0],
                minutes=time_arr[1],
                seconds=time_arr[2],
                milliseconds=time_arr[3]
            )

        seq_start, seq_end = str_seq_time.replace(' ', '').split('-->')

        return (
            parse_time(seq_start),
            parse_time(seq_end),
        )

    def set_time(self, seq_time: (timedelta, timedelta)) -> None:
        '''
        default
        '''
        if seq_time[0] < timedelta(0, 0, 0):
            seq_time = (timedelta(0, 0, 0), seq_time[1])

        if seq_time[1] < timedelta(0, 0, 0):
            seq_time = (seq_time[0], timedelta(0, 0, 0))

        self.time = seq_time

    def set_seq_number(self, seq_number: int) -> None:
        '''
        default
        '''
        self.seq_number = seq_number

    def append_caption(self, caption_line: str) -> None:
        '''
        default
        '''
        self.caption_text.append(caption_line)

    def strf_seq_time(self) -> str:
        '''
        default
        '''
        def strf_time(time_delta: timedelta) -> str:
            total_seconds = time_delta.total_seconds()

            hours = int(total_seconds/3600)
            minutes = int((total_seconds % 3600) / 60)
            seconds = int(total_seconds - (hours * 3600) - (minutes * 60))
            milliseconds = int((total_seconds - int(total_seconds)) * 1000)

            return f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}'

        start_time = strf_time(self.time[0])
        end_time = strf_time(self.time[1])

        str_seq_time = f'{start_time} --> {end_time}'
        return str_seq_time
