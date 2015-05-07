#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;
import datetime;
import random;
import MySQLdb;
import math;

class Sampling_Tool:
    
    def __init__(self,day_num,d_date_str,ratio,file_name,pos_num):
        self.day_num=day_num;
        self.d_date_str=d_date_str;
        self.ratio=ratio;
        self.file_name=file_name;
        self.d_date=datetime.date(int(d_date_str[0:4]),int(d_date_str[5:7]),int(d_date_str[-2:]));
        self.pos_num = pos_num;

    #Gaussian Sampling
    def Gaussian(self,sigma,u=0):
        result=0.0;
        u1=random.random();
        u2=random.random();
        #print u1,u2;
        r=math.sqrt(-2*math.log(u1));
        theta=2*math.pi*u2;
        result=r*math.cos(theta);
        return int(abs(u+(result*sigma)));


    #cal days between two datetime
    def get_dis(self,time,d_time):
        d_time=datetime.datetime(int(d_time[0:4]),int(d_time[5:7]),int(d_time[-2:]));
        time=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[-2:]));
        return (d_time-time).days;
    

    #Combine pos and neg
    def combin_sampling(self):
        pos_reader=csv.reader(open('pos_%s_%s.csv'%(self.day_num,self.d_date_str),'rb'));
        neg_reader=csv.reader(open('neg_%s_%s.csv'%(self.day_num,self.d_date_str),'rb'));
        whole_writer=csv.writer(open('samples_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));
        for num,row in enumerate(neg_reader):
            if num % self.ratio == 0:
                pos_row=pos_reader.next();
                whole_writer.writerow([pos_row[0],pos_row[1],pos_row[6],pos_row[5],pos_row[4]]);
            whole_writer.writerow([row[0],row[1],row[6],row[5],row[4]]);
            

    #Regular Sampling for negative samples
    def Regular_sampling(self):
        ui_dict=dict();
        csv_reader = csv.reader(open(self.file_name,'rb'));
        for row in csv_reader:
            temp_str = row[0]+'_'+row[1];
            if not ui_dict.has_key(temp_str):
                ui_dict[temp_str]=[row[5][:10],1];
            else:
                temp_list=ui_dict[temp_str];
                if self.get_dis(row[5][:10],temp_list[0])>0:
                    temp_list[0]=row[5][:10];
                temp_list[1]+=1;
        
        ui_list=sorted(ui_dict.keys(),key = lambda \
                x:ui_dict[x][1],reverse=True);
        ui_length = len(ui_list);
        print ui_length;
        print ui_dict[ui_list[ui_length/100]];

        pos_writer=csv.writer(open('pos_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));
        neg_writer=csv.writer(open('neg_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));

        for dis in range(self.day_num):
            temp_date=self.d_date-datetime.timedelta(dis);
            temp_reader=csv.reader(open('../test_data/'+str(temp_date)[-5:]+'th_act.csv','rb'));
            act_set=set();
            pos_num = 0;
            

            for row in temp_reader:
                if row[2] == '4':
                    pos_writer.writerow(row+[1]);
                    pos_num+=1;
                act_set.add(row[0]+'_'+row[1]);
            neg_num=0;


            while neg_num < pos_num*self.ratio:
                temp_index = ui_length;
                while temp_index >= ui_length:
                    temp_index = self.Gaussian(ui_length/100);
            
                ui_str=ui_list[temp_index];
                ui_date=ui_dict[ui_str][0];
                if self.get_dis(ui_date,str(temp_date)) <= 0:
                    continue;
                if not ui_str in act_set:
                    temp_list = ui_str.split('_');
                    act_set.add(ui_str);
                    neg_writer.writerow(temp_list+['','','',str(temp_date)+' 0',0]);
                    neg_num+=1;
        return;
        
    #Random User + Random Item sampling
    def Random_ui_sampling(self):
        user_list=set();
        item_list=dict();
        csv_reader = csv.reader(open('../train_data/train_user_cleaned.csv','rb'));
        for row in csv_reader:
            user_list.add(row[0]);
            item_list[row[1]]=row[4];

        pos_writer=csv.writer(open('pos_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));
        neg_writer=csv.writer(open('neg_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));

        for dis in range(self.day_num):
            temp_date=self.d_date-datetime.timedelta(dis);
            temp_reader=csv.reader(open('../test_data/'+str(temp_date)[-5:]+'th_act.csv','rb'));
            act_set=set();
            pos_num = 0;

            for row in temp_reader:
                if row[2] == '4':
                    pos_writer.writerow(row+[1]);
                    pos_num+=1;
                    act_set.add(row[0]+'_'+row[1]);

            neg_num=0;
            temp_u=list(user_list);
            temp_i=item_list.keys();
            while neg_num < pos_num*self.ratio:
                user_id = random.choice(temp_u);
                item_id = random.choice(temp_i);
                ui_str = user_id + '_' + item_id;

                if not ui_str in act_set:
                    temp_list = ui_str.split('_');
                    act_set.add(ui_str);
                    neg_writer.writerow(temp_list+['','',item_list[item_id],str(temp_date)+' 0',0]);
                    neg_num+=1;
        return;

    #Random Sampling for negative samples
    def Random_sampling(self):
        pos_writer=csv.writer(open('pos_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));
        neg_writer=csv.writer(open('neg_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));
        for dis in range(self.day_num):
            temp_date=self.d_date-datetime.timedelta(dis);
            temp_reader=csv.reader(open('../test_data/'+str(temp_date)[-5:]+'th_act.csv','rb'));
            neg_list=list();
            neg_set=set();
            pos_num = 0;
            for row in temp_reader:
                if row[2] == '4':
                    pos_writer.writerow(row+[1]);
                    pos_num+=1;
                else:
                    neg_list.append(row);
            neg_num=0;
            while neg_num < pos_num*self.ratio:
                row = random.choice(neg_list);
                if not row[0]+'_'+row[1] in neg_set:
                    neg_set.add(row[0]+'_'+row[1]);
                    neg_writer.writerow(row+[0]);
                    neg_num+=1;
        return;

    #Don't limited to a certain day , let it go freely
    def all_random_sampling(self):
        csv_reader = csv.reader(open('../train_data/user.csv','rb'));
        pos_writer = csv.writer(open('pos_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));
        neg_writer = csv.writer(open('neg_%s_%s.csv'%(self.day_num,self.d_date_str),'wb'));
        pos_list = [];
        neg_list = [];
        samples_set = set();
        tittle = csv_reader.next();
        died_date = datetime.datetime(2014,11,25);
        for row in csv_reader:
            temp_data = datetime.datetime.strptime(row[5][:10],'%Y-%m-%d');
            temp_days = (temp_data-died_date).days;
            if temp_days>=0 and temp_days<12:
                if row[2] == '4':
                    pos_list.append(row);
                else:
                    neg_list.append(row);
        count = 0;
        while True:
            if count > self.pos_num:
                break;
            row = random.choice(pos_list);
            if not row[0]+' '+row[1] in samples_set:
                samples_set.add(row[0]+' '+row[1]);
                pos_writer.writerow(row+[1]);
                count += 1;
        #end while
        count = 0;
        while True:
            if count > self.pos_num*self.ratio:
                break;
            row = random.choice(neg_list);
            if not row[0]+' '+row[1] in samples_set:
                samples_set.add(row[0]+' '+row[1]);
                neg_writer.writerow(row+[0]);
                count += 1;
        #end while
        return;
                
def main(day_num,d_date_str):
    st=Sampling_Tool(day_num,d_date_str,5,'../train_data/train_user_cleaned.csv',17000);
    st.all_random_sampling();
    st.combin_sampling();

if __name__ == '__main__':
    main(5,'2014-12-02');
