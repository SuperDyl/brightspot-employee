"""
Random utility functions used by the professor package

Constants:
NAME_SUFFIXES - default name suffixes to ignore while splitting a name
"""
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

from typing import Iterable, Callable, Any, Optional
from threading import Thread

NAME_SUFFIXES = ['jr.', 'iii', 'sr.']


def chunk_iterator(count: int, iterable: Iterable):
    """
    Iterates in chunks of up to size count
    """
    iterator = iter(iterable)
    items = []

    try:
        while True:
            items.append(next(iterator))
            if len(items) >= count:
                yield items
                items = []
    except StopIteration:
        yield items


def stepped_limited_multithread(functions: Iterable[Callable[[Any], None]],
                                args: Iterable = (), kwargs: Optional[dict] = None, limit: int = 10) -> None:
    """
    Calls each function, using up to limit threads at a time.

    :param functions: functions to call in each thread
    :param args: arguments to pass to each function (same arguments used for each)
    :param kwargs: other arguments to pass to each function
    :param limit: number of threads to run as a chunk at a time
    """
    if kwargs is None:
        kwargs = dict()

    for function_chunk in chunk_iterator(limit, functions):
        current_threads = []
        for func in function_chunk:
            new_thread = Thread(target=func, args=args, kwargs=kwargs)
            new_thread.start()
            current_threads.append(new_thread)

        for thread in current_threads:
            thread.join()


def split_name(full_name: str, name_suffixes: Optional[Iterable[str]] = None) -> (str, str):
    """Return the estimated first and last name as a tuple"""
    if name_suffixes is None:
        name_suffixes = NAME_SUFFIXES
    full_split_name = full_name.split(' ')
    if full_split_name[-1].lower() in name_suffixes:
        *first, last = full_split_name[:-1]
        return ' '.join(first), ' '.join((last, full_split_name[-1]))
    # else
    *first, last = full_split_name
    return ' '.join(first), last


def tag_iterator(url: str, args: Iterable = (), kwargs: Optional[dict] = None) -> ResultSet:
    """
    Return an iterable of the specified found tags in the html found at url
    Provided args and kwargs are directly passed as if in a BeautifulSoup.find_all function

    :param url: url of html text to pull
    :param args: args to filter the iterator by
    :param kwargs: key-value pairs to filter the iterator by
    """
    if not args:
        args = 'div',
    if kwargs is None:
        kwargs = {'class_': 'ListVerticalImage-items-item'}

    with requests.get(url) as request:
        html_data = request.text
    bs = BeautifulSoup(html_data, 'html.parser')
    return bs.find_all(*args, **kwargs)


def remove_prefix(input_string: str, prefix: str) -> str:
    """Return input_string but without prefix (if it exactly appears at the start of input_string)."""
    if prefix != input_string[0:len(prefix)]:
        return input_string
    return input_string[len(prefix):]
