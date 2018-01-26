import os.path
import numpy as np
import pandas
import pickle
import requests
import ast
import typing
from json import JSONDecoder
from typing import List
from primitive_interfaces.base import PrimitiveBase, CallResult

from d3m_metadata import container, hyperparams, metadata as metadata_module, params, utils

__author__ = 'Distil'
__version__ = '1.0.0'

Inputs = container.List[str]
Outputs = str

class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    pass

class duke(PrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    metadata = metadata_module.PrimitiveMetadata({
        # Simply an UUID generated once and fixed forever. Generated using "uuid.uuid4()".
        'id': "46612a42-6120-3559-9db9-3aa9a76eb94f",
        'version': __version__,
        'name': "duke",
        # Keywords do not have a controlled vocabulary. Authors can put here whatever they find suitable.
        'keywords': ['Dataset Descriptor'],
        'source': {
            'name': __author__,
            'uris': [
                # Unstructured URIs.
                "https://github.com/NewKnowledge/duke-thin-client",
            ],
        },
        # A list of dependencies in order. These can be Python packages, system packages, or Docker images.
        # Of course Python packages can also have their own dependencies, but sometimes it is necessary to
        # install a Python package first to be even able to run setup.py of another package. Or you have
        # a dependency which is not on PyPi.
         'installation': [{
            'type': metadata_module.PrimitiveInstallationType.PIP,
            'package_uri': 'git+https://github.com/NewKnowledge/duke-thin-client.git@{git_commit}#egg=DukeThinClient'.format(
                git_commit=utils.current_git_commit(os.path.dirname(__file__)),
            ),
        }],
        # The same path the primitive is registered with entry points in setup.py.
        'python_path': 'd3m.primitives.distil.duke',
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.
        'algorithm_types': [
            metadata_module.PrimitiveAlgorithmType.RECURRENT_NEURAL_NETWORK,
        ],
        'primitive_family': metadata_module.PrimitiveFamily.DATA_CLEANING,
    })
    
    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: typing.Dict[str, str] = None)-> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed, docker_containers=docker_containers)
                
        self._decoder = JSONDecoder()
        self._params = {}

    def fit(self) -> None:
        pass
    
    def get_params(self) -> Params:
        return self._params

    def set_params(self, *, params: Params) -> None:
        self.params = params

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        pass
        
    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
        """
        Produce primitive's best guess for the structural type of each input column.
        
        Parameters
        ----------
        inputs : Input pandas frame

        Returns
        -------
        Outputs
            The outputs is a list that has length equal to number of columns in input pandas frame. 
            Each entry is a list of strings corresponding to each column's multi-label classification.
        """
        
        """ Accept a pandas data frame, predicts column types in it
        frame: a pandas data frame containing the data to be processed
        -> a list of lists of column labels
        """
        
        filename = inputs[1]
        files = {'file':open(filename,'rb')}
        
        try:
            r = requests.post(inputs[0]+"/fileUpload", files=files)
            return self._decoder.decode(r.text)
        except:
            # Should probably do some more sophisticated error logging here
            return "Failed processing input file"


if __name__ == '__main__':
    address = 'http://localhost:5001/'
    client = duke(hyperparams={})
    filename = "https://s3.amazonaws.com/d3m-data/merged_o_data/o_4550_merged.csv"
    result = client.produce(inputs = list([address,filename]))
    print(result)