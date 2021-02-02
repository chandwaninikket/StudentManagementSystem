from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import requests
import sqlite3
import bs4
import os.path
import matplotlib.pyplot as plt

#addstudent
def f1():
	root.withdraw()
	add_st.deiconify()

#backonaddwindow
def f2(): 
	add_st.withdraw()
	root.deiconify()

#viewbutton
def f3(): 
	root.withdraw()
	view_st.deiconify()
	view_st_data.delete(1.0,END)
	con=None
	try:
		con=connect("student.db")
		sql="select * from student"
		cursor = con.cursor()
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info+"rno"+str(d[0]) + " name " + str(d[1]) + " marks " + str(d[2]) +"\n"
		view_st_data.insert(INSERT,info)
	except Exception as e:
		msg="Error opening the records, error : " + e
		showerror("issue",msg)
	finally:
		if con is not None:
			con.close()
#backonview
def f4(): 
	view_st.withdraw()
	root.deiconify()

#addbuttononaddwindow
def f5():
	flag=0
	try:
		rno=int(add_st_entrno.get())
		marks=int(add_st_marks.get())
		name=add_st_entname.get()
		try:
			if 0<=marks<=100:
				pass
			else:
				raise Exception("Enter marks in a valid range")
		except Exception as e:
			showerror("Invalid Range", e)
			flag=1
	except ValueError as e:
		flag=1
		showerror("Invalid Value", "Please enter an Integer")
	if flag==0:
		con=None
		try:
			con=connect("student.db")
			sql="insert into student values('%d' , '%s' , '%d')"
			cursor=con.cursor()
			cursor.execute(sql % (rno,name,marks))
			con.commit()
			showinfo("Success", "record added")
		except Exception as e:
			showerror("Failure", e)
		finally:
			if con is not None:
				con.close()
#updbutton
def f6():
	root.withdraw()
	upd_st.deiconify()
def upd_save():
	flagu=0
	try:
		rno=int(upd_st_entrno.get())
		marks=int(upd_st_marks.get())
		name=upd_st_entname.get()
		try:
			if 0<=marks<=100:
				pass
			else:
				raise Exception("Enter marks in a valid range")
		except Exception as e:
			showerror("Invalid Range", e)
			flagu=1
	except ValueError as e:
		flagu=1
		showerror("Invalid Value", "Please enter an Integer")
	if flagu==0:
		con=None
		try:
			con=connect("student.db")
			sql="update student set name='%s', marks='%d' where rno=('%d')"
			cursor=con.cursor()
			cursor.execute(sql % (name,marks,rno))
			con.commit()
			showinfo("Success", "record updated")
		except Exception as e:
			showerror("Failure", e)
		finally:
			if con is not None:
				con.close()
def upd_back():
	upd_st.withdraw()
	root.deiconify()
#delbutton
def f7():
	root.withdraw()
	delete_st.deiconify()
def btnback_del(): #backondelwindow
	delete_st.withdraw()
	root.deiconify()
def deleterec():
	con = None
	try:
		con=connect("student.db")
		sql = "delete from student where rno='%d' "
		cursor=con.cursor()
		rno=int(delete_st_entrno.get())
		cursor.execute(sql % (rno))
		con.commit()
		if cursor.rowcount==1:
			con.commit()
			showinfo("Deletion Successful","record deleted")
		else:
			showerror("Deletion Unsuccessful","record doesn't exist")
	except Exception as e:
		msg="Issue in deleting with error: " + e
		showerror("Deletion Unsuccessful" , msg)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def qotd():
	web_add="https://brainyquote.com/quote_of_the_day"
	res=requests.get(web_add)
	data=bs4.BeautifulSoup(res.text,"html.parser")
	info=data.find('img',{"class":"p-qotd"})
	quote=info['alt']
	return quote
def loca():
	web_add = "https://ipinfo.io/"
	res=requests.get(web_add)
	data=res.json()
	locat=data['city']
	return locat
def tempe():
	a1="https://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q=" + loca()
	a3="&appid=c6e315d09197cec231495138183954bd"
	web_address=a1+a2+a3
	res=requests.get(web_address)
	data=res.json()
	temp=data['main']['temp']
	return temp
def charts_click():
	marks=[]
	names=[]
	try:
		con=connect("student.db")
		sql="select * from student"
		cursor = con.cursor()
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			marks.append(int(d[2]))
			names.append(str(d[1]))
	except Exception as e:
		msg="Error opening the records, error : " + e
		showerror("msg")
	finally:
		if con is not None:
			con.close()
	plt.bar(names,marks)
	plt.xlabel("Names")
	plt.ylabel("Marks")
	plt.title("Marks Distribution")
	plt.show()



#*******************************************************************************************************#
if os.path.exists("student.db"):
	pass
else:
	con = None
	con=connect("student.db")
	print("Connected")
	sql = "create table student(rno int primary key,name text,marks int)"
	cursor=con.cursor()
	cursor.execute(sql)
	print("table created ")

#main window
root = Tk()
root.resizable(False,False)
root.title( " S M S " )
root.geometry("1280x720+300+200")
lblqotd="QOTD: " + qotd()
lblloc="Location: " +loca()
lbltemp="Temperature: " +str(tempe())
#MAINWINDOW
btnAdd=Button(root, text="Add",width=10, font=('Segoe UI',20,'bold'),command=f1) #ADD
btnView=Button(root, text="View",width=10, font=('Segoe UI',20,'bold'),command=f3) #view
btnUpd=Button(root, text="Update",width=10, font=('Segoe UI',20,'bold'),command=f6) #update
btnDel=Button(root, text="Delete",width=10, font=('Segoe UI',20,'bold'),command=f7) #delete
btnCharts=Button(root, text="Charts",width=10, font=('Segoe UI',20,'bold'),command=charts_click) #Location
lblLocation=Label(root,text=lblloc,font=('Segoe UI',15,'bold'))
lblTemp=Label(root,text=lbltemp,font=('Segoe UI',15,'bold'))
lblQOTD=Label(root,text=lblqotd,font=('Segoe UI',10,'bold'))
btnAdd.pack(pady=15)
btnView.pack(pady=15)
btnUpd.pack(pady=15)
btnDel.pack(pady=15)
btnCharts.pack(pady=15)
lblLocation.pack(pady=20,padx=5,side=LEFT)
lblTemp.pack(pady=20,padx=5,side=RIGHT)
lblQOTD.pack(pady=30)

#*******************************************************************************************************#
#add window
add_st=Toplevel(root)
add_st.title("Add Student")
add_st.geometry("400x650+400+200")
add_st_lblrno=Label(add_st,text="enter rno",font=('Segoe UI',20,'bold'))
add_st_entrno=Entry(add_st,bd=5,font=('Segoe UI',20,'bold'))
add_st_lblname=Label(add_st,text="enter name",font=('Segoe UI',20,'bold'))
add_st_entname=Entry(add_st,bd=5,font=('Segoe UI',20,'bold'))
add_st_lblmarks=Label(add_st,text="Enter Marks",font=('Segoe UI',20,'bold'))
add_st_marks=Entry(add_st,bd=5,font=('Segoe UI',20,'bold'))
add_st_btnsave=Button(add_st,text="Save",font=('Segoe UI',20,'bold'),command=f5)
add_st_btnback=Button(add_st,text="Back",font=('Segoe UI',20,'bold'),command=f2)
add_st_lblrno.pack(pady=10)
add_st_entrno.pack(pady=10)
add_st_lblname.pack(pady=10)
add_st_entname.pack(pady=10)
add_st_lblmarks.pack(pady=10)
add_st_marks.pack(pady=10)
add_st_btnsave.pack(pady=10)
add_st_btnback.pack(pady=10)
add_st.withdraw()

#*******************************************************************************************************#
#view window
view_st=Toplevel(root)
view_st.title("View Student")
view_st.geometry("450x450+400+200")
view_st_data=ScrolledText(view_st,width=25,height=10,font=('Segoe UI', 20,'bold'))
view_st_btnback=Button(view_st,text="Back",font=('Segoe UI', 20,'bold'),command=f4)
view_st_data.pack()
view_st_btnback.pack(pady=10)
view_st.withdraw()
#*******************************************************************************************************#
delete_st=Toplevel(root)
delete_st.title("Delete a record")
delete_st.geometry("400x450+400+200")
delete_st_lblrno=Label(delete_st,text="enter rno",font=('Segoe UI',20,'bold'))
delete_st_entrno=Entry(delete_st,bd=5,font=('Segoe UI',20,'bold'))
delete_st_btndelete=Button(delete_st,text="Delete",font=('Segoe UI',20,'bold'),command=deleterec)
delete_st_btnback=Button(delete_st,text="Back",font=('Segoe UI',20,'bold'),command=btnback_del)
delete_st_lblrno.pack(pady=10)
delete_st_entrno.pack(pady=10)
delete_st_btndelete.pack(pady=10)
delete_st_btnback.pack(pady=10)
delete_st.withdraw()
#*******************************************************************************************************#

#add window
upd_st=Toplevel(root)
upd_st.title("Update Student")
upd_st.geometry("400x650+400+200")
upd_st_lblrno=Label(upd_st,text="enter rno",font=('Segoe UI',20,'bold'))
upd_st_entrno=Entry(upd_st,bd=5,font=('Segoe UI',20,'bold'))
upd_st_lblname=Label(upd_st,text="enter name",font=('Segoe UI',20,'bold'))
upd_st_entname=Entry(upd_st,bd=5,font=('Segoe UI',20,'bold'))
upd_st_lblmarks=Label(upd_st,text="Enter Marks",font=('Segoe UI',20,'bold'))
upd_st_marks=Entry(upd_st,bd=5,font=('Segoe UI',20,'bold'))
upd_st_btnsave=Button(upd_st,text="Save",font=('Segoe UI',20,'bold'),command=upd_save)
upd_st_btnback=Button(upd_st,text="Back",font=('Segoe UI',20,'bold'),command=upd_back)
upd_st_lblrno.pack(pady=10)
upd_st_entrno.pack(pady=10)
upd_st_lblname.pack(pady=10)
upd_st_entname.pack(pady=10)
upd_st_lblmarks.pack(pady=10)
upd_st_marks.pack(pady=10)
upd_st_btnsave.pack(pady=10)
upd_st_btnback.pack(pady=10)
upd_st.withdraw()

#*******************************************************************************************************#

root.mainloop()
