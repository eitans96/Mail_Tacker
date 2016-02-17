import pytest
import os
from Mail_Tracker import delete
from Mail_Tracker import get_files

PACKAGE_DIR = os.path.expanduser('~/.packages/')

# - test 1: Checking if the package we gave it is a list or singular


@pytest.mark.parametrize(('expected', 'func_input'), [
    ("Its a list", delete(['1, 2, 3, 4'])),
    ("Its a singular number", delete('3'))
])


def test_if_package_is_singular_or_list(func_input, expected):
    assert expected == func_input

# - test 2: Checking if the id is even in the file list


@pytest.mark.parametrize(('func', 'id'), [
    (get_files(), '903299'),
    # (get_files(), '600000')
])


def test_if_file_in_files(func, id):
    full_name = os.path.join(PACKAGE_DIR, id + ".txt")
    assert full_name not in func


# - test 3: Checking if the id is in the file list, then can it delete it
# test only works once with actual ids, otherwise it fails

@pytest.mark.parametrize(('func', 'id'), [
    (get_files(), '1234'),
    # (get_files(), '900111003299')
])


def test_if_file_exists_then_will_it_delete(func, id):
    full_name = os.path.join(PACKAGE_DIR, id + ".txt")
    if full_name in func:
        os.remove(full_name)
    assert full_name not in get_files()


