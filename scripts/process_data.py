import os
import pandas as pd
from typing import TypeVar, NamedTuple
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.decorator import dominotask

@dominotask(use_latest=True, hardware_tier_id="medium-k8s")
def process_data(merged_data: FlyteFile[TypeVar('csv')]) -> FlyteFile[TypeVar('csv')]:

    # Load data
    df = pd.read_csv(merged_data) 

    # Process data
    print(df)
    print('Processing the data ...')
    df = df.drop('RandomColumn', axis=1)
    print(df)

    # Write output
    df.to_csv('/tmp/processed_data.csv', index=False)
    return FlyteFile(path="/tmp/processed_data.csv")


