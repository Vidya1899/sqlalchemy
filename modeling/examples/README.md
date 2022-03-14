## Data Modeling for Unit Conversion 

Conversion Formula:    
```
y + c1 = mx + c2
{to} + {offset_value_1} = {multiplier} * {value} + {offset_value_2}
```

Condition: 
If dimensions are same convert to the desired unit.


#### Table 1 - Dimension

|  Id  |   Quantity |    
|:----:|:----------:|
| 1    |    Length  | 
| 2    |    Mass    |   
| 3    |    Time    |     
 
 #### Table 2 - Units
|    Id       |       Dimension Id      | Base unit |  Symbol  |
|:-------------------:|:----------------:|:----------------:|:----------------:|
| 1 | 1 | meters | (m) |
|2 | 1  | centimeters | (cm)


 #### Table 3 - Converions
 |       Units Id (from)   |       Units Id (to)     |  value | Multiplier | Offset Val 1 | Offset val2 |
|:-------------------:|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
|   1 |   2   |  500 | 100 | 0  |0|
| 2 |  1   |     5    | 0.01 | 0 |0 |
 
