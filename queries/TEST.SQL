insert	into test_table (column1, column2)
VALUES('6/18/2020', 'test');

SELECT	* from test_table
WHERE column1='6/18/2020' AND	column2='test';

delete from test_table;