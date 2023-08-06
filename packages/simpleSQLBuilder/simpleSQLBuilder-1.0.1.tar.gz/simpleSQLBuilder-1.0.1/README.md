# simpleSQLBuilder

## Example

```python
from simpleSQLBuilder.QueryBuilder import QueryBuilder

print(QueryBuilder().from_('users').select('id').select('name', 'email').where('id < 3').build().result) # 'SELECT id,name,email FROM users WHERE id < 3'

print(QueryBuilder().from_('users').where('id < 3').where('coin > 100').build().result) # 'SELECT * FROM users WHERE id < 3 AND coin > 100'
```