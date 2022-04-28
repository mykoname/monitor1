# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
# automated_monitor1

!!!!!trying search '.ru'

"""
import numpy as np
import pandas as pd
import re
import codecs
datafilename = "d:/progs/avtom_monitor/29-05_12__2021/2021-12-06-07-05-08-EST-feed-download--groups&pages29-05_12__.csv"
dataf = pd.read_csv(datafilename, index_col= None, encoding='utf-8-sig')
df = dataf  # назначаю df  для игрищ, а dataf - полный фрейм
df.shape  #receiving a data structure
df.dtypes  #выяснение типа данных в столбцах
df.head

# df.iloc[1]    #доступ к строке по порядку(номеру(?))
# df2.loc[:,'Message']   #доступ к столбцу по названию
# df2.id1 = list(range(len(df.index)))  #вставка во фрейм в сущестуующий столбец порядковых индексов
#! df3 = df.assign(id2=list(range(len(df.index))))  #вставка в нов.фрейм столбца с порядковыми индексами
#! df3.set_index(['id2'])  #назначения столбца индексом
# df.reset_index       #убирание индекса(ов)
# вероятно, потом если буду брать два файла по отдельности, 
# для того чтоб их соединить вероятно надо будет поиграться с индексами ??
# df['Message'].memory_usage(deep=True)   #сколько памяти использует столбец 
# df.memory_usage(deep=True)

#! df.nunique() # подсчет уникальных элементов  # df['Type'].nunique()  -- а это если в одном столбце
# подсчет кол-ва групп и пабликов из которых взяты данные:
df['Group Name'].nunique() 

# выборка всех, где в столбце Message есть  СССР
# df_5=df[(df['Message'].isnull() != True) & (df['Message'].str.contains('СССР'))]

# пробую три слова на выбор:
## df_6=df[(df['Message'].isnull() != True) & ((df['Message'].str.contains('СССР')) 
##        | (df['Message'].str.contains('СРСР')) | (df['Message'].str.contains('детст')))]

#!! пробую исключить думскую ():
#df_7=df[((df['Message'].isnull() != True) & (~ (df['Group Name'].str.contains('Думская net'))))
#        & ((df['Message'].str.contains('СССР')) 
#        | (df['Message'].str.contains('СРСР')) 
#        | (df['Message'].str.contains('детст')))]

# например вот это берет все месседжи, в которых что-то есть и убирает думскую:  
# df_7777=df[((df['Message'].isnull() != True) & (~ (df['Group Name'].str.contains('Думская'))))]

#списки:
#! список хороших групп (пока второй-третей группы нет -- не беру):
#    l_good_groups = ['Думская net','']
#    groupsgood = '|'.join(l_good_groups) 
# список плохих групп(потенциально сплошь пропаганда):
    
# список хороших URL's & Links (еще поотслеживать: ukr-times.in.ua, 400928366716548 (одесса творческая), 106963360910053):
# "стоп гремлин"    
l_good_links = ['205838236106547','DumskayaTV','usionline.com',
                    '1352747551511718','gov.ua','ukr-times.in.ua',
                    '400928366716548', '106963360910053', 'liga.net',
                    '#ЭкскурсиипоОдессе', '#фотоОдессы', '#историяОдессы', 
                    '#гидпоОдессе', '#гидОдесса', '#МестовстречиОдесса', 'mesto.vstrechi.Odessa']
linksgood = '|'.join(l_good_links)  

#! список хороших в Description (пока добавляю в хор линки):    
#    l_good_descr = ['gov.ua']

#список под 7 критерий:
#потом разобраться  ЛДНР, ЛНР, ДНР, Крым, новороссия, новороссии, новороссией
# республика, самооборона, 
l_7mark = [    
   'ополчение', 'ополченцы', 'в Донбассе', 'правительственные войска', 
   'правительственных войск', 'правительственными войсками']

mark7 = '|'.join(l_7mark) 
#  поиск потенциальных пропаг. постов в месседжах по 7 критерию:    
df_7=df[((~ (df['Group Name'].str.contains('Думская net')))
               & (~ (df['Link'].str.contains(linksgood, na=False)))
               & (~ (df['Message'].str.contains(linksgood, na=False)))
               & (~ (df['Description'].str.contains(linksgood, na=False)))
               & (~ (df['URL'].str.contains(linksgood, na=False)))  )              
               & (((df['Message'].str.contains(mark7, na=False)))
               | ((df['Link Text'].str.contains(mark7, na=False)))
               | ((df['Image Text'].str.contains(mark7, na=False)))
               | ((df['Link'].str.contains(mark7, na=False)))
               | ((df['Description'].str.contains(mark7, na=False)))
               )] 

#экспорт в csv:
df_7.to_csv("df_7nr.csv",encoding='utf-8-sig')

# Подсчет пересечения (надо еще доразобраться (возм., лучше взять конкатенацию (внизу))):

# полдсчет количества уникальных групп:
# разобраться еще с их списком и подсчетом их аудитории
# df_1234567 = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7])
# print df_1234567['Group Name'].nunique()