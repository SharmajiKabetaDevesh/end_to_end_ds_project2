 I have created an end to end Data Science project that involve setting up the ETL pipeline that fetches the data from mongodb atlas,after fetching it validates
 the data it is has the correct data tyepes and columns then it is stored as an artifact ,after extraction it is transformed by dealing with null values with knn 
 imputer and stored as numpy objects as loading stage.
 this data is then used to train our models and the best one is found out by r2 score measure and pushed to dvc and mlflow for tracking ,the models were also saved 
 on an azure blob for versioning and fault tolerance and at the later stages it was used to create an api using fast API to be used in a web applicaiton: heres a part of code
