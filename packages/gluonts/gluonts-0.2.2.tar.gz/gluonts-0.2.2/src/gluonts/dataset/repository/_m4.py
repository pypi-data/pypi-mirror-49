from pathlib import Path
import os
import json

import pandas as pd
import numpy as np

from gluonts.dataset.repository._util import metadata, save_to_file, to_dict


def generate_m4_dataset(
    dataset_path: Path, m4_freq: str, pandas_freq: str, prediction_length: int
):
    m4_dataset_url = (
        "https://github.com/M4Competition/M4-methods/raw/master/Dataset"
    )
    train_df = pd.read_csv(
        f'{m4_dataset_url}/Train/{m4_freq}-train.csv', index_col=0
    )
    test_df = pd.read_csv(
        f'{m4_dataset_url}/Test/{m4_freq}-test.csv', index_col=0
    )

    os.makedirs(dataset_path, exist_ok=True)

    with open(dataset_path / 'metadata.json', 'w') as f:
        f.write(
            json.dumps(
                metadata(
                    cardinality=len(train_df),
                    freq=pandas_freq,
                    prediction_length=prediction_length,
                )
            )
        )

    train_file = dataset_path / "train" / "data.json"
    test_file = dataset_path / "test" / "data.json"

    train_target_values = [ts[~np.isnan(ts)] for ts in train_df.values]

    test_target_values = [
        np.hstack([train_ts, test_ts])
        for train_ts, test_ts in zip(train_target_values, test_df.values)
    ]

    if m4_freq == 'Yearly':
        # some time series have more than 300 years which can not be represented in pandas,
        # this is probably due to a misclassification of those time series as Yearly
        # we simply use only the last 300 years for training
        # note this does not affect test time as prediction length is less than 300 years
        train_target_values = [ts[-300:] for ts in train_target_values]
        test_target_values = [ts[-300:] for ts in test_target_values]

    # the original dataset did not include time stamps, so we use a mock start date for each time series
    # we use the earliest point available in pandas
    mock_start_dataset = "1750-01-01 00:00:00"

    save_to_file(
        train_file,
        [
            to_dict(target_values=target, start=mock_start_dataset, cat=[cat])
            for cat, target in enumerate(train_target_values)
        ],
    )

    save_to_file(
        test_file,
        [
            to_dict(target_values=target, start=mock_start_dataset, cat=[cat])
            for cat, target in enumerate(test_target_values)
        ],
    )
