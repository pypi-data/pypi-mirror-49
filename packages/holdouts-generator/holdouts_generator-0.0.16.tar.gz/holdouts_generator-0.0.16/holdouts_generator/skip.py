from typing import Dict, List
from dict_hash import sha256
import os
import pandas as pd
from .utils import build_query, results_path, hyper_parameters_path, history_path, trained_model_path, true_labels_path, predictions_labels_path
from keras import Model
from keras.models import load_model
import json
import shutil

def build_keys(holdouts_key: str, hyper_parameters: Dict)->Dict:
    if hyper_parameters is None:
        hyper_parameters = {}
    return {
        "holdouts_key": holdouts_key,
        "hyper_parameters_key": sha256(hyper_parameters)
    }


def skip(key: str, hyper_parameters: Dict, results_directory: str)->bool:
    """Default function to choose to load or not a given holdout.
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    path = results_path(results_directory)
    return os.path.exists(path) and not pd.read_csv(path).query(build_query(build_keys(key, hyper_parameters))).empty

def store_result(key: str, new_results: Dict, hyper_parameters: Dict, results_directory: str = "results"):
    """Store given results in a standard way, so that the skip function can use them.
        key: str, key identifier of holdout to be skipped.
        new_results: Dict, results to store.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    hppath = hyper_parameters_path(results_directory, hyper_parameters)
    rpath = results_path(results_directory)
    results = pd.DataFrame({
        **new_results,
        **build_keys(key, hyper_parameters),
        "hyper_parameters_path":hppath
    }, index=[0])
    pd.DataFrame(hyper_parameters).to_json(hppath)
    if os.path.exists(rpath):
        results = pd.concat([
            pd.read_csv(rpath),
            results
        ])
    results.to_csv(rpath, index=False)

def load_result(key: str, hyper_parameters: Dict=None, results_directory: str = "results"):
    """Load standard results corresponding at given key and 
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    return pd.read_csv(results_path(results_directory)).query(
        build_query(build_keys(key, hyper_parameters))
    ).to_dict('records')[0]

def store_keras_result(key: str, history: Dict, y_pred:List[bool], y_true:List[bool], hyper_parameters: Dict=None, model:Model=None, results_directory: str = "results"):
    """Store given keras model results in a standard way, so that the skip function can use them.
        key: str, key identifier of holdout to be skipped.
        history: Dict, training history to store.
        y_pred:List[bool], predicted classes labels.
        y_true:List[bool], original classes labels.
        hyper_parameters: Dict, hyper parameters to check for.
        model:Model=None, model to save, by default None to not store it.
        results_directory: str = "results", directory where to store the results.
    """
    hpath = history_path(results_directory, history)
    mpath = trained_model_path(results_directory, key, hyper_parameters)
    plpath = predictions_labels_path(results_directory, y_pred)
    tlpath = true_labels_path(results_directory, y_true)

    dfh = pd.DataFrame(history)
    store_result(key, {
        **dfh.iloc[-1].to_dict(),
        "history_path":hpath,
        "model_path":mpath if model is not None else None,
        "predictions_labels_path":plpath,
        "true_labels_path":tlpath
    }, hyper_parameters, results_directory)
    dfh.to_csv(hpath, index=False)
    pd.DataFrame(y_pred).to_csv(plpath, index=False)
    pd.DataFrame(y_true).to_csv(tlpath, index=False)
    if model is not None:
        model.save(mpath)

def load_keras_results(key: str, hyper_parameters: Dict=None, results_directory: str = "results"):
    """Load standard keras results corresponding at given key and 
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    row = load_result(key, hyper_parameters, results_directory)
    model = None if row["model_path"] is None else load_model(row["model_path"])
    return (
        row,
        model,
        pd.read_csv(row["history_path"]),
        pd.read_csv(row["predictions_labels_path"]),
        pd.read_csv(row["true_labels_path"])
    )

def delete_results(results_directory: str = "results"):
    """Delete the results stored in a given directory. 
        results_directory: str = "results", directory where results are stores.
    """
    if os.path.exists(results_directory):
        shutil.rmtree(results_directory)
