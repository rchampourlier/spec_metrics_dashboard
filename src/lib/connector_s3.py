import boto3
import re
import numpy as np
import pandas as pd
from datetime import datetime
import json
from tqdm import tqdm
import codecs

BUCKET = "jt-spec-metrics"

def client():
    return boto3.client('s3')

def resource():
    return boto3.resource('s3')

def objects(a_client, bucket):
    objs = []
    paginator = a_client.get_paginator("list_objects")
    page_iterator = paginator.paginate(Bucket=bucket)
    for page in tqdm(page_iterator):
        objs = objs + page["Contents"]
    return objs

def fetch_run_keys():
    return [object["Key"] for object in objects(client(), BUCKET)]

def fetch_object_data(a_resource, bucket, obj_key):
    obj = a_resource.Object(bucket, obj_key)
    reader = codecs.getreader("utf-8")
    return json.load(reader(obj.get()["Body"]))

def fetch_run_data(run_key):
    data = fetch_object_data(resource(), BUCKET, run_key)
    data["run_key"] = run_key
    return data

def fetch_run_datas(run_keys):
    run_datas = []
    for run_key in tqdm(run_keys):
        run_datas.append(fetch_run_data(run_key))
    return run_datas
