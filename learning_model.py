import numpy as np
import pandas as pd
import os
import json
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import ARDRegression
from sklearn.linear_model import HuberRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.svm import LinearSVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.cluster import KMeans
from sklearn.datasets import make_regression
from sklearn.feature_selection import RFECV
import statsmodels.api as sm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import average_precision_score

def round_up(x, a):
	return np.ceil(x/a)*a

def round_down(x, a):
	return np.floor(x/a)*a

def segment(x,y,train_pct):
	new_data = np.concatenate((x,y),axis=1)
	num = new_data.shape[0]
	train_size = int(num*train_pct)
	np.random.shuffle(new_data)
	train = new_data[:train_size]
	test = new_data[train_size:]
	x_train = train[:,:x.shape[1]]
	x_test = test[:,:x.shape[1]]
	y_train = train[:,x.shape[1]:]
	y_test = test[:,x.shape[1]:]
	return x_train,x_test,y_train,y_test

def read_file(team_name):
	file_name = team_name.replace(' ','_').replace('.','') + ".csv"

	try:
		os.chdir('/Users/kalebryler/Desktop/MLB_Project/2019_Game_Logs')
	except:
		os.mkdir('/Users/kalebryler/Desktop/MLB_Project/2019_Game_Logs')
		os.chdir('/Users/kalebryler/Desktop/MLB_Project/2019_Game_Logs')

	data = pd.read_csv(file_name)
	data.set_index('Date',inplace=True)
	data = data.fillna(0)

	return data

def output_vars():
	outs = []

	for stat in ['Win','Hit','Pitch','Over','F5_Over','Cover']:
		outs.append('Overall_30_'+str(stat))
		outs.append('Overall_15_'+str(stat))
		outs.append('Home_Away_'+str(stat))
		outs.append('Right_Left_'+str(stat))
		outs.append('Series_By_Game_'+str(stat))
		outs.append('Betting_Profile_'+str(stat))
		outs.append('Opp_Team_Profile_'+str(stat))
		outs.append('Matchup_Profile_'+str(stat))

		outs.append('Opp_Team_Overall_30_'+str(stat))
		outs.append('Opp_Team_Overall_15_'+str(stat))
		outs.append('Opp_Team_Home_Away_'+str(stat))
		outs.append('Opp_Team_Right_Left_'+str(stat))
		outs.append('Opp_Team_Series_By_Game_'+str(stat))
		outs.append('Opp_Team_Betting_Profile_'+str(stat))
		outs.append('Opp_Team_Opp_Team_Profile_'+str(stat))
		outs.append('Opp_Team_Matchup_Profile_'+str(stat))

		for num in range(1,6):
			outs.append('Overall_'+str(stat)+'_'+str(num))
			outs.append('Home_Away_'+str(stat)+'_'+str(num))
			outs.append('Right_Left_'+str(stat)+'_'+str(num))
			outs.append('Pitcher_'+str(stat)+'_'+str(num))
			outs.append('Pitcher_Home_Away_'+str(stat)+'_'+str(num))
			outs.append('Series_By_Game_'+str(stat)+'_'+str(num))
			outs.append('Betting_Profile_'+str(stat)+'_'+str(num))
			outs.append('Opp_Team_Profile_'+str(stat)+'_'+str(num))
			outs.append('Matchup_Profile_'+str(stat)+'_'+str(num))
			outs.append('vs_Team_'+str(stat)+'_'+str(num))
			outs.append('Pitcher_Betting_Profile_'+str(stat)+'_'+str(num))
			outs.append('Pitcher_Opp_Team_Profile_'+str(stat)+'_'+str(num))
			outs.append('Pitcher_Matchup_Profile_'+str(stat)+'_'+str(num))
			outs.append('Pitcher_vs_Team_'+str(stat)+'_'+str(num))

			outs.append('Opp_Team_Overall_'+str(stat)+'_'+str(num))
			outs.append('Opp_Team_Home_Away_'+str(stat)+'_'+str(num))
			outs.append('Opp_Team_Right_Left_'+str(stat)+'_'+str(num))
			outs.append('Opp_Pitcher_'+str(stat)+'_'+str(num))
			outs.append('Opp_Pitcher_Home_Away_'+str(stat)+'_'+str(num))
			outs.append('Opp_Team_Series_By_Game_'+str(stat)+'_'+str(num))
			outs.append('Opp_Team_Betting_Profile_'+str(stat)+'_'+str(num))
			outs.append('Opp_Team_Opp_Team_Profile_'+str(stat)+'_'+str(num))
			outs.append('Opp_Team_Matchup_Profile_'+str(stat)+'_'+str(num))
			outs.append('Opp_Pitcher_Betting_Profile_'+str(stat)+'_'+str(num))
			outs.append('Opp_Pitcher_Opp_Team_Profile_'+str(stat)+'_'+str(num))
			outs.append('Opp_Pitcher_Matchup_Profile_'+str(stat)+'_'+str(num))
			outs.append('Opp_Pitcher_vs_Team_'+str(stat)+'_'+str(num))

	return outs

def get_inputs_outputs(df):
	var_list = output_vars()

	d = {}

	for outcome in ['Win','Over','F5_Over','Cover']:
		d[outcome] = {}

		inputs = df[var_list]
		outputs = df[['True_'+outcome]]
		# outputs = df[[outcome]]
		try:
			ml = df[[outcome + "_ML"]]
		except:
			ml = df[["ML"]]

		d[outcome]['Inputs'] = inputs.to_numpy()
		d[outcome]['Outputs'] = outputs.to_numpy()
		d[outcome]['Payout'] = ml.to_numpy()

	return d

def print_model(team_name,model_name,outcome):
	team_df = read_file(team_name)
	var_dict = get_inputs_outputs(team_df)

	model = model_name(var_dict[outcome]['Inputs'],var_dict[outcome]['Outputs'],var_dict[outcome]['Payout'])
	model.model()

	print(model.metrics)
	print(model.results)
	print("Error: " + '{:.2%}'.format(model.error))
	print("Accuracy: " + '{:.2%}'.format(model.accuracy))
	print("Profit: " + '{:.2%}'.format(model.profit))


def model_team(team_name):
	d = {}

	team_df = read_file(team_name)
	var_dict = get_inputs_outputs(team_df)

	for outcome in ['Win','Over','F5_Over','Cover']:
		d[outcome] = {}

		d[outcome]['NeuralNet'] = {}
		net = NeuralNet(var_dict[outcome]['Inputs'],var_dict[outcome]['Outputs'],var_dict[outcome]['Payout'])
		net.model()
		# d[outcome]['NeuralNet']['Results'] = net.results
		d[outcome]['NeuralNet']['Error'] = '{:.2%}'.format(net.error)
		d[outcome]['NeuralNet']['Accuracy'] = '{:.2%}'.format(net.accuracy)
		d[outcome]['NeuralNet']['Profit'] = '{:.2%}'.format(net.profit)

		d[outcome]['SVM'] = {}
		svm = SVM(var_dict[outcome]['Inputs'],var_dict[outcome]['Outputs'],var_dict[outcome]['Payout'])
		svm.model()
		# d[outcome]['SVM']['Results'] = svm.results
		d[outcome]['SVM']['Error'] = '{:.2%}'.format(svm.error)
		d[outcome]['SVM']['Accuracy'] = '{:.2%}'.format(svm.accuracy)
		d[outcome]['SVM']['Profit'] = '{:.2%}'.format(svm.profit)

	return d


def model_all():
	d = {}

	teams = ['All_Teams','St. Louis Cardinals', 'Toronto Blue Jays', 'Los Angeles Angels', 'New York Yankees', 'Arizona Diamondbacks', 'San Diego Padres', 'Atlanta Braves', 'Oakland Athletics', 'Boston Red Sox', 'Cleveland Indians', 'Miami Marlins', 'Colorado Rockies', 'Milwaukee Brewers', 'Houston Astros', 'Minnesota Twins', 'Cincinnati Reds', 'New York Mets', 'Detroit Tigers', 'Philadelphia Phillies', 'Chicago Cubs', 'Seattle Mariners', 'Los Angeles Dodgers', 'San Francisco Giants', 'Pittsburgh Pirates', 'Texas Rangers', 'Chicago White Sox', 'Tampa Bay Rays', 'Kansas City Royals', 'Baltimore Orioles', 'Washington Nationals']

	for team in teams:
		d[team] = model_team(team)

	return d


class NeuralNet:
	def __init__(self,x,y,ml):
		self.x = x
		self.y = y
		self.ml = ml

		self.input_size = self.x.shape[1]

		self.x_train, self.x_test, self.y_train, self.y_test, self.ml_train, self.ml_test = train_test_split(self.x, self.y, self.ml, test_size = 0.25)

	def model(self):
		scaler = StandardScaler()
		scaler.fit(self.x_train)
		self.x_train = scaler.transform(self.x_train)
		self.x_test = scaler.transform(self.x_test)

		encoder = preprocessing.LabelEncoder()
		encoder.fit(self.y_train.ravel())
		self.y_train = encoder.transform(self.y_train.ravel())
		self.y_test = encoder.transform(self.y_test.ravel())

		self.output_size = len(set(self.y_train))

		net = MLPClassifier(hidden_layer_sizes=(int(round_up(self.input_size,100)),int(round_up(self.input_size/2,100)),int(round_up(self.input_size/5,100))), max_iter=10000)
		fit = net.fit(self.x_train, self.y_train.ravel())
		predictions = fit.predict(self.x_test)

		self.metrics = classification_report(self.y_test,predictions)

		self.results = pd.DataFrame([predictions,self.y_test,self.ml_test.ravel()]).T

		self.results.columns = ['Predicted','Actual','ML']
		self.results['Error'] = abs(self.results['Predicted']-self.results['Actual'])
		if self.output_size <= 2:
			self.results['Success'] = np.where(self.results['Predicted']==self.results['Actual'],1,0)
		else:
			self.results['Success'] = np.where(self.results['Error']<=1,1,0)
		self.results['Payout'] = np.select([self.results['Success']==1,self.results['Success']==0],[self.results['ML'],-1],0)

		self.error = self.results['Error'].mean()
		self.accuracy = self.results['Success'].mean()
		self.profit = self.results['Payout'].mean()


class SVM:
	def __init__(self,x,y,ml):
		self.x = x
		self.y = y
		self.ml = ml

		self.x_train, self.x_test, self.y_train, self.y_test, self.ml_train, self.ml_test = train_test_split(self.x, self.y, self.ml, test_size = 0.25)

	def model(self):
		scaler = StandardScaler()
		scaler.fit(self.x_train)
		self.x_train = scaler.transform(self.x_train)
		self.x_test = scaler.transform(self.x_test)

		encoder = preprocessing.LabelEncoder()
		encoder.fit(self.y_train.ravel())
		self.y_train = encoder.transform(self.y_train.ravel())
		self.y_test = encoder.transform(self.y_test.ravel())

		net = svm.SVR(gamma='auto')
		fit = net.fit(self.x_train, self.y_train.ravel())
		predictions = fit.predict(self.x_test)

		self.metrics = average_precision_score(self.y_test, predictions)

		self.results = pd.DataFrame([predictions,self.y_test,self.ml_test.ravel()]).T

		self.results.columns = ['Predicted','Actual','ML']
		self.results['Error'] = abs(self.results['Predicted']-self.results['Actual'])
		self.results['Success'] = np.select([round_up(self.results['Predicted']-0.05,0.5)==self.results['Actual'],round_down(self.results['Predicted']+0.05,0.5)==self.results['Actual']],[1,1],0)
		self.results['Payout'] = np.select([self.results['Success']==1,self.results['Success']==0],[self.results['ML'],-1],0)

		self.error = self.results['Error'].mean()
		self.accuracy = self.results['Success'].mean()
		self.profit = self.results['Payout'].mean()

##########
# a = read_file('Los Angeles Dodgers')
# d = get_inputs_outputs(a)
# hitter_net = NeuralNet(d['Win']['Inputs'],d['Win']['Outputs'],d['Win']['Payout'])
# hitter_net.model()

a = print_model("All Teams",NeuralNet,"F5_Over")
# print(json.dumps(a, indent=4, sort_keys=True))

