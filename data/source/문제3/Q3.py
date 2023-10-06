import json
import argparse
from pydub import AudioSegment
from os import path
# import os
# print(os.getcwd())

def find_silence(audio, silence_threshold=500, silence_length=64000):
    silent_ranges = []
    start = None
    samples = audio.get_array_of_samples()

    for t, sample in enumerate(samples):
        if abs(sample) < silence_threshold:
            if start is None:
                start = t
        else:
            if start is not None:
                end = t
                if (end - start) >= silence_length:
                    silent_ranges.append(
                        {
                            "beg": (start / audio.frame_rate),
                            "end": (end / audio.frame_rate),
                        }
                    )
                start = None
    return silent_ranges

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process audio files to find silent ranges.')
    parser.add_argument('--pcm_list', type=str, required=True, help='Path to PCM list file.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to output JSON file.')
    parser.add_argument('--thresholds', type=json.loads, default='{}', help='JSON formatted string that maps filenames to silence thresholds.')

    args = parser.parse_args()

    with open(args.pcm_list, "r", encoding="utf-8") as f:
        files = f.readlines()

    result = {}

    for file in files:
        file = file.strip()
        file_name = path.basename(file)
        silence_threshold = args.thresholds.get(file_name, 500)

        audio = AudioSegment.from_file(
            file, format="pcm", sample_width=2, frame_rate=16000, channels=1
        )
        silent_ranges = find_silence(audio, silence_threshold)
        result[file] = silent_ranges

    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
