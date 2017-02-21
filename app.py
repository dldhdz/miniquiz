import os
from flask import Flask, session, render_template, url_for, redirect, request, flash
from copy import deepcopy
from datetime import datetime, date, time
from random import choice, shuffle
# Create a flask app and set its secret key
app = Flask(__name__)
app.secret_key = os.urandom(24)
#
questions = {
'1': {'tip': 'func_name does not work for built-in functions', 'answer': 'theFunction.__name__', 'question': 'Which of the following is the correct way to output the name of any function (including builtin functions) using Python?', 'options': ['theFunction.__func_name__', 'theFunction.func_name', 'theFunction.__name__', 'theFunction.name()']}, '4': {'tip': 'a[start:end] slicing means items start through end-1', 'answer': 'thelist[3:]', 'question': "For the list 'thelist = [1, 2, 3, 4, 5]', how could the last two elements of the list (4,5) be selected using slices?", 'options': ['thelist[3:]', 'thelist[-2]', 'thelist[3:4]', 'thelist[3,4]']}, '2': {'tip': 'to simply amend your path, sys.path.append can be used', 'answer': 'Put __init__.py file in the module path and import it using the import statement', 'question': 'Which option will import a module which is not in PYTHONPATH or the current directory?', 'options': ['Put __init__.py file in the module path and import it using the import statement', 'import <modulename>', 'Add the path in program by sys.path.insert(<path>)', '<modulename> import *']}, '6': {'tip': 'a[start:end] slicing means items start through end-1', 'answer': 'installtools', 'question': 'Which is not used to install Python packages?', 'options': ['installtools', 'easy_install', 'distribute', 'pip']}, '5': {'tip': 'a[start:end] slicing means items start through end-1', 'answer': "Do not bind to a specific port, or bind to port 0, e.g. sock.bind(('',0))", 'question': 'Which is correct about getting a free port number?', 'options': ["Do not bind to a specific port, or bind to port 0, e.g. sock.bind(('',0))", 'use sock.getsockname() to get a free port number', 'We cannot get a free port number', "Directly use a desired port number in bind function,e.g. sock.bind(('',port_number))"]}, '3': {'tip': 'raw_input() does not exist in Python 3.x, it has been renamed to input(), and the old input() is gone', 'answer': 'sys.stdin', 'question': 'Which user input method will act like a file-object on which read and readline function can be callled', 'options': ['input()', 'sys.argv', 'sys.stdin', 'raw_input()']}, '7': {'tip': 'a[start:end] slicing means items start through end-1', 'answer': '__floordiv__()', 'question': 'Which function overloads the // operator?', 'options': ['__truediv__()', '__radd__', '__floordiv__()', '__ceildiv__()']}
}
#
py_summary={}
py_summary["correct"]=[]
py_summary["wrong"]=[]
py_summary["curretq"]=1
#
app.nquestions=len(questions)
#
# options to the questions can be shuffled
#
# for item in questions.keys():
   # shuffle(questions[item]['options'])   
#
#
# Route for the URL /python accepting GET and POST methods
# We are using session variables to keep track of the current question
# the user is in and show him just that question even if he reloads the page
# or opens the page in a new tab.
@app.route('/python', methods=['GET', 'POST'])
def index():
#	
  if request.method == "POST":
    
    # The data has been submitted via POST request.
    #
    entered_answer = request.form.get('answer_python', '')
#   
    if not entered_answer:
      flash("Please choose an answer", "error") # Show error if no answer entered
    
    else:

      curr_answer=request.form['answer_python']
      correct_answer=questions[session["current_question"]]["answer"]
# 
      if curr_answer == correct_answer[:len(curr_answer)]: 
        py_summary["correct"].append(int(session["current_question"]))
#      
      else:
        py_summary["wrong"].append(int(session["current_question"]))
#		
      # set the current question to the next number when checked
      session["current_question"] = str(int(session["current_question"])+1)
      py_summary["curretq"]= max(int(session["current_question"]), py_summary["curretq"])	  
#   
      if session["current_question"] in questions:
        # If the question exists in the dictionary, redirect to the question
        #
        redirect(url_for('index'))
      
      else:
        # else redirect to the summary template as the quiz is complete.
        py_summary["wrong"]=list(set(py_summary["wrong"]))
        py_summary["correct"]=list(set(py_summary["correct"]))		
        return render_template("end_miniquiz.html",summary=py_summary)
#  
  if "current_question" not in session:
    # The first time the page is loaded, the current question is not set.
    # This means that the user has not started to quiz yet. So set the 
    # current question to question 1 and save it in the session.
    session["current_question"] = "1"
#  
  elif session["current_question"] not in questions:
    # If the current question number is not available in the questions
    # dictionary, it means that the user has completed the quiz. So show
    # the summary page.
    py_summary["wrong"]=list(set(py_summary["wrong"]))
    py_summary["correct"]=list(set(py_summary["correct"]))	
    return render_template("end_miniquiz.html",summary=py_summary)
  
  # If the request is a GET request 
  currentN=int(session["current_question"])   
  currentQ =  questions[session["current_question"]]["question"]
  a1, a2, a3,a4 = questions[session["current_question"]]["options"] 
  # 
  return render_template('python_miniquiz.html',num=currentN,ntot=app.nquestions,question=currentQ,ans1=a1,ans2=a2,ans3=a3,ans4=a4)   
#
@app.route('/checkform_python',methods=['GET','POST'])
def check_answer():
    the_color1='Black';the_color2='Black';the_color3='Black';	
    the_color4='Black';the_color6='Black';
    the_check1='';the_check2='';the_check3='';the_check4='';
#
#    session["current_question"]=str(py_summary["curretq"])
    if "current_question" not in session:
        session["current_question"] = "1"		
    #
#	
    currentN = int(session["current_question"])   
    currentQ = questions[session["current_question"]]["question"]
    a1, a2, a3, a4 = questions[session["current_question"]]["options"] 
#
#
    curr_answer=request.form['answer_python']
    correct_answer=questions[session["current_question"]]["answer"]
    tip=questions[session["current_question"]]["tip"]
# track quiz check history
    f = open('mini_log.txt','a') #a is for append
    f.write('%s\n'%(datetime.now().strftime("%A, %d. %B %Y %I:%M%p")))		
    f.write('Current number: %s, '%(currentN))			
    f.write('Current question: %s\n'%(currentQ))	
    f.write('Correct answer: %s\n'%(correct_answer))
    f.write('Current selection: %s\n'%(curr_answer))	#	
    f.close()
#
    if curr_answer == correct_answer[:len(curr_answer)]: the_color6="Green"
    if curr_answer in a1[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color1="Green"
            the_check1=' - correct'
        else: 
            the_color1="Red"		
            the_check1=' - incorrect'		
#
    if curr_answer in a2[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color2="Green"
            the_check2='- correct'
        else: 
            the_color2="Red"			
            the_check2=' - incorrect'
#
    if curr_answer in a3[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color3="Green"
            the_check3=' - correct'
        else: 
            the_color3="Red"			
            the_check3=' - incorrect'
#			
    if curr_answer in a4[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color4="Green"
            the_check4=' - correct'
        else: 
            the_color4="Red"			
            the_check4=' - incorrect'
#
		
    return render_template('python_answer.html',num=currentN,ntot=app.nquestions,descript=tip,anscheck1=the_check1,anscheck2=the_check2,anscheck3=the_check3,anscheck4=the_check4,ans_color1=the_color1,ans_color2=the_color2,ans_color3=the_color3,ans_color4=the_color4,ans_color6=the_color6,question=currentQ,ans1=a1,ans2=a2,ans3=a3,ans4=a4)
# Runs the app using the web server on port 80, the standard HTTP port
if __name__ == '__main__':
	app.run( 
        # host="0.0.0.0",
        # port=33507

  )
