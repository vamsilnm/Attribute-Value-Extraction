# Attribute-Value-Extraction
This is used for Extracting Attributes and Values Pairs from product descriptions.

For Example if there is a description like "The weight of mobile is 155 gms", So the main aim of this project is to extract weight as attribute and 150 gms as value.

For this I have used Naive Bayes classifier for building the model and features as words with context-window of size 4 and pos tagging for the same.

I have used Expectation Maximization algorithm after building a basic model.
naive_bayes_implementation_mobiles_modified.py is file to look for.

