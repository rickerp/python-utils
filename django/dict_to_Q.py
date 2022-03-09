from django.db.models import Q


def dict_to_Q(filters_dict, valid_fields_operations=None, prefix=''):
    """ Converts a dictionary to Q filter object
    Args:
        filters_dict (dict): 
            Must contain fields, filter lookups and values. 
            Example: {'ts__gte': '2020-10-12', ...}
        valid_fields_operations (dict, optional): 
            Mapping for valid field names and corresponding filter lookups. 
            Defaults to None : doesn't verify validity (insecure)
            Example: {'ts': ['gte', 'lte', 'exact'], ...}
        prefix (str, optional): 
            Specifies a model to add at the begining of every field. 
            Defaults to ''.
            Example: 
            >>> dict_to_Q({'ts__gte': '2020-10-12'}, prefix='pc')
            <Q: (AND: ('pc__ts__gte', '2020-10-12'))>
    Raises:
        TypeError: Invalid field name
        TypeError: Invalid filter lookup for the field
    Returns:
        Q: Q object with the filters of the dictionary
    """
    ret_dict = dict()
    if prefix != '':
        prefix += '__'

    for filter_field in filters_dict:
        filter_sep = filter_field.split('__')
        fname = filter_sep[0]
        lookup = filter_sep[1] if len(filter_sep) == 2 else 'exact'

        if valid_fields_operations:
            if fname not in valid_fields_operations:
                raise TypeError(f"Invalid field name: '{fname}'")
            if lookup not in valid_fields_operations.get(fname):
                raise TypeError(f"There is no valid operation '{lookup}' for the '{fname}' field")

        ret_dict[prefix + filter_field] = filters_dict.get(filter_field)

    return Q(**ret_dict)