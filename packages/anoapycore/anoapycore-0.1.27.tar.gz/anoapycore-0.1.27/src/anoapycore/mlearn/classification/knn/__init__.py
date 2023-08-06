import anoapycore as __ap
from sklearn.neighbors import KNeighborsClassifier as __model

def run (a_x_train,a_x_test,a_y_train,a_y_test,b_threshold=0.5,b_n_neighbors=3) :
    loc_model = __model(n_neighbors=b_n_neighbors)
    return __ap.mlearn.classification.__template.__run(loc_model,a_x_train=a_x_train,a_x_test=a_x_test,a_y_train=a_y_train,a_y_test=a_y_test,b_threshold=b_threshold)

def predict (a_model,a_data,b_features='',b_threshold=0.5) :
    return __ap.mlearn.classification.__template.__predict(a_model=a_model,a_data=a_data,b_features=b_features,b_threshold=b_threshold)


