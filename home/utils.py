from typing import (Type, T)

def cleaned_field(form: Type[T]) -> dict:
    """
    Given a form, returns a dictionary of cleaned field values.

    :param form: The form to extract cleaned data from.
    :type form: Type[T]
    :return: A dictionary of cleaned field values.
    :rtype: dict
    """
    fields_value = {}
    for key in form.fields.keys():
        fields_value[key] = (form.cleaned_data[key])
    return fields_value

def pick(object:dict, *args):
    """
    Pick values from a dictionary by keys.
    
    Args:
    object: dict: the dictionary from which the values will be picked
    args: tuple of keys to pick the values from the dictionary
    
    Returns:
    list: list of values picked from the dictionary
    """
    values = []
    for key in object.keys():
       if key in args:
           values.append(object[key])
    return values 
