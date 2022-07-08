import subprocess
import os
import sys
import re
import argparse
import platform

remove_cmd = "del" if platform.system() == "Windows" else "rm"


def match_filters(title: str, filters: list[str]) -> bool:
    for filter in filters:
        if re.search(filter, title.lower()):
            return True
    return False


def convert_time_stamp(stamp):
    seconds = int(stamp[:stamp.index(".")])
    m, s = seconds // 60, seconds % 60
    return f"00:{m:02d}:{s:02d}.00"


# print(downloaded)

def main(out, temp, filter_file):
    with open(filter_file, "r") as f:
        filters = [filter[:-1] for filter in f.readlines()]
    # print(filters)
    with open("titles.txt", "r", encoding="utf-8") as f:
        titles = f.readlines()
    with open("engines.csv", "r") as f:
        data = [[p.strip() for p in l.split(",")] for l in f.readlines()]

    downloaded = [n[:n.index(".")] for n in os.listdir(out)]

    cmds = []
    for (id, start, end, *tags), title in list(zip(data, titles)):
        if match_filters(title, filters) and id not in downloaded:
            url = f"https://www.youtube.com/watch?v={id}"
            temp_path = os.path.join(temp, f"{id}.wav")
            out_path = os.path.join(out, f"{id}.wav")
            start, end = convert_time_stamp(start), convert_time_stamp(end)
            cmd = f'youtube-dl -x "{url}" --audio-format wav -o "{temp_path}"'
            cmd2 = f'ffmpeg -ss {start} -i {temp_path} -t 10 {out_path}'
            cmds.append(cmd)
            cmds.append(cmd2)
            cmds.append(f"{remove_cmd} {temp_path}")
            # print(title.strip())
    for cmd in cmds:
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--temp", required=True)
    parser.add_argument("--filter", required=True)
    args = parser.parse_args()

    main(args.out, args.temp, args.filter)
