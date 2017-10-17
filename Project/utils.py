import requests
import json

from json import JSONDecodeError
from functools import reduce
from collections import OrderedDict


def get_json_data(url):
    """
    Get json document and deserialize it to a Python object

    Parameters
    ----------
    url : srt
        URL

    Returns
    -------
    dict
        Python object
    """
    response = requests.get(url=url)
    text = response.text

    try:
        data = json.loads(text)
    except JSONDecodeError:
        data = json.loads(text.replace("'", '"'))

    return data


def get_spares():
    """
    Method to get 'Spares' dictionary

    Returns
    -------
    dict
        Spare parts
    """
    url = 'https://job.firstvds.ru/spares.json'
    return get_json_data(url)


def get_alternatives():
    """
    Method to get 'Alternative parts' dictionary

    Returns
    -------
    dict
        Alternative parts
    """
    url = 'https://job.firstvds.ru/alternatives.json'
    return get_json_data(url).get('alternatives')


def mark_shortage(dictionary):
    """
    Take dictionary and add extra info about whether
    there is a shortage

    Returns
    -------
    dict
        'Spares' dictionary with extra info
    """
    for value in dictionary.values():
        shortage = value['mustbe'] >= value['count'] + value['arrive']
        value.update({'shortage': shortage})
    return dictionary


def make_ordered(dictionary):
    """
    Take dictionary and make it ordered

    Returns
    -------
    OrderedDict
        'Spares' dictionary with ordered info
    """
    for key, value in dictionary.items():
        dictionary[key] = OrderedDict(sorted(value.items(),
                                             key=lambda i: i[0]))
    return dictionary


def get_merged(ordered=True):
    """
    Take two dictionaries and merge them into one

    Returns
    -------
    dict
        Merged 'Spare parts' dictionary
    """
    spares = get_spares()
    alternatives = get_alternatives()

    alternatives_list = [item for sub in alternatives.values()
                         for item in sub]

    for alt_category, alt_list in alternatives.items():
        alt_list_info = [spares.get(name)
                         for name in alt_list if spares.get(name)]

        if alt_list_info:
            q = reduce(lambda x, y: {'mustbe': max(x['mustbe'], y['mustbe']),
                                     'count': x['count'] + y['count'],
                                     'arrive': x['arrive'] + y['arrive']},
                       alt_list_info)
            spares.update({alt_category: q})

    for name in alternatives_list:
        if name in spares:
            del spares[name]

    if ordered:
        return make_ordered(spares)
    else:
        return spares


def get_tobuy():
    """
    Extract information about required parts

    Returns
    -------
    dict
        Spares to buy
    """
    spares = get_merged(ordered=False)
    required = {k: v['mustbe'] - v['count'] - v['arrive']
                for k, v in spares.items()
                if v['count'] + v['arrive'] < v['mustbe']}

    return required
