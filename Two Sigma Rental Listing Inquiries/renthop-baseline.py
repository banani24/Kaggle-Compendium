import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy
import hashfeatures


def get_naive_bayes_models():
    gnb = GaussianNB()
    mnb = MultinomialNB()
    bnb = BernoulliNB()
    classifier_list = [gnb,mnb,bnb]
    classifier_name_list = ['Gaussian NB','Multinomial NB','Bernoulli NB']
    return classifier_list,classifier_name_list


def get_neural_network(hidden_layer_size=50):
    mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_size)
    return [mlp], ['MultiLayer Perceptron']


def get_ensemble_models():
    rf = RandomForestClassifier(n_estimators=51,min_samples_leaf=5,min_samples_split=3)
    bagg = BaggingClassifier(n_estimators=71,random_state=42)
    extra = ExtraTreesClassifier(n_estimators=57,random_state=42)
    ada = AdaBoostClassifier(n_estimators=51,random_state=42)
    grad = GradientBoostingClassifier(n_estimators=101,random_state=42)
    classifier_list = [rf,bagg,extra,ada,grad]
    classifier_name_list = ['Random Forests','Bagging','Extra Trees','AdaBoost','Gradient Boost']
    return classifier_list,classifier_name_list


def get_label_encoded_features(rent_frame,text_columns):
    description_list = list(rent_frame['description'].values)
    features_list = list(rent_frame['features'].values)
    features_list = map(lambda s: " ".join(s), features_list)
    address_list = list(rent_frame['display_address'].values)
    street_list = list(rent_frame['street_address'].values)
    feature_hash = hashfeatures.FeatureHash(max_feature_num=150)
    description_hash = feature_hash.get_feature_set(description_list)
    features_list_hash = feature_hash.get_feature_set(features_list)
    address_hash = feature_hash.get_feature_set(address_list)
    street_hash = feature_hash.get_feature_set(street_list)
    rent_frame.drop(text_columns,axis=1,inplace=True)
    numerical_features = rent_frame.values
    return numpy.hstack((numerical_features,description_hash,features_list_hash,address_hash,street_hash))


def print_evaluation_metrics(trained_model,trained_model_name,X_test,y_test):
    print '--------- For Model : ', trained_model_name, '--------------------'
    predicted_values = trained_model.predict(X_test)
    print metrics.classification_report(y_test,predicted_values)
    print "Accuracy Score : ",metrics.accuracy_score(y_test,predicted_values)
    print "---------------------------------------\n"


filename = 'train.json'
rent_frame = pd.read_json(filename)
print rent_frame.columns
print len(rent_frame)
print rent_frame.head(3)
target_variable = 'interest_level'
columns_to_delete = ['building_id','created','listing_id','manager_id','photos','interest_level']
class_labels = list(rent_frame[target_variable].values)
text_columns = ['description','features','display_address','street_address']
rent_frame.drop(columns_to_delete,axis=1,inplace=True)
full_features = get_label_encoded_features(rent_frame,text_columns)
X_train,X_test,y_train,y_test = train_test_split(full_features,class_labels,test_size=0.2,random_state=42)
classifier_list,classifier_name_list = get_ensemble_models()
for classifier,classifier_name in zip(classifier_list,classifier_name_list):
    classifier.fit(X_train,y_train)
    print_evaluation_metrics(classifier,classifier_name,X_test,y_test)
