# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
# automated_monitor1
!!! считаю сумму пабликов с попагандой (по общему сначала собранному файлу из df-ов):

"""
import numpy as np
import pandas as pd
import re
import codecs
datafilename = "d:/progs/avtom_monitor/06-12_12_2021/6-12_12_2021_groups&pages.csv"
datafp = pd.read_csv(datafilename, index_col= None, encoding='utf-8-sig')
dfp = datafp  # назначаю df  для игрищ, а dataf - полный фрейм
dfp.shape  #receiving a data structure
dfp.dtypes  #выяснение типа данных в столбцах
dfp.head

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
dfp['Group Name'].nunique() 
dfp_groups_all = dfp['Group Name'].value_counts()
dfp_types_all = dfp['Type'].value_counts()
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
    


#===========  _новое_  =====================
# составление списка уникальных значений поля Type
# l_tipov = df.Type.unique()
# df_4types = df_4['Type'].value_counts().to_frame()
# df_4typ = df_4['Type'].value_counts()
#запись во фрейм частот уник значений:

# подсчет дины строки - кривоват:
# df_4["length3"] = df_4[(df_4["Type"].apply(lambda x: len(x)))]
#  подсчет количества точек с пробелом после них:
# df_4['Len7'] = df_4['Message'].str.count('\. ')
#!!! двуступенчатый подсчет руками: 
# 1) выборка всех с числом предложений (в  Мессадже) больше 3:
# df123 = df_4.loc[(df_4['Len7'] >= 3)]   #определние типов в найденном:
# df123['Type'].value_counts()
# может вот такое еще попробовать: views = df.groupby('hour')['views'].sum()
# =====================================



#экспорт в csv: -- исправить кириллицу (UTF-8 ??)   

# df_4.to_csv("df_4rus20.csv",encoding='utf-8-sig')




# Подсчет пересечения (надо еще доразобраться (возм., лучше взять конкатенацию (внизу))):
    


    

# разобраться еще с их списком и подсчетом их аудитории
# df_1234567 = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7])
# print df_1234567['Group Name'].nunique()