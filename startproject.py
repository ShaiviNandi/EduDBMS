# # This is the main file that produces the user interface menu with multiple input options and controls program flow
# Author: Shaivi Nandi, Class 12 A, Meridian School Madhapur
# Copyright: All rights reserved

import io
import math
import re
import os
import time
import mysql.connector
# import mysql.connector.errors
import projectfunctions

# define constants and variables
# When 10 is entered, program quites
ExitMenuIndexConstant = 10
# Initializes a constant to 1 to keep the system in the while loop below
LoopEntryConstant = 1
# Constant that stores how long in seconds the system waits after displaying key messages
waitbeforeclearscreen = 15
# Stores the choice of the user from the menu. Initialized to the LoopEntryConstant to start off the looping
choice = LoopEntryConstant
# Stores the number of records updated, deleted or inserted into a database table
recordsimpacted = 0

# Stores the handle to the mysql database instance that is used in the project. Connection is established connecttodb function.
activedb = projectfunctions.connecttodb()

#start looping and keep looping till exit choice == 10 is not selected by the user.
while choice != ExitMenuIndexConstant:
    #Error handling block starts
    try:
        #Call the shared function breaks the input string into menu items and displays the menu.This function is called repeatedly to navigate the various levels in the menu
        choice = projectfunctions.prepmenu('1. maintain student record#2. maintain faculty record#3. maintain courses#4. maintain cohort')
        if choice == 1:
            # maintain student record
            choice = projectfunctions.prepmenu('1. register new student#2. delete student record#3. update student record#4. search student record')
            if choice == 1:
                # collect all student details to register new student
                studentfirstname = "'" + input("First name: ") + "'"
                studentsurname = "'" + input("Sur name: ") +"'"
                studentmiddlename = "'" + input("Middle name: ") + "'"
                studentisactive = 1
                studentdob = "'" + input("Date of Birth (YYYY-MM-DD): ") + "'"
                studentaddress = "'" + input("Address: ") + "'"
                studentphone1 = input("Phone: ")
                studentphone2 = input("Alt Phone: ")
                studentgender = "'" + input("Gender M/F/O: ") + "'"
                # call the function that updates the database and returns the number of records
                recordsimpacted = projectfunctions.registerstudent(activedb,studentfirstname, studentsurname, studentmiddlename, studentisactive, studentdob, studentaddress, studentphone1, studentphone2,  studentgender)
                # call the function that prints a message with number of records updated and waits for the time defined by the waitbeforeclearscreen constant.
                projectfunctions.databaserecordupdatestatus(recordsimpacted,waitbeforeclearscreen)
            elif choice == 2:
                # delete a student record given by studentid
                studentid = int(input("\nPlease enter student id"))
                # call the function that deletes a student record
                recordsimpacted = projectfunctions.unregisterstudent(activedb,studentid)
                projectfunctions.databaserecordupdatestatus(recordsimpacted,waitbeforeclearscreen)
            elif choice == 4:
                # Search a student record. Display various mechanisms by which one can search eg id, phone number,first name, last name etc. Call the function that searches and displays student records.
                choice = projectfunctions.prepmenu('1. search by id#2. search by phone number#3. search by first name#4. search by last name')
                if choice == 1:
                    studentid = int(input("\nPlease enter student id"))
                    projectfunctions.searchanddisplayrecord(activedb,"studentid,studentfirstname,studentsurname,studentmiddlename,studentdob,studentaddress,studentphone1,studentphone2,studentgender","studentid",str(studentid))
                elif choice == 2:
                    studentphone1 = int(input("\nPlease enter phone number"))
                    projectfunctions.searchanddisplayrecord(activedb,"studentid,studentfirstname,studentsurname,studentmiddlename,studentdob,studentaddress,studentphone1,studentphone2,studentgender","studentphone1",str(studentphone1))
                elif choice == 3:
                    studentfirstname = str(input("\nPlease enter student first name"))
                    projectfunctions.searchanddisplayrecord(activedb,"studentid,studentfirstname,studentsurname,studentmiddlename,studentdob,studentaddress,studentphone1,studentphone2,studentgender","studentfirstname","'"+str(studentfirstname)+"'")
                elif choice == 4:
                    studentsurname = str(input("\nPlease enter student last name"))
                    projectfunctions.searchanddisplayrecord(activedb,"studentfirstname,studentsurname,studentmiddlename,studentdob,studentaddress,studentphone1,studentphone2,studentgender","studentsurname","'"+str(studentsurname)+"'")
            elif choice == 3:
                # update a student record ie first name, last name etc given by studentid
                choice = projectfunctions.prepmenu('1. update student first name#2. update student surname#3. update student middle name#4. update student DOB#5. update student phone#6. update student address')
                studentid = int(input("\nPlease enter student id"))
                if choice == 1:
                    studentfirstname =str(input("Please enter changed first name"))
                    # call the function that generates and SQL and updates the relevant column in the student record
                    recordsimpacted = projectfunctions.updaterecord(activedb,'studentfirstname',"'"+studentfirstname+"'",'studentid',studentid)
                elif choice == 2:
                    studentfirstname =str(input("Please enter changed surname"))
                    recordsimpacted = projectfunctions.updaterecord(activedb,'studentsurname',"'"+studentsurname+"'",'studentid',studentid)
                elif choice == 3:
                    studentmiddlename =str(input("Please enter changed middlename"))
                    recordsimpacted = projectfunctions.updaterecord(activedb,'studentmiddlename',"'"+studentmiddlename+"'",'studentid',studentid)
                elif choice == 4:
                    studentdob =str(input("Please enter changed Date Of Birth(YYYY-MM-DD)"))
                    recordsimpacted = projectfunctions.updaterecord(activedb,'studentdob',"'"+str(studentdob)+"'",'studentid',studentid)
                elif choice == 5:
                    studentphone1 =str(input("Please enter changed phone"))
                    recordsimpacted = projectfunctions.updaterecord(activedb,'studentphone1',str(studentphone1),'studentid',studentid)
                elif choice == 6:
                    studentaddress =str(input("Please enter changed address"))
                    recordsimpacted = projectfunctions.updaterecord(activedb,'studentaddress',"'"+str(studentaddress)+"'",'studentid',studentid)
                if choice == 1 or choice ==2 or choice ==3 or choice ==4 or choice ==5 or choice ==6 : projectfunctions.databaserecordupdatestatus(recordsimpacted,waitbeforeclearscreen)
        elif choice == 2:
            # maintain i.e. Add or Delete a faculty record by leveraging similar functions that build menus and updates the database
            choice = projectfunctions.prepmenu('1. Add new faculty#2. Delete faculty record')
            if choice == 1:
                recordsimpacted = projectfunctions.addnewfaculty(activedb,"'"+ input("faculty full name") + "'")
            elif choice == 2:
                recordsimpacted = projectfunctions.deletefaculty(activedb,input("faculty id"))
            if choice == 1 or choice ==2: projectfunctions.databaserecordupdatestatus(recordsimpacted,waitbeforeclearscreen)
        elif choice == 3:
            # maintain i.e. Add or update a course record by leveraging similar functions that build menus and updates the database
            choice = projectfunctions.prepmenu('1. Add new course#2. Update course details')
            if choice == 1:
                recordsimpacted = projectfunctions.addnewcourse(activedb,"'"+ str(input("course short code"))+"'","'" + str(input("course description"))+"'",str(input("course duration in days")),str(input("course fees")),"'"+str(input("any course prerequisites"))+"'")
            elif choice == 2:
                choice = projectfunctions.prepmenu('1. update course description#2. update course duration#3. update course fees#4. update course prerequisites')
                courseid = "'" + input("Enter course code:") + "'"
                if choice == 1: recordsimpacted=projectfunctions.updatecourse(activedb,courseid,'coursedescription',"'"+input("input new course description: ")+"'")
                elif choice == 2: recordsimpacted=projectfunctions.updatecourse(activedb,courseid,'coursedurationdays',str(input("input new course duration: ")))
                elif choice == 3: recordsimpacted=projectfunctions.updatecourse(activedb,courseid,'coursefees',str(input("input new course fees: ")))
                elif choice == 4: recordsimpacted=projectfunctions.updatecourse(activedb,courseid,'Prerequisites',"'"+input("input new course prerequisites: ")+"'")
            if choice == 1 or choice == 2 or choice ==3 or choice == 4:
                projectfunctions.databaserecordupdatestatus(recordsimpacted, waitbeforeclearscreen)
        elif choice == 4:
            #Maintain cohort or batch
            choice = projectfunctions.prepmenu('1. assign student to cohort#2. search cohorts available#3. start new cohort#4. mark cohort complete')
            if choice == 1:
                # Assign a student to a particular batch
                studentid = input("Please enter student id")
                cohortid = input("Please enter cohort id (batch id)")
                recordsimpacted = projectfunctions.assignstudentcohort(activedb,studentid,cohortid)
                projectfunctions.databaserecordupdatestatus(recordsimpacted,waitbeforeclearscreen)
            elif choice == 2:
                # Search and display all active cohorts for a particular course
                courseid = "'" + str(input("Please enter course id")) + "'"
                projectfunctions.searchanddisplayavailablecohorts(activedb,courseid)
            elif choice == 3:
                # Start a new batch or a cohort for a particular course
                cohortcourseid = "'" + input("Course Id: ") + "'"
                cohortstartdate = "'" + input("Cohort/Batch start date (YYYY-MM-DD): ") + "'"
                cohortenddate = "'" + input("Cohort/Batch end date (YYYY-MM-DD): ") + "'"
                cohortisactive = 1
                cohortfacultyid = input("Faculty assigned to the cohort/batch ")
                cohortclassstarttime = "'" + input("Cohort/Batch start time ('24'HH:MM:SS): ") + "'"
                cohortclassduration = input("Class duration in hours")
                cohortismondayclass = input("is class held on monday; Enter 1- Yes, 0 - No")
                cohortistuesdayclass = input("is class held on tuesday; Enter 1- Yes, 0 - No")
                cohortiswednesdayclass = input("is class held on wednesday; Enter 1- Yes, 0 - No")
                cohortisthursdayclass = input("is class held on thursday; Enter 1- Yes, 0 - No")
                cohortisfridayclass = input("is class held on friday; Enter 1- Yes, 0 - No")
                cohortissaturdayclass = input("is class held on saturday; Enter 1- Yes, 0 - No")
                cohortissundayclass = input("is class held on sunday; Enter 1- Yes, 0 - No")
                recordsimpacted = projectfunctions.registercohort(activedb,cohortcourseid,cohortstartdate,cohortenddate, cohortisactive,cohortfacultyid,
                                                              cohortclassstarttime,cohortclassduration,cohortismondayclass,cohortistuesdayclass,
                                                              cohortiswednesdayclass,cohortisthursdayclass, cohortisfridayclass,cohortissaturdayclass,
                                                              cohortissundayclass)
                projectfunctions.databaserecordupdatestatus(recordsimpacted,waitbeforeclearscreen)
            elif choice == 4:
                #inactivate a completed cohort by setting its isactive column to 0 so tha it no longer turns up in search results
                cohortid = input("Cohort Id to set as inactive: ")
                recordsimpacted = projectfunctions.inactivatecohort(activedb,cohortid)
                projectfunctions.databaserecordupdatestatus(recordsimpacted,waitbeforeclearscreen)
        #reset the choice to 1 so that the main menu is displayed and the while iterates except when choice == 10 i.e. user wants to exit program
        if choice != ExitMenuIndexConstant:
            choice = LoopEntryConstant
    #Handle errors gracefully by catching and dealing with exceptions related to wrong/invalid user input
    except TypeError:
        print("Incompatible data provided, please reenter data")
        time.sleep(waitbeforeclearscreen)
    except mysql.connector.errors.ProgrammingError:
        print("Incompatible data provided, please reenter data")
        time.sleep(waitbeforeclearscreen)
    except mysql.connector.errors.IntegrityError:
        print("You tried to delete or update data that is referenced by other entities.\n This is not allowed.Please Update/Delete the child records first")
        time.sleep(waitbeforeclearscreen)
    except mysql.connector.errors.DataError:
        print("Incompatible data provided, please reenter data")
        time.sleep(waitbeforeclearscreen)





