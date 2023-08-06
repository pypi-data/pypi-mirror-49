import os
import re
import traceback
from pathlib import Path

import configargparse
import cv2
import numpy as np

def run():

    p = configargparse.ArgParser(default_config_files=['*.conf'])
    p.add("-s" , "--settings", is_config_file=True, help="Config file path, usually *.conf")
    p.add("-d", "--directory", help="Directory containing frame files")
    p.add("-f", "--fileformat", help="Naming convention for frame files")
    p.add("-c", "--codec", help="Codec as FOURCC, see http://www.fourcc.org/codecs.php")
    p.add("-o", "--output", help="Output file name")
    p.add("-r", "--rate", help="Frames Per Second")
    p.add("-W", "--width", help="Output frame width")
    p.add("-H", "--height", help="Output frame height")

    options = p.parse_args()

    print(options)
    print("----------")
    print(p.format_help())
    print("----------")
    print(p.format_values())

    out = None

    try:
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*options.codec)

        if os.path.exists(options.output):
            os.remove(options.output)

        frame_size = (int(options.width), int(options.height))

        destination = Path(options.output).resolve()
        out = cv2.VideoWriter(destination.as_posix(), fourcc, int(options.rate), frame_size)

        source_base = Path(options.directory).resolve()

        frames = source_base.glob(options.fileformat)
        frames_list = list((f.stem, f.absolute().as_posix()) for f in frames)

        def sort_key(f):
            return int(re.findall(r'\d+', f[0])[0])

        sorted_frames = (el[-1] for el in sorted(frames_list, key=sort_key))

        for frame_file in sorted_frames:
            print("Processing", frame_file)
            frame = cv2.imread(frame_file)
            frame = cv2.resize(frame, frame_size)
            out.write(np.array(frame, dtype=np.uint8))

        print("Done!")

    except Exception:
        error_message = traceback.format_exc ()
        print(error_message)

    finally:

        try:
            # Release everything if job is finished
            out.release()
        except AttributeError:
            # if creation of out fails will throw error which may print strange
            pass

if __name__ == "__main__":
    run()
