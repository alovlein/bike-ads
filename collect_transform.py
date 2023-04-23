import pandas as pd
import re


def read_bike_data() -> pd.DataFrame:
    """
    Reads bike data from 2 separate json files and unions them roughly
    :return: All bike data for a subset of columns
    """
    # read data from local json file and remove price so it doesn't accidentally get added to features.
    ebay = pd.read_json('bike-ad-data/data_ebay.json', lines=True).drop('Price', axis=1)
    ebay_used = ebay.loc[ebay['Condition'].isin(['Used', 'Seller refurbished', 'Manufacturer refurbished'])].set_index('ID')
    be = pd.read_json('bike-ad-data/data_bike_exchange.json', lines=True).drop(['Price now', 'Price was'], axis=1)
    be_used = be.loc[be['Item condition'] == 'Used'].set_index('ID')

    # create a map that unifies column names where possible.
    be_to_ebay_column_map = {
        'Title': 'Title Edited', 'Brand': 'Brand', 'Type': 'Type', 'Color': 'Color',
        'Size': None, 'Gender': 'Gender', 'Riding Style': None,
        'Material': 'Material Edited', 'Wheel Size': 'Wheel Size', 'Rear Derailleur': None,
        'Size CM': 'Frame Size', 'Braking Type': 'Brake Type'
    }

    ''' 
    for the columns without a clear mapping, we should search through the ebay listing for relevant language based on 
    the entries from bike exchange data. In the interest of time, we will skip those.
    '''

    # combine some columns in the eBay data because it is less formal than bike exchange
    ebay_used['Title Edited'] = ebay_used['Title'] + ebay_used['Seller notes']
    ebay_used['Material Edited'] = ebay_used['Material'] + ebay_used['Frame Material']

    # trim data columns and combine into a single dataset
    keep_cols = [x for x in be_to_ebay_column_map.values() if x]
    be_used = be_used.rename(columns=be_to_ebay_column_map)[keep_cols]
    return pd.concat([be_used, ebay_used[keep_cols]])


def regex_get_first_num_in_str(free_text: str) -> int:
    """
    Reduce a string to the first number present. If there is not a number in the string, it returns -1
    :param free_text: String to reduce
    :return: The first number in the string
    """
    try:
        out = int(re.findall(r'^\D*(\d+)', free_text)[0])
    except IndexError:
        out = -1

    return out


def reduce_col_to_first_number(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Extracts first number in the column and removes all other text.
    :param df: Table containing column to be reduced
    :param column: Text title of column in dataframe that should be reduced
    :return: The input dataframe with the single specified column reduced
    """
    # get the first number of the free text description of size. With more time we would have something more elegant
    df[column] = df[column].fillna(' ').apply(regex_get_first_num_in_str).astype(int)
    return df

