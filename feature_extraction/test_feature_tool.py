#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import MySQLdb;
import sys;
import csv;
import datetime;

class Get_feature:
    
    def __init__(self):
        self.db=MySQLdb.connect("localhost",'root','','Recommender');
        self.cursor=self.db.cursor();

    def __del__(self):
        self.db.close();

    def get_dis(self,time,d_time):
        d_time=datetime.datetime(int(d_time[0:4]),int(d_time[5:7]),int(d_time[-2:]));
        time=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[-2:]));
        return (d_time-time).days;


    def creat_tabel(self,tabel_name,feature_list):
        sql="drop table if exists %s" % tabel_name;
        self.cursor.execute(sql);
        sql="create table %s ( item_id int(13) primary key" % tabel_name;
        for feature in feature_list:
            sql+=", %s int" % feature;
        sql+=")";
        self.cursor.execute(sql);
        self.db.commit();

    #Whole feature
    def get_whole_feature(self,user_id,item_id,died_date,day_num):
        feature_dir={};
        day_num=31-day_num;
        #feature_dir.update(self.get_beh_feature(user_id,item_id,died_date,day_num));
        #feature_dir.update(self.get_peonum_feature(user_id,item_id,died_date,day_num));
        #feature_dir.update(self.get_pop_feature(user_id,item_id,died_date,day_num));
        feature_dir.update(self.get_pair_feature(user_id,item_id,died_date,day_num));
        #print len(feature_dir)
        #feature_dir.update(self.get_user_feature(user_id,item_id,died_date,day_num));
        #print len(feature_dir)

        #feature_dir['bias']=1;
        return feature_dir;


    #Item Feature
    def get_item_feature(self,user_id,item_id,died_date,day_num):
        feature_dir={};
        sql="""select * from train_data where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();
        if len(result)==0:
            print 'item_id:%s is not exist' % item_id;
            sys.exit(1);
        #feature_dir.update(self.get_beh_feature(result,died_date,day_num));
        #feature_dir.update(self.get_peonum_feature(result,died_date,day_num));
        #feature_dir.update(self.get_pop_feature(result,died_date,day_num));

        return feature_dir;

    #get item behaivor feature
    def get_beh_feature(self, user_id, item_id, died_date, day_num):
        result_dir={};

        sql="""select * from train_data where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        time_list=range(1,day_num+1);
        beh_list=['item_look','item_collection','item_add','item_buy'];
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+'_'+str(time)]=0;

        last_act=day_num+1;
        last_buy=day_num+1;
        

        for row in result:
            beh=beh_list[row[2]-1];
            
            time=str(row[5])[:10];


            day=self.get_dis(time,died_date);
            if day<=0:
                continue;

            if row[2] == 4:
                last_buy=day;
            last_act=day;

            result_dir[beh+'_'+str(day)]+=1;

        #result_dir['item_last_act']=last_act;
        #result_dir['item_last_buy']=last_buy;
        return result_dir;
   
    #get Item_last behavior feature
    def get_item_last_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};

        sql="""select * from train_data where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        last_act=day_num+1;
        last_buy=day_num+1;

        for row in result:
            beh=beh_list[row[2]-1];
            
            time=str(row[5])[:10];

            day=self.get_dis(time,died_date);
            if day<=0:
                continue;

            if row[2] == 4:
                last_buy=day;
            last_act=day;
        result_dir['item_last_act']=last_act;
        result_dir['item_last_buy']=last_buy;
        return result_dir;
        

    #get the num of person who buys the item per day
    def get_peonum_feature(self, user_id, item_id, died_date, day_num):
        result_dir={};

        sql="""select * from train_data where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        for time in range(1,day_num+1):
            result_dir['buy_people'+'_'+str(time)]=set();

        for row in result:
            beh=row[2];
            if beh!=4:
                continue;
            time=str(row[5])[:10];
            
            day=self.get_dis(time,died_date);
            if day <=0:
                continue;

            result_dir['buy_people'+'_'+str(day)].add(row[0]);

        for key in result_dir:
            result_dir[key]=len(result_dir[key]);

        return result_dir;
    
    #get item popularity per day
    def get_item_pop_feature(self, user_id, item_id, died_date,day_num):
        result_dir={};

        sql="""select * from train_data where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        for time in range(1,day_num+1):
            result_dir['item_pop'+'_'+str(time)]=set();

        for row in result:
            time=str(row[5])[:10];

            day=self.get_dis(time,died_date);
            if day <= 0:
                continue;
            result_dir['item_pop'+'_'+str(day)].add(row[0]);

        for key in result_dir:
            result_dir[key]=len(result_dir[key]);

        return result_dir;
    
    #Pair Feature
    def get_pair_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};
        
        beh_list=['pair_look','pair_collection','pair_add','pair_buy'];
        time_list=range(1,day_num+1);
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+'_'+str(time)]=0;

        sql="""select * from train_data where user_id="%s" and item_id = "%s"
        order by data_time """ % (user_id,item_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        last_act=day_num+1;
        last_buy=day_num+1;

        for row in result:
            beh=beh_list[row[2]-1];
            time=str(row[5])[:10];
            
            day=self.get_dis(time,died_date);
            if day <=0 or day > day_num:
                continue;
            if row[2] == 4:
                last_buy=day;
            last_act=day;
            result_dir[beh+'_'+str(day)]+=1;
        
        #result_dir['pair_last_act']=last_act;
        #result_dir['pair_last_buy']=last_buy;
        return result_dir;

    #Pair Last feature
    def get_pair_last_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};

        sql="""select * from train_data where user_id="%s" and item_id = "%s"
        order by data_time """ % (user_id,item_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        last_act=day_num+1;
        last_buy=day_num+1;

        for row in result:
            beh=beh_list[row[2]-1];
            time=str(row[5])[:10];
            
            day=self.get_dis(time,died_date);
            if day <=0:
                continue;
            if row[2] == 4:
                last_buy=day;
            last_act=day;
        
        result_dir['pair_last_act']=last_act;
        result_dir['pair_last_buy']=last_buy;
        return result_dir;

    #User Feature
    def get_user_feature(self, user_id, item_id, died_date, day_num):
        result_dir={};
        temp_dir={};
        beh_list=['user_look','user_collection','user_add','user_buy'];
        time_list=range(1,day_num+1);
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+'_'+str(time)]=0;
        for time in range(1,day_num+1):
            temp_dir['user_pop'+'_'+str(time)]=set();
        
        sql="""select * from train_data where user_id="%s" order by data_time """%user_id;
        self.cursor.execute(sql);
        result = self .cursor.fetchall();
        last_act=day_num+1;
        last_buy = day_num+1;

        for row in result:
            beh=beh_list[row[2]-1];
            time = str(row[5])[:10];
            day = self.get_dis(time,died_date);

            if day <= 0:
                continue;
            if row[2]==4:
                last_buy=day;
            last_act=4;
            #temp_dir['user_pop'+'_'+str(day)].add(row[1]);
            result_dir[beh+'_'+str(day)]+=1;
        
        for key in temp_dir:
            temp_dir[key]=len(temp_dir[key]);
        #result_dir.update(temp_dir);
        #del(temp_dir);
        #result_dir['user_last_act']=last_act;
        #result_dir['user_last_buy']=last_buy
        return result_dir;

    #User Last feature
    def get_user_last_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};
        
        sql="""select * from train_data where user_id="%s" order by data_time """%user_id;
        self.cursor.execute(sql);
        result = self .cursor.fetchall();
        last_act=day_num+1;
        last_buy = day_num+1;

        for row in result:
            beh=beh_list[row[2]-1];
            time = str(row[5])[:10];
            day = self.get_dis(time,died_date);

            if day <= 0:
                continue;
            if row[2]==4:
                last_buy=day;
            last_act=4;
        
        result_dir['user_last_act']=last_act;
        result_dir['user_last_buy']=last_buy
        return result_dir;

    #User Popularity feature
    def get_user_pop_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};
        time_list=range(1,day_num+1);
        for time in range(1,day_num+1):
            result_dir['user_pop'+'_'+str(time)]=set();
        
        sql="""select * from train_data where user_id="%s" order by data_time """%user_id;
        self.cursor.execute(sql);
        result = self .cursor.fetchall();
        for row in result:
            time = str(row[5])[:10];
            day = self.get_dis(time,died_date);

            if day <= 0:
                continue;
            result_dir['user_pop'+'_'+str(day)].add(row[1]);
        
        for key in result_dir:
            result_dir[key]=len(result_dir[key]);
        return result_dir;

    #Geographical Feature
    def get_geo_feature(self,user_id,item_id,died_date,day_num):
        feature_dir={};
        
        return feature_dir;

if __name__=='__main__':
    gf=Get_feature();
    sql="""select * from train_data where user_id="%s" """%(100014756);
    gf.cursor.execute(sql);
    #print gf.cursor.fetchall();
    f=getattr(gf,'get_whole_feature');
    result_dir=f(100014756,164834991,'2014-12-17',31);
    print len(result_dir);
