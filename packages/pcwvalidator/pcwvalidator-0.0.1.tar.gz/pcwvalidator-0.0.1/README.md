#### PCW Validator

- This small program can be used to validate a batch csv file sent by price comparison websites against a series of operators. 

- Base Operators are defined and then combined together to form operators which are executed on a specified column in the CSV file.

##### *Usage*

```
pip install pcwvalidator
```

```
from pcwvalidator.validate import execute

execute('/full/path/to/csvfile')
```

- This will return return True if that CSV is valid 
 
*Command line Usage*

```
export PYTHONPATH=$(pwd)
```
Then in the command line:
```
python run.py -f { csv_file }
```

- Use full paths for each element, i.e:
```
/PATH/bin/python /full/path/src/run.py -f /full/path/src/{ csv_file }
```



###### Author 
- Alexander Isherwood 



