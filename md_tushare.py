
# coding: utf-8

# # 获取指定时间段指定个股代码的收盘价
# ## 使用依赖 [tushare](http://tushare.org/)
#  - 安装python
#  - 安装pandas
#  - lxml也是必须的，正常情况下安装了Anaconda后无须单独安装，如果没有可执行：pip install lxml
# 
# 建议安装 [Anaconda](http://www.continuum.io/downloads)
# 一次安装包括了Python环境和全部依赖包，减少问题出现的几率。
# 
# ## [安装 tushare ](http://tushare.org/index.html#id5)

# In[1]:

import os
import re
import numpy as np
import pandas as pd
import tushare as ts
print(ts.__version__)


# In[2]:

col_code = u'证券代码'


# In[3]:

# 文件夹路径
dirpath = os.getcwd()
print("current directory is : " + dirpath)
path_sep = os.path.sep


# **下面的cell获取全量个股列表**

# In[8]:

base = ts.get_stock_basics()
code_list = base.index.unique().sort_values()
code_list.name = col_code


# **下面的cell：**
#  - 标记是否从当前目录下的 security.csv 文件中读取产品代码
#  - 若*load_security_from_file* 为False， 取上面的全量个股列表code_list 
#  - 若*load_security_from_file* 为True，取文件中读取结果 

# In[9]:

load_security_from_file = True

if load_security_from_file:
    security_file = dirpath + path_sep + 'security.csv'
    securities_csv =  pd.read_csv(security_file, header=None, dtype=str, names=[col_code])
    securities_from_file = securities_csv[col_code]
    code_list = securities_from_file


# **下面的cell：**
# - 设置日期范围 [date_start, date_end)<br>
# - *date_start* 开始日期 <br>
# - *date_end* 结束日期（不含当日）<br>
# - 格式为 *YYYY-MM-DD* 

# In[11]:

date_start = '2018-01-01'
date_end = '2018-05-30'
cal = ts.trade_cal()
date_list = cal[cal.isOpen==1]['calendarDate']
date_list_range = date_list[(date_list > date_start) & (date_list < date_end)].tolist()


# In[12]:

fmt_date_list_range = [re.sub('-','',x) for x in date_list_range]


# ** 形成 代码为行索引，日期为列索引的 矩阵（dataframe，一种pandas的数据结构），初始化为NaN **

# In[14]:

index_len = len(code_list)
column_len = len(date_list_range)
init_matrix = np.empty((index_len,column_len))
init_matrix[:] = np.nan
frame_securities = pd.DataFrame(init_matrix, columns=fmt_date_list_range, index=code_list)


# **下面的cell：**
#  - loop 产品列表，对每个产品，通过tushare的 get_k_data得到历史数据，取其中的 *date*和*close*部分，并依次为刚才建立的frame_securities赋值
#  - 每 *output_freq* 个产品处理后输出一次
#  - 对于给定的日期范围内，全部处于停牌或未上市状态的产品，d_data_security不含数据，此时输出相关提示
# 

# In[15]:

cnt = 0
output_freq = 100
total = len(code_list)

for security in code_list:
    try:
        d_data_security = ts.get_k_data(code=security, start=date_start, end=date_end)
        if ('date' in d_data_security.columns) and ('close' in d_data_security.columns) :
            frame = d_data_security[['date','close']]
            
            for index, row in frame.iterrows():
                fmt_date = re.sub('-','',row['date'])
                frame_securities.at[security, fmt_date] = row['close']
        else:
            # 停牌或未上市 不返回数据
            print(cnt, 'no data for ', security, ' in [', date_start, ' , ', date_end, ']')
            continue
            
        cnt += 1
        if cnt % output_freq == 0 :
            print(cnt, ' in total count', total)
    except Exception as e:
        print('error for ', cnt, ',', security, str(e))
        continue
        
print('done')
print(frame_securities.head())



# ** 保存至当前路径下的excel： output.xlsx** 

# In[66]:

frame_securities.to_excel('output.xlsx')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



