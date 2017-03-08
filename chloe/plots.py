import sqlite3
import matplotlib.pyplot as plt
import numpy as np



# GIVEN A DEPARTMENT, MAKE A BAR CHART OF THE AVERAGE HOURS SPENT PER WEEK 
# FOR EACH CLASS IN THAT DEPARTMENT

def get_all_hours(dept):

    conn = sqlite3.connect("../jae/eval.db")
    c = conn.cursor()

    hours = []
    course_nums = []

    depts_in_ex = c.execute("SELECT DISTINCT Dept FROM e_xTA;").fetchall()
    depts_in_ex = [entry[0] for entry in depts_in_ex]

    depts_in_eo = c.execute("SELECT DISTINCT Dept FROM e_oTA;").fetchall()
    depts_in_e0 = [entry[0] for entry in depts_in_eo]

    depts_in_bio = c.execute("SELECT DISTINCT Dept FROM e_bio;").fetchall()
    depts_in_bio = [entry[0] for entry in depts_in_bio]

    depts_in_lang = c.execute("SELECT DISTINCT Dept FROM e_lang;").fetchall()
    depts_in_lang = [entry[0] for entry in depts_in_lang]


    if dept in depts_in_ex:

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_xTA WHERE Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results1 = c.execute(query, data)

        for row in results1:
            hours.append(row[1])
            course_nums.append(row[0])

    if dept in depts_in_eo:

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_oTA WHERE Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results2 = c.execute(query, data)

        for row in results2:
            hours.append(row[1])
            course_nums.append(row[0])

    if dept in depts_in_bio:

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_bio WHERE Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results3 = c.execute(query, data)

        for row in results3:
            hours.append(row[1])
            course_nums.append(row[0])

    if dept in depts_in_lang:

        query = "SELECT CourseNum, AVG(MedHrs) FROM e_xlang WHERE Dept = ? GROUP BY CourseNum"
        data = (dept,)

        results4 = c.execute(query, data)

        for row in results4:
            hours.append(row[1])
            course_nums.append(row[0])


    return course_nums, hours


def make_dept_plot(dept):

    course_nums, hours = get_all_hours(dept)


    N = len(course_nums)

    ind = np.arange(N)
    width = 1.0

    fig, ax = plt.subplots()
    rects = ax.bar(ind, hours, width, color='b')

    ax.set_ylabel('Average Hours Spent Per Class')
    ax.set_title('Average Hours Spent in Each Class in the '+dept+' Department')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(course_nums, rotation=45)

    plt.show()


make_dept_plot("BIOS")



# PLOT AVERAGE HOURS SPENT FOR EACH DEPARTMENT


def plot_all_depts():

    conn = sqlite3.connect("../jae/eval.db")
    c = conn.cursor()

    dept_hour_dict = {}

    query1 = "SELECT Dept, AVG(MedHrs), SUM(NumResponses) FROM e_xTA GROUP BY Dept"
    results1 = c.execute(query1)

    for dept, hour, responses in results1:
        if dept not in dept_hour_dict:
            dept_hour_dict["dept"] = [hour, responses]
        else:
            dept_hour_dict["dept"] = 
        

    query2 = "SELECT Dept, AVG(MedHrs), SUM(NumResponses) FROM e_oTA GROUP BY Dept"
    results2 = c.execute(query2)

    query3 = "SELECT Dept, AVG(MedHrs), SUM(NumResponses) FROM e_bio GROUP BY Dept"
    results3 = c.execute(query3)

    query4 = "SELECT Dept, AVG(MedHrs), SUM(NumResponses) FROM e_lang GROUP BY Dept"
    results4 = c.execute(query4)