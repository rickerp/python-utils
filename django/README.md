# rickerp-django-utils

My django utils repo

## Includes

- [Dict to Q object](#dict_to_Q)

---

## <a name="dict_to_Q"></a> Dict to Q object

[dict_to_Q.py](./dict_to_Q.py)  
Django function to convert a `dict` with filters (allows lookups) to a `Q` object  
Useful when receiving **query params** in the URL (API)

**_function_** **dict_to_Q(filters_dict, valid_fields_operations=None, prefix='')**

- **filters_dict** : `dict`
  - A dictionary containing the fields and respective filter lookups and values
  - Example: {'ts**gte': '2020-10-12', 'ts**lte': '2021-10-12', ...}
- **valid_fields_operations** : `dict` | _optional_
  - Allowed fields and respective lookups in **filters_dict**
  - Default = None : doesn't verify validity (insecure)
  - Example: {'ts': ['gte', 'lte', 'exact'], 'hostname': []}
- **prefix** : `str` | _optional_
  - Specifies a model to add at the begining of every field in the returned `Q` object.
  - Defaults to ''.
  - Example:
    ```py
    >>>dict_to_Q({'ts__gte': '2020-10-12'}, prefix='pc')
    <Q: (AND: ('pc__ts__gte', '2020-10-12'))>
    ```

**_Returns_**:

- `django.db.models.Q` : `Q` object with the filters of the dictionary

**_Raises_**:

- **TypeError:** Invalid field name
- **TypeError:** Invalid filter lookup for the field

### Example:

```py
>>> print(request.GET.dict())
{'ts__gte': ['2020-02-15'], 'ts__lte': ['2020-10-12']}
>>> print(ComputerRecordFilter.get_fields())
OrderedDict([('pc__hostname', ['exact', 'iexact', 'isnull', 'regex', 'iregex', 'contains', 'icontains', 'in', 'gt', 'gte', 'lt', 'lte', 'startswith', 'istartswith', 'endswith', 'iendswith', 'range']), ('ts', ['exact', 'iexact', 'isnull', 'regex', 'iregex', 'contains', 'icontains', 'in', 'gt', 'gte', 'lt', 'lte', 'startswith', 'istartswith', 'endswith', 'iendswith', 'range', 'date', 'year', 'iso_year', 'month', 'day', 'week', 'week_day', 'quarter', 'time', 'hour', 'minute', 'second'])])
>>> dict_to_Q(request.GET.dict(), ComputerRecordFilter.get_fields(), 'computerrecord')
 <Q: (AND: ('computerrecord__ts__gte', '2020-10-12'), ('computerrecord__ts__lte', '2021-02-15'))>
```
