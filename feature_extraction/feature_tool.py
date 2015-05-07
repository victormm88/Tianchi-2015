#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import MySQLdb;
import sys;
import csv;
import datetime;
import math;

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
    def get_whole_feature(self,user_id,item_id,died_date,day_num,category_id):
        feature_dir={};
        day_num = 31 - day_num;
        #feature_dir.update(self.get_beh_feature(user_id,item_id,died_date,day_num));
        #feature_dir.update(self.get_peonum_feature(user_id,item_id,died_date,day_num));
        #feature_dir.update(self.get_pop_feature(user_id,item_id,died_date,day_num));
        feature_dir.update(self.get_pair_feature(user_id,item_id,died_date,day_num));
        #print len(feature_dir)
        #feature_dir.update(self.get_user_feature(user_id,item_id,died_date,day_num));
        #print len(feature_dir)

        feature_dir.update(self.get_user_category_feature(user_id,category_id,died_date,day_num));
        #feature_dir['bias']=1;
        return feature_dir;


    #Item Feature
    def get_item_feature(self,user_id,item_id,died_date,day_num):
        feature_dir={};
        sql="""select * from train_data3 where item_id="%s" order by data_time""" % item_id;
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
    def get_item_beh_feature(self, user_id, item_id, died_date, day_num):
        result_dir={};
        died_date = died_date[:10];
        sql="""select * from train_data3 where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        time_list=range(1,day_num+1);
        beh_list=['item_look','item_collection','item_add','item_buy'];
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+'_'+str(time)]=0;

        last_act=30;
        last_buy=30;
        

        for row in result:
            beh=beh_list[row[2]-1];
            
            time=str(row[5])[:10];


            day=self.get_dis(time,died_date);
            if day<=0 :
                continue;
            if row[2] == 4:
                last_buy=day;
            last_act=day;

            if day>day_num:
                continue;
            result_dir[beh+'_'+str(day)]+=1;

        result_dir['item_last_act']=last_act;
        result_dir['item_last_buy']=last_buy;
        return result_dir;
   
    #get Item_last behavior feature
    def get_item_last_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};

        sql="""select * from train_data3 where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        last_act=day_num+1;
        last_buy=day_num+1;

        for row in result:
            beh=beh_list[row[2]-1];
            
            time=str(row[5])[:10];

            day=self.get_dis(time,died_date);
            if day<=0 or day > day_num:
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
        died_date = died_date[:10];
        sql="""select * from train_data3 where item_id="%s" """ % item_id;
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
            if day <=0 or day > day_num:
                continue;

            result_dir['buy_people'+'_'+str(day)].add(row[0]);

        for key in result_dir:
            result_dir[key]=len(result_dir[key]);

        return result_dir;
    
    #get item popularity per day
    def get_item_pop_feature(self, user_id, item_id, died_date,day_num):
        result_dir={};

        sql="""select * from train_data3 where item_id="%s" order by data_time""" % item_id;
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        for time in range(1,day_num+1):
            result_dir['item_pop'+'_'+str(time)]=set();

        for row in result:
            time=str(row[5])[:10];

            day=self.get_dis(time,died_date);
            if day <= 0 or day > day_num:
                continue;
            result_dir['item_pop'+'_'+str(day)].add(row[0]);

        for key in result_dir:
            result_dir[key]=len(result_dir[key]);

        return result_dir;
    
    #User-Category pair feature
    def get_user_category_feature(self,user_id,category_id,died_date,day_num):
        result_dir=dict();
        died_date = died_date[:10];
        beh_list=['uc_look','uc_collection','uc_add','uc_buy'];
        time_list=range(1,day_num+1);
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+'_'+str(time)]=0;

        sql="""select * from train_data3 where user_id="%s" and category = "%s"
        order by data_time """ % (user_id,category_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        last_act = 30;
        last_buy = 30;
        for row in result:
            beh=beh_list[row[2]-1];
            time=str(row[5])[:10];
            day=self.get_dis(time,died_date);
            if day <=  0:
                continue;
            if row[2]==4:
                last_buy = day;
            last_act = day;

            if day > day_num:
                continue;
            result_dir[beh+'_'+str(day)]+=1;
        #end for
        result_dir['uc_last_act']=last_act;
        result_dir['uc_last_buy']=last_buy;
        return result_dir;

    #Pair Feature
    def get_pair_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};
        died_date = died_date[:10];
        beh_list=['pair_look','pair_collection','pair_add','pair_buy'];
        time_list=range(1,day_num+1);
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+'_'+str(time)]=0;

        sql="""select * from train_data3 where user_id="%s" and item_id = "%s"
        order by data_time""" % (user_id,item_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();

        last_act=30;
        last_buy=30;

        for row in result:
            beh=beh_list[row[2]-1];
            time=str(row[5])[:10];
            
            day=self.get_dis(time,died_date);
            if day <= 0:
                continue;
            if row[2] == 4:
                last_buy=day;
            last_act=day;
            if day > day_num:
                continue;
            result_dir[beh+'_'+str(day)]+=1;
        
        result_dir['pair_last_act']=last_act;
        result_dir['pair_last_buy']=last_buy;
        return result_dir;

    #Pair Last feature
    def get_pair_proportion_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};

        sql="""select * from train_data3 where user_id="%s" and item_id = "%s"
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
        
        result_dir['pair_last_act']=last_act;
        result_dir['pair_last_buy']=last_buy;
        return result_dir;

    #User Feature
    def get_user_feature(self, user_id, item_id, died_date, day_num):
        result_dir={};
        died_date = died_date[:10];
        temp_dir={};
        beh_list=['user_look','user_collection','user_add','user_buy'];
        time_list=range(1,day_num+1);
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+'_'+str(time)]=0;
        for time in range(1,day_num+1):
            temp_dir['user_pop'+'_'+str(time)]=set();
        
        sql="""select * from train_data3 where user_id="%s" order by data_time """%user_id;
        self.cursor.execute(sql);
        result = self .cursor.fetchall();
        last_act=30;
        last_buy=30;

        for row in result:
            beh=beh_list[row[2]-1];
            time = str(row[5])[:10];
            day = self.get_dis(time,died_date);
            if day <= 0 :
                continue;
            if row[2]==4:
                last_buy=day;
            last_act=day;
            if day > day_num:
                continue;
            #temp_dir['user_pop'+'_'+str(day)].add(row[1]);
            result_dir[beh+'_'+str(day)]+=1;
        
        for key in temp_dir:
            temp_dir[key]=len(temp_dir[key]);
        #result_dir.update(temp_dir);
        #del(temp_dir);
        result_dir['user_last_act']=last_act;
        result_dir['user_last_buy']=last_buy
        return result_dir;

    #User Last feature
    def get_user_last_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};
        
        sql="""select * from train_data3 where user_id="%s" order by data_time """%user_id;
        self.cursor.execute(sql);
        result = self .cursor.fetchall();
        last_act=day_num+1;
        last_buy = day_num+1;

        for row in result:
            beh=beh_list[row[2]-1];
            time = str(row[5])[:10];
            day = self.get_dis(time,died_date);

            if day <= 0 or day > day_num:
                continue;
            if row[2]==4:
                last_buy=day;
            last_act=day;
        
        result_dir['user_last_act']=last_act;
        result_dir['user_last_buy']=last_buy
        return result_dir;

    #User Popularity feature
    def get_user_pop_feature(self,user_id,item_id,died_date,day_num):
        result_dir={};
        time_list=range(1,day_num+1);
        for time in range(1,day_num+1):
            result_dir['user_pop'+'_'+str(time)]=set();
        
        sql="""select * from train_data3 where user_id="%s" order by data_time """%user_id;
        self.cursor.execute(sql);
        result = self .cursor.fetchall();
        for row in result:
            time = str(row[5])[:10];
            day = self.get_dis(time,died_date);

            if day <= 0 or day > day_num:
                continue;
            result_dir['user_pop'+'_'+str(day)].add(row[1]);
        
        for key in result_dir:
            result_dir[key]=len(result_dir[key]);
        return result_dir;

    #get action before buying a item
    def __get_actbefbuy_feature(self, user_id, item_id, died_time, piece_num, day_num):
        result_dir=dict();
        beh_list=['abb_look_','abb_col_','abb_add_'];
        for i in range(piece_num*day_num):
            for act in beh_list:
                result_dir[act+str(i)]=0;

        sql='''select * from train_data3 where user_id="%s" and item_id="%s"
            order by data_time , behavior desc''' %(user_id,item_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();
        piece_hours = 24 / piece_num;
        died_datetime = datetime.datetime.now();#datetime.datetime.strptime(died_time,'%Y-%m-%d %H');
        count = 0;
        last_act = 1;
        flag = False;
        for row in result:
            act_datetime = row[5];#datetime.datetime.strptime(row[5],'%Y-%m-%d %H');
            if row[2] == 4:
                flag = True;
                died_datetime = act_datetime;
                if last_act != 4:
                    count+=1;
                    last_act=4;
                continue;
            days = (died_datetime-act_datetime).days;

            if days < 0 or days >= day_num:
                continue;
            hours = (died_datetime-act_datetime).seconds/3600+24*days;
            if hours == day_num * 24:
                continue;

            if flag:
                piece_index = hours / piece_hours;
                beh = beh_list[row[2]-1];
                result_dir[beh+str(piece_index)]+=1;

            last_act = row[2];
        
        if count == 0:
            return result_dir;

        for key in result_dir.keys():
            result_dir[key] = int(math.ceil(result_dir[key]/count));

        return result_dir;

    #get action before buying a item
    def get_actbef_feature(self, user_id, item_id, died_time, piece_num, day_num):
        result_dir=dict();
        beh_list=['abb_look_','abb_col_','abb_add_'];
        for i in range(piece_num*day_num):
            for act in beh_list:
                result_dir[act+str(i)]=0;

        sql='''select * from train_data3 where user_id="%s" and item_id="%s"
            order by data_time , behavior''' %(user_id,item_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();
        piece_hours = 24 / piece_num;
        died_datetime = datetime.datetime.strptime(died_time,'%Y-%m-%d %H');
        count = 0;
        last_act = 1;
        flag = True;
        for row in result:
            act_datetime = row[5];#datetime.datetime.strptime(row[5],'%Y-%m-%d %H');

            days = (died_datetime-act_datetime).days;
            if days < 0 or days >= day_num:
                continue;
            hours = (died_datetime-act_datetime).seconds/3600+24*days;
            if hours == day_num * 24:
                continue;

            if row[2] == 4:
                if flag:
                    print row[0],row[1];
                    return 1;
                else:
                    break;

            piece_index = hours / piece_hours;
            beh = beh_list[row[2]-1];
            result_dir[beh+str(piece_index)]+=1;

            flag=False;
        return result_dir;

    #Pair Feature
    def get_actbefpair_feature(self,user_id,item_id,died_date,day_num,label):
        result_dir={};
        died_date = died_date[:10];
        beh_list=['pair_look_','pair_collection_','pair_add_'];
        time_list=range(1,day_num+1);
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+str(time)]=0;
        #end for
        sql="""select * from train_data3 where user_id="%s" and item_id = "%s"
        order by data_time,behavior""" % (user_id,item_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();
        has_flag = False;
        flag = True;
        for row in result:
            time=str(row[5])[:10];
            
            day=self.get_dis(time,died_date);
            if day <=0 or day > day_num:
                continue;
            if row[2] == 4:
                if flag and label == '1':
                    return 1;
                else:
                    break;

            beh=beh_list[row[2]-1];
            result_dir[beh+str(day)]+=1;
            has_flag = True;
            flag = False;
        #end for

        if has_flag or label== '0':
            return result_dir;
        else:
            return 1;


    #User-Category pair act-bef feature
    def get_uc_actbef_pair_feature(self,user_id,category_id,died_date,day_num,label):
        result_dir=dict();
        died_date = died_date[:10];
        beh_list=['uc_look','uc_collection','uc_add'];
        time_list=range(1,day_num+1);
        for beh in beh_list:
            for time in time_list:
                result_dir[beh+str(time)]=0;

        sql="""select * from train_data3 where user_id="%s" and category = "%s"
        order by data_time , behavior""" % (user_id,category_id);
        self.cursor.execute(sql);
        result = self.cursor.fetchall();
        has_flag = False;
        flag = True;
        for row in result:
            time=str(row[5])[:10];
            
            day=self.get_dis(time,died_date);
            if day <=0 or day > day_num:
                continue;
            if row[2] == 4:
                if flag and label == '1':
                    return 1;
                else:
                    break;

            beh=beh_list[row[2]-1];
            result_dir[beh+str(day)]+=1;
            has_flag = True;
            flag = False;
        #end for

        if has_flag or label== '0':
            return result_dir;
        else:
            return 1;

    #Geographical Feature
    def get_geo_feature(self,user_id,item_id,died_date,day_num):
        feature_dir={};
        
        return feature_dir;

if __name__=='__main__':
    gf=Get_feature();
    sql="""select * from train_data3 where user_id="%s" """%(100014756);
    gf.cursor.execute(sql);
    #print gf.cursor.fetchall();
    f=getattr(gf,'get_user_feature');
    result_dir=f(115338753,228911200,'2014-12-01 12',5);
    print (result_dir.keys());
