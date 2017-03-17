# Autor: Felipe Martins dos Santos
# Kaggle: Titanic - Machine Learning from Disaster
# IAsc Blog: http://iascblog.wordpress.com
# coding: utf-8
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
import re

train_file = 'train.csv'
test_file = 'test.csv'

# Lê arquivos csv.
def read_train_test_data(train_file, test_file):
	train = pd.read_csv(train_file)
	test = pd.read_csv(test_file)
	return (train, test)

# Limpa os DataFrames tratando os dados.

def titanic_dataframe_cleaner (df):
	df.drop('Ticket', axis = 1, inplace = True)
	for i in range(0, len(df.Name)):
		if re.match('.*Mr\..*|.*Don\..*|.*Major\..*|.*Capt\..*|.*Jokheer\..*|.*Rev\..*|.*Col\..*|.*Capt\..*', df.Name[i]) != None:
			df.Name[i] = 'Mr'
		elif re.match('.*Countess\..*|.*Mme\..*|.*Mrs\..*|.*Dona\..*', df.Name[i]) != None:
			df.Name[i] = 'Mrs'
		elif re.match('.*Mlle\..*|.*Ms\..*|.*Miss\..*', df.Name[i]) != None:
			df.Name[i] = 'Miss'
		else:
			if df.Sex[i] == 'Male':
				df.Name[i] = 'Mr'
			else:
				df.Name[i] = 'Mrs'
			
	df.Cabin.fillna(0, inplace = True)
	for i in range(0, len(df.Cabin)):
		if (df.Cabin[i] != 0):
			cabins = df.Cabin[i].split(' ')
			number_of_cabins = len(cabins)
			df.Cabin[i] = number_of_cabins
	
	df['Family Size'] = df.SibSp + df.Parch
	ages_median = df.Age.median()
	df.Age.fillna(ages_median, inplace = True)
	fare_median = df.Fare.median()
	df.Fare.fillna(fare_median, inplace = True)
	df['Fare Per Person'] = df['Fare'] / (df['Family Size'] + 1)
	df['Age*Class'] = df['Age'] * df['Pclass']
	df = pd.get_dummies(df)
	return df
	
# Divide o conjunto de dados de treino em treino e validação.
def split_train_to_validate(train, fraction_to_train):
	total = len(train)
	new_train_size = int (total * fraction_to_train)
	y_train = train.Survived
	y_validation = train.Survived 
	train.drop('Survived', axis = 1, inplace = True)
	X_train = train.loc[0:new_train_size]
	y_train = y_train.loc[0:new_train_size]
	X_validation = train.loc[new_train_size + 1:]
	y_validation = y_validation.loc[new_train_size + 1:]
	return (X_train, y_train, X_validation, y_validation)

# Obtem a taxa de sucesso na validação.
def get_accuracy_on_validation (X_train, y_train, X_validation, y_validation):
	# clf = svm.SVC(gamma = 0.001) # accuracy = 65%
	# clf = svm.SVC(gamma = 0.001, kernel = 'poly') # accuracy = 75%
	# clf = GaussianNB() # accuracy = 80%
	clf = AdaBoostClassifier() # accuracy = 83%/85%
	clf.fit(X_train, y_train)
	predicted = clf.predict(X_validation)
	correct_ans = predicted == y_validation
	accuracy = sum(correct_ans) / float(len(y_validation))
	return accuracy

# Obtem valores previstos para o teste final.
def get_predictions_for_test(X_train, y_train, X_test):
	# clf = svm.SVC(gamma = 0.001) # accuracy = 65%
	# clf = svm.SVC(gamma = 0.001, kernel = 'poly') # accuracy = 75%
	# clf = GaussianNB() # accuracy = 80%
	clf = AdaBoostClassifier() # accuracy = 83%/85%
	clf.fit(X_train, y_train)
	predictions = clf.predict(X_test)
	return predictions

# Salva respostas previstas para o teste final em um arquivo.
def save_answers(PassengerId, predictions):
	d = {'PassengerId': PassengerId, 'Survived': predictions}
	answer_df = pd.DataFrame(d)
	answer_df.to_csv('answer.csv', index_names = False, index = False)

(train, test) = read_train_test_data(train_file, test_file)
train = titanic_dataframe_cleaner(train)
test = titanic_dataframe_cleaner(test)
#(X_train, y_train, X_validation, y_validation) = split_train_to_validate(train, 0.66) #0.83
(X_train, y_train, X_validation, y_validation) = split_train_to_validate(train, 0.9) #0.85
accuracy = get_accuracy_on_validation (X_train, y_train, X_validation, y_validation)
predictions = get_predictions_for_test(X_train, y_train, test)
save_answers(test.PassengerId, predictions)
