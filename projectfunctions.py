# This file contains all the functions used in the computer coaching center management system
# Author: Shaivi Nandi, Class 12 A, Meridian School Madhapur
# Copyright: All rights reserved
import os
import io
import re
import time
import mysql

def prepmenu(menutext):
  """
  function clears screen and prints the menu
  Args: menu text # delimited string that contains all the menu items to display
  returns: the index of the menu item chosen by the user
  """

  os.system('cls')
  print('\033[1m Welcome to Erudite Computer Institute \033[0m', sep='/n/n')
  print('\033[1m Please select from the following options \033[0m', sep='/n/n')
  print('_' * 100)
  # Accept the menu items as a string and break it using regex functions and return the formatted string
  lst = re.split('#',menutext)
  lst.append("10. exit")
  for i in range(0,len(lst)):
    print(lst[i])
  print('_' * 100, sep='/n')
  choice = int(input('Please make a selection\n'))
  return choice


def buildSQL(statement, table, columns, values, condition,displaycolumns,updatecondition=''):
  """
  Builds an SQL statement based on the given parameters.

  Args:
    statement: The type of SQL statement to build.
    table: The name of the table to operate on.
    columns: A list of column names to insert or update
    values: A list of values to insert or update.
    condition: A condition for the SQL statement eg =, > etc
    displaycolumns - columns to display in a select clause or use in the where clause for updates
    updatecondition - The new values to be updated in an update statement

  Returns:
    The SQL statement.
  """

  sql = ""
  if statement == "INSERT":
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table, "".join(columns), "".join(values))
  elif statement == "UPDATE":
    sql = "UPDATE {} SET {}={} WHERE {}{}{}".format(table,columns,values,displaycolumns,condition,updatecondition)
  elif statement == "DELETE":
    sql = "DELETE FROM {} WHERE {}{}{}".format(table,columns,condition,values)
  elif statement == "SELECT":
    sql = "SELECT {} from {} WHERE".format(displaycolumns,table) + " {}{}{}".format(columns,condition,values)
  else:
    raise ValueError("Invalid statement type: {}".format(statement))

  return sql


def connecttodb():
  """
  establishes a database connection and returns the handle to the database object
  """
  mydb = mysql.connector.connect(
    host="localhost",
    user="appuser",
    password="appuser",
    database="computerinstitute"
  )
  return mydb

def returncursor(mydb):
  """
  Opens and returns a cursor object
  Args:
    mydb - The database object on which the cursor needs to be opened
  Returns:
    cursor - Returns cursor object
  """
  mycursor = mydb.cursor()
  return mycursor



def registerstudent(mydb,studentfirstname,studentsurname,studentmiddlename,studentisactive,studentdob,studentaddress, studentphone1,studentphone2,studentgender):
  """
  function builds and executes an insert into the student table in the connected data base
  Args:
    mydb - is the handle to the database object
    rest of the args are strings received with student particulars as input by the user
  Return:
    number of records impacted
  """
  mycursor = returncursor(mydb)
  querystring = buildSQL('INSERT','student','studentfirstname,studentsurname,studentmiddlename,studentisactive,studentdob,studentaddress, studentphone1,studentphone2,studentgender',
                         "{},{},{},{},{},{},{},{},{}".format(studentfirstname,studentsurname,studentmiddlename,studentisactive,studentdob,studentaddress, studentphone1,studentphone2,studentgender),'','','')
  #print (querystring)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def registercohort(mydb,cohortcourseid,cohortstartdate,cohortenddate, cohortisactive,cohortfacultyid,
                cohortclassstarttime,cohortclassduration,cohortismondayclass,cohortistuesdayclass,
                cohortiswednesdayclass,cohortisthursdayclass, cohortisfridayclass,cohortissaturdayclass,
                cohortissundayclass):
  """
  Inserts a new cohort for a particular course
  Args:
    activedb - active database connection handle
    cohortcourseid- course id
    cohortstartdate- start date
    cohortenddate - end date
    cohortisactive = 1 as this record is active
    cohortfacultyid - faculty id
    cohortclassstarttime - HH:MM:SS when class starts
    cohortclassduration - how long a class lasts
    rest of the args capture whether class is held on a particular day of week using 1 for yes and 0 for no
  Return:
    number of records impacted
  """
  mycursor = returncursor(mydb)
  querystring = buildSQL('INSERT','cohort','cohortcourseid,cohortstartdate,cohortenddate, cohortisactive,cohortfacultyid,cohortclassstarttime,' +
                                           'cohortclassduration,cohortismondayclass,cohortistuesdayclass,cohortiswednesdayclass,cohortisthursdayclass,' +
                                           'cohortisfridayclass,cohortissaturdayclass,cohortissundayclass',
                         "{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(cohortcourseid,cohortstartdate,cohortenddate, cohortisactive,cohortfacultyid,
                                                             cohortclassstarttime,cohortclassduration,cohortismondayclass,cohortistuesdayclass,
                                                             cohortiswednesdayclass,cohortisthursdayclass, cohortisfridayclass,cohortissaturdayclass,
                                                             cohortissundayclass),'','','')
  #print (querystring)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount



def unregisterstudent(mydb,studentid):
  """
  function deletes a student record from the data base
  Args:
    mydb - is the handle to the database object
    studentid - unique id for each student registered in the system
  Return:
    number of records impacted
  """
  mycursor = returncursor(mydb)
  querystring = buildSQL('DELETE','student','studentid',studentid,'=','','')
  print (querystring)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def searchanddisplayrecord(mydb,columnstodisplay,searchcolumn,values):
  """
  searches and displays records based on a search criteria
  Args:
    mydb - handle to the database object
    columnstodisplay - columns to be displayed in search results
    searchcolumn - column on which query is issued
    values - value of the search column

  return:
    none
  """
  mycursor = returncursor(mydb)
  querystring = buildSQL('SELECT','student',searchcolumn,values,"=",columnstodisplay,'')
  mycursor.execute(querystring)
  #print(querystring)
  mysequence = mycursor.column_names
  #iterate on the cursor that returns a tuples containing the query results and a sequence containing the column names and display results on screen
  for thistuple in mycursor.fetchall():
    for i in range(0,len(thistuple)):
      print(str(mysequence[i])+" : " + str(thistuple[i]))
    print("-" * 100)
  try:
    input("press any key to continue ..")
  except SyntaxError:
    pass

def updaterecord(mydb,columnstoupdate,updatevalue,searchcolumn,searchvalues):
  """
  updates a database record based on a search criteria
  Args
    mydb- handle to the database object
    columnstoupdate  - column to update
    updatevalue - new value the column takes
    searchcolumn - column that determines which record to update
    searchvalues - the value of the search values
  return
    number of records impacted
  """
  querystring = buildSQL('UPDATE','student',columnstoupdate,updatevalue,'=',searchcolumn,searchvalues)
  mycursor = returncursor(mydb)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def assignstudentcohort(mydb,studentid,cohortid):
  """
  Assigns students to a batch for a particular course
  Args:
  studentid - unique student id
  cohortid - unique batch id
  return:
  number of records updated
  """
  querystring = buildSQL('INSERT','studentcohort','studentid,cohortid',str(studentid)+","+str(cohortid),'=','','')
  mycursor = returncursor(mydb)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def searchanddisplayavailablecohorts(mydb, courseid):
  """
  Displays available cohorts or batches for a given course
  Args:
  courseid - unique id for the course
  return:
  nothing
  """
  mycursor = returncursor(mydb)
  querystring = buildSQL('SELECT','coursecohort','courseid',str(courseid),"=",' * ','')
  mycursor.execute(querystring)
  mysequence = mycursor.column_names
  #iterate on the cursor that returns a tuples containing the query results and a sequence containing the column names and display results on screen
  #print(querystring)
  for thistuple in mycursor.fetchall():
    for i in range(0,len(thistuple)):
      print(str(mysequence[i])+" : " + str(thistuple[i]))
    print("-" * 100)
  try:
    input("press any key to continue ..")
  except SyntaxError:
    pass

def databaserecordupdatestatus(recordsimpacted,waitdelay):
  """
  Function prints the record update status for any database function
  Args:
  recordsimpacted - integer indicating the number of records updated
  waitdelay - how long the printed message is displayed before screen is cleaned
  return - has no return value
  """
  if int(recordsimpacted) > 0:
    print(str(recordsimpacted) + " record(s) updated successfully !!")
  else:
    print("database operation failed. please recheck input values")
  time.sleep(waitdelay)

def inactivatecohort(mydb,cohortid):
  """
  Function sets a particular cohort to inactive or 0
  Args:
  cohortid - unique id for the cohort
  mydb - handle to the database object
  return:
  records impacted
  """
  querystring = buildSQL('UPDATE','cohort','cohortisactive',0,'=','cohortid',cohortid)
  mycursor = returncursor(mydb)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def addnewfaculty(mydb,facultyname):
  """
  Function adds a new faculty record
  Args:
  facultyname - unique id for the cohort
  mydb - handle to the database object
  return:
  records impacted
  """
  querystring = buildSQL('INSERT','faculty','facultyname',facultyname,'=','','')
  mycursor = returncursor(mydb)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def deletefaculty(mydb,facultyid):
  """
  Function sets a particular cohort to inactive or 0
  Args:
  facultyid - unique id for the faculty
  mydb - handle to the database object
  return:
  records impacted
  """
  mycursor = returncursor(mydb)
  querystring = buildSQL('DELETE','faculty','facultyid',facultyid,'=','','')
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def addnewcourse(mydb,courseid,coursedescription,coursdurationdays,coursefees,prerequisites):
  """
  Function adds a new course
  Args:
  courseid - unique id for the course
  coursedescription: brief details of the course
  coursdurationdays: no. of days the course takes place over
  coursefees:cost of course to student
  prerequisites: any prior qualifications required to participate
  mydb - handle to the database object
  return:
  records impacted
  """
  querystring = buildSQL('INSERT','course','courseid,coursedescription,coursedurationdays,coursefees,prerequisites',"{},{},{},{},{}".format(courseid,coursedescription,coursdurationdays,coursefees,prerequisites),'=','','')
  mycursor = returncursor(mydb)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount

def updatecourse(mydb,courseid,columntoupdate,columnvalue):
  """
  Function updates existing course with fresh details
  Args:
  courseid- unique id for course
  columntoupdate- detail that has been changed
  columnvalue- value of detail that has been changed
  mydb - handle to the database object
  return:
  records impacted
  """
  querystring = buildSQL('UPDATE','course',columntoupdate,columnvalue,'=','courseid',courseid)
  mycursor = returncursor(mydb)
  mycursor.execute(querystring)
  mydb.commit()
  return mycursor.rowcount