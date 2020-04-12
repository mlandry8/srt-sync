import argparse
from SRT import SRT

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file', type=str, nargs='+',
         help='files to sync'
    )
    parser.add_argument(
        '--output-file', type=str, default=None,
        help='file to output srt to. used only if processing one file'
    )
    parser.add_argument(
        '--time', type=int,
        help='time to shift in milliseconds'
    )

    args = parser.parse_args()

    for srt_file in args.file:
        srt_obj = SRT(srt_file=srt_file)
        srt_obj.parse_file()
        srt_obj.time_shift(args.time)
        
        if len(args.file) > 1 or not args.output_file :
            srt_obj.write_file()
        else:
            srt_obj.write_file(output_file=args.output_file)
