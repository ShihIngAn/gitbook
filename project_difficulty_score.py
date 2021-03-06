"""
calculates the project's difficulty score based on the number of lines of code 
Author : Ashwath Rajendran
"""
import os
import sys
import json
import time
import pprint
import requests
import curl
import pycurl
import urllib
import marshal
import pickle
import cStringIO
import math
import copy

from collections import defaultdict
from read_data import *
from resource_manager import ResourceManager

rm = ResourceManager()
pp = pprint.PrettyPrinter(depth = 6)

class ProjectDifficultyCalculator():
  """
  takes in the {project ID: {lang1: LOC, lang2:LOC} } data structure and assigns a project difficulty score for each language to the project.
  If a project has multiple languages, then a cumulative difficult will be assigned as the overall difficulty of the project

  """
  d = {'a':'poioi', 'adovfnr':'asdfgrtr', 'asa': {1:2, 2:3}}
  #pp.pprint(d)
  def readDataAndDump(self):
    pp = pprint.PrettyPrinter(depth = 6)
    allProjects = defaultdict()
    with open(rm.LOC,'rb') as f:
      print "loading the dict from pickle file.. please wait.. "
      cnt =0
      while 1:
        try:
          allProjects.update(pickle.load(f))
          cnt+=1
          #if cnt>20:
          #  break
        except EOFError:
          print 'parsing done!'
          break # no more data in the file
    print "allprojects"
    #pp.pprint(allProjects)


    print 'there are ',len(allProjects), 'projects in total in the pickle file'

    allProjLang = defaultdict()   #just stores the sum of squares of all LOC for normalising
    difficultyScore = defaultdict() # the final that stores { project: score }  final DS to dump with pickle
    langToprojs = defaultdict(set)
    for proj in allProjects:
      #print proj
      sumThisProjLang = defaultdict()
      languages = allProjects[proj]
      for lang in languages:
        #print lang
        if lang in allProjLang:
          allProjLang[lang] += float(languages[lang]*languages[lang])
        else:
          allProjLang[lang] = float(languages[lang]*languages[lang])
    #pp.pprint(langToprojs)
    
    # substitute the LOC to a normalized LOC
    for proj in allProjects:
      languages = allProjects[proj]
      for lang in languages:
        allProjects[proj][lang] = float(allProjects[proj][lang]/math.sqrt(float(allProjLang[lang])))

    # normalize a single project's languages... remove all those languages which have very less normalized value
    newProjects = copy.deepcopy(allProjects)
    newProjects1 = copy.deepcopy(allProjects)
    for proj in newProjects1:
      sumThisLangNorm = 0.0
      languages = newProjects1[proj]
      for lang in languages:
        sumThisLangNorm += languages[lang]
      for lang in languages:
        if sumThisLangNorm == 0:
          print proj
          print newProjects1[proj]
          continue
        newProjects[proj][lang] = newProjects[proj][lang]/float(sumThisLangNorm)
        if newProjects[proj][lang] < 0.2:       # threshold for removing project's languages
          #print "deleting ", proj, " this lang: ", lang
          del newProjects[proj][lang]
          del allProjects[proj][lang]         # delete the same language in the original allProjects dict as well

    # print 'projects after throwing away langs'
    # scale it all from 0 to 1 --> 1 is the max project's score. divide every lang's score by that max score
    maxScore = defaultdict()
    for lang in allProjLang:
      maxScore[lang] = float(0.0)
    # find max scores for each language
    for proj in allProjects:
      languages = allProjects[proj]
      for lang in languages:
        maxScore[lang] = max(maxScore[lang] , languages[lang] )
    # divide each value by the maximum value
    for proj in allProjects:
      languages = allProjects[proj]
      for lang in languages:
        allProjects[proj][lang] = float(allProjects[proj][lang]/float(maxScore[lang]))
        #languages[lang] = float(languages[lang]/maxScore[lang])
    # DONE!!! all scores in langiages is a score from 0 to 1
    for proj in allProjects:
      languages = allProjects[proj]
      difficultyScore[proj] = 0
      for lang in languages:
        langToprojs[lang].add(proj)
        difficultyScore[proj] = max(languages[lang], difficultyScore[proj])
    #print 'final difficultyScore'
    #pp.pprint(difficultyScore)
    #print 'num of langs: ',len(langToprojs)
    #print langToprojs
    with open('difficulty_score.p','wb') as f:
      pickle.dump(difficultyScore,f)
    print "pickle has dumped all difficulty scores in difficulty_score.p file.. unpickle and integrate"
    
    with open('lang_to_projects.p','wb') as f:
      pickle.dump(langToprojs,f)
    print "pickle has dumped all lang to proj lists in lang_to_projects.p file.. unpickle and integrate"

    with open('new_LOC.p','wb') as f:
      pickle.dump(allProjects,f)
    print "pickle has dumped proj and list of langs to new_LOC.p file.. unpickle and integrate"


if __name__ == '__main__':
    #obj = createRequest()
    #obj.get_auth_token()
    #obj.get_top_users_with_followers(6000, 20000)  
    locObj =ProjectDifficultyCalculator()
    locObj.readDataAndDump()
