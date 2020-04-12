from SRT_Sequence import SRT_Sequence
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
            with open(self.file, 'r') as srt_file:
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
