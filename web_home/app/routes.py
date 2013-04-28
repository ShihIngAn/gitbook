from flask import Flask, render_template
 
app = Flask(__name__)      
 
@app.route('/')
@app.route('/index')
def home():
	languages = ['C++', 'Ruby']
	aoi = ['machine-learning', 'artificial-intelligence']
	return render_template('index.html', languages = languages, areas_of_interest = aoi)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/layout')
def layout():
  return render_template('layout.html')

if __name__ == '__main__':
  app.run(debug=True)
