from CanvasCrawler import CanvasCrawler
from CoursePieCrawler import CoursePieCrawler
from course_list import *

canvas_usr_id = input("请输入canvas的学号：")
canvas_usr_password = input("请输入canvas的密码：")
pie_usr_id = input("请输入课堂派的账号：")
pie_usr_password = input("请输入课堂派的密码：")
driver_path = input("请输入edgedriver的路径（输入-1则为默认路径）")
if driver_path == '-1':
    driver_path = r'C:\Users\Administrator\Downloads\edgedriver_win64\msedgedriver.exe'

canvas = CanvasCrawler(canvas_usr_id, canvas_usr_password, driver_path)
course_pie = CoursePieCrawler(pie_usr_id, pie_usr_password, driver_path)

canvas_message = canvas.auto_work()
course_pie_message = course_pie.auto_work()
course_list = CourseList()
for course in canvas_message:
    if len(course['course_message']) != 0:
        course_list.add_course(Course(platform="canvas", course_name=course['course_name'], course_message=course['course_message']))

# print(canvas_message)
# print(course_pie_message)
course_list.print()