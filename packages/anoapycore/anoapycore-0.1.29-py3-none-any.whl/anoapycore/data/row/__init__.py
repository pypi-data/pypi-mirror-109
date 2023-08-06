import numpy as __np

import anoapycore as __ap

def count (a_data) :
    return len(a_data)    
    
# check if there are duplicated rows
def duplicate (a_data) :
    return a_data.duplicated(keep=False).sum()    
    
def index (a_data,a_index) :
    '''
    Show row by index
    '''
    loc_data_as_series = a_data.iloc[a_index]
    return __ap.data.series_to_array(loc_data_as_series)
    
def value (a_data,a_column,a_value,b_method='exact') :
    '''
    Show row by value of column
    '''
    if b_method == 'exact' :
        loc_return = a_data.loc[a_data[a_column] == a_value]
    elif b_method == 'nearest' :
        loc_array = __ap.data.df_to_array(a_data[a_column])
        loc_difference_array = __np.absolute(loc_array - a_value)
        loc_index = loc_difference_array.argmin()
        loc_row = __ap.data.row.index(a_data=a_data,a_index=loc_index)
        loc_value = loc_row.at[loc_index,a_column]
        loc_return = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=loc_value,b_method='exact')
    return loc_return
    