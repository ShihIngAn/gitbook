from flask import Flask, render_template
import pickle
 
app = Flask(__name__)      
 
@app.route('/')
@app.route('/index')
def home():
	languages = ['C++', 'Ruby']
	aoi = ['machine-learning', 'artificial-intelligence']
	return render_template('index.html', languages = languages, areas_of_interest = aoi)

@app.route('/about')
def about():
  print "this is printed whenever the about page is called!!!!!!!!!!!!!!!!!!!!!!!"
  return render_template('about.html')

@app.route('/results')
def results():
  results = [{'projectName': 'login' , 'owner':'ownername'} , {'projectName': 'login' , 'owner':'ownername'}]
  with open("/home/ash/code/IR/gitbook/web_home/app/tmpProjs.p","rb") as fr: 
    results1 = pickle.load(fr)
  with open("/home/ash/code/IR/gitbook/web_home/app/project_contributors.p","rb") as fr: companies = pickle.load(fr)
  aoi = ['machine-learning', 'artificial-intelligence']
  return render_template('results.html' , areas_of_interest=aoi, results=results1 , companies = companies)

@app.route('/layout')
def layout():
  return render_template('layout.html')

if __name__ == '__main__':
  app.run(debug=True)
