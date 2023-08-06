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
    
def value (a_data,a_column,a_value) :
    '''
    Show row by value of column
    '''
    return a_data.loc[a_data[a_column] == a_value]
    