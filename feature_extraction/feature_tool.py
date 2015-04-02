#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import MySQLdb;
import sys;

class Get_feature:
    
    def __init__(self):
        self.db=MySQLdb.connect("localhost",'root','','Recommender');
        self.cursor=self.db.cursor();

    def __del__(self):
        self.db.close();

    def get_disday(self,time,d_month,d_day):
        month=int(time[5:7]);
        day=int(time[-2:]);
        if month==d_month:
            return d_day-day;
        else:
            return 30+d_day-day;

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
    def get_whole_feature(self,user_id,item_id,died_day,day_num):
        feature_dir={};
        feature_dir.update(self.get_item_feature(item_id,died_day,day_num));
        feature_dir.update(self.get_pair_feature(user_id,item_id,died_day,day_num));
        
        feature_dir['bias']=1;
        return feature_dir;


    #Item Feature
    def get_item_feature(self,item_id,died_day,day_num):
        feature_dir={};
        sql="""select * from train_data where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();
        if len(result)==0:
            print 'item_id:%s is not exist' % item_id;
            sys.exit(1);
        feature_dir.update(self.get_beh_feature(result,died_day,day_num));
        feature_dir.update(self.get_peonum_feature(result,died_day,day_num));
        feature_dir.update(self.get_pop_feature(result,died_day,day_num));

        return feature_dir;

    def get_beh_feature(self,result,died_day,day_num):
        result_dir={};
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


            day=self.get_disday(time,12,died_day);
            if day<=0:
                continue;

            if row[2] == 4:
                last_buy=day;
            last_act=day;

            result_dir[beh+'_'+str(day)]+=1;

        result_dir['item_last_act']=last_act;
        result_dir['item_last_buy']=last_buy;
        return result_dir;
    
    def get_peonum_feature(self,result,died_day,day_num):
        result_dir={};
        for time in range(1,day_num+1):
            result_dir['buy_people'+'_'+str(time)]=set();

        for row in result:
            beh=row[2];
            if beh!=4:
                continue;
            time=str(row[5])[:10];
            
            day=self.get_disday(time,12,died_day);
            if day <=0:
                continue;

            result_dir['buy_people'+'_'+str(day)].add(row[0]);

        for key in result_dir:
            result_dir[key]=len(result_dir[key]);

        return result_dir;

    def get_pop_feature(self,result,died_day,day_num):
        result_dir={};
        for time in range(1,day_num+1):
            result_dir['pop'+'_'+str(time)]=set();

        for row in result:
            time=str(row[5])[:10];

            day=self.get_disday(time,12,died_day);
            if day <= 0:
                continue;
            result_dir['pop'+'_'+str(day)].add(row[0]);

        for key in result_dir:
            result_dir[key]=len(result_dir[key]);

        return result_dir;
    
    #Pair Feature
    def get_pair_feature(self,user_id,item_id,died_day,day_num):
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
            
            day=self.get_disday(time,12,died_day);
            if day <=0:
                continue;
            if row[2] == 4:
                last_buy=day;
            last_act=day;
            result_dir[beh+'_'+str(day)]+=1;
        
        result_dir['pair_last_act']=last_act;
        result_dir['pair_last_buy']=last_buy;
        return result_dir;


if __name__=='__main__':
    gf=Get_feature();
    sql="""select * from train_data where user_id="%s" and item_id="%s" """ %(100014756,125153101);
    gf.cursor.execute(sql);
    print gf.cursor.fetchall();
    print gf.get_pair_feature(100014756,125153101,17,29);
