from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class CanvasCrawler:
    def __init__(self, usr_id, usr_password, driver_path):
        self.usr_id = usr_id
        self.usr_password = usr_password
        self.driver_path = driver_path
        self.driver = None
        self.course_messages = []

    # 初始化 WebDriver
    def start_driver(self):
        service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Edge(service=service)

    # 登录 Canvas
    def login(self):
        self.driver.get("https://canvas.tongji.edu.cn")
        id_blank = self.driver.find_element(By.ID, "j_username")
        password_blank = self.driver.find_element(By.ID, "j_password")
        id_blank.send_keys(self.usr_id + '\n')
        password_blank.send_keys(self.usr_password + '\n')

    # 抓取所有课程信息
    def fetch_courses(self):
        try:
            # 获取课程信息
            courses = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ic-DashboardCard__header_content"))
            )
            for i in range(len(courses)):
                self.driver.implicitly_wait(1)
                course_message = {}
                try:
                    # 重新获取课程
                    courses = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "ic-DashboardCard__header_content"))
                    )
                    course = courses[i]
                    course_name = course.find_element(By.TAG_NAME, "span").text
                    course_message["course_name"] = course_name
                    course_message["course_message"] = []
                    course.click()

                except StaleElementReferenceException as e:
                    print(f"元素失效: {e}")
                    continue

                # 进入作业部分
                if self.enter_homework_section():
                    self.fetch_homeworks(course_message)

                # 返回课程首页
                self.driver.get("https://canvas.tongji.edu.cn/")

                # 将课程信息保存
                self.course_messages.append(course_message)

        except Exception as e:
            print(f"发生错误: {e}")

    # 进入作业部分
    def enter_homework_section(self):
        try:
            menu = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "sticky-container"))
            )
            homework_buttons = menu.find_elements(By.TAG_NAME, "li")
            for item in homework_buttons:
                if item.text == "作业":
                    item.click()
                    try:
                        WebDriverWait(self.driver, 3).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "ig-title"))
                        )
                    except Exception:
                        return False
                    return True
            return False
        except Exception as e:
            print(f"无法进入作业部分: {e}")
            return False

    # 抓取单个课程的作业信息
    def fetch_homeworks(self, course_message):
        homeworks = self.driver.find_elements(By.ID, "assignment_group_undated")
        for homework in homeworks:
            homework = homework.find_element(By.CLASS_NAME, "ig-title")
            homework.click()

            # 等待作业页面加载
            try:
                assignment = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, "assignment_show"))
                )
                # 记录作业信息
                homework_message = {}
                homework_name = assignment.find_element(By.CLASS_NAME, "title-content").text
                assignment_overview = assignment.find_element(By.TAG_NAME, "ul")
                lt = assignment_overview.find_elements(By.TAG_NAME, "li")

                message_list = []
                for item in lt:
                    tmp = item.find_elements(By.TAG_NAME, "span")
                    title = tmp[0].text
                    if title == "截止":
                        title = "due_date"
                    value = tmp[1].text
                    message_list.append([title, value])

                homework_message["homework_name"] = homework_name
                homework_message["message"] = message_list
                course_message["course_message"].append(homework_message)

                # 返回上一页
                self.driver.back()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sticky-container"))
                )
            except Exception:
                self.driver.back()



    # 关闭浏览器
    def quit(self):
        if self.driver:
            self.driver.quit()

    # 打印抓取到的课程信息
    def print_courses(self):
        print(self.course_messages)

    def courses_data(self):
        return self.course_messages
    def auto_work(self):
        self.start_driver()
        self.login()
        self.fetch_courses()
        self.quit()
        return self.courses_data()
# 使用 CanvasCrawler 类
if __name__ == "__main__":
    usr_id = input("请输入canvas的学号：")
    usr_password = input("请输入canvas的密码：")
    driver_path = r'C:\Users\Administrator\Downloads\edgedriver_win64\msedgedriver.exe'

    # 实例化爬虫类并执行操作
    crawler = CanvasCrawler(usr_id, usr_password, driver_path)
    crawler.start_driver()
    crawler.login()
    crawler.fetch_courses()
    crawler.print_courses()
    crawler.quit()
