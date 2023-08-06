#!/usr/bin/env python3
import requests
import json
import math
import pandas as pd
import numpy as np
from operator import add 
from statistics import mean 
from datetime import datetime, timedelta

def performance_issue(df):
    issue_score = df.assign(issue_score = df['Issue Total'] / df['Issue Total'].mean())
    return issue_score.round(2)

def performance_pull(df):
    pull_score = df.assign(pull_score = df['PR Total'] / df['PR Total'].mean())
    return pull_score.round(2)

def performance_commit(df):
    commit_score = df.assign(commit_score = df['Commit Total'] / df['Commit Total'].mean())
    return commit_score.round(2)



def performance_LOC(df):
    
    loc_score = df.assign(loc_score = df['LOC Total'] / df['LOC Total'].mean())
    return loc_score.round(2)

def Total(merge1):
    issue = []
    pull = []
    commit = []
    loc = []

    for i in range(len(merge1['User Name'])):
        iss = merge1['issue_score'][i]
        pll = merge1['pull_score'][i]
        cmm = merge1['commit_score'][i]
        lc = merge1['loc_score'][i]
        issue.append(iss)
        pull.append(pll)
        commit.append(cmm)
        loc.append(lc)

    totalState = []
    for j in range(len(issue)):
        result = issue[j] + pull[j] + commit[j] + loc[j]
        totalState.append(result)
        
    return totalState.round(2)