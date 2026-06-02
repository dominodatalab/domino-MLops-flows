import os
import pandas as pd
from typing import TypeVar, NamedTuple
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.decorator import dominotask

@dominotask(use_latest=True, hardware_tier_id="small-k8s")
def load_data_a(data_path: str) -> FlyteFile[TypeVar('csv')]:
    # Read the location of the csv from the task input blob
    input_name = "data_path"
    input_location = f"/workflow/inputs/{input_name}"
    with open(input_location, "r") as file:
        input_csv = file.read()

    # Read input csv to dataframe
    df = pd.read_csv(input_csv) 


    # Write to Flow output
    df.to_csv('/tmp/datasetA.csv', index=False)
    return FlyteFile(path="/tmp/datasetA.csv")

