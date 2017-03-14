CS 122 Final Project TestMe

Testing our project (Course Scheduler Website)

Set up
----------
# 1) Open Chrome
# 
# 2) enter into the URL bar: localhost/Scheduler/Scheduler.php

#########################

Website Breakdown
----------
# - Max Hours - 
# You will first be prompted to enter a max amount of hours
# which the website will later use to keep track of your class time load.
#
# - Class Search - 
# The website contains scraped classes for Winter 2017 and evaluation data
# going as far back as 2011 for certain classes (many classes have no evals).
# You can search by any of the filters on the new AIS website.
#
# These include: Class Title, Course Number, 
# Day of the Week (contains/only), Class Description 
# (our search performs better than AIS here),
# professor names, and max hours.
# 
# - Hour Search -
# Specifying a max hour means you want no classes with an aggeregated
# average amount of hours greater than specified.
# If you do NOT specify a max number of hours, no classes will be linked
# with evals and hours will not show up in the results.
# If you DO specify a max number of hours, it is possible that many Winter 2017
# classes will not show up because they either a) did not have evaluations or 
# b) their evaluation forms did not fit our criteria while scraping.
#
# We were able to link around 430 unique classes to evals.
#
# - Adding/Tracking/Deleting Classes -
# When results from a query pop up, you can add classes to the calendar
# using the "add" button to visualize your schedule.
#
# If hours was included in the results of a class you add, 
# a gauge will pop up with your max and count the hours added
#
# If a class has No Days or Times, its default time is 12AM Saturday.
# You can drag and drop classes to different times, and view your schedule
# by day, week, or month!
#
# Click on an event to delete it!