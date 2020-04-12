import re
from datetime import timedelta

class SRT:
    def __init__(self, srt_file=None):
        self.file = srt_file
        self.sequences = []

    def parse_file(self):
        def init_sequence(sequence_arr):
            seq_number = int(sequence_arr.pop(0).strip('\n'))
            seq_time = SRT_Sequence.parse_times(
                sequence_arr.pop(0).strip('\n')
            )

            srt_sequence = SRT_Sequence(
                seq_number=seq_number,
                seq_time=seq_time
            )

            for caption_line in sequence_arr:
                srt_sequence.append_caption(caption_line.strip('\n'))

            return srt_sequence

        def generate_sequence():
            with open(self.file,'r') as srt_file:
                temp_sequence = []
                for line in srt_file:
                    if line == '\n':
                        yield init_sequence(temp_sequence)
                        temp_sequence = []
                        continue

                    temp_sequence.append(line) 

        self.sequences = [sequence for sequence in generate_sequence()]

    def write_file(self, output_file=None):
        output_file = output_file if output_file else self.file
        with open(output_file,'w') as srt_file:
            for sequence in self.sequences:
                srt_file.write(f'{sequence.seq_number}\n')
                srt_file.write(f'{sequence.strf_seq_time()}\n')

                for caption_line in sequence.caption_text:
                    srt_file.write(f'{caption_line}\n')

                srt_file.write('\n')

    def time_shift(self, time_shift):
        time_shift_delta = timedelta(milliseconds=time_shift)
        for sequence in self.sequences:
            shifted_time = (
                sequence.time[0] + time_shift_delta,
                sequence.time[1] + time_shift_delta
            )
            sequence.set_time(shifted_time)


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
