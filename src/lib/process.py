import boto3
import re
import numpy as np
import pandas as pd
from datetime import datetime
import json
from tqdm import tqdm
import codecs

def fetch_run_keys(connector):
    return connector.fetch_run_keys()

def fetch_run_datas(connector, run_keys=None):
    if type(run_keys) == type(None):
        run_keys = fetch_run_keys(connector)
    run_datas = connector.fetch_run_datas(run_keys)
    return [add_info_to_run_data(run_data) for run_data in run_datas]

def add_info_to_run_data(run_data):
    run_key = run_data["run_key"]
    (date, branch, sha) = run_key_info(run_key)
    run_data["date"] = date
    run_data["branch"] = branch
    run_data["sha"] = sha
    return run_data

def run_key_info(run_key):
    """
    Returns (date, branch, sha) for the specified run key
    """
    extract_re = re.compile("\A.+/(\d{17})-(.+)-(\w+)\.json\Z")
    matches = extract_re.search(run_key)
    return (matches.group(1), matches.group(2), matches.group(3))

def branches(run_keys=None, run_keys_df=None):
    if type(run_keys_df) == type(None):
        if run_keys == None:
            raise Exception("Must provide run_keys_df or run_keys")
        run_keys_df = build_run_keys_df(run_keys)
    return set(run_keys_df.branch)

def build_run_keys_df(run_keys):
    run_dicts = []
    for run_key in run_keys:
        (date, branch, sha) = run_key_info(run_key)
        run_dicts.append({
            "run_key": run_key,
            "date": datetime.strptime(date, "%Y%m%d%H%M%S%f"),
            "branch": branch,
            "sha": sha
        })
    return pd.DataFrame.from_dict(run_dicts)

def run_info(run_data):
    date = datetime.strptime(run_data["date"], "%Y%m%d%H%M%S%f")
    return {
        "run_key": run_data["run_key"],
        "around_queries_count": run_data["around"]["queries_count"],
        "around_queries_duration": run_data["around"]["queries_duration"],
        "around_requests_count": run_data["around"]["requests_count"],
        "around_requests_duration": run_data["around"]["requests_duration"],
        "duration": run_data["duration"],
        "example_count": run_data["example_count"],
        "failure_count": run_data["failure_count"],
        "pending_count": run_data["pending_count"],
        "seed": run_data["seed"],
        "seed_used": run_data["seed_used"],
        "system_hostname": run_data["system"]["hostname"],
        "date": date,
        "branch": run_data["branch"],
        "sha": run_data["sha"]
    }

def build_run_infos_df(run_datas):
    ri_dicts = []
    for run_data in run_datas:
        ri_dicts.append(run_info(run_data))
    return pd.DataFrame.from_dict(ri_dicts)

def flatten_example(example):
    p_items = example["file_path"].split("/")[2:] # just remove "." and "spec"
    return {
        "description": example["description"],
        "dir_0": p_items[0],
        "dir_1": p_items[1] if len(p_items) > 2 else None,
        "dir_2": p_items[2] if len(p_items) > 3 else None,
        "dir_3": p_items[3] if len(p_items) > 4 else None,
        "file_name": p_items[-1],
        "line_number": example["line_number"],
        "run_time": example["execution_result"]["run_time"],
        "status": example["execution_result"]["status"],
        "queries_count": example["queries_count"],
        "queries_duration": example["queries_duration"],
        "requests_count": example["requests_count"],
        "requests_duration": example["requests_duration"]
    }

def flatten_examples(run_data):
    return [flatten_example(example) for example in run_data["examples"]]

def build_run_examples_df(run_data):
    return pd.DataFrame.from_dict(flatten_examples(run_data))

def build_runs_examples_df(run_datas):
    df = None
    for run_data in run_datas:
        run_df = build_run_examples_df(run_data)
        run_df["run_key"] = run_data["run_key"]
        if type(df) == type(None):
            df = run_df
        else:
            df = df.append(run_df, ignore_index=True)
    return df

def all_paths(data):
    return set([example["file_path"] for example in data["examples"]])

def dirs_at_level(data, level):
    paths = all_paths(data)
    return set([path.split("/")[level] for path in paths])
