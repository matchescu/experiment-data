import os
from pathlib import Path

import polars as pl


DS_NAMES = ["affiliationstrings", "cora1", "fodors_zagat_nophone", "geographicSettelments", "musicbrainz-20k"]
DIR_PATH = Path(__file__).parent


def _read_cs(path, prefix) -> dict:
    df = pl.read_csv(path, ignore_errors=True)
    no_match = df.filter(pl.col("label") == 0)
    full_match = df.filter(pl.col("label") == 1)
    bridge_links = df.filter((pl.col("label") > 0) & (pl.col("right_source") == "ambiguity-generator"))

    bridges = len(bridge_links)
    full_matches = len(full_match)
    positives = full_matches + bridges
    negatives = len(no_match)

    return {
        f"{prefix}_cs_size": len(df),
        f"{prefix}_negatives": negatives,
        f"{prefix}_positives": positives,
        f"{prefix}_bridges": bridges,
        f"{prefix}_neg_pos_ratio": negatives / positives,
        f"{prefix}_match_bridge_ratio": full_matches / bridges if bridges != 0 else 0,
    }


def _is_directed(name) -> bool:
    return name.endswith("_dir")


def _is_ambiguous(name) -> bool:
    return name.startswith("amb_")


if __name__ == "__main__":
    stats = []
    required_files = {"train.csv", "test.csv", "valid.csv", "runtime-cs.csv"}
    for current_dir, dirs, files in os.walk(DIR_PATH):
        dirpath = Path(current_dir)
        if dirs or dirpath.name.startswith("."):
            continue
        existing = set(files)
        not_found = required_files - existing
        if not_found:
            print(f'"{'", "'.join(not_found)}" required but not found in {current_dir}. skipping.')
            continue
        stats.append(
            {
                "dataset": dirpath.name,
                "directed": _is_directed(dirpath.name),
                "ambiguous": _is_ambiguous(dirpath.name),
                **_read_cs(dirpath/ "train.csv", "train"),
                **_read_cs(dirpath/ "test.csv", "test"),
                **_read_cs(dirpath/ "valid.csv", "valid"),
                **_read_cs(dirpath/ "runtime-cs.csv", "runtime"),
            }
        )
        print("computed stats for", current_dir)
    pl.DataFrame(stats).write_csv("ds_stats.csv")
