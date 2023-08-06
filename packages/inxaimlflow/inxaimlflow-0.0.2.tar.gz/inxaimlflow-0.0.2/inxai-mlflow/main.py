import warnings

warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
import itertools

from sklearn.model_selection import train_test_split

from consistency import Consistency
from stability import Stability
from accelerated_loss import AcceleratedLoss
from ensemble import Ensemble

data = pd.read_csv("data/application_record.csv", encoding='utf-8')
record = pd.read_csv("data/credit_record.csv", encoding='utf-8')

plt.rcParams['figure.facecolor'] = 'white'

begin_month = pd.DataFrame(record.groupby(["ID"])["MONTHS_BALANCE"].agg(min))
begin_month = begin_month.rename(columns={'MONTHS_BALANCE': 'begin_month'})
new_data = pd.merge(data, begin_month, how="left", on="ID")  # merge to record data

record['dep_value'] = None
record['dep_value'][record['STATUS'] == '2'] = 'Yes'
record['dep_value'][record['STATUS'] == '3'] = 'Yes'
record['dep_value'][record['STATUS'] == '4'] = 'Yes'
record['dep_value'][record['STATUS'] == '5'] = 'Yes'

cpunt = record.groupby('ID').count()
cpunt['dep_value'][cpunt['dep_value'] > 0] = 'Yes'
cpunt['dep_value'][cpunt['dep_value'] == 0] = 'No'
cpunt = cpunt[['dep_value']]
new_data = pd.merge(new_data, cpunt, how='inner', on='ID')
new_data['target'] = new_data['dep_value']
new_data.loc[new_data['target'] == 'Yes', 'target'] = 1
new_data.loc[new_data['target'] == 'No', 'target'] = 0

print(cpunt['dep_value'].value_counts())
cpunt['dep_value'].value_counts(normalize=True)

new_data.rename(columns={'CODE_GENDER': 'Gender', 'FLAG_OWN_CAR': 'Car', 'FLAG_OWN_REALTY': 'Reality',
                         'CNT_CHILDREN': 'ChldNo', 'AMT_INCOME_TOTAL': 'inc',
                         'NAME_EDUCATION_TYPE': 'edutp', 'NAME_FAMILY_STATUS': 'famtp',
                         'NAME_HOUSING_TYPE': 'houtp', 'FLAG_EMAIL': 'email',
                         'NAME_INCOME_TYPE': 'inctp', 'FLAG_WORK_PHONE': 'wkphone',
                         'FLAG_PHONE': 'phone', 'CNT_FAM_MEMBERS': 'famsize',
                         'OCCUPATION_TYPE': 'occyp'
                         }, inplace=True)

new_data.dropna()
new_data = new_data.mask(new_data == 'NULL').dropna()

# In[10]:


ivtable = pd.DataFrame(new_data.columns, columns=['variable'])
ivtable['IV'] = None
namelist = ['FLAG_MOBIL', 'begin_month', 'dep_value', 'target', 'ID']

for i in namelist:
    ivtable.drop(ivtable[ivtable['variable'] == i].index, inplace=True)


# + Define `calc_iv` function to [calculate](https://www.kaggle.com/puremath86/iv-woe-starter-for-python) Information Value and WOE Value

# ### Binary Features

# In[11]:


# Calculate information value
def calc_iv(df, feature, target, pr=False):
    lst = []
    df[feature] = df[feature].fillna("NULL")

    for i in range(df[feature].nunique()):
        val = list(df[feature].unique())[i]
        lst.append([feature,  # Variable
                    val,  # Value
                    df[df[feature] == val].count()[feature],  # All
                    df[(df[feature] == val) & (df[target] == 0)].count()[feature],  # Good (think: Fraud == 0)
                    df[(df[feature] == val) & (df[target] == 1)].count()[feature]])  # Bad (think: Fraud == 1)

    data = pd.DataFrame(lst, columns=['Variable', 'Value', 'All', 'Good', 'Bad'])
    data['Share'] = data['All'] / data['All'].sum()
    data['Bad Rate'] = data['Bad'] / data['All']
    data['Distribution Good'] = (data['All'] - data['Bad']) / (data['All'].sum() - data['Bad'].sum())
    data['Distribution Bad'] = data['Bad'] / data['Bad'].sum()
    data['WoE'] = np.log(data['Distribution Good'] / data['Distribution Bad'])

    data = data.replace({'WoE': {np.inf: 0, -np.inf: 0}})

    data['IV'] = data['WoE'] * (data['Distribution Good'] - data['Distribution Bad'])

    data = data.sort_values(by=['Variable', 'Value'], ascending=[True, True])
    data.index = range(len(data.index))

    if pr:
        print(data)
        print('IV = ', data['IV'].sum())

    iv = data['IV'].sum()
    print('This variable\'s IV is:', iv)
    print(df[feature].value_counts())
    return iv, data


# In[12]:


def convert_dummy(df, feature, rank=0):
    pos = pd.get_dummies(df[feature], prefix=feature)
    mode = df[feature].value_counts().index[rank]
    biggest = feature + '_' + str(mode)
    pos.drop([biggest], axis=1, inplace=True)
    df.drop([feature], axis=1, inplace=True)
    df = df.join(pos)
    return df


# In[13]:


def get_category(df, col, binsnum, labels, qcut=False):
    if qcut:
        localdf = pd.qcut(df[col], q=binsnum, labels=labels)  # quantile cut
    else:
        localdf = pd.cut(df[col], bins=binsnum, labels=labels)  # equal-length cut

    localdf = pd.DataFrame(localdf)
    name = 'gp' + '_' + col
    localdf[name] = localdf[col]
    df = df.join(localdf[name])
    df[name] = df[name].astype(object)
    return df


# In[14]:


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# #### Gender

# In[15]:


new_data['Gender'] = new_data['Gender'].replace(['F', 'M'], [0, 1])
print(new_data['Gender'].value_counts())
iv, data = calc_iv(new_data, 'Gender', 'target')
ivtable.loc[ivtable['variable'] == 'Gender', 'IV'] = iv
data.head()

# #### Having a car or not

# In[16]:


new_data['Car'] = new_data['Car'].replace(['N', 'Y'], [0, 1])
print(new_data['Car'].value_counts())
iv, data = calc_iv(new_data, 'Car', 'target')
ivtable.loc[ivtable['variable'] == 'Car', 'IV'] = iv
data.head()

# #### Having house reality or not

# In[17]:


new_data['Reality'] = new_data['Reality'].replace(['N', 'Y'], [0, 1])
print(new_data['Reality'].value_counts())
iv, data = calc_iv(new_data, 'Reality', 'target')
ivtable.loc[ivtable['variable'] == 'Reality', 'IV'] = iv
data.head()

# #### Having a phone or not

# In[18]:


new_data['phone'] = new_data['phone'].astype(str)
print(new_data['phone'].value_counts(normalize=True, sort=False))
new_data.drop(new_data[new_data['phone'] == 'nan'].index, inplace=True)
iv, data = calc_iv(new_data, 'phone', 'target')
ivtable.loc[ivtable['variable'] == 'phone', 'IV'] = iv
data.head()

# #### Having an email or not

# In[19]:


print(new_data['email'].value_counts(normalize=True, sort=False))
new_data['email'] = new_data['email'].astype(str)
iv, data = calc_iv(new_data, 'email', 'target')
ivtable.loc[ivtable['variable'] == 'email', 'IV'] = iv
data.head()

# #### Having a Work Phone or not

# In[20]:


new_data['wkphone'] = new_data['wkphone'].astype(str)
iv, data = calc_iv(new_data, 'wkphone', 'target')
new_data.drop(new_data[new_data['wkphone'] == 'nan'].index, inplace=True)
ivtable.loc[ivtable['variable'] == 'wkphone', 'IV'] = iv
data.head()

# ### Continuous Variables
#
# #### Children Numbers

# In[21]:


new_data.loc[new_data['ChldNo'] >= 2, 'ChldNo'] = '2More'
print(new_data['ChldNo'].value_counts(sort=False))

# In[22]:


iv, data = calc_iv(new_data, 'ChldNo', 'target')
ivtable.loc[ivtable['variable'] == 'ChldNo', 'IV'] = iv
data.head()

# In[23]:


new_data = convert_dummy(new_data, 'ChldNo')

# #### Annual Income
# bins the data based on sample quantiles

# In[24]:


new_data['inc'] = new_data['inc'].astype(object)
new_data['inc'] = new_data['inc'] / 10000
print(new_data['inc'].value_counts(bins=10, sort=False))
new_data['inc'].plot(kind='hist', bins=50, density=True)

# In[25]:


new_data = get_category(new_data, 'inc', 3, ["low", "medium", "high"], qcut=True)
iv, data = calc_iv(new_data, 'gp_inc', 'target')
ivtable.loc[ivtable['variable'] == 'inc', 'IV'] = iv
data.head()

# In[26]:


new_data = convert_dummy(new_data, 'gp_inc')

# #### Age
# Bucketing Continuous Variables

# In[27]:


new_data['Age'] = -(new_data['DAYS_BIRTH']) // 365
print(new_data['Age'].value_counts(bins=10, normalize=True, sort=False))
new_data['Age'].plot(kind='hist', bins=20, density=True)

# In[28]:


new_data = get_category(new_data, 'Age', 5, ["lowest", "low", "medium", "high", "highest"])
iv, data = calc_iv(new_data, 'gp_Age', 'target')
ivtable.loc[ivtable['variable'] == 'DAYS_BIRTH', 'IV'] = iv
data.head()

# In[29]:


new_data = convert_dummy(new_data, 'gp_Age')

# #### Working Years
# + Equal-length Bucketing

# In[30]:


new_data['worktm'] = -(new_data['DAYS_EMPLOYED']) // 365
new_data[new_data['worktm'] < 0] = np.nan  # replace by na
new_data['DAYS_EMPLOYED']
new_data['worktm'].fillna(new_data['worktm'].mean(), inplace=True)  # replace na by mean
new_data['worktm'].plot(kind='hist', bins=20, density=True)

# In[31]:


new_data = get_category(new_data, 'worktm', 5, ["lowest", "low", "medium", "high", "highest"])
iv, data = calc_iv(new_data, 'gp_worktm', 'target')
ivtable.loc[ivtable['variable'] == 'DAYS_EMPLOYED', 'IV'] = iv
data.head()

# In[32]:


new_data = convert_dummy(new_data, 'gp_worktm')

# #### Famliy Size

# In[33]:


new_data['famsize'].value_counts(sort=False)

# In[34]:


new_data['famsize'] = new_data['famsize'].astype(int)
new_data['famsizegp'] = new_data['famsize']
new_data['famsizegp'] = new_data['famsizegp'].astype(object)
new_data.loc[new_data['famsizegp'] >= 3, 'famsizegp'] = '3more'
iv, data = calc_iv(new_data, 'famsizegp', 'target')
ivtable.loc[ivtable['variable'] == 'famsize', 'IV'] = iv
data.head()

# In[35]:


new_data = convert_dummy(new_data, 'famsizegp')

# ### Categorical Features

# #### Income Type

# In[36]:


print(new_data['inctp'].value_counts(sort=False))
print(new_data['inctp'].value_counts(normalize=True, sort=False))
new_data.loc[new_data['inctp'] == 'Pensioner', 'inctp'] = 'State servant'
new_data.loc[new_data['inctp'] == 'Student', 'inctp'] = 'State servant'
iv, data = calc_iv(new_data, 'inctp', 'target')
ivtable.loc[ivtable['variable'] == 'inctp', 'IV'] = iv
data.head()

# In[37]:


new_data = convert_dummy(new_data, 'inctp')

# #### Occupation Type

# In[38]:


new_data.loc[(new_data['occyp'] == 'Cleaning staff') | (new_data['occyp'] == 'Cooking staff') | (
        new_data['occyp'] == 'Drivers') | (new_data['occyp'] == 'Laborers') | (
                     new_data['occyp'] == 'Low-skill Laborers') | (new_data['occyp'] == 'Security staff') | (
                     new_data['occyp'] == 'Waiters/barmen staff'), 'occyp'] = 'Laborwk'
new_data.loc[
    (new_data['occyp'] == 'Accountants') | (new_data['occyp'] == 'Core staff') | (new_data['occyp'] == 'HR staff') | (
            new_data['occyp'] == 'Medicine staff') | (new_data['occyp'] == 'Private service staff') | (
            new_data['occyp'] == 'Realty agents') | (new_data['occyp'] == 'Sales staff') | (
            new_data['occyp'] == 'Secretaries'), 'occyp'] = 'officewk'
new_data.loc[(new_data['occyp'] == 'Managers') | (new_data['occyp'] == 'High skill tech staff') | (
        new_data['occyp'] == 'IT staff'), 'occyp'] = 'hightecwk'
print(new_data['occyp'].value_counts())
iv, data = calc_iv(new_data, 'occyp', 'target')
ivtable.loc[ivtable['variable'] == 'occyp', 'IV'] = iv
data.head()

# In[39]:


new_data = convert_dummy(new_data, 'occyp')

# #### House Type

# In[40]:


iv, data = calc_iv(new_data, 'houtp', 'target')
ivtable.loc[ivtable['variable'] == 'houtp', 'IV'] = iv
data.head()

# In[41]:


new_data = convert_dummy(new_data, 'houtp')

# #### Education

# In[42]:


new_data.loc[new_data['edutp'] == 'Academic degree', 'edutp'] = 'Higher education'
iv, data = calc_iv(new_data, 'edutp', 'target')
ivtable.loc[ivtable['variable'] == 'edutp', 'IV'] = iv
data.head()

# In[43]:


new_data = convert_dummy(new_data, 'edutp')

# ####  Marriage Condition

# In[44]:


new_data['famtp'].value_counts(normalize=True, sort=False)

# In[45]:


iv, data = calc_iv(new_data, 'famtp', 'target')
ivtable.loc[ivtable['variable'] == 'famtp', 'IV'] = iv
data.head()

# In[46]:


new_data = convert_dummy(new_data, 'famtp')

# ## IV、WOE：Concept and Application

# Weight of Evidence(WoE):
#
# $$wo{e_i} = \ln {{{P_{yi}}} \over {{P_{ni}}}} = \ln {{{y_i}/{y_s}} \over {{n_i}/{n_s}}}$$
# $wo{e_i}$ is the I category's WOE value. ${{P_{yi}}}$ is the proportion of the positive samples in this category to all positive samples.   ${{P_{ni}}}$ is the ratio of negative samples (${{n_i}}$) in this class to all negative samples (${{n_s}}$).
#
# Information Value (IV):
# $$I{V_i} = ({P_{yi}} - {P_{ni}}) \times wo{e_i}$$
# The IV values of the various types are the difference between the conditional positive rate and the conditional negative rate multiplied by the WOE value of the variable. The total IV value of the variable can be understood as the weighted sum of the conditional positive rate and the conditional negative rate difference:
# $$IV = \sum\limits_i^n {I{V_i}} $$
#
# The IV value measures the variable's ability to predict.
#

# Relationship between IV value and predictive power
#
# | IV| Ability to predict |
# |:------|:------:|
# | <0.02 | Almost no predictive power |
# |0.02~0.1 |weak predictive power|
# |0.1~0.3|Moderate predictive power|
# |0.3~0.5|Strong predictive power|
# |>0.5|Predictive power is too strong, need to check variables|


ivtable = ivtable.sort_values(by='IV', ascending=False)
ivtable.loc[ivtable['variable'] == 'DAYS_BIRTH', 'variable'] = 'agegp'
ivtable.loc[ivtable['variable'] == 'DAYS_EMPLOYED', 'variable'] = 'worktmgp'
ivtable.loc[ivtable['variable'] == 'inc', 'variable'] = 'incgp'
ivtable

Y = new_data['target']
X = new_data[['Gender', 'Reality', 'ChldNo_1', 'ChldNo_2More', 'wkphone',
              'gp_Age_high', 'gp_Age_highest', 'gp_Age_low',
              'gp_Age_lowest', 'gp_worktm_high', 'gp_worktm_highest',
              'gp_worktm_low', 'gp_worktm_medium', 'occyp_hightecwk',
              'occyp_officewk', 'famsizegp_1', 'famsizegp_3more',
              'houtp_Co-op apartment', 'houtp_Municipal apartment',
              'houtp_Office apartment', 'houtp_Rented apartment',
              'houtp_With parents', 'edutp_Higher education',
              'edutp_Incomplete higher', 'edutp_Lower secondary', 'famtp_Civil marriage',
              'famtp_Separated', 'famtp_Single / not married', 'famtp_Widow']]

Y = Y.astype('int')
X_balance, Y_balance = SMOTE().fit_resample(X, Y)
X_balance = pd.DataFrame(X_balance, columns=X.columns)

X_train, X_test, y_train, y_test = train_test_split(X_balance, Y_balance,
                                                    stratify=Y_balance, test_size=0.3,
                                                    random_state=10086)

print(y_test.unique)

X_train.loc[:, ['wkphone']] = X_train['wkphone'].astype('float', copy=False)

X_test.loc[:, ['wkphone']] = X_test['wkphone'].astype('float', copy=False)

# # ML Flow

# #### Used MLFlow version 1.14.1
# Install using `conda install -c conda-forge mlflow`
#
# To connect ML pipeline with MLFlow, do the following:
# 1. Import mlflow library along with `log_metric`, `log_param` and `log_model` functions
# 2. Start the ml flow block with: `with mlflow.start_run():`
# 3. Inside the block, specify used parameters with mlflows `log_param` function, used metric with `log_metric` function and trained model with `log_model` function
# 4. From the same directory from which the notebook was opened, run `mlflow ui` to see and compare the results


from sklearn.metrics import recall_score, f1_score
import mlflow

import shap
import lime
from sklearn.linear_model import LogisticRegression
import xgboost as xgb

from sklearn.metrics import accuracy_score, confusion_matrix

y_test = y_test.values

print(X_test.columns)

X_train.columns


# Dodać parametr z jakich algorytmów korzystać: lime, shap czy ensemble robić
# Nazewnictwo
# Sprawdzić jak stworzyć z projektu paczkę
# Opisac w README jak odpalić już stworzoną paczkę i użyć w innym projekcie
# Dodać do metod log start runy z mlflow


def func(num_leaves=70, lr=0.07):
    with mlflow.start_run(run_name='nested', nested=True):
        mlflow.log_param("num_leaves", num_leaves)
        mlflow.log_param("lr", lr)


from urllib.parse import urlparse

with mlflow.start_run(run_name='inxai', nested=True):
    num_leaves = 70
    lr = 0.07
    n_estimators = 350
    max_depth = 12
    min_child_weight = 8
    subsample = 0.8
    colsample_bytree = 0.8
    model = LogisticRegression()

    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    f1 = f1_score(y_test, y_predict)
    print('Accuracy Score is {:.5}'.format(accuracy))
    print('Recall Score is {:.5}'.format(recall))

    print(pd.DataFrame(confusion_matrix(y_test, y_predict)))

    mlflow.log_param("num_leaves", num_leaves)
    mlflow.log_param("lr", lr)
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("min_child_weight", min_child_weight)
    mlflow.log_param("subsample", subsample)
    mlflow.log_param("colsample_bytree", colsample_bytree)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    func()

    # inxai metrics
    X_test, y_test = X_test[:20], y_test[:20]

    # 1. Stability
    stability = Stability(model)
    stability.calculate(X=X_test, y=y_test)
    stability.log()

    # 2. Consistency
    xgb_model = xgb.XGBClassifier()
    xgb_model.fit(X_train, y_train)
    xgb_y_pred = xgb_model.predict(X_test)

    consistency = Consistency(models=[model, xgb_model])
    consistency.calculate(X=X_test, y=y_test)
    consistency.log()

    #   3. Area under the ACC LOSS
    shap_explainer = shap.KernelExplainer(model.predict_proba, X_train[:100])
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(X_train[:100], feature_names=list(X_train.columns),
                                                            class_names=['0', '1'], discretize_continuous=False)

    acc_loss = AcceleratedLoss(model, shap_explainer=shap_explainer, lime_explainer=lime_explainer)
    acc_loss.calculate(X=X_test, y=y_test)
    acc_loss.log()

    #     4. Combined explanation
    # 4.1 Stability
    ensemble = Ensemble(stability, consistency, acc_loss)
    ensemble.calculate_stability(X=X_test)
    ensemble.log_stability()

    # 4.2 Consistency
    ensemble.calculate_consistency()
    ensemble.log_consistency()

    # 4.3 ACCLOSS
    ensemble.calculate_acc_loss(X=X_test, y=y_test)
    ensemble.log_acc_loss()

    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

    # Model registry does not work with file store
    if tracking_url_type_store != "file":
        mlflow.sklearn.log_model(model, "model", registered_model_name="LightGBM")
    else:
        mlflow.sklearn.log_model(model, "model")
