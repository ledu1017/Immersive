import argparse
import wave
import numpy as np
import json
from os import path


def arg_parse():
    parser = argparse.ArgumentParser(
        description='Detect Silence and Errors in WAV files')
    parser.add_argument('--input_file_list', type=str,
                        required=True, help='Path to the input file list')
    parser.add_argument('--output_silence_file', type=str, required=True,
                        help='Path to the output file for silence detection')
    parser.add_argument('--output_error_file', type=str, required=True,
                        help='Path to the output file for error detection')

    return parser.parse_args()
# 入力・出力ファイルパスをここで設定
# input_file_list_path = path.join(path.dirname(__file__), "wavlist.txt")
# output_file_path_silence = path.join(path.dirname(__file__), "output_silence")
# output_file_path_error = "output/Q2.json"


def detect_silence(file_list, out_file):
    silence_threshold = -50  # This is in dB, change as needed.
    silent_files = []

    with open(file_list, "r", encoding="utf-8") as f:
        for line in f.readlines():
            file_name = line.strip()
            if file_name.endswith(".wav"):
                try:
                    with wave.open(file_name, "rb") as wav_file:
                        frames = wav_file.readframes(wav_file.getnframes())
                        samples = np.frombuffer(frames, dtype=np.int16)

                        # Check for empty samples
                        if len(samples) > 0:
                            if np.any(samples == 0):
                                print(
                                    f"Warning: Zero samples detected in {file_name}")

                            abs_samples = np.abs(samples)
                            # Replace zeros to avoid log(0)
                            abs_samples[abs_samples == 0] = 1
                            abs_samples = np.where(abs_samples <= 0, 1, abs_samples)
                            dBs = 20 * np.log10(abs_samples)
                            # abs_samples[abs_samples == 0] = 1
                            # dBs = 20 * np.log10(abs_samples)
                            avg_dB = np.mean(dBs)
                        else:
                            # Handle the case where samples array is empty
                            avg_dB = None  # or some other value

                        # Check for silence
                        if avg_dB is not None and avg_dB < silence_threshold:
                            silent_files.append(file_name)
                except Exception as e:
                    pass  # Handle or log exceptions if needed

    with open(out_file, "w") as f:
        json.dump({"silent_files": silent_files}, f)


def detect_wav_error(file_list, out_file):
    output_dict = {"error_list": {}}  # ネストされた辞書を作成

    with open(file_list, "r", encoding="utf-8") as f:
        for line in f.readlines():
            file_name = line.strip()
            if file_name.endswith(".wav"):
                try:
                    print(f"Processing {file_name}")  # デバッグ出力を追加
                    with wave.open(file_name, "rb") as wav_file:
                        frames = wav_file.readframes(wav_file.getnframes())

                        if len(frames) == 0:
                            output_dict["error_list"][file_name] = "데이터 값이 없는 경우"
                        else:
                            samples = np.frombuffer(frames, dtype=np.int16)
                            if max(samples) >= 32767 or min(samples) <= -32768:
                                output_dict["error_list"][file_name] = "클리핑 에러"
                except Exception as e:
                    if "file does not start with RIFF id" in str(e):
                        output_dict["error_list"][file_name] = "헤더만 있는 경우"
                    elif "not a WAVE file" in str(e):
                        output_dict["error_list"][file_name] = "데이터만 있는 경우"
                    else:
                        output_dict["error_list"][file_name] = str(e)
                        print(f"An exception occurred with file {file_name}: {e}")


    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_dict, f, ensure_ascii=False)  # ネストされた辞書をJSONに変換


if __name__ == "__main__":
    args = arg_parse()
    input_file_list_path = args.input_file_list
    output_file_path_silence = args.output_silence_file
    output_file_path_error = args.output_error_file

    detect_silence(input_file_list_path, output_file_path_silence)
    detect_wav_error(input_file_list_path, output_file_path_error)
    # 関数を呼び出す際に先ほど設定したファイルパスを使用
    # detect_silence(input_file_list_path, output_file_path_silence)
    # detect_wav_error(input_file_list_path, output_file_path_error)
