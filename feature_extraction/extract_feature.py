#!/usr/bin/env python
# coding=utf-8
import MySQLdb
import sqlalchemy as sa
import pandas as pd

#connect to db
engine = sa.create_engine('mysql+mysqldb://root:020011@localhost/Recommender')

#return day diff
def calc_day_diff(end_date):
    return 'timestampdiff(day, data_time, \'%s\')'%end_date

#calculate average activeness
def calc_person_activeness(user_id, days, end_date):
    day_diff = calc_day_diff(end_date)
    query = 'select * from train_data where user_id=%s and %s<=%d and %s>0 order by data_time desc'%(user_id, day_diff, days, day_diff)
    df = pd.read_sql_query(query, engine)
    activeness = len(set(df['item_id']))
    avtiveness_mean = float(activeness)/days
    return avtiveness_mean

#calculate frequency of each behavior
def cal_behavior_freq(user_id, days, end_date):
    day_diff = calc_day_diff(end_date)
    query = 'select count(*) as count,behavior from train_data where user_id=%s and %s<=%d and %s>0 group by behavior'%(user_id, day_diff, days, day_diff)
    df = pd.read_sql_query(query, engine)
    bdict = dict()
    for i,value in enumerate(df['behavior']): bdict[value] = int(df['count'][i])
    for i in range(4): 
        if not bdict.has_key(i+1): bdict[i+1] = 0
    return bdict

#calculate trans rate of each behavior
def calc_trans_rate(user_id, behavior, end_date):
    query1 = 'select distinct item_id,data_time from train_data where user_id=%s and behavior=4 and data_time < \'%s\' order by data_time desc'%(user_id, end_date)
    df1 = pd.read_sql_query(query1, engine)
    bcount, sum = 0, 0
    if len(df1.index) == 0: return 0
    for i in range(len(df1.index)):
        query = 'select count(behavior) as count from train_data where user_id = %s and item_id=%s and behavior = %s and data_time < \'%s\''%(user_id,df1['item_id'][i],behavior, df1['data_time'][i])
        df_temp = pd.read_sql_query(query, engine)
        bcount = df_temp['count'][0]
        sum += bcount
    rate = 0 if sum == 0 else float(len(df1.index))/sum
    return rate

#calculate time diff between 2 buying behavior
def calc_buying_diff(user_id, end_date):
    query = 'select distinct item_id, data_time from train_data where user_id = %s and behavior = 4 and data_time < \'%s\' order by data_time desc'%(user_id, end_date)
    df = pd.read_sql_query(query, engine)
    hours = 0
    for i in df.index:
        if i == 0: timestamp = pd.to_datetime(end_date) - df['data_time'][i] 
        else: timestamp =  df['data_time'][i-1]-df['data_time'][i]
        hours += timestamp.days * 24 + float(timestamp.seconds)/3600
    timestamp = df['data_time'][len(df.index)-1] - pd.to_datetime('2014-11-17')
    hours += timestamp.days * 24 + float(timestamp.seconds)/3600
    diff = hours/(len(df.index)+1)
    return diff 

#calculate time diff between last behavior and end date 
def calc_end_diff(user_id, behavior, end_date):
    query = 'select data_time from train_data where user_id = %s and behavior = %s and data_time < \'%s\' order by data_time desc limit 1'%(user_id, behavior, end_date)
    df = pd.read_sql_query(query, engine)
    timestamp = pd.to_datetime(end_date) - df['data_time'][0]
    hours = timestamp.days * 24 + float(timestamp.seconds)/3600
    return hours

def main():
    end_date = '2014-12-17'
    query = 'select * from train_data limit 5'
    df = pd.read_sql_query(query, engine)
    ffile = open('feature.csv', 'w')
    for i in df.index:
        feature = list()
        #3,7,30 days mean activeness
        feature.append(calc_person_activeness(df['user_id'][i], 3, end_date))
        feature.append(calc_person_activeness(df['user_id'][i], 7, end_date))
        feature.append(calc_person_activeness(df['user_id'][i], 30, end_date))
        #3,7,30 days mean behavior frequency
        for k,v in cal_behavior_freq(df['user_id'][i], 3, end_date).items(): feature.append(v)
        for k,v in cal_behavior_freq(df['user_id'][i], 7, end_date).items(): feature.append(v)
        for k,v in cal_behavior_freq(df['user_id'][i], 30, end_date).items(): feature.append(v)
        #behavior trans rate
        feature.append(calc_trans_rate(df['user_id'][i], 1, end_date))
        feature.append(calc_trans_rate(df['user_id'][i], 2, end_date))
        feature.append(calc_trans_rate(df['user_id'][i], 3, end_date))
        #buying behavior time diff
        feature.append(calc_buying_diff(df['user_id'][i], end_date))
        #time diff to end date
        feature.append(calc_end_diff(df['user_id'][i], 1, end_date))
        feature.append(calc_end_diff(df['user_id'][i], 2, end_date))
        feature.append(calc_end_diff(df['user_id'][i], 3, end_date))
        ffile.write('%s\n'%','.join(feature))
    ffile.close()

if __name__ == '__main__':
    main()
