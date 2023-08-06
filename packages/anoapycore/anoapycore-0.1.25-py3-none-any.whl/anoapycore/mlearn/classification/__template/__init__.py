import sklearn.metrics as __metrics
import matplotlib.pyplot as __plt
import scikitplot as __skplt
import pandas as __pd
import numpy as __np

import anoapycore as __ap


class __data :
    y_test_actual = None
    y_test_pred = None
    y_test_pred_proba_all = None
    fpr = None # false positive rate
    tpr = None # true positive rate
    ix_roc = None # index fpr & tpr
    best_threshold = None
    prc_precisions = None
    prc_recalls = None
    prc_fscores = None
    prc_thresholds = None

class __best_threshold :
    value : None
    precision = None
    recall = None

class __result :
    model = None
    evals = {}
    report = None
    best_threshold = None
    data = None

class __result_predict :
    probability = None
    prediction = None
    worksheet = None

def __run (a_model,a_x_train,a_x_test,a_y_train,a_y_test,b_threshold=0.5) :
    
    loc_model = a_model
    loc_model.fit(a_x_train,a_y_train)
       
    loc_prob_train = loc_model.predict_proba(a_x_train)[:,1]
    if b_threshold == 0.5 :
        loc_predic_train = loc_model.predict(a_x_train)
    else :
        loc_predic_train = (loc_prob_train >= b_threshold).astype(int)

    loc_prob_test = loc_model.predict_proba(a_x_test)[:,1]
    if b_threshold == 0.5 :
        loc_predic_test = loc_model.predict(a_x_test)
    else :
        loc_predic_test = (loc_prob_test >= b_threshold).astype(int)

    loc_report = __metrics.classification_report(a_y_test,loc_predic_test)
    
    loc_predict_proba_all = loc_model.predict_proba(a_x_test)
    loc_predict_proba = loc_model.predict_proba(a_x_test)[:,1]
    # calculate roc curves : false positive rate, true positive rate
    loc_fpr, loc_tpr, loc_thresholds = __metrics.roc_curve(a_y_test,loc_predict_proba)
    # calculate the g-mean for each threshold
    loc_gmeans = __np.sqrt(loc_tpr * (1-loc_fpr))
    # locate the index of the largest g-mean
    ix_roc = __np.argmax(loc_gmeans)
    loc_best_threshold = loc_thresholds[ix_roc]
    
    # calculate prc (precision-recall curve)
    loc_prc_precisions,loc_prc_recalls,loc_prc_thresholds = __metrics.precision_recall_curve(a_y_test,loc_predict_proba)
    loc_prc_fscores = (2 * loc_prc_precisions * loc_prc_recalls) / (loc_prc_precisions + loc_prc_recalls)
        
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals['train'] = __ap.__eval.evals(a_y_train.to_numpy(),loc_predic_train)
    loc_result.evals['test'] = __ap.__eval.evals(a_y_test.to_numpy(),loc_predic_test)
    loc_result.report = loc_report
    loc_result.best_threshold = loc_best_threshold
    
    loc_result.data = __data()
    loc_result.data.y_test_actual = a_y_test
    loc_result.data.y_test_pred = loc_predic_test
    loc_result.data.y_test_pred_proba_all = loc_predict_proba_all
    loc_result.data.fpr = loc_fpr # false positive rate
    loc_result.data.tpr = loc_tpr # true positive rate
    loc_result.data.ix_roc = ix_roc # index fpr & tpr
    loc_result.data.prc_precisions = loc_prc_precisions
    loc_result.data.prc_recalls = loc_prc_recalls
    loc_result.data.prc_fscores = loc_prc_fscores
    loc_result.data.prc_thresholds = loc_prc_thresholds

    return loc_result

def __predict (a_model,a_data,b_features='',b_threshold=0.5) :
    if b_features == '' :
        loc_features = a_data.columns
    else :
        loc_features = b_features
        
    loc_prob_y = a_model.model.predict_proba(a_data[loc_features])[:,1]
    if b_threshold == 0.5 :
        loc_pred_y = a_model.model.predict(a_data[loc_features])
    else :
        loc_pred_y = (loc_prob_y >= b_threshold).astype(int)
        
    loc_probability = __pd.DataFrame(loc_prob_y,columns=['__prob_y'])
    loc_prediction = __pd.DataFrame(loc_pred_y,columns=['__pred_y'])
    
    loc_merge = a_data
    loc_merge = __pd.merge(loc_merge,loc_probability,left_index=True,right_index=True)
    loc_merge = __pd.merge(loc_merge,loc_prediction,left_index=True,right_index=True)

    loc_result_predict = __result_predict()
    loc_result_predict.probability = loc_probability
    loc_result_predict.prediction = loc_prediction
    loc_result_predict.worksheet = loc_merge
    return loc_result_predict


