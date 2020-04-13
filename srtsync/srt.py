'''
default
'''

from datetime import timedelta
from typing import List, Generator

from srtsync.srt_sequence import SRTSequence


class SRT:
    '''
    default
    '''

    def __init__(self, srt_file: str = None):
        self.file = srt_file
        self.sequences = []

    def parse_file(self) -> None:
        '''
        default
        '''
        def init_sequence(sequence_arr: List[str]) -> SRTSequence:
            try:
                seq = sequence_arr.pop(0).strip('\n')
                seq_number = int(seq)
            except ValueError:
                seq_number = int(seq.replace('\ufeff', ''))

            seq_time = SRTSequence.strp_seq_time(
                sequence_arr.pop(0).strip('\n')
            )

            srt_sequence = SRTSequence(
                seq_number=seq_number,
                seq_time=seq_time
            )

            for caption_line in sequence_arr:
                srt_sequence.append_caption(caption_line.strip('\n'))

            return srt_sequence

        def generate_sequence() ->  Generator[SRTSequence, None, None]:
            with open(self.file, 'r') as srt_file:
                temp_sequence = []

                for line in srt_file:
                    if line == '\n':
                        yield init_sequence(temp_sequence)
                        temp_sequence = []
                    else:
                        temp_sequence.append(line)

        self.sequences = [sequence for sequence in generate_sequence()]

    def write_file(self, output_file: str = None) -> None:
        '''
        default
        '''
        output_file = output_file if output_file else self.file

        with open(output_file, 'w') as srt_file:
            for sequence in self.sequences:
                srt_file.write(str(sequence))

    def time_shift(self, time_shift: int) -> None:
        '''
        default
        '''
        time_shift_delta = timedelta(milliseconds=time_shift)
        for sequence in self.sequences:
            sequence.set_time((
                sequence.time[0] + time_shift_delta,
                sequence.time[1] + time_shift_delta
            ))
