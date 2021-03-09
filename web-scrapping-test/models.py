from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


page = requests.get('https://en.wikipedia.org/wiki/Gross_domestic_product.html')

soup = BeautifulSoup(page.content, 'html.parser')

print(soup)

def define_title(soup):
    wikitable_class = soup.find_all("table", {"class": "wikitable"})[0]
    tbody_class = list(wikitable_class.children)[1]
    td_class_titles = list(tbody_class.children)[0]
    return td_class_titles
    
td_class_titles = define_title(soup)


def removed_tag_titles(soup=soup, tag= '', regex = ''):
    import re
    text_corpus = soup.find_all(tag) 
    title_list = []
    
    if type(regex) == str:
        regex_in = regex
    elif type(regex) == list:
        regex_in = '|'.join(regex)
    else:
        raise ValueError('Use only a regex string or list of regex strings')

    for node in text_corpus:
        text = node.get_text()
        text= re.sub(regex_in, '', text)
        title_list.append(text)
    return title_list

filtered_titles = removed_tag_titles(td_class_titles, 'td' , ["\[[^\]]*\]", '\n'])


def make_titles(arr):
    final_titles = {}
    j = 0
    for i, val in enumerate(arr, 1):
        if val != '\n':
            j += 1
            final_titles[f'Table_{j}'] = val
    return final_titles

final_titles = make_titles(filtered_titles)




def locate_tables(soup=soup):
    tbody_class_tables_dict = {}
    wikitable_sortable_class = soup.find_all("table", {"class": "wikitable sortable"})
    for i, wiki_table in enumerate(wikitable_sortable_class):
        tbody_class_tables_dict[f'Table_{i + 1}'] = wikitable_sortable_class[i]
            
    return tbody_class_tables_dict

tbody_class_tables_dict = locate_tables(soup)

def removed_tag_tables(soup=soup, tag= '', regex = ''):
    import re
    text_corpus = soup.find_all(tag) 
    final_text = []
    
    if type(regex) == str:
        regex_in = regex
    elif type(regex) == list:
        regex_in = '|'.join(regex)
    else:
        raise ValueError('Use only a regex string or list of regex strings')

    for node in text_corpus:
        text = node.get_text()
        text= re.sub(regex_in, '', text)
        final_text.append(text)
    return final_text

def filter_tables(tables_dict):        
    filtered_table_dict = {}
    for key, val in tables_dict.items():

        tbody_class_table_clean = removed_tag_tables(val, 'tr' , ["\[[^\]]*\]", '\xa0', ',', '\n$', '^\n'])
        filtered_table_dict[key] = tbody_class_table_clean
        
    return filtered_table_dict

filter_tables_dict = filter_tables(tbody_class_tables_dict)


def fill_nulls(tables_dict):
    import numpy as np
    filled_filter_tables_dict = {}
    for key, table in tables_dict.items():
        filled_nulls_table = []
        for i, row in enumerate(table):
            if '\n' in row[0:1]:
                row_filled = 'NaN' + row           
                filled_nulls_table.append(row_filled)
            else:
                row_filled = row
                filled_nulls_table.append(row_filled)
        filled_filter_tables_dict[key] = filled_nulls_table
    return filled_filter_tables_dict
    
filtered_tables_rows = fill_nulls(filter_tables_dict)

def make_tables(tables_dict):
    import re   
    final_tables_dict = {}
    for key, table in tables_dict.items():
        filtered_tables_rows_dict = {}
        for i, val in enumerate(table, 1):
            row = re.split(r"\n", val)
            filtered_tables_rows_dict[f'Row_{i}'] = row
        final_tables_dict[key] = filtered_tables_rows_dict
    return final_tables_dict
    
final_rows = make_tables(filtered_tables_rows)

def make_dataframe(tables_dict):
    final_tables = {}
    for key, table in tables_dict.items():
        final_tables[key] = pd.DataFrame.from_dict(table).transpose()
        final_tables[key] = final_tables.get(key).reset_index(drop = True)
        final_tables[key].columns = final_tables[key].iloc[0]
        final_tables[key] = final_tables[key][1:]
    return final_tables

final_tables = make_dataframe(final_rows)

def name_tables(titles, tables):

    final_df = {titles[key] : value for key, value in tables.items()} 
    return final_df

final_df = name_tables(final_titles, final_tables)

def finaldf_to_csv(final_df):
    for i in final_df: 
        final_df[i].to_csv('GDP(Nominal)'+str(i)+'.csv')
        
finaldf_to_csv(final_df)