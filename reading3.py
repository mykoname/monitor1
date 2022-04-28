# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
# automated_monitor1
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
                    '400928366716548', '106963360910053', '410274922719569', 'liga.net',
                    '#ЭкскурсиипоОдессе', '#фотоОдессы', '#историяОдессы', 
                    '#гидпоОдессе', '#гидОдесса', '#МестовстречиОдесса', 'mesto.vstrechi.Odessa',
                    "831992277000711",
                    
                    'Срочный репост!', "Браво!!", "Срочно!", "Спасем трассу",
                     'Срочный репост !', "Спасем Трассу",
                     "#ВсемирныйКлубОдесситов",
                     "Официальный курс НБУ:"
                     "Одеської міської",                    
                    "З/П від", "з/п від"
                    ]
linksgood = '|'.join(l_good_links)  
#! список хороших в Description (пока добавляю в хор линки):    
#    l_good_descr = ['gov.ua']
#список под 1 критерий: (потом решить: 'мова', 'мови', 'мовы', 'майдан',  Без восстаний и майданов, 'омбудсмен', 'Кремень', 
#   'патриот', 'СВОБОДІ', 'Креминь', )
l_1mark = ['патрийоты', 'нацики'
                'пэрэклад', 'майдаун', 
               'майданут','шпрехенфюрер','соросята','подлость']
mark1 = '|'.join(l_1mark) 
#  поиск потенциальных пропаг. постов в месседжах по 1 критерию:    
df_1=df[((~ (df['Group Name'].str.contains('Думская net')))
               & (~ (df['Link'].str.contains(linksgood, na=False)))
               & (~ (df['Message'].str.contains(linksgood, na=False)))
               & (~ (df['Description'].str.contains(linksgood, na=False)))
               & (~ (df['URL'].str.contains(linksgood, na=False)))  )              
               & (((df['Message'].str.contains(mark1, na=False)))
               | ((df['Link Text'].str.contains(mark1, na=False)))
               | ((df['Image Text'].str.contains(mark1, na=False)))
               | ((df['Link'].str.contains(mark1, na=False)))
               | ((df['Description'].str.contains(mark1, na=False)))
               )]     
    
#список под 2 критерий:
# потом решить: еще лет 10 таких цен и зарплат, и перепись населения не понадобиться    
# празднует д.р. бандеры, 
# врачи в наших поликлиниках, весь 'зароботок уходит на оплату питания' и крыши над головой
# обман---не брать, наверное
# 'незалежна',  трус, трусость, скандал, скандальный, скандального, 'провокац' 
#  находятся обычные аферы: 'продать землю',
l_2mark =[
        'надо так испортить настоящее','мечтая о будущем, хотели вернуть прошлое',
        'ограбление страны',
        'нелюбовь к стране','повышение пенсионного возраста', 
        'наша власть как наркоман',       
        'все москали виноваты', 
        'зароботок уходит на оплату питания',
        'вытворяет с народом власть',
        'вытворяет власть',
        'прощение у Януковича',
        'прощения у Януковича',
        'умчи меня олень в свою страну оленью',
        'единые с Россией',
        'ейленский', 'незалэжна', "незалежный"]
mark2 = '|'.join(l_2mark) 
#  поиск потенциальных пропаг. постов в месседжах по 2 критерию:    
df_2=df[((~ (df['Group Name'].str.contains('Думская net')))
               & (~ (df['Link'].str.contains(linksgood, na=False)))
               & (~ (df['Message'].str.contains(linksgood, na=False)))
               & (~ (df['Description'].str.contains(linksgood, na=False)))
               & (~ (df['URL'].str.contains(linksgood, na=False)))  )              
               & (((df['Message'].str.contains(mark2, na=False)))
               | ((df['Link Text'].str.contains(mark2, na=False)))
               | ((df['Image Text'].str.contains(mark2, na=False)))
               | ((df['Link'].str.contains(mark2, na=False)))
               | ((df['Description'].str.contains(mark2, na=False)))
               )] 
    
#список под 3 критерий: ('геноцид' -- в неделю голодомора дает ложные срабатывания)
# 'подорожание', -- (надо чем-то взвесить дополнительно)
l_3mark = ['обманы вакцин', "обман вакц", 'подскочили тарифы', # "подскочили цены",
               'продовольственная катастрофа', 'продовольственной катастрофы']
mark3 = '|'.join(l_3mark) 
#  поиск потенциальных пропаг. постов в месседжах по 3 критерию:    
df_3=df[((~ (df['Group Name'].str.contains('Думская net')))
               & (~ (df['Link'].str.contains(linksgood, na=False)))
               & (~ (df['Message'].str.contains(linksgood, na=False)))
               & (~ (df['Description'].str.contains(linksgood, na=False)))
               & (~ (df['URL'].str.contains(linksgood, na=False)))  )              
               & (((df['Message'].str.contains(mark3, na=False)))
               | ((df['Link Text'].str.contains(mark3, na=False)))
               | ((df['Image Text'].str.contains(mark3, na=False)))
               | ((df['Link'].str.contains(mark3, na=False)))
               | ((df['Description'].str.contains(mark3, na=False)))
               )]

#список под 4 критерий
#(возможно уточнить этих: програмы стоянова, российский шоубизнес, российские СМИ,)
#возм., добавить сюда персонали из старых (Азаров, Янукович, Курченко, Клименко 
#(только отсечь их позиивные/негативные упоминания -- взять здесь только позитивные))
# vesti.ua
# !!поставить поиск только больших букв и целого слова: 'РИА' ---  '\bРИА\b' но не ищется,  
# сильно много лишних -- определить слово и тогда вернуть: 'znaj',
# !!решить еще ссылки на ютуб каналы типа Стоянова
# +сделать обработку неск пробелов типа "проект(А) стоянова"  +обрабатывать склонения
# !!! l_4mark = ['\.ru', '\.su']

l_4mark = ['\.ru\b', '\.ru/', '\.su\b', '\.su/', 'hyser\.', 'ura.news', '112ua.tv','zikua.tv','nash.live','klymenko-time',
               'sharij','ukrainian.ru','topinform','mignews.ua', '#НАШ',
               'politeca','dubinsky.ua', 'программы стоянова',
               'программа Стоянова', 'нашего Стоянова', 'нашего городка', 'российский шоубизнес', 'одесский городок',
              'РИА новости','eadaily.com', "do-slez.com",
              'летел в Москв']

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

#список под 5 критерий: 
# точно не беру или ищу адекв замену:'молоды' 'российский' 'бессмертн']# Кремль', 'Москв']'как в детств''молодост'
# найти хвосты правильно: отечественной эстрады
# сомительно, но для количества можно взять: 'А знаете ли Вы?' (пока взял) 
# надо проверять еще: 'комсомол'
# надо бы но как-то скорректировать дополнительно(возможно, по источнику -- хор/не_хор): 'советск''отечество'
# пока не беру след слова: 'детст',  'ХХ',    'г.', 'год', СРСР
#                'Росси', 'российск', 'россиян', 'русски', 'русско','ГОСТу'
# пока беру, но возможно не надо: 'Та ещё Одесса', "Та еще Одесса", 'привет из прошлого',
#              'из прошлой жизни', 'пионер','коммунист'
# РСФСР пока не беру, потом можно, но надо отсекать по языку группы или поста -- если укр, то не брать

l_5mark = ['отечественной эстрады', "отечественная эстрада", 'ВМФ России', 'ВМФ РФ', 'Питер', 'Красная Армия',
   'Маршал Победы', "Жуков", 'росСМИ', "рос-СМИ", "Аэрофлот", '100001952462898', "658764777849387",
   '1912264852341821', '590624458721237',
   "ностальг", 
   'Вот такая Одесса', 
   'советские фильмы', 'советский фильм', "советских фильм", 'молодежи не понять', 'Та ещё Одесса', "Та еще Одесса",
   'А знаете ли Вы?',
   'привет из прошлого', 'из прошлой жизни', 'пионер','коммунист', 'Мульт из СССР',  
   'артист СССР', 'артист РСФСР', "артистка РСФСР", "артистка СССР", "#Ленинград", "#ТоварищКино", "#СССР",
               'ПУТЕШЕСТВИЕ ВО ВРЕМЕНИ',
               'ОДЕССА В СТАРОЙ КИНОХРОНИКЕ',
               'КИНОСЪЁМОЧНЫЕ ПЛОЩАДКИ ОДЕССЫ',
               'ОДЕССА В СТАРЫХ ФОТОГРАФИЯХ',            
               'советская Одесса', '30-е', '40-е',
               '50-е', '60-е', '70-е', '80-е',
               '50-х', '60-х', '70-х', '80-х',
               '50-ом', '60-е', '70-е', '80-е',
               'в старых фотографиях',
               'старая аркадия', 'старая Аркадия',
               'старая дерибасовская', 'старая Дерибасовская',
               'фотоархивы',
               'наш день 9 мая',
]

mark5 = '|'.join(l_5mark) 
#  поиск потенциальных пропаг. постов в месседжах по 5 критерию:    
df_5=df[((~ (df['Group Name'].str.contains('Думская net')))
               & (~ (df['Link'].str.contains(linksgood, na=False)))
               & (~ (df['Message'].str.contains(linksgood, na=False)))
               & (~ (df['Description'].str.contains(linksgood, na=False)))
               & (~ (df['URL'].str.contains(linksgood, na=False)))  )              
               & (((df['Message'].str.contains(mark5, na=False)))
               | ((df['Link Text'].str.contains(mark5, na=False)))
               | ((df['Image Text'].str.contains(mark5, na=False)))
               | ((df['Link'].str.contains(mark5, na=False)))
               | ((df['Description'].str.contains(mark5, na=False)))
               )]
    
#список под 6 критерий:
# потом решить: на каком языке говорила старая одесса,
# ОДЕССИТЫ И ОДЭСЫТЫ - ДВЕ БОЛЬШИЕ РАЗНИЦЫ',
# Какие мы? Что это за нация, такая бесшабашная и обезбашенная, и такая талантливая, разбросанная по всему земному шару?
# 'уникальность',     'неповторимые',     'наш язык',    'наш менталитет',    'ментальность',
l_6mark = ['Одесситы - это отдельная каста','отдельная каста',
    'одесская речь', 'Одесская речь',
    'одесский язык', 'Одесский язык',
    'свой язык',
    'одессит! помни свою историю',
    'одесская вышиванка',
    'Одесса будет свободн',
    'одесский гимн',
    'национальность - одессит',
    'ОДЕССИТЫ И ОДЭСЫТЫ',
    'Кто мы такие - Одесситы',
    
    'красно-жёлтый биколор', 'бессарабский биколор', 
    'бессарабским биколор', "биколор", "знамя родного города", "знамя Белгорода",
    "флаг Белгород"]
mark6 = '|'.join(l_6mark) 
#  поиск потенциальных пропаг. постов в месседжах по 6 критерию:    
df_6=df[((~ (df['Group Name'].str.contains('Думская net')))
               & (~ (df['Link'].str.contains(linksgood, na=False)))
               & (~ (df['Message'].str.contains(linksgood, na=False)))
               & (~ (df['Description'].str.contains(linksgood, na=False)))
               & (~ (df['URL'].str.contains(linksgood, na=False)))  )              
               & (((df['Message'].str.contains(mark6, na=False)))
               | ((df['Link Text'].str.contains(mark6, na=False)))
               | ((df['Image Text'].str.contains(mark6, na=False)))
               | ((df['Link'].str.contains(mark6, na=False)))
               | ((df['Description'].str.contains(mark6, na=False)))
               )] 
        
#список под 7 критерий:
#потом разобраться  ЛДНР, ЛНР, ДНР, Крым, новороссия, новороссии, новороссией
# республика, самооборона, 
l_7mark = [    
    'ополчение', 'ополченцы', 'в Донбассе', 'правительственные войска', 
    'правительственных войск', 'правительствеными войсками']
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

#===========  _новое_  =====================
# составление списка уникальных значений поля Type
l_tipov = df.Type.unique()

df_1typ = df_1['Type'].value_counts()
df_3typ = df_3['Type'].value_counts()

df_4typ = df_4['Type'].value_counts()
#запись во фрейм частот уник значений:
# df_4types = df_4['Type'].value_counts().to_frame()
df_5typ = df_5['Type'].value_counts()
df_6typ = df_6['Type'].value_counts()
df_7typ = df_7['Type'].value_counts()

# подсчет дины строки - кривоват:
# df_4["length3"] = df_4[(df_4["Type"].apply(lambda x: len(x)))]
#  подсчет количества точек с пробелом после них:
df_1['Len7'] = df_1['Message'].str.count('\. ')
df_3['Len7'] = df_3['Message'].str.count('\. ')
df_4['Len7'] = df_4['Message'].str.count('\. ')
df_5['Len7'] = df_5['Message'].str.count('\. ')
df_6['Len7'] = df_6['Message'].str.count('\. ')
df_7['Len7'] = df_7['Message'].str.count('\. ')

#!!!!!!!!!!!!!! двуступенчатый подсчет руками: !!!!!!!!!!!!!!!!!!!!!!!!!!
# 1) выборка всех с числом предложений (в  Мессадже) больше 3:
# df123 = df_4.loc[(df_4['Len7'] >= 3)]   #определние типов в найденном:
# df123['Type'].value_counts()
# может вот такое еще попробовать: views = df.groupby('hour')['views'].sum()


# делает что-то классное, но непонятное: 
# rt = df_4.drop_duplicates('Type')['Type'].apply( \
# lambda x: df_4[df_4['Type'] == x].index.tolist())

# подсчет количества уникальных групп каждого типа:

# 1_group:
# сумма лайков всех видов по группе:
tot_likes1 = (df_1['Likes'].sum())+(df_1['Love'].sum())+ \
   (df_1['Wow'].sum()) + (df_1['Haha'].sum()) + (df_1['Sad'].sum()) + \
   (df_1['Angry'].sum()) + (df_1['Care'].sum())
# сумма комментариев по группе:    
tot_comments1 = df_1['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share1 = df_1['Shares'].sum()      
    
# 2_group:
# сумма лайков всех видов по группе:
tot_likes2 = (df_2['Likes'].sum())+(df_2['Love'].sum())+ \
   (df_2['Wow'].sum()) + (df_2['Haha'].sum()) + (df_2['Sad'].sum()) + \
   (df_2['Angry'].sum()) + (df_2['Care'].sum())
# сумма комментариев по группе:    
tot_comments2 = df_2['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share2 = df_2['Shares'].sum()      

# 3_group:
# сумма лайков всех видов по группе:
tot_likes3 = (df_3['Likes'].sum())+(df_3['Love'].sum())+ \
   (df_3['Wow'].sum()) + (df_3['Haha'].sum()) + (df_3['Sad'].sum()) + \
   (df_3['Angry'].sum()) + (df_3['Care'].sum())
# сумма комментариев по группе:    
tot_comments3 = df_3['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share3 = df_3['Shares'].sum()        

# 4_group:
# tot_likes4 = df_4['Likes'].sum()   
# сумма лайков всех видов по группе:
tot_likes4 = (df_4['Likes'].sum())+(df_4['Love'].sum())+ \
   (df_4['Wow'].sum()) + (df_4['Haha'].sum()) + (df_4['Sad'].sum()) + \
   (df_4['Angry'].sum()) + (df_4['Care'].sum())
# сумма комментариев по группе:    
tot_comments4 = df_4['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share4 = df_4['Shares'].sum()    

# 5-group:
# сумма только лайков:    
# сумма лайков всех видов по группе:
tot_likes5 = (df_5['Likes'].sum())+(df_5['Love'].sum())+ \
   (df_5['Wow'].sum()) + (df_5['Haha'].sum()) + (df_5['Sad'].sum()) + \
   (df_5['Angry'].sum()) + (df_5['Care'].sum())
# сумма комментариев по группе:    
tot_comments5 = df_5['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share5 = df_5['Shares'].sum()        

# 6_group:
# сумма лайков всех видов по группе:
tot_likes6 = (df_6['Likes'].sum())+(df_6['Love'].sum())+ \
   (df_6['Wow'].sum()) + (df_6['Haha'].sum()) + (df_6['Sad'].sum()) + \
   (df_6['Angry'].sum()) + (df_6['Care'].sum())
# сумма комментариев по группе:    
tot_comments6 = df_6['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share6 = df_6['Shares'].sum()      

# 7-group:
# сумма только лайков:    
# сумма лайков всех видов по группе:
tot_likes7 = (df_7['Likes'].sum())+(df_7['Love'].sum())+ \
   (df_7['Wow'].sum()) + (df_7['Haha'].sum()) + (df_7['Sad'].sum()) + \
   (df_7['Angry'].sum()) + (df_7['Care'].sum())
# сумма комментариев по группе:    
tot_comments7 = df_7['Comments'].sum()   
# сумма репостов (Share) по группе:    
tot_share7 = df_7['Shares'].sum()        

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
df_1.to_csv("df_1.csv",encoding='utf-8-sig')
df_2.to_csv("df_2.csv",encoding='utf-8-sig')
df_3.to_csv("df_3.csv",encoding='utf-8-sig')
df_4.to_csv("df_4.csv",encoding='utf-8-sig')
df_5.to_csv("df_5.csv",encoding='utf-8-sig')
df_6.to_csv("df_6.csv",encoding='utf-8-sig')
df_7.to_csv("df_7.csv",encoding='utf-8-sig')

# Подсчет пересечения (надо еще доразобраться (возм., лучше взять конкатенацию (внизу))):
df_45 = pd.merge(df_4,df_5)
df_57 = pd.merge(df_5,df_7)
df_46 = pd.merge(df_4,df_6)
df_56 = pd.merge(df_5,df_6)

# полдсчет количества уникальных групп:
# разобраться еще с их списком и подсчетом их аудитории
# df_1234567 = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7])
# print df_1234567['Group Name'].nunique()