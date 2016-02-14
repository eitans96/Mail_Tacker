#!/Users/eitanshaulson/.virtualenvs/mail_tracker/bin/python
import json
import urllib2
import glob
import os
import sys
import logging
from datetime import datetime
from pyslack import SlackClient
from bs4 import BeautifulSoup


logging.captureWarnings(True)


# constants
O_URL = "http://www.israelpost.co.il/itemtrace.nsf/trackandtraceJSON?openagent&lang=EN&itemcode="
LINE_SEP = '------------------'
LOCATION = 'Location: '
TRACKER_ID = 'Tracker ID: '
ITEM = 'Item name: '
LOG = 'Log: '
PACKAGE_DIR = os.path.expanduser('~/.packages/')
LOG_FILE_DIR = os.path.expanduser('~/.packages/conf/Mail_tracker_log.log')


def create_package_folder_if_doesnt_exist():
    # function to make new file on desktop to store all data
    if not os.path.exists(PACKAGE_DIR):
        os.mkdir(PACKAGE_DIR)


def get_files():
    # returns the glob list of all our tracker files
    return glob.glob(os.path.join(PACKAGE_DIR, "*.txt"))


def update_all_files():
    # updates all the files in the list
    for file_name in get_files():
        update_item_info(file_name)
    talk_to_slack()


def update_item_info(file_name, item=None):
    return_ls = []
    # The logic to updating the files
    # test 1 - if the file name exists then, then read the data so we can get old location vs new
    # else, just assume is is empty
    if os.path.exists(file_name):
        lines = open(file_name).readlines()
    else:
        lines = []
    old_location = ''
    # test 2 - if the length of the lines is bigger then 0 the last line in the list is -----
    # then look for old location in the second to last item of that split
    if len(lines) > 0 and lines[-1].strip() == LINE_SEP:
        sll = lines[-2].strip()
        if LOCATION in sll:
            _, old_location = lines[-2].split(LOCATION)
            old_location = old_location[1:-1]
    # opening the file to write all the tracking info in it according to results of different tests
    with open(file_name, "a+") as fp:
        # current time log
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fp.write(LOG + now + '\n')
        if item is not None:
            fp.write(ITEM + item + '\n')
        # getting the id number from the file name so we can add it to the url to pull the data
        file_path, full_file_name = os.path.split(file_name)
        id, file_ext = os.path.splitext(full_file_name)
        fp.write("%s %s\n" % (TRACKER_ID, id))
        return_ls.append(id)
        # Test 4 - if internet works then gather info from url using specific id and putting it in json format
        # otherwise output the error so we can see the problem
        try:
            n_url = "".join(urllib2.urlopen(O_URL + id).readlines())
            data = json.loads(unicode(n_url, 'utf-8'))
            new_location = data["itemcodeinfo"]
        except urllib2.URLError as err:
            new_location = str(err)
        new_location = new_location.encode('utf-8')
        soup = BeautifulSoup(new_location, "html.parser")
        # test 5 - First it grabs the string of text which has our location,
        # then if that's enough, that will be our string, and if its not,
        # it will grab the text from that string and make it our location
        soup2 = soup.contents[0]
        try:
            new_location = unicode.encode(soup2.get_text(), 'utf-8')
        except AttributeError:
            new_location = unicode.encode(soup2, 'utf-8')
        # test 6 - if new location is the same as the old one then notify me
        if old_location == new_location:
            fp.write("Status: The package is still in the same location as the last log." + '\n')
            return_ls.append(new_location)
        fp.write("%s %s\n" % (LOCATION, new_location))
        fp.write("%s\n" % LINE_SEP)
    return return_ls


def talk_to_slack():
    data = []
    ls = []
    last_data = []
    # this function sends the same output of the files to slack
    token_dir = os.path.expanduser('~/.packages/conf/conf.txt')
    files = get_files()
    client = None
    if os.path.exists(token_dir):
        with open(token_dir, 'r') as fp:
            client = SlackClient(fp.readlines()[0].strip())
    for filen in files:
        with open(filen, 'r') as fp:
            lines = fp.readlines()
            if "Item name:" in lines:
                    print "yes"
            for line in lines:
                line = line.rstrip()
                if line != LINE_SEP:
                    ls.append(line)
                else:
                    data.append(ls)
                    ls = []
            last_data.append(data[-1])
    last_data = '\n'.join(str(line) for item in last_data for line in item)
    with open(LOG_FILE_DIR , 'a+') as fp:
        fp.write(last_data + '\n')
    if client is not None:
        client.chat_post_message('#mail-tracker-notif', last_data, username='slackbot')
    sys.exit(0)


def add(package_num, item=None):
    # Function to add files to our package folder
    if len(package_num) > 13:
        print "Illegal tracker number. Can only be up to 13 numbers"
        sys.exit(2)
    else:
        full_name = os.path.join(PACKAGE_DIR, package_num + ".txt")
        if full_name in get_files():
            print "Sorry, you already have file with this name."
            sys.exit(1)
        else:
            update_item_info(full_name, item)
            print "Added successfully :)"
            sys.exit(0)


def delete(package):
    # Function to delete files from our package folder
    if type(package) == list:
        for file_name in package:
            full_name = os.path.join(PACKAGE_DIR, file_name + ".txt")
            if full_name in get_files():
                os.remove(full_name)
                print "Files deleted successfully :)"
            else:
                print "The id you are trying to delete, does not exist. %s" % file_name
            # return "Its a list"
    else:
        full_name = os.path.join(PACKAGE_DIR, package + ".txt")
        if full_name in get_files():
            os.remove(full_name)
            print "Files deleted successfully :)"
        else:
            print "The id you are trying to delete, does not exist. %s" % package
        # return "Its a singular number"
    sys.exit(0)


def command_tool():
    # we can add in the call to our script, if we want to add or delete files
    # using a sys.argv command
    if len(sys.argv) > 1:
        if len(sys.argv) < 3:
            print "usage: %s [--add|--del  package_id]" % sys.argv[0]
            sys.exit(1)
        if sys.argv[1] == '--add':
            if len(sys.argv) == 3:
                add(sys.argv[2])
            elif len(sys.argv) == 4:
                add(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == '--delete':
            if len(sys.argv) > 3:
                delete(sys.argv[2:])
            else:
                delete(sys.argv[2])
    else:
        if len(get_files()) > 0:
            update_all_files()
        else:
            print "The file drawer is empty."


if __name__ == "__main__":
    create_package_folder_if_doesnt_exist()
    command_tool()


