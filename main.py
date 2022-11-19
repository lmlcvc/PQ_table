import os
import re
import string

import numpy as np
import pandas as pd

input_dir_raw = "input/raw"
input_dir = "input"
output_dir = "output"

q_dict = {"a": 0, "b": 0, "c": 0, "č": 0, "ć": 0, "d": 0, "dž": 0, "đ": 0, "e": 0, "f": 0,
          "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, "lj": 0, "m": 0, "n": 0, "nj": 0,
          "o": 0, "p": 0, "r": 0, "s": 0, "š": 0, "t": 0, "u": 0, "v": 0, "z": 0, "ž": 0,
          " ": 0, "w": 0, "x": 0, "y": 0}


def set_pq_dict():
    """ Returns all-0 matrix (dict). """
    return {"a": q_dict.copy(), "b": q_dict.copy(), "c": q_dict.copy(), "č": q_dict.copy(), "ć": q_dict.copy(),
            "d": q_dict.copy(), "dž": q_dict.copy(), "đ": q_dict.copy(), "e": q_dict.copy(), "f": q_dict.copy(),
            "g": q_dict.copy(), "h": q_dict.copy(), "i": q_dict.copy(), "j": q_dict.copy(), "k": q_dict.copy(),
            "l": q_dict.copy(), "lj": q_dict.copy(), "m": q_dict.copy(), "n": q_dict.copy(), "nj": q_dict.copy(),
            "o": q_dict.copy(), "p": q_dict.copy(), "r": q_dict.copy(), "s": q_dict.copy(), "š": q_dict.copy(),
            "t": q_dict.copy(), "u": q_dict.copy(), "v": q_dict.copy(), "z": q_dict.copy(), "ž": q_dict.copy(),
            " ": q_dict.copy(), "w": q_dict.copy(), "x": q_dict.copy(), "y": q_dict.copy()}


def write_formatted_text(filename):
    """
    Formatting: all lowercase, remove punctuation, breaks or double spaces.
    Write result to file input directory.
    """
    filepath_r = os.path.join(input_dir_raw, filename)
    filepath_w = os.path.join(input_dir, filename)
    text = ""
    with open(filepath_r, "r") as f_r:
        text = f_r.read()
        text = text.lower()  # all lowercase
        text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
        text = re.sub("[–“”]", "", text)  # remove hyphens, quotes
        text = "".join([i for i in text if not i.isdigit()])  # remove digits
        text = " ".join(text.split())  # remove whitespace (newlines, tabs, multiple spaces...)
    f_r.close()

    with open(filepath_w, "w") as f_w:
        f_w.write(text)
    f_w.close()


def generate_pq_matrix(filename, pq_dict):
    curr = 0
    double_letter = False

    with open(os.path.join(input_dir, filename), "r") as f:
        text = f.read()

    for next in range(1, len(text)):
        if double_letter:
            pq_dict[text[curr - 1] + text[curr]][text[next]] += 1
            double_letter = False
        else:
            pq_dict[text[curr]][text[next]] += 1

        if (text[next] == "j" and (text[curr] == "l" or text[curr] == "n")) \
                or (text[next] == "ž" and text[curr] == "d"):
            double_letter = True
            curr += 1
            continue

        curr += 1

    return pq_dict


if __name__ == '__main__':
    for filename in os.listdir(input_dir_raw):
        write_formatted_text(filename)
        pq_matrix = generate_pq_matrix(filename, set_pq_dict())
        pq_df = pd.DataFrame.from_dict(pq_matrix)
        pq_df = pq_df.div(pq_df.sum(axis=1), axis=0)
        pq_df = pq_df.replace(np.nan, 0)
        pq_df = pq_df.rename(columns={" ": "space"}, index={" ": "space"})
        pq_df = pq_df.round(6)
        pq_df.to_csv(os.path.join(output_dir, filename))
