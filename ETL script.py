#!/usr/bin/env python
# coding: utf-8

# In[16]:


# importing my tools for ETl
import pandas as pd
from sqlalchemy import create_engine
import logging
import time
import numpy as np



# logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger=logging.getLogger(__name__)



## Extraction function
def extract (file_path):
    time.sleep(1)
    logger.info(F"Extraction started")
    try:
        df=pd.read_csv(file_path)
        time.sleep(1)
        logger.info(f"{len(df):,} rows and {len(df.columns)} columns extracted")
    except Exception as e:
        logger.error(f"loading failed {e}")
        raise

    return df



### Inspection and Exploration
def inspect(df):
    logger.info(f"Inspection Started")
    nulls=df.isna().sum()
    dupes=df.duplicated().sum()
    for col in df.columns:
        if np.issubdtype(df[col].dtype, np.number):
            negative_outliers=(df[col]<0).sum()
            logger.info(f" {negative_outliers} negative outliers found")
            logger.info(f"{nulls} nulls found")
            logger.info(f"|{dupes} duplicated rows detected")
            logger.info(f"Inspection Complete")
        return df



## cleaning
def cleaning (df):

    logger.info(f"Cleaning Started")

    dupes = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    logger.info(f"{dupes} duplicated rows dropped")
    for col in df.columns:
        nulls=df[col].isna().sum()
        logger.info(f"{nulls} null rows detected")

        if np.issubdtype(df[col].dtype, np.number):
            q1=df[col].quantile(0.25)
            q3=df[col].quantile(0.75)
            iqr=q3-q1
            lower=q1-(1.5*iqr)
            upper=q3+(1.5*iqr)
            mean_val=df[col].mean()
            negative=(df[col]<0).sum()
            df['age']=df['age'].round(0)
            df['salary']=df['salary'].round(2)

            if nulls>0:
                df[col]=df[col].fillna(mean_val)

            df[col]=df[col].apply(lambda x: mean_val if x <lower or  x> upper else x)
            logger.info(f" Nulls filled  in {col}")



            if negative > 0:
                df.loc[df[col] < 0, col] = mean_val
                logger.info(f"{negative} negative rows replaced in {col}")




        elif df[col].dtype=='object':
            df[col]=df[col].fillna('Unknown')
            df[col]=df[col].str.strip().str.title()
            logger.info(f"String columns cleaned")

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col]=df[col].fillna(df[col].mode()[0])
            logger.info(f" Date Nulls Filled in {col}")

    logger.info(f"cleaning completely cleaned")
    return df



#EDA -exploration

def EDA(df):
    logger.info(f"EDA Started")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")

    for col in df.columns:
        logger.info(f"\n--- {col} ---")

        if np.issubdtype(df[col].dtype, np.number):
            stats = df[col].agg(['count', 'mean', 'max', 'min', 'std'])
            logger.info(f"Numeric stats:\n{stats}")

        elif df[col].dtype == 'object':
            logger.info(f"Unique values: {df[col].nunique()}")
            logger.info(f"Top values:\n{df[col].value_counts().head()}")

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            logger.info(f"Date range: {df[col].min()} to {df[col].max()}")

    logger.info(f"EDA Completed")
    return df




##loading 
def load(df):
    logger.info(f"Loading Started")
    try:
        engine=create_engine(
        "postgresql://postgres:4700@localhost:5432/ernest_de")

        df.to_sql(
            name= "Cleaned_HR",
            con=engine,
            if_exists='replace',
            index=False)
        logger.info(f'Data Extraction, Inspection , Cleaning & Loading Completed')
    except Exception as e:
        logger.error(f"Loading failed: {e}")    
        raise   

# entry point
if __name__ == "__main__":
    df = extract(r"C:\Users\USER\Downloads\messy_data_20k.csv")
    inspect(df)
    df = cleaning(df)
    EDA(df)
    load(df)




# In[17]:


df
df.head(1000)


# In[47]:


df.info()


# In[ ]:




