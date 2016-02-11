Mail tracker service
version 1.0
Eitan Shaulson

The purpose of this app is to track the packages you order.

Note: 
This only works with packages inside of Israel, because it uses the israel-post database.
Useful for slack users. (can be simply edited to not use slack)
If your package location is in a different language, it may get confused.


Useful for:

When you purchase something online, you receive a tracking number to track your package as it travels towards you.

Now, you can go on the israel-post website and just search for your package, using your tracker ID and it will tell you the location of your parcel.

Using this program, you can just add your tracking ID to a list of your ID’s that all get tracked, either manually when you click ‘run’ or automatically in an intervals.

How it works:

How it works is, When the script is first run, it looks on your computer to see if you have a folder named ‘~/.packages/‘. If you don’t, it will create one for you (a hidden folder called ‘packages’ on your desktop). If you do have one, it will move on.
Next it goes and checks if you have any files inside your ‘packages’ folder. If you do, then it goes automatically updates each one (Ill explain the updating logic in abit), and if it sees that you have no files in your folder, it will tell you its empty.

Now, there are 3 options in the program. Add, Delete, Update.

Add - is the option to add a new file to the ‘packages’ folder. Which means going and giving the ID number which creates the new file in the folder.
First it checks if you your ID number is legal. A legal number is under 13. If its legal, it will go on to check if you already have a file like so existing in the folder. If you do, it will prompt you, if you don’t, it will create the file. 

Delete - is the option to put in your ID and the program will go and look for your ID in the folder. If its not there, you will get prompted and if it is, it will get deleted. You also have a multiple delete option were the program will read how many options you put in after delete. If it sees that it is a list(multiple options), it will go through it and check each one. If it sees its singular, then it will get deleted normally.
 
Update - is when either, you click run(if you’re using a GUI, like pycharm or IDLE), or you have it running in a crontab at a set interval.
When the program sees that is has no ‘add’, or ‘delete’ argument added, it will first start off by going to our function that gets a list of all the files from ‘packages’ folder and returns it and gives it to the logic function one by one.
Then it goes through the logic based function to update each file according to the ID that its attached to. It writes all the new info down into 3 places: Each ID has its own file, a log file, and slack(if you have it).

How it updates:

It goes to each file and grabs the ID from its name, which you gave it in the first place. Then it goes and opens up the file for reading and checks for the last location that was registered. If none is found, then it saves the old location as an empty string. 
Next, the file is opened up for appending and first it saves a ‘log time’ to the file, so you can know when each update was made. Next it goes goes and gets just the ID number from the full path file name and sticks it into the link for the package search page on israel-post website and grabs the return data in json format. 
If the internet is not working, it will stick the error in the file. 
Once its in json format, it looks for a specific thing holding the newly updated location.
Now it compares the old location with the new to see if its still in the same place. If it is, it will prompt you.

So what gets written to each file is:
log time
tracker id
(if in same place) status
location




