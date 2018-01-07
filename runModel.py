import json
import numpy
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, \
    AdaBoostClassifier,BaggingClassifier,GradientBoostingClassifier,VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

json_file=open("trainFeatures.json", 'r')
ax=json.load(json_file)
finalFeatures=numpy.array(ax['features'])
labels=numpy.array(ax['labels'])

clf1 = MLPClassifier(hidden_layer_sizes=(144,72,3))
clf2 = AdaBoostClassifier(n_estimators=100)
clf3 = RandomForestClassifier(n_estimators=50)
clf4 = ExtraTreesClassifier(n_estimators=50)
clf5 = BaggingClassifier(n_estimators=50,warm_start=True,bootstrap_features=True)
clf6 = GradientBoostingClassifier(n_estimators=500)
lin_clf=VotingClassifier(estimators=[('mlp', clf1), ('ada', clf2),('rf',clf3),('extr',clf4),('bgc',clf5),('gbc',clf6)],voting='soft')
lin_clf.fit(finalFeatures,labels)

json_file=open("testFeatures.json", 'r')
ax=json.load(json_file)
finalFeatures=numpy.array(ax['features'])

import sys
sys.stdout = open('eval.out', 'w')
lip=lin_clf.predict(finalFeatures)
for item in lip:
    print(int(item))