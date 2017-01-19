## python-sqlparse


sqlparse提供了三个简单的函数对SQL语句进行一些简易的工作。
举几个例子。

 split()：对一个或多个SQL语句的字符串进行分割切片，返回包含多个SQL语句的一个列表。

   para: sql – A string containing one or more SQL statements.
         encoding – The encoding of the statement (optional).
   Returns:	A list of strings.

    >>> import sqlparse
    >>> sql = 'select * from foo; select * from bar;'
    >>> sqlparse.split(sql)
    [u'select * from foo; ', u'select * from bar;']

 format():
    
    para: encoding, ...(见下)
    return: 得到想要的格式的SQL语句字符串
    
    >>> sql = 'select * from foo where id in (select id from bar);'
    >>> print sqlparse.format(sql, reindent=True, keyword_case='upper')
    SELECT *
    FROM foo
    WHERE id IN
      (SELECT id
      FROM bar);
   在这个例子中,SQL语句中所有关键字 变成大写. 也变成了更可读的方式.
   
   关于format函数的参数:
     
     keyword_case:
       SQL关键字的格式: “upper”, “lower” and “capitalize”
     identifier_case:
       SQL标识符(常量名，变量名，游标名，函数名)的格式: “upper”, “lower”, and “capitalize”
     strip_comments:
       True表示去掉语句中的comments.
     truncate_strings
         If truncate_strings is a positive integer, string literals longer than the given value will be truncated. 
     truncate_char (default: “[...]”)
         If long string literals are truncated (see above) this value will be append to the truncated string.
     reindent
         If True the indentations of the statements are changed.
     indent_tabs
         If True tabs instead of spaces are used for indentation.
     indent_width
         The width of the indentation, defaults to 2.
     wrap_after
         The column limit for wrapping comma-separated lists. If unspecified, it puts every item in the list on its own line.
     output_format
         If given the output is additionally formatted to be used as a variable in a programming language. Allowed values are “python” and “php”.

 sqlparse.parse(sql, encoding=None)
Parse sql and return a list of statements.

Parameters:	
sql – A string containing one or more SQL statements.
encoding – The encoding of the statement (optional).
Returns:	
A tuple of Statement instances.