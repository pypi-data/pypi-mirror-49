#!/usr/bin/env python3
import requests
import json
import math
import pandas as pd
import numpy as np
from operator import add 
from statistics import mean 
from datetime import datetime, timedelta


def parsed_api(url):
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    
    return parsed

def countIssue(dt_upt, df_agg_issue):
    today = datetime.today()
    one_day = timedelta(days=1)
    
    dates = dt_upt.date()
    week = 0
    while dates != today.date():
        week+=1
        dict_issue_weekly = {}
        for i in range(len(df_agg_issue)):
            issue = 0
            for j in range(7):
                if df_agg_issue['date'][i].date() == dates:
                    issue+=df_agg_issue['Issue'][i]
                    
                if dates == today.date():
                    if df_agg_issue['User Name'][i] not in dict_issue_weekly:
                        dict_issue_weekly[df_agg_issue['User Name'][i]] = issue
                    else:
                        dict_issue_weekly[df_agg_issue['User Name'][i]] = dict_issue_weekly[df_agg_issue['User Name'][i]] + issue
                        
                    df_issue = pd.DataFrame(list(dict_issue_weekly.items()), columns=['User Name','Issue Total'])
                    save = df_issue.to_csv(r'E:/TA/Hasil/Issue/Base/issue_week{counter}.csv'.format(counter = week), index = None, header= True)
                    break; break
                    
                dates = dates + one_day
                
            if df_agg_issue['User Name'][i] not in dict_issue_weekly:       
                dict_issue_weekly[df_agg_issue['User Name'][i]] = issue
            else:
                dict_issue_weekly[df_agg_issue['User Name'][i]] = dict_issue_weekly[df_agg_issue['User Name'][i]] + issue
                
            dates = dates - timedelta(days=7)
            
        df_issue = pd.DataFrame(list(dict_issue_weekly.items()), columns=['User Name','Issue Total'])
        save = df_issue.to_csv(r'app/hasil/Issue/Base/issue_week{counter}.csv'.format(counter = week), index = None, header= True)
        dates = dates + timedelta(days=7)
        
    return week

def countPR(dt_upt, df_agg_pull):
    today = datetime.today()
    one_day = timedelta(days=1)
    
    dates = dt_upt.date()
    week = 0
    while dates != today.date():
        week+=1
        dict_pull_weekly = {}
        for i in range(len(df_agg_pull)):
            pull = 0
            for j in range(7):
                if df_agg_pull['date'][i].date() == dates:
                    pull+=df_agg_pull['Pull'][i]
                if dates == today.date():
                    if df_agg_pull['User Name'][i] not in dict_pull_weekly: 
                        dict_pull_weekly[df_agg_pull['User Name'][i]] = pull
                    else:
                        dict_pull_weekly[df_agg_pull['User Name'][i]] = dict_pull_weekly[df_agg_pull['User Name'][i]] + pull
                    
                    df_pull = pd.DataFrame(list(dict_pull_weekly.items()), columns=['User Name','PR Total'])
                    save = df_pull.to_csv(r'app/hasil/Pull/Base/PR_week{counter}.csv'.format(counter = week), index = None, header= True)
                    break; break

                dates = dates + one_day
            
            if df_agg_pull['User Name'][i] not in dict_pull_weekly: 
                dict_pull_weekly[df_agg_pull['User Name'][i]] = pull
            else:
                dict_pull_weekly[df_agg_pull['User Name'][i]] = dict_pull_weekly[df_agg_pull['User Name'][i]] + pull
                    
            dates = dates - timedelta(days=7)

        df_pull = pd.DataFrame(list(dict_pull_weekly.items()), columns=['User Name','PR Total'])
        save = df_pull.to_csv(r'E:/TA/Hasil/Pull/Base/PR_week{counter}.csv'.format(counter = week), index = None, header= True)
        dates = dates + timedelta(days=7)
        
    return week

def countCommit(api_contributor):

    dict_commit_weekly = {}
    for i in range(len(api_contributor)):
        weeks = 0
        for j in range(len(api_contributor[i]['weeks'])):
            weeks+=1
            commit = api_contributor[i]['weeks'][j]['c']
            dict_commit_weekly[api_contributor[i]['author']['login']] = commit
            df_commit = pd.DataFrame(list(dict_commit_weekly.items()), columns=['User Name','Commit Total'])
            save = df_commit.to_csv(r'app/hasil/Commit/Base/commit_week{counter}.csv'.format(counter = weeks), index = None, header= True)

def countLOC(api_contributor):
    
    dict_loc_weekly = {}
    for i in range(len(api_contributor)):
        weeks = 0
        for j in range(len(api_contributor[i]['weeks'])):
            loc = 0
            weeks+=1
            loc += api_contributor[i]['weeks'][j]['a']
            loc += api_contributor[i]['weeks'][j]['d']
            dict_loc_weekly[api_contributor[i]['author']['login']] = loc
            df_loc = pd.DataFrame(list(dict_loc_weekly.items()), columns=['User Name','LOC Total'])
            save = df_loc.to_csv(r'app/hasil/LOC/Base/LOC_week{counter}.csv'.format(counter = weeks), index = None, header= True)