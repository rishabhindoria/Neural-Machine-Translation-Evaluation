# Neural-Machine-Translation-Evaluation

• Built a classifier for evaluating quality of machine translation to predict best matching sentence to the reference sentence.

• Performed feature engineering to select metrics like METEOR and BLEU for evaluating quality of machine translation
using Python libraries such as nltk, sklearn and numpy.

• Computed features once on the training data (consisiting of sentences) like cosine similarity from neural skip n-gram models and pos tagging to better take context into account and then stored them as file.

• Trained a combination of SVM, RandomForest, neural MLP based voting classifier on the computed features. 

• Saved the model using Python Pickle library to a file for quick use next time to classify new test data.

• Outperformed other classmates to be in top 5 among 180. 
