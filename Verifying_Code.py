import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn import tree

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import *

def SupportVectorMachine(descr):
    dataframe = pd.read_csv('fake_job_postings.csv')
    x = dataframe['description'].values.astype('U')
    y = dataframe['fraudulent'] 
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=0)
    vect = TfidfVectorizer(stop_words='english',max_df=0.7)
    tfid_x_train  = vect.fit_transform(x_train)
    tfid_x_test = vect.transform(x_test)
    classifier = PassiveAggressiveClassifier(max_iter=50)
    classifier.fit(tfid_x_train,y_train)
    #verifying
    input_data = [descr]
    vectorized_input_data = vect.transform(input_data)
    prediction = classifier.predict(vectorized_input_data)
    return prediction

def Other2Classifiers(title,location,description):
    dataset = pd.read_csv("fake_job_postings.csv")

    #Removing unnecessary columns
    dataset['text']=dataset['description']+' '+dataset['requirements']+' '+dataset['benefits']
    columns=['job_id','description','benefits','department','company_profile','requirements','telecommuting', 'has_company_logo', 'has_questions','required_experience','required_education','industry','function' ,'salary_range', 'employment_type']
    for col in columns:
        del dataset[col]
    #Fill NaN values with blank space
    dataset.fillna(' ', inplace=True)

    dataset.loc[-1] = [title, location,' ', description] #Adding a row to our dataset
    dataset.index = dataset.index + 1  # shifting index
    dataset = dataset.sort_index()

    #Converting our data to numbers 
    le_title = LabelEncoder()
    le_location = LabelEncoder()
    le_description = LabelEncoder()

    data = dataset['fraudulent']
    ddf = pd.DataFrame(data,columns=['fraudulent'])

    ddf['title_n'] = le_title.fit_transform(dataset['title'])
    ddf['location_n'] = le_location.fit_transform(dataset['location'])
    ddf['description_n'] = le_description.fit_transform(dataset['text'])
    
    Info_to_verify = ddf.iloc[0,].values
    Info_to_verify = np.delete(Info_to_verify,0)
    ddf = ddf.drop(0)
    
    x = ddf.iloc[:,1:4].values
    y = ddf['fraudulent'].astype(int)
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=0)

    #K-Nearest Neighbor
    ourScaler = StandardScaler()
    x_train = ourScaler.fit_transform(x_train)
    x_test = ourScaler.transform(x_test)
    classifier = KNeighborsClassifier(n_neighbors = 59, p=2,metric='euclidean')
    classifier.fit(x_train,y_train)
    KNN_prediction = classifier.predict(Info_to_verify.reshape(1,-1))

    #Decision Tree
    model = tree.DecisionTreeClassifier()
    model.fit(x_train,y_train)
    DecTree_prediction = model.predict(Info_to_verify.reshape(1,-1))

    if KNN_prediction == 0 & DecTree_prediction == 0:
        return 0
    elif KNN_prediction == 1 & DecTree_prediction == 1: 
        return 1
    else:
        return 1

def Verify(title,location,description):
    if SupportVectorMachine(description) == 1 & Other2Classifiers(title,location,description) == 1:
       return 1
    elif SupportVectorMachine(description) == 0 & Other2Classifiers(title,location,description) == 0:
        return 0
    else:
        return 1 

