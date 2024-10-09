from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


class CoursePieCrawler:
    def __init__(self, usr_id, usr_password, driver_path):
        self.usr_id = usr_id
        self.usr_password = usr_password
        self.driver_path = driver_path
        self.driver = None
        self.course_messages = []  # 用于存储所有课程和作业信息

    # 启动 WebDriver
    def start_driver(self):
        service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Edge(service=service)

    # 登录课堂派
    def login(self):
        self.driver.get("https://w.ketangpai.com/login")

        id_blank = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入账号/手机/邮箱']"))
        )
        password_blank = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入密码']"))
        )
        id_blank.send_keys(self.usr_id)
        password_blank.send_keys(self.usr_password)

        btn_zone = self.driver.find_element(By.CLASS_NAME, "btnZone")
        btn_zone.click()

    # 抓取所有课程信息
    def fetch_courses(self):
        try:
            # 读取课程列表
            course_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "unfold-list"))
            )
            courses = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "courseName"))
            )

            for i in range(len(courses)):
                # 重新获取课程列表
                courses = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "courseName"))
                )
                course = courses[i]
                course_name = course.text  # 课程名称
                course.click()

                # 进入作业页面
                homework_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='作业']"))
                )
                homework_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='card-item']"))
                )
                assignments = self.driver.find_elements(By.XPATH, "//div[@class='card-item']")

                # 用于存储单个课程的详细信息
                course_message = {
                    "course_name": course_name,
                    "course_message": []  # 存储作业信息
                }

                # 提取每个作业的信息
                for j in range(len(assignments)):
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='card-item']"))
                    )
                    assignments = self.driver.find_elements(By.XPATH, "//div[@class='card-item']")
                    assignment = assignments[j]

                    # 提取作业标题
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, ".//h2[@class='title-h2']//span"))
                    )
                    homework_name = assignment.find_element(By.XPATH, ".//h2[@class='title-h2']//span").text

                    # 提取作业状态标签
                    status_tags_elements = assignment.find_elements(By.XPATH, ".//p[@class='tag-list']//span")
                    status_tags = [tag.text for tag in status_tags_elements]

                    # 点击进入作业详情
                    button = assignment.find_element(By.XPATH, ".//span[contains(@class, 'tip-btn')]")
                    button.click()

                    # 提取作业详细信息（如截止日期）
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'work-cart-layout')]"))
                    )
                    homework_card = self.driver.find_element(By.XPATH, "//div[contains(@class, 'work-cart-layout')]")

                    due_date = homework_card.find_element(By.XPATH, ".//span[contains(text(), '截止')]").text

                    # 填充作业信息
                    homework_message = {
                        "homework_name": homework_name,
                        "due_date": due_date,
                        "status_tags": status_tags
                    }

                    # 将作业信息加入课程信息中
                    course_message["course_message"].append(homework_message)

                    # 返回作业列表
                    self.driver.back()

                # 返回课程列表
                self.driver.back()

                # 将课程信息加入总课程列表
                self.course_messages.append(course_message)

        except Exception as e:
            print(f"发生错误: {e}")

    # 关闭浏览器
    def quit(self):
        if self.driver:
            self.driver.quit()

    # 打印抓取到的课程信息
    def print_courses(self):
        print(self.course_messages)

    def course_data(self):
        return self.course_messages
    def auto_work(self):
        self.start_driver()
        self.login()
        self.fetch_courses()
        self.quit()
        return self.course_data()


# 使用 CoursePreCrawler 类
if __name__ == "__main__":
    usr_id = input("请输入课堂派的账号：")
    usr_password = input("请输入课堂派的密码：")
    driver_path = r'C:\Users\Administrator\Downloads\edgedriver_win64\msedgedriver.exe'

    # 实例化爬虫类并执行操作
    crawler = CoursePieCrawler(usr_id, usr_password, driver_path)
    crawler.start_driver()
    crawler.login()
    crawler.fetch_courses()
    crawler.print_courses()
    crawler.quit()
