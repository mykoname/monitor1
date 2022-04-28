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
datafilename = "d:/progs/avtom_monitor/06-12_12_2021/6-12_12_2021_groups&pages.csv"
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


#список под 4 критерий
#(возможно уточнить этих: програмы стоянова, российский шоубизнес, российские СМИ,)
#возм., добавить сюда персонали из старых (Азаров, Янукович, Курченко, Клименко 
#(только отсечь их позиивные/негативные упоминания -- взять здесь только позитивные))
# vesti.ua
# !!поставить поиск только больших букв и целого слова: 'РИА' ---  '\bРИА\b' но не ищется,  
# сильно много лишних -- определить слово и тогда вернуть: 'znaj',
# !!! l_4mark = ['\.ru', '\.su']

l_4mark = ['\.ru\b', '\.ru/', '\.su\b', '\.su/', 'hyser\.', '112ua.tv','zikua.tv','nash.live','klymenko-time',
               'sharij','ukrainian.ru','topinform','mignews.ua',
               'politeca','dubinsky.ua', 'программы стоянова',
               'программа Стоянова', 'нашего Стоянова', 'нашего городка', 'российский шоубизнес', 'одесский городок',
              'РИА новости','eadaily.com']

# l_4mark = ['\bРИА\b']

mark4 = '|'.join(l_4mark) 
#  поиск потенциальных пропаг. постов в месседжах по 4 критерию:    
df_4=df[((~ (df['Group Name'].str.contains('Думская net')))
               & (~ (df['Link'].str.contains(linksgood, na=False)))
               & (~ (df['Message'].str.contains(linksgood, na=False)))
               & (~ (df['Description'].str.contains(linksgood, na=False)))
               & (~ (df['URL'].str.contains(linksgood, na=False)))  )              
               & (((df['Message'].str.contains(mark4, na=False)))
               | ((df['Link Text'].str.contains(mark4, na=False)))
               | ((df['Image Text'].str.contains(mark4, na=False)))
               | ((df['Link'].str.contains(mark4, na=False)))
               | ((df['Description'].str.contains(mark4, na=False)))
               )] 


#===========  _новое_  =====================
# составление списка уникальных значений поля Type
l_tipov = df.Type.unique()
df_4types = df_4['Type'].value_counts().to_frame()
df_4typ = df_4['Type'].value_counts()
#запись во фрейм частот уник значений:

# подсчет дины строки - кривоват:
# df_4["length3"] = df_4[(df_4["Type"].apply(lambda x: len(x)))]
#  подсчет количества точек с пробелом после них:
df_4['Len7'] = df_4['Message'].str.count('\. ')
#!!! двуступенчатый подсчет руками: 
# 1) выборка всех с числом предложений (в  Мессадже) больше 3:
# df123 = df_4.loc[(df_4['Len7'] >= 3)]   #определние типов в найденном:
# df123['Type'].value_counts()
# может вот такое еще попробовать: views = df.groupby('hour')['views'].sum()


# делает что-то классное, но непонятное: 
# rt = df_4.drop_duplicates('Type')['Type'].apply( \
# lambda x: df_4[df_4['Type'] == x].index.tolist())

# подсчет количества уникальных групп каждого типа:

# сумма только лайков:    
# tot_likes4 = df_4['Likes'].sum()   
# сумма лайков всех видов по группе:
tot_likes4 = (df_4['Likes'].sum())+(df_4['Love'].sum())+ \
   (df_4['Wow'].sum()) + (df_4['Haha'].sum()) + (df_4['Sad'].sum()) + \
   (df_4['Angry'].sum()) + (df_4['Care'].sum())
# сумма комментариев по группе:    
tot_comments4 = df_4['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share4 = df_4['Shares'].sum()    

# лайки, репосты и комменты по всему массиву: 
tot_likes = (df['Likes'].sum())+(df['Love'].sum())+ \
   (df['Wow'].sum()) + (df['Haha'].sum()) + (df['Sad'].sum()) + \
   (df['Angry'].sum()) + (df['Care'].sum())
# сумма комментариев по группе:    
tot_comments = df['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share = df['Shares'].sum()    

# надо еще расчет процента лайков и прочего группы поотношению ко всем за неделю
# =====================================



#экспорт в csv: -- исправить кириллицу (UTF-8 ??)   

df_4.to_csv("df_4_1.csv",encoding='utf-8-sig')




# Подсчет пересечения (надо еще доразобраться (возм., лучше взять конкатенацию (внизу))):
    


    

# разобраться еще с их списком и подсчетом их аудитории
# df_1234567 = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7])
# print df_1234567['Group Name'].nunique()