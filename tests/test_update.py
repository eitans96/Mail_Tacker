import pytest
from Mail_Tracker import update_item_info
from Mail_Tracker import get_files
import os


PACKAGE_DIR = os.path.expanduser('~/.packages/')

# - test 1: Checking if file id exists in file list
# for the test, you need to use an actual file in list


@pytest.mark.parametrize(('func', 'id'), [
    (get_files(), '9000003299'),
])

def test_check_if_file_actually_exists(func, id):
    full_name = os.path.join(PACKAGE_DIR, id + ".txt")
    assert full_name in func


# - test 2: If file exists, then can it read into the lines of the file
# for this test, we need an actual id in the file list

@pytest.mark.parametrize(('func', 'id'), [
    (get_files(), '9000003299')
])


def test_check_if_file_exists_then_can_we_read_into_it(func, id):
    full_name = os.path.join(PACKAGE_DIR, id + ".txt")
    lines = open(full_name, 'r').readlines()
    assert lines > 0

# - test 3: if file doesnt exist, does it make a new one?
# this tests needs a file that does not exist


@pytest.mark.parametrize(('func', 'id'), [
    (get_files(), '1234'),
    # (get_files(), '900111003299')
])


def test_if_file_doesnt_exists_then_will_it_create(func, id):
    full_name = os.path.join(PACKAGE_DIR, id + ".txt")
    if full_name not in func:
        create = open(full_name, 'a+')
    assert full_name in get_files()


# - test 4: Getting just the id from the full path

@pytest.mark.parametrize(('full_path', 'expected'), [
    (os.path.join(PACKAGE_DIR, str(123456) + ".txt"), '123456'),
    (os.path.join(PACKAGE_DIR, str(654321) + ".txt"), '654321')
])


def test_checking_if_it_can_pull_id_from_fullPath(full_path, expected):
    assert expected == update_item_info(full_path)[0]


# - test 5: Check if it actually pulled down internet from the web
# - you will need a real tracker id for this test to actually grab from the web

@pytest.mark.parametrize(('id', 'expected'), [
    ('RS349201615NL', 'The postal item was delivered to its destination on 30/12/2015 via the Givat Sharet postal unit in Beit Shemesh.'),
    ('RS349183355NL', 'The postal item was delivered to its destination on 11/12/2015 via the Givat Sharet postal unit in Beit Shemesh.')
])


def test_Checking_if_it_can_pull_data_from_web(id, expected):
    full_name = os.path.join(PACKAGE_DIR, id + ".txt")
    assert expected == update_item_info(full_name)[1]


# - test 6: This wil check if it can actually tell us if new location is different than the last

@pytest.mark.parametrize(('full_path', 'old_loc'), [
    (os.path.join(PACKAGE_DIR, 'RS349183355NL') + ".txt", 'The postal item was delivered to its destination on 11/12/2015 via the Givat Sharet postal unit in Beit Shemesh.')
])


def test_if_it_can_tell_if_old_loc_and_new_loc_are_different(full_path, old_loc):
    assert old_loc == update_item_info(full_path)[1]