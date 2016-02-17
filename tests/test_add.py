import pytest
from Mail_Tracker import add

# - test 1: - Checks if the id is bigger than 13


def test_id_bigger_than_13():
    big_id = '1234567890123456'
    with pytest.raises(SystemExit) as exit_val:
        add(big_id)
    assert 2 == exit_val.value.code

# - test 2: Checks if the id is smaller than 13, if it exists or not


def test_id_smaller_than_13_if_exists_or_not():
    lil_id = '9000003299'
    with pytest.raises(SystemExit) as exit_num:
        add(lil_id)
    assert 1 == exit_num.value.code

# - test 3: Checks if id is smaller than 13, and doesnt exist, than create
# this test had to work with an actual new id otherwise it wont create


def test_if_file_is_smaller_than_13_and_doesnt_exist_create():
    lil_id = '900111003299'
    with pytest.raises(SystemExit) as exit_num:
        add(lil_id)
    assert 0 == exit_num.value.code









