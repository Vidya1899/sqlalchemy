### 1. Modeling 
The data model determines the logical structure of a database. It fundamentally determines in which manner data can be stored, organized and manipulated. The most popular example of a database model is the relational model. Examples of relational database models can be found here.

### 2. Database normalization

Normalization entails organizing the columns (attributes) and tables (relations) of a database to ensure that their dependencies are properly enforced by database integrity constraints

#### 1.1	Satisfying 1NF
Each column of a table must have a single value. Columns which contain sets of values or nested records are not allowed.
#### 1.2	Satisfying 2NF
A relation is in 2NF if it is in 1NF and every non-prime attribute of the relation is dependent on the whole of every candidate key.     
(A non-prime attribute of a relation is an attribute that is not a part of any candidate key of the relation.)    

Reference : [Wiki](https://en.wikipedia.org/wiki/Database_normalization) 
