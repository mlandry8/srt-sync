import re
from datetime import timedelta

class SRT_Sequence:
    def __init__(self, seq_number=None, seq_time=None):
        self.seq_number = seq_number
        self.time = seq_time
        self.caption_text = []

    @staticmethod
    def parse_times(str_seq_time):
        def parse_time(str_time):
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

        seq_start, seq_end = str_seq_time.replace(' ','').split('-->')

        return (
            parse_time(seq_start),
            parse_time(seq_end),
        )

    def set_time(self, seq_time):
        self.time = seq_time

    def set_seq_number(self, seq_number):
        self.seq_number = seq_number

    def append_caption(self, caption_line):
        self.caption_text.append(caption_line)

    def strf_seq_time(self):
        def strf_time(time_delta):
            total_seconds = time_delta.total_seconds()

            hours = int(total_seconds/3600)
            minutes = int((total_seconds % 3600) / 60)
            seconds = int(total_seconds - (hours * 3600) - (minutes * 60))
            milliseconds = int((total_seconds - int(total_seconds)) * 1000)

            return f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}'

        start_time = strf_time(self.time[0])
        end_time = strf_time(self.time[1])

        str_seq_time =  f'{start_time} --> {end_time}'
        return str_seq_time
