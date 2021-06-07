import pandas as pd
import numpy as np
import os

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def fuzzy_compare_value_to_list(value, compare_list, score_threshold = 60):
    """
    Take in an input value and score it's similarity relative to a list of other string values

    :param value: string value to be binned
    :param compare_list: list of possible labels the string value can be binned
    :param score_threshold: score to define similarity

    :return label with most similar score if above score threshold:
    """
    fuzzy_guess = process.extractOne(value, compare_list, scorer=fuzz.partial_ratio)

    genre = fuzzy_guess[0]    
    score = fuzzy_guess[1]

    if score < score_threshold:
        genre = 'unknown'
    
    return genre

def stack_dummy_cols(df, column, symbol = '|',count_threshold=100):
    """
    :param df: master_df with all features for modeling
    :param column: column to transform to dummies
    :param symbol: symbol separating values in column
    :param count_threshold: threshold of count of string values that will be dummied

    :return df with new columns of most frequent string features:
    """
    #create keyword columns
    merge_df = df[column].str.split(symbol,expand=True).stack().reset_index() # split columns by | into separate columns
    count_df = merge_df[0].value_counts().reset_index() # get count of keyword values
    keep_list = list(count_df[count_df[0]>count_threshold]['index']) # filter by keywords that show up more than 100 times
    merge_df = merge_df[merge_df[0].isin(keep_list)][['level_0',0]] # only keep top keywords
    merge_df = pd.get_dummies(merge_df[0]).reset_index() # create dummy variables from those keywords
    merge_df = merge_df.groupby(['index']).sum().reset_index(drop=True) # group by index to transform data to row equaling a single movie
    df = pd.concat([df,merge_df],axis=1) # merge in with master data
    df[keep_list] = df[keep_list].fillna(0) # fill NaN with 0 where there is no data after the merge
    return df


def get_season(month):
    """
    :param month: integer representing month of the year

    :return string representing season of the year:
    """
    if month in [3,4,5]:
        return 'spring'
    elif month in [6,7,8]:
        return 'summer'
    elif month in [9,10,11]:
        return 'fall'
    elif month in [12,1,2]:
        return 'winter'