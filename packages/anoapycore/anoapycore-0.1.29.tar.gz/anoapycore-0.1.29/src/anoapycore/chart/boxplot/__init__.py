import matplotlib.pyplot as __plt
import seaborn as __sns

class __data :
    q1 = None
    q2 = None
    q3 = None
    iqr = None
    lower_fence = None
    upper_fence = None
    report = None

def show (a_data,a_column) :
    loc_plot = __sns.boxplot(x=a_data[a_column])
    loc_data = __data()
    loc_data.q1 = a_data[a_column].quantile(0.25)
    loc_data.q2 = a_data[a_column].quantile(0.50)
    loc_data.q3 = a_data[a_column].quantile(0.75)
    loc_data.iqr = loc_data.q3 - loc_data.q1
    loc_data.lower_fence = loc_data.q1 - (1.5 * loc_data.iqr)
    loc_data.upper_fence = loc_data.q3 + (1.5 * loc_data.iqr)
    loc_data.report = "" + \
        "Q1 : " + str(loc_data.q1) + "\n" + \
        "Q2 : " + str(loc_data.q2) + "\n" + \
        "Q3 : " + str(loc_data.q3) + "\n" + \
        "IQR : " + str(loc_data.iqr) + "\n" + \
        "Lower Fence : " + str(loc_data.lower_fence) + "\n" + \
        "Upper Fence : " + str(loc_data.upper_fence)
    return loc_plot,loc_data

def shows (a_data,a_column_x,a_column_y,b_group_by='',b_orientation='') :
    """
    b_orientation = '', 'v' or 'h'
    """
    if b_orientation == 'v' :
        if b_group_by == '' :
            loc_plot = __sns.boxplot(data=a_data,y=a_column_x,x=a_column_y,orient=b_orientation)
        else :
            loc_plot = __sns.boxplot(data=a_data,y=a_column_x,x=a_column_y,hue=b_group_by,orient=b_orientation)            
    else :
        if b_group_by == '' :
            loc_plot = __sns.boxplot(data=a_data,x=a_column_x,y=a_column_y,orient=b_orientation)
        else :
            loc_plot = __sns.boxplot(data=a_data,x=a_column_x,y=a_column_y,hue=b_group_by,orient=b_orientation)
    return loc_plot
    
    # function to draw points on the plot
    # loc_plot = __sns.swarmplot(data=a_data,y=a_column_x,x=a_column_y,orient=b_orientation,color=".25")

'''    
Q1 = df["COLUMN_NAME"].quantile(0.25)
Q3 = df["COLUMN_NAME"].quantile(0.75)
IQR = Q3 - Q1
Lower_Fence = Q1 - (1.5 * IQR)
Upper_Fence = Q3 + (1.5 * IQR)
'''