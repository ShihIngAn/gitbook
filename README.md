gitbook
=======

A project to help more people get into open source development.

What it does.
It suggests github projects to work on based on user preferences.

Main Components
 - Crawler: To retrieve data from github APIs
 - Bayes Classifier: Naive Bayes Classifier trained with specific vocabulary and training data to capture Areas of interest
 - User Ranker: Ranks Github users according to their importance using pagerank
 - Web Interface: Built using Python Flask API

Instructions to run
 - Requires sklearn 0.14, flask
 - clone using git clone git://github.com/suvodeep-pyne/gitbook
 - Add a sym link inside app folder ln -s ../../ gitbook (TODO: refactor)
 - run python web_home/run.py from parentmost directory of the project

Language - python
