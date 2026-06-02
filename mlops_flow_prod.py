from flytekit import workflow
from flytekit.types.file import FlyteFile
from typing import TypeVar, NamedTuple
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT, Annotated
from flytekitplugins.domino.decorator import dominotask
from scripts.load_data_A import load_data_a
from scripts.load_data_B import load_data_b
from scripts.merge_data import merge_data
from scripts.process_data import process_data
from scripts.train_model import train_model

# As this is considered a PROD Flow definition, we do not the use_project_defaults_for_omitted parameter
# and explictly set every required parameter in the task defintion to ensure reproducability.
# These are the additional parameters that need to be explicitly set of each task. 

environment_name="Domino Standard Environment Py3.10 R4.5 - Latest Cloud Release"  # Change to the name of your deployments Domino Standard Environment
environment_revision_id="68cb02b5536add3e634e7cd1"              # Change to the latest revision ID of your deployments Domino Standard Environment
hardware_tier_name="Small"                                 # Change to the name of one of your Domino's hardware tiers
GitRef_type="commitId"                                     
GitRef_value="c4f273e63e3267d079ebb7c5e5dbcef600521829"   # Change to the commitId of main Git repository 
volume_size_gib=10
dfs_repo_commit_id="8add2e00c1046b552149b669fd728de488b4d001"   # Change to the latest commit ID of the Artifacts file system in your project


# Set if you want caching on or off for all your tasks.
cache=True

# This calls the Artifact library, to create two named Flow Artifacts that we can label our merged data and model files as. 
DataArtifact = Artifact("Merged Data", DATA)
ModelArtifact = Artifact("Random Forest Model", MODEL)




@workflow
def model_training(data_path_a: str, data_path_b: str) -> Annotated[FlyteFile, ModelArtifact]: 
    '''
    Sample data preparation and training flow. This flow:
    
        1. Loads two datasets in from different sources
        2. Merges the data together
        3. Does some data preprocessing
        4. Trains a model using the processed data
        5. Output the merged data and model as Flow Artifacts

    To run this flow, execute the following line in the terminal

    pyflyte run --remote  mlops_flow_prod.py model_training --data_path_a /domino/datasets/local/flows_decorator/datasetA.csv --data_path_b /domino/datasets/local/flows_decorator/datasetB.csv
    '''

    data_a = load_data_a(data_path_a)
    data_b = load_data_b(data_path_b)
    
    merged_data = merge_data(data_a, data_b)

    processed_data = process_data(merged_data)

    return train_model(processed_data, 100)
