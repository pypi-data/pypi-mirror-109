import scikitplot as __skplt

def show (a_model) :

    loc_y_test = a_model.data.y_test_actual
    loc_y_pred_proba_all = a_model.data.y_test_pred_proba_all # all means 2 values included : positive, negative
    
    __skplt.metrics.plot_lift_curve(loc_y_test,loc_y_pred_proba_all).figure

