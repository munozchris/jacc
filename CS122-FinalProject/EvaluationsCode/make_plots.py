import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# The functions in this file will create visual representations
# of some of the evaluation information we scraped


# First, some helper functions to determine if a department is
# in a certain table in the evaluations database

def is_dept_in_ex(c, dept):
    '''
    Given a connection cursor to a SQLite database (specifically,
    the eval database), and a department, this function determines 
    if that department can be found in the e_xTA table. 
    '''

    depts_in_ex = c.execute("SELECT DISTINCT Dept FROM e_xTA;").fetchall()
    depts_in_ex = [entry[0] for entry in depts_in_ex]

    if dept in depts_in_ex:
        return True

    else:
        return False

def is_dept_in_eo(c, dept):
    '''
    Given a connection cursor to a SQLite database (specifically,
    the eval database), and a department, this function determines 
    if that department can be found in the e_oTA table. 
    '''

    depts_in_eo = c.execute("SELECT DISTINCT Dept FROM e_oTA;").fetchall()
    depts_in_eo = [entry[0] for entry in depts_in_eo]

    if dept in depts_in_eo:
        return True
    else:
        return False

def is_dept_in_bio(c, dept):
    '''
    Given a connection cursor to a SQLite database (specifically,
    the eval database), and a department, this function determines 
    if that department can be found in the e_bio table. 
    '''

    depts_in_bio = c.execute("SELECT DISTINCT Dept FROM e_bio;").fetchall()
    depts_in_bio = [entry[0] for entry in depts_in_bio]

    if dept in depts_in_bio:
        return True
    else:
        return False

def is_dept_in_lang(c, dept):
    '''
    Given a connection cursor to a SQLite database (specifically,
    the eval database), and a department, this function determines 
    if that department can be found in the e_lang table. 
    '''

    depts_in_lang = c.execute("SELECT DISTINCT Dept FROM e_lang;").fetchall()
    depts_in_lang = [entry[0] for entry in depts_in_lang]

    if dept in depts_in_lang:
        return True
    else:
        return False


# Next, here is a function to help with plotting time on the x-axis

def assign_x_values_to_dates(date):

    '''
    Given a date as a string, this function gives it a numerical 
    value to make graphing easier (we can put this number on the 
    x-axis)
    '''

    first_digit = float(date[-1:])-2

    if date[:6] == "Winter":
        decimal = 0.0

    elif date[:6] == "Spring":
        decimal = 0.25

    elif date[:6] == "Summer":
        decimal = 0.5

    elif date[:6] == "Autumn":
        decimal = 0.75

    x_value = first_digit+decimal

    return x_value


# Now, onto the visualization functions

def get_all_hours(dept):
    '''
    Given a department, this function returns two lists: one of every
    course number in the department, and one of the average hours 
    spent per week for each corresponding class. 
    '''

    conn = sqlite3.connect("../Databases/eval.db")
    c = conn.cursor()

    # connect to the eval database

    hours = []
    course_nums = []


    # check to see if that department can be found in each table.
    # if it can't, we want to skip that table

    # if it is the table, we want to add the course number and
    # the average hours to lists, which we can plot

    if is_dept_in_ex(c, dept):

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_xTA WHERE\
                Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results1 = c.execute(query, data)

        for row in results1:
            hours.append(row[1])
            course_nums.append(row[0])

    if is_dept_in_eo(c, dept):

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_oTA WHERE\
                Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results2 = c.execute(query, data)

        for row in results2:
            hours.append(row[1])
            course_nums.append(row[0])

    if is_dept_in_bio(c, dept):

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_bio WHERE\
                Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results3 = c.execute(query, data)

        for row in results3:
            hours.append(row[1])
            course_nums.append(row[0])

    if is_dept_in_lang(c, dept):

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_xlang WHERE\
                Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results4 = c.execute(query, data)

        for row in results4:
            hours.append(row[1])
            course_nums.append(row[0])


    return course_nums, hours


def make_dept_plot(dept):
    '''
    Given a department, this function makes a bar chart of the 
    average hours spent per week for each class in that department
    by calling the get_all_hours function. 
    '''

    course_nums, hours = get_all_hours(dept)


    N = len(course_nums)

    ind = np.arange(N)
    width = 1.0

    fig, ax = plt.subplots()
    rects = ax.bar(ind, hours, width, color='b')

    ax.set_ylabel('Average Hours Spent Per Class')
    ax.set_title('Average Hours Spent in Each Class in the\
                '+dept+' Department')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(course_nums, rotation=45)

    plt.show()



def plot_all_depts():
    '''
    This function plots the average hours worked per week for each
    department
    '''

    conn = sqlite3.connect("../Databases/eval.db")
    c = conn.cursor()

    dept_hour_dict = {}

    tables = ["e_xTA", "e_oTA", "e_lang", "e_bio"]

    for table in tables:

        query = "SELECT Dept, AVG(MedHrs), SUM(NumResponses) FROM\
                    "+table+" GROUP BY Dept"
        results = c.execute(query)

        for dept, hour, responses in results:
            if dept not in dept_hour_dict:
                dept_hour_dict[dept] = [hour, responses]
            else:
                total_responses = dept_hour_dict[dept][1] + responses
                dept_hour_dict[dept][0] = (dept_hour_dict[dept][1] 
                                            * dept_hour_dict[dept][0] + hour 
                                            * responses) / total_responses
                dept_hour_dict[dept][1] = total_responses


    initial_list = dept_hour_dict.items()

    departments = [value[0] for value in initial_list]
    hours = [value[1][0] for value in initial_list]

    N = len(departments)

    ind = np.arange(N)
    width = 1.0

    fig, ax = plt.subplots()
    rects = ax.bar(ind, hours, width, color='b')

    ax.set_ylabel('Average Hours Spent Per Department')
    ax.set_title('Average Hours Spent in Each Department')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(departments, rotation=45)

    plt.show()



def plot_hours_over_time(dept, coursenum):
    '''
    Given a course (specified by the course number in a certain
    department), this function plots the average, max, and min 
    hours spent per week over the past few years. 
    '''

    conn = sqlite3.connect("../Databases/eval.db")
    c = conn.cursor()

    min_hours = []
    max_hours = []
    med_hours = []
    dates = []
    x_values = []


    if is_dept_in_ex(c, dept):
        query = "SELECT CourseSection, MinHrs, MedHrs, MaxHrs FROM\
                e_xTA WHERE Dept = ? AND CourseNum = ?;"


    if is_dept_in_eo(c, dept):
        query = "SELECT CourseSection, MinHrs, MedHrs, MaxHrs FROM\
                e_oTA WHERE Dept = ? AND CourseNum = ?;"


    if is_dept_in_bio(c, dept):
        query = "SELECT CourseSection, MinHrs, MedHrs, MaxHrs FROM\
                e_bio WHERE Dept = ? AND CourseNum = ?;"


    if is_dept_in_lang(c, dept):
        query = "SELECT CourseSection, MinHrs, MedHrs, MaxHrs FROM\
                e_lang WHERE Dept = ? AND CourseNum = ?;"
    
    data = (dept, coursenum)

    results = c.execute(query, data).fetchall()


    for info, min_hrs, med_hrs, max_hrs in results:
        year = str(info[-4:])
        quarter = info[-11:][:-5]

        date = quarter+", "+year


        min_hours.append(min_hrs)
        max_hours.append(max_hrs)
        med_hours.append(med_hrs)
        dates.append(date)
        x_values.append(assign_x_values_to_dates(date))


    fig, ax = plt.subplots()

    ax.scatter(x_values, med_hours, color='r')
    ax.scatter(x_values, min_hours, color='b')
    ax.scatter(x_values, max_hours, color='g')

    ax.get_xaxis().set_ticks([])
    ax.set_xlabel("2011 through 2016")
    ax.set_ylabel("Max, Min, and Average Hours Spent Per Week")
    ax.set_title("Hours Spent Per Week over Time")

    plt.show()
