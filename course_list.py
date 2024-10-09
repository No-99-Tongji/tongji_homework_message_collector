class Course:
    def __init__(self, platform: str, course_name: str, course_message: str):
        self.platform = platform
        self.course_name = course_name
        self.course_message = course_message
    def __str__(self) -> str:
        return (f"Course Name: {self.course_name}\n"
                f"Platform: {self.platform}\n"
                f"Course Message: {self.course_message}")

class CourseList:
    def __init__(self):
        self.courses = []  # 初始化课程列表

    def add_course(self, course: Course):
        self.courses.append(course)  # 添加课程
        # 课程数量为当前列表长度
        self.course_num = len(self.courses)

    def get_course_num(self) -> int:
        return len(self.courses)  # 返回课程数量

    def __str__(self) -> str:
        return f"CourseList with {self.get_course_num()} courses."
    def print(self):
        print("课程个数：" + str(len(self.courses)))
        for course in self.courses:
            print(course)