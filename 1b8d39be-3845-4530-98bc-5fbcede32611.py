#!/usr/bin/env python
# coding: utf-8

# # Исследование надёжности заёмщиков
# 
# Заказчик — кредитный отдел банка. Нужно разобраться, влияет ли семейное положение и количество детей клиента на факт погашения кредита в срок. Входные данные от банка — статистика о платёжеспособности клиентов.
# 
# Результаты исследования будут учтены при построении модели **кредитного скоринга** — специальной системы, которая оценивает способность потенциального заёмщика вернуть кредит банку.

# 
# <div class="alert alert-info">
# Привет! Меня зовут Никита Мишин и я буду твоим ревьюером по этому проекты.
# Для простоты предлагаю общение на 'ты'. Буду предполагать, что ты не против:) 
# Если более предпочтительно обращение на 'Вы', пиши, не стесняйся.
# Также если будут возникать вопросы, аналогично, пиши:)
# 
# Предлагаю работать в известном тебе итеративном формате.
# Итерация состоит в моей проверке твоего решения. 
# После решения могут остаться какие-то недочеты, которые я попрошу тебя устранить, ты их исправляешь и я проверяю твои решения.
#     Оставленные мною комментарии могут быть разного вида:
#    
#     - зеленый: элегантные решения, которые тебе стоит запомнит и в дальнейшем взять на вооружение:) 
#     
#     - желтый: сигнал о том, что есть некритичная вещь(не всегда ошибка), что нужно точно поправить в следующей работе, даже желательно в этой (полезно, в первую очередь, для тебя:) ).Также это рекомендации на будущее    
# 
#     - красный: недочет, который нужно исправить в этой работе, для того, чтобы она была принята
#     
#     - синий: полезная информация, доп ресурсы, "вопросы на подумать"
# 
# Также попрошу не удалять мои комментарии:) <a class="tocSkip">
# </div>

# 
# <div class="alert alert-info">
# Никита, привет! Рад познакомиться :).
# Большое спасибо за подсказки и за замечания. Я закомментировал некоторые поля, чтобы ты видел старый код и оценил мощь нового :))
#  
# Постарался исправить все недочёты, которые ты указал. Приятного просмотра!

# ## Шаг 1. Откройте файл с данными и изучите общую информацию

# In[1]:


import pandas as pd
from pymystem3 import Mystem 
m = Mystem()
from collections import Counter 



df = pd.read_csv('/datasets/data.csv')


# In[2]:


df.columns #Проверяем корректность названия столбцов. Пробелов и ошибок не обнаружено


# In[3]:


display(df.head(10))


# In[4]:


df.info() #Получаем общую информацию о таблице, типах данных
df.isnull().sum() #Вычисляем количество пропусков


# In[5]:


df.describe()


# In[6]:


days_employed_real_numb = (70 - 18) * 247
print(days_employed_real_numb)


# Где:
#     70 - возраст, до которого человек работает (с запасом к пенисонному)
#     18 - возраст зачисления на работу 
#     247 - среднее количество рабочих дней в году
# Таким образом, мы получили более-менее реалистичную цифру. Однако в нашей таблице мы увидели значения, которые намного превышают это число.
# 

# .
# <div class="alert alert-info">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Также советую использовать следующие методы:
#   - describe --- просмотр основных статистик выборки (ты много аномалий пропустил в датасете)
#   - sample(random_state=some) --- позволяет посмотреть на  случайные n строк выборки
# </div>

# **Вывод** 
# 
# 

# В прочитанном нами файле обнаружены следующие недочёты:
# 1. В столбце 'days_employed' во множестве случаев представлено число отработанных дней со знаком минус. Также имеется артефакт с данными отработанных дней у людей, которые старше 50 лет.
# 2. В столбце 'education' сведения об образовании заполнены везде по-разному: заглавными, строчными, заглавными и строчными буквами.
# 3. В столбце 'purpose' имеются одинаковые цели получения кредита, которые написанные разными словами
# 
# Вызвав метод info() , были обнаружены пропуски в столбцах:
# 1. days_employed (NaN) -float64
# 2. total_income (NaN) -float64
# 
# Вызвав метод describe() , мы обнаружили аномалии в столбце days_employed.Показатель mean гласит, что якобы в среднем люди работали по 66 000 дней, что никак невозможно. Относительно реальное количество рабочих дней составляет порядка 13 тысяч. В следующее наше действие - более детально изучить эти данные и принять решение каким способом их заменить.

# .
# <div class="alert alert-success">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Также советую использовать следующие методы:
# Молодец, что локализовал проблемы</div>

# ## Шаг 2. Предобработка данных

# ### Обработка пропусков

# In[7]:


df['days_employed'] = df['days_employed'].abs()
display(df.head(10))


# In[8]:


#df.loc[df.isnull().any(axis=1)] #Запрашиваем строки с пропущенными значениями


# In[9]:


days_empl_median = df['days_employed'].median()


# In[10]:


df['income_type'].unique()


# In[11]:


#df['total_income'] > days_employed_real_numb
df.loc[(df['days_employed'] > days_employed_real_numb)].count()


# In[12]:


df['days_employed'].mean()


# In[13]:


df.loc[(df['days_employed'] > days_empl_median)].count()


# In[14]:


df.pivot_table(index='income_type', values=['days_employed', 'dob_years'], aggfunc='median')


# При выгрузке некоторых данных явно произошла какая-то ошибка, либо данные в систему были внесены некорректно. Человек с типом занятости "Сотрудник" и медианным возрастом 39 лет отработал всего 1574 дня, что составляет порядка 6 лет стажа, то есть получается, что сотрудник якобы устроился на работу в 33 года, ну или до этого примерно 10 лет работал неофициально. Допустим, это возможно, это значение мы оставим.
# Люди с типом занятости "Пенсионер" и "Безработный" выглядят абсолютно неправдоподобно. Была допущена ошибка. Вполне возможно, что сотрудник внёс данные об отработанных часах, в таком случае, это похоже на правду для пенсионера, но никак не похоже на безработного (если ещё учесть, что медианный возраст 38 лет)
# Данные по остальным группам выглядят правдоподобно.
# 
# Что делаем:
# 1. В пропусках для категорий "Сотрудник", "В декрете", "Студент", "Госслужащий", "Предприниматель", "Компаньон" заменяем данные по медиане этих категорий
# 2. В пропусках для категории "Пенсионер" заменяем данные по медиане, разделенной на 24 (ч)
# 3. В пропусках для категории "Безработный" заменяем данные по общей медиане. Такое решение я принял в связи с тем, что какое-то минимальное количество рабочих дней так или иначе было отработано этими людьми, поэтому я взял самое минимальное медианное число из всех представленных.
# 

# In[15]:


especially_group = 'сотрудник', 'компаньон', 'госслужащий','предприниматель', 'студент', 'в декрете'


# In[16]:


print(especially_group)


# In[17]:


df.loc[df['income_type']=='пенсионер', 'days_employed'] /= 24

pens_median = df.loc[(df['income_type'] =='пенсионер') & (df['days_employed'])].median()

print(pens_median)


# In[18]:


df.loc[(df['days_employed'].isna())&(df['income_type']=='пенсионер'), 'days_employed' ] = 15217


# In[19]:


df.loc[(df['income_type'] =='пенсионер')].isna().sum()


# In[20]:


df.loc[(df['income_type'] =='безработный')].count()


# In[21]:


df.loc[df['income_type']=='безработный', 'days_employed'] = df['days_employed'].median()


# In[22]:


df.loc[(df['income_type'] =='безработный')]


# In[ ]:





# In[23]:


def change_nan(data, category, value):
  for type in especially_group:
    data.loc[(data[value].isna())&(data[category]==type), value ] =data.loc[data[category]==type, value].median()


# In[24]:


change_nan(df, 'income_type', 'days_employed')


# In[25]:


df.info()

#df.loc[(df['total_income'].isnull())&(df['income_type'].count()

#df.pivot_table(index='income_type', values='days_employed', aggfunc='mean')
                                      

#df.loc[df.isnull().any(axis=1)]


# In[26]:


df['days_employed'].isna().sum()


# In[27]:


def change_nan(dataset, category, value):
    for type in dataset[category].unique():
        dataset.loc[(dataset[value].isna())&(dataset[category]==type), value ] =dataset.loc[dataset[category]==type, value].median()


# 
# <div class="alert alert-success">
# <h1>Комментарий ревьюера v2 <a class="tocSkip"></a></h1>
# Молодец, что поправил замечание:)</div>

# In[28]:


change_nan(df, 'income_type', 'total_income')


# In[29]:


df['total_income'].isna().sum()


# In[30]:


df.info()


# **Вывод**
# Обнаруженные аномальные значения в столбце days_employed были вычислены и заменены, также мы обработали все пропуски.
# С помощью функции были обработаны все пропуски в столбце total_income.

# <div class="alert alert-danger">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Все же 10 процентов пропусков довольно существенная часть данных, результаты получатся искаженные.
# 
# 
# Подсказка: заполнение медианой по группа по income_type (fillna+transform)
# </div>

# In[31]:


#df.dropna(subset=['days_employed', 'total_income'], inplace=True) #удаляем все строки, где есть пропущенные значения


# In[32]:


#df.info() #проверяем удалились ли дубликаты


# ### Замена типа данных

# In[33]:


df['days_employed'] = df['days_employed'].astype(int) # заменяем тип данных float64 на int в столбце days_employed
df['total_income'] = df['total_income'].astype(int)# заменяем тип данных float64 на int в столбце total_income
df.info()


# In[ ]:





# **Вывод**
# Заменены значения на целочисленные

# 
# <div class="alert alert-info">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Интересно было бы исследовать природу пропусков. Возможно, это относится к какой-то специфичной группе людей.
# 
# 
# Также отсутствует анализ экстримальных значений
# </div>

# ### Обработка дубликатов

# In[34]:


df.duplicated().sum() #вычисляем сумму дубликатов в df


# In[35]:


df.loc[df.duplicated()]


# In[36]:


df['education'].unique() #посмотрим на количество уникальных значений в столбце education


# In[37]:


df['education'] = df['education'].str.lower() #сделаем все буквы строчными, чтобы избавиться от дубликатов

df['education'].unique() #проверяем результат замены


# In[38]:


df.loc[df.duplicated()]


# 
# <div class="alert alert-warning">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Это надо было делать после привидения к нижнему регистру образования</div>

# In[39]:


df['purpose'].value_counts() #проверяем наличие дубликатов в столбце purpose


# **Вывод**
# Ручным способом были обнаружены дубликаты в столбце purpose. Похожие слова, измененный порядок слов.

# 
# <div class="alert alert-info">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Да, когда данные регистронезависимые, их всегда нужно приводить к единому формату</div>

# Данные приведены в порядок

# ### Лемматизация

# In[40]:



df['purpose_new'] = df['purpose'].apply(m.lemmatize) #создаем новый столбец с лемматизированными словами


print(Counter(df['purpose_new'].sum())) #получаем часто используемые цели кредита. Выделили 4 категории: недвижимость, образование, автомобиль, свадьба



# 
# <div class="alert alert-info">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Все импорты лучше располагать в начале проекта</div>

# In[41]:


def change_purpose(purpose):
    if 'жилье'  in purpose:
        return 'недвижимость'
    if 'автомобиль' in purpose:
        return 'автомобиль'
    if 'образование' in purpose:
        return 'образование'
    if 'свадьба' in purpose:
        return 'свадьба'
    if 'недвижимость' in purpose:
        return 'недвижимость'

df['purpose_aggr'] = df['purpose_new'].apply(change_purpose) #создали новый столбец с измененной целью кредита
print(df.tail(10))


# 
# <div class="alert alert-info">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Молодец, основные категории верно выделены</div>

# **Вывод**

# С помощью лемматизации выделили 4 основные цели кредита

# ### Категоризация данных

# In[42]:


#разобьём наших заемщиков на категории по уровню ЗП

def category_income(total_income):
    if total_income < 30000:
        return('низкий')
    if total_income < 70000:
        return('ниже среднего')
    if total_income < 120000:
        return('средний')
    if total_income > 120000:
        return('высокий')
#print(category_income(1000000)) # проверка работоспособности функции

df['category_income'] = df['total_income'].apply(category_income) #добавляем новый столбец с уровнем дохода, согласно нашему правилу

print(df)


# 
# <div class="alert alert-info">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Тут лучше всего для разбиения использовать квантили и квартили</div>

# **Вывод**

# Провели категоризацию по уровню дохода, чтобы решить одну из поставленных задач.

# ## Шаг 3. Ответьте на вопросы

# - Есть ли зависимость между наличием детей и возвратом кредита в срок?

# In[67]:


#childfree = df.loc[(df['children']==0)&(df['debt']==0), 'debt'].count()
#print(childfree)

#parents = df.loc[(df['children']>0)&(df['debt']==0), 'debt'].count()

#debt_parents = df.loc[(df['children']>0)&(df['debt']==1), 'debt'].count()

#debt_childfree = df.loc[(df['children']==0)&(df['debt']==1), 'debt'].count()

#total = childfree + parents + debt_parents + debt_childfree
#print(total)
#part_childfree_debt = debt_childfree / childfree
#part_parents_debt = debt_parents / parents


#print('Количество бездетных не имеющих задолженности:', childfree)
#print('Количество бездетных с задолженностью:', debt_childfree,', ' 'Доля от числа бездетных: {:.1%}'.format(part_childfree_debt))
#print('Кол-во родителей не имеющих задолженности:', parents)
#print('Количество родителей с задолженностью:', debt_parents, ', ' 'Доля от числа родителей: {:.1%}'.format(part_parents_debt))


# In[68]:


df.pivot_table(index='debt', columns='children', aggfunc='count')


# In[69]:


df.groupby('children')['debt'].mean()


# <div class="alert alert-danger">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# а верно ли ты считаешь процент?
# 
# Попробуй посчитать ответ через pivot_table - и практику закрепишь  и короче и проще код будет
# </div>

# **Вывод**

# Если судить по цифрам, то есть незначительная зависимость между наличием детей и возвратом кредита в срок. Но разница небольшая: порядка 2%. Если ещё учесть тот факт, что родителям нужно явно больше средств, чем бездетным, то эту разницу между этими категорями можно не принимать во внимание. Скажем, если бы разница была от 10% и более, то да, могли бы увеличить ставку по кредиту для родителей, но вместе с этим пришлось бы увеличить срок погашения кредита.

# 
# <div class="alert alert-warning">
# <h1>Комментарий ревьюера v2 <a class="tocSkip"></a></h1>
# Смотри, разница даже в 1 процент может быть значительна, когда речь идет о больших данных:)</div>

# - Есть ли зависимость между семейным положением и возвратом кредита в срок?

# In[18]:


print(df.groupby('family_status')['debt'].value_counts())

married = df[df['family_status'] == 'женат / замужем']['family_status'].count()
debt_married = df.loc[(df['family_status']=='женат / замужем')&(df['debt']==1), 'debt'].count()
debt_to_married = debt_married / married

unmarried = df[df['family_status'] == 'Не женат / не замужем']['family_status'].count()
debt_unmarried = df.loc[(df['family_status']=='Не женат / не замужем')&(df['debt']==1), 'debt'].count()
debt_to_unmarried = debt_unmarried / unmarried

wid = df[df['family_status'] == 'вдовец / вдова']['family_status'].count()
debt_wid = df.loc[(df['family_status']=='вдовец / вдова')&(df['debt']==1), 'debt'].count()
debt_to_wed = debt_wid / wid

roommates = df[df['family_status'] == 'гражданский брак']['family_status'].count()
debt_roommates = df.loc[(df['family_status']=='гражданский брак')&(df['debt']==1), 'debt'].count()
debt_to_roommates = debt_roommates / roommates

print('Доля должников среди женатых составляет: {:.1%}'.format(debt_to_married))
print('Доля должников среди неженатых / незамужних составляет: {:.1%}'.format(debt_to_unmarried))
print('Доля должников среди вдов  составляет: {:.1%}'.format(debt_to_wed))
print('Доля должников среди сожителей в гражданском браке составляет: {:.1%}'.format(debt_to_roommates))


# In[ ]:





# **Вывод**

# Есть определенная зависимость. Чем старше человек, тем меньше вероятность появления задолженности. 

# - Есть ли зависимость между уровнем дохода и возвратом кредита в срок?

# In[19]:


print(df.groupby('category_income')['debt'].value_counts())

total_hight = df[df['category_income'] == 'высокий']['category_income'].count()
debt_hight = df.loc[(df['category_income']=='высокий')&(df['debt']==1), 'debt'].count()
debt_to_hight = debt_hight / total_hight

total_middle = df[df['category_income'] == 'средний']['category_income'].count()
debt_middle = df.loc[(df['category_income']=='средний')&(df['debt']==1), 'debt'].count()
debt_to_middle = debt_middle / total_middle

total_lower_mid = df[df['category_income'] == 'ниже среднего']['category_income'].count()
debt_lower_mid = df.loc[(df['category_income']=='ниже среднего')&(df['debt']==1), 'debt'].count()
debt_to_lower_mid = debt_lower_mid / total_lower_mid

total_low = df[df['category_income'] == 'низкий']['category_income'].count()
debt_low = df.loc[(df['category_income']=='низкий')&(df['debt']==1), 'debt'].count()
debt_to_low = debt_low / total_low 

print('Доля должников среди обеспеченных составляет: {:.1%}'.format(debt_to_hight))
print('Доля должников среди среднего класса составляет: {:.1%}'.format(debt_to_middle))
print('Доля должников среди ниже среднего класса  составляет: {:.1%}'.format(debt_to_lower_mid))
print('Доля должников среди низкого класса составляет: {:.1%}'.format(debt_to_low))


# In[70]:


df.groupby('category_income')['debt'].mean()


# **Вывод**

# Те, кто зарабатывают меньше всего имеют более высокий процент просрочек. Самые расчётливые - люди ниже среднего класса

# - Как разные цели кредита влияют на его возврат в срок?

# In[20]:


print(df.groupby('purpose_aggr')['debt'].value_counts())

total_cars = df[df['purpose_aggr'] == 'автомобиль']['purpose_aggr'].count()
debt_cars = df.loc[(df['purpose_aggr']=='автомобиль')&(df['debt']==1), 'debt'].count()
debt_to_cars = debt_cars / total_cars

total_flats = df[df['purpose_aggr'] == 'недвижимость']['purpose_aggr'].count()
debt_flats = df.loc[(df['purpose_aggr']=='недвижимость')&(df['debt']==1), 'debt'].count()
debt_to_flats = debt_flats / total_flats

total_lower_ed = df[df['purpose_aggr'] == 'образование']['purpose_aggr'].count()
debt_lower_ed = df.loc[(df['purpose_aggr']=='образование')&(df['debt']==1), 'debt'].count()
debt_to_lower_ed = debt_lower_ed / total_lower_ed

total_wedding = df[df['purpose_aggr'] == 'свадьба']['purpose_aggr'].count()
debt_wedding = df.loc[(df['purpose_aggr']=='свадьба')&(df['debt']==1), 'debt'].count()
debt_to_wedding = debt_wedding / total_wedding 

print('Доля должников среди владельцев авто составляет: {:.1%}'.format(debt_to_cars))
print('Доля должников среди владельцев недвижимости составляет: {:.1%}'.format(debt_to_flats))
print('Доля должников среди обучающихся  составляет: {:.1%}'.format(debt_to_lower_ed))
print('Доля должников среди женатых составляет: {:.1%}'.format(debt_to_wedding))


# In[62]:


df.groupby('purpose_aggr')['debt'].mean()


# 
# <div class="alert alert-warning">
# <h1>Комментарий ревьюера <a class="tocSkip"></a></h1>
# Очень много кода, тут можно через groupby:
#     df.groupby('purpose_aggr')['debt'].mean() --- процент должников
#     
#  </div>

# **Вывод**

# Получается, что самые исправные плательщики - владельцы недвижимости. Можно предположить, что эти люди как минимум погашают задолженность вдвоём, а также у них есть стабильная работа в отличие от студентов, например. Следующая категория - молодожены. Вероятно, сумма платежа небольшая, плюс какая-то часть средств может быть подарена родственниками, поэтому нет больших просрочек. Второе место занимают студенты. Можем предположить, что у них ещё нет работы или низкооплачиваемая работа и денег едва хватает на бытовые расходы. На первом месте владельцы авто, можем предположить, что эта категория людей довольно много денег тратит на обслуживание автомобиля (особенно, если это б/у), страховку и прочие расходы.

# ## Шаг 4. Общий вывод

# На основании проанализированных данных можно выделить самые предпочтительные категории людей и цели кредита:
# 1. Молодоженам на свадьбу
# 2. Людям, которые ближе к среднему и обеспеченному классу
# 3. Вдовцы / вдовы
# 4. Недвижимость
# 
# На наличие / отсутствие детей можно не обращать внимание - разница между задолженностью небольшая. Самые небезопасные цели кредита - это автомобиль и обучение. Также высока доля должников среди низкооплачиваемых людей
# 

# 
# <div class="alert alert-success">
# <h1>Комментарий ревьюера v2 <a class="tocSkip"></a></h1>
# Спасибо за правки:)
#     
# С праздниками и удачи в следующих проектах!    
# </div>

# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# -Спасибо за качественно сделанный проект, было приятно проверять.
# 
# - Код написан хорошо, оставил варианты, как его можно еще улучшить 
# 
# - Соблюдена структура проекта
# 
# 
# Есть пара недочетов, которые надо поправить. Жду твоих исправлений (совсем чуть-чуть поправить надо):
#     
#     - заполнение пропусков
#     
#     - подсчет процента
# 
# 
# 
# </div>

# ## Чек-лист готовности проекта
# 
# Поставьте 'x' в выполненных пунктах. Далее нажмите Shift+Enter.

# - [x]  открыт файл;
# - [x]  файл изучен;
# - [x]  определены пропущенные значения;
# - [x]  заполнены пропущенные значения;
# - [x]  есть пояснение, какие пропущенные значения обнаружены;
# - [x]  описаны возможные причины появления пропусков в данных;
# - [x]  объяснено, по какому принципу заполнены пропуски;
# - [x]  заменен вещественный тип данных на целочисленный;
# - [x]  есть пояснение, какой метод используется для изменения типа данных и почему;
# - [x]  удалены дубликаты;
# - [x]  есть пояснение, какой метод используется для поиска и удаления дубликатов;
# - [x]  описаны возможные причины появления дубликатов в данных;
# - [x]  выделены леммы в значениях столбца с целями получения кредита;
# - [x]  описан процесс лемматизации;
# - [x]  данные категоризированы;
# - [x]  есть объяснение принципа категоризации данных;
# - [x]  есть ответ на вопрос: "Есть ли зависимость между наличием детей и возвратом кредита в срок?";
# - [x]  есть ответ на вопрос: "Есть ли зависимость между семейным положением и возвратом кредита в срок?";
# - [x]  есть ответ на вопрос: "Есть ли зависимость между уровнем дохода и возвратом кредита в срок?";
# - [x]  есть ответ на вопрос: "Как разные цели кредита влияют на его возврат в срок?";
# - [x]  в каждом этапе есть выводы;
# - [x]  есть общий вывод.
# 
