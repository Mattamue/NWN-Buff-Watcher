"""
Author: Mattamue
Last updated: 05/04/2021
Program: friends_list.py

Scrapes the portal and shows a friends list that the user creates
New window inside the "NWN-Buff-Watcher" that the user can
also have open, writes to a CSV to keep track of friends
"""

from urllib import request  #this is a solid package for getting urls
import bs4 as BS #BS package
import time # used for sleep to keep the loop running and re-check the online friends
import datetime # for the time stamp
import csv

def open_friends_csv():
    with open("NWN-Buff-Watcher\get_friends_list\\friends.csv", 'r') as csv_friends:
        csv_reader = csv.reader(csv_friends, delimiter=',')

        csv_friends_list=[]

        for row in csv_reader:
            csv_friends_list.append(row)

    return csv_friends_list

def scrape_portal():
    friends_list = open_friends_csv()

    url="https://portal.nwnarelith.com/" #set the url you are scraping

    page = request.urlopen(url) #have the urllib package call it

    soup = BS.BeautifulSoup(page.read(), features="lxml") #soupify it so you can read the tags

    names = soup.find_all("div", class_="character-name") #Find all the div tags with the class character-name

    online=[]

    for i in range(0,len(names)): #This for loop steps through each name in the list
        for x in friends_list: # this loops through the friends list and goes to the 1st index, which is a list
            if names[i].text in [x][0]: #checks to see if it matches a value in the friends_list sub-list
                online.append([x[0], x[1]]) # appends the name and faction to the online list

    return_string = ""

    for x in sorted(online, key=lambda z: z[1]): # sorted() is a weird function that requires that you use a function to sort with the "key=" and so you can cheat that with lambda which is a dummy nothing function
        padding = 22 - len(x[0]) # makes the text all the same width, even with different length names, so the formatting looks like
        return_string = return_string + x[0] + padding * ' ' + '::' + x[1] + '\n' # prints out the online list somewhat nicely
    
    # print(f'Debug online list: {online}')
    goodTime = datetime.datetime.now()
    return_string = return_string + f"{goodTime.ctime()}" # also stamps the last time it was scanned so you know how old list is

    return return_string

if __name__ == "__main__":
    print(scrape_portal()) # debugging