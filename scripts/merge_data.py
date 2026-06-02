import os
import pandas as pd
from typing import TypeVar, NamedTuple
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.decorator import dominotask

@dominotask(use_latest=True, hardware_tier_id="small-k8s")
def merge_data(datasetA: FlyteFile[TypeVar('csv')], datasetB: FlyteFile[TypeVar('csv')]) -> FlyteFile[TypeVar('csv')]:

    # Load data
    a = pd.read_csv(datasetA, index_col='Id') 
    b = pd.read_csv(datasetB, index_col='Id') 

    # Merge data
    print('Merging data...')
    merged = pd.concat([a, a], axis=0).reset_index(drop=True)
    print(merged)

    # Write output
    merged.to_csv('/tmp/merged_data.csv', index=False)
    return FlyteFile(path="/tmp/merged_data.csv")

