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


#make_dept_plot("BIOS")


def is_dept_in_ex(dept):

    conn = sqlite3.connect("../jae/eval.db")
    c = conn.cursor()

    depts_in_ex = c.execute("SELECT DISTINCT Dept FROM e_xTA;").fetchall()
    depts_in_ex = [entry[0] for entry in depts_in_ex]

    if dept in depts_in_ex:
        return True

    else:
        return False



def is_dept_in_eo(dept):

    conn = sqlite3.connect("../jae/eval.db")
    c = conn.cursor()

    depts_in_eo = c.execute("SELECT DISTINCT Dept FROM e_oTA;").fetchall()
    depts_in_eo = [entry[0] for entry in depts_in_eo]

    if dept in depts_in_eo:
        return True
    else:
        return False


def os_dept_in_bio(dept):

    conn = sqlite3.connect("../jae/eval.db")
    c = conn.cursor()

    depts_in_bio = c.execute("SELECT DISTINCT Dept FROM e_bio;").fetchall()
    depts_in_bio = [entry[0] for entry in depts_in_bio]

    if dept in depts_in_bio:
        return True
    else:
        return False


def is_dept_in_lang(dept):

    conn = sqlite3.connect("../jae/eval.db")
    c = conn.cursor()

    depts_in_lang = c.execute("SELECT DISTINCT Dept FROM e_lang;").fetchall()
    depts_in_lang = [entry[0] for entry in depts_in_lang]

    if dept in depts_in_lang:
        return True
    else:
        return False






# PLOT AVERAGE HOURS SPENT FOR EACH DEPARTMENT


def plot_all_depts():

    conn = sqlite3.connect("../jae/eval.db")
    c = conn.cursor()

    dept_hour_dict = {}

    tables = ["e_xTA", "e_oTA", "e_lang", "e_bio"]

    for table in tables:

        query = "SELECT Dept, AVG(MedHrs), SUM(NumResponses) FROM "+table+" GROUP BY Dept"
        results = c.execute(query)

        for dept, hour, responses in results:
            if dept not in dept_hour_dict:
                dept_hour_dict[dept] = [hour, responses]
            else:
                total_responses = dept_hour_dict[dept][1] + responses
                dept_hour_dict[dept][0] = (dept_hour_dict[dept][1] * dept_hour_dict[dept][0] +
                                            hour * responses) / total_responses
                dept_hour_dict[dept][1] = total_responses


    initial_list = dept_hour_dict.items()

    departments = [value[0] for value in initial_list]
    print(departments)
    hours = [value[1][0] for value in initial_list]
    print(hours)



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

plot_all_depts()