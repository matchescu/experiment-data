import polars as pl


if __name__ == "__main__":
    datasets = ["abt-buy", "amazon-google", "beer", "company", "dblp-acm", "dblp-scholar", "fodors-zagat", "itunes-amazon", "walmart-amazon"]

    ds_info = []
    for ds in datasets:
        left = pl.read_csv(f"./{ds}/tableA.csv", ignore_errors=True)
        right = pl.read_csv(f"./{ds}/tableB.csv", ignore_errors=True)
        train = pl.read_csv(f"./{ds}/train.csv", ignore_errors=True)
        valid = pl.read_csv(f"./{ds}/valid.csv", ignore_errors=True)
        test = pl.read_csv(f"./{ds}/test.csv", ignore_errors=True)

        n_train_true_matches = len(train.filter(pl.col("label") == 1))
        n_valid_true_matches = len(valid.filter(pl.col("label") == 1))
        n_test_true_matches = len(test.filter(pl.col("label") == 1))
        gt_size = n_train_true_matches + n_valid_true_matches + n_test_true_matches

        ds_info.append({
            "name": ds,
            "left_size": len(left),
            "left_attr_count": len(left.columns),
            "right_size": len(right),
            "right_attr_count": len(right.columns),
            "total_comparisons": len(left)*len(right),
            "actual_comparisons": len(train) + len(valid) + len(test),
            "gt_size": gt_size,
        })

    df = pl.DataFrame(ds_info)
    df.write_csv("stats.csv")