from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
import os

# Đọc token từ biến môi trường
TOKEN = os.getenv("BOT_TOKEN")

# URL của trang đăng nhập và trang điểm học tập
LOGIN_URL = "https://student.husc.edu.vn/Account/Login"
GRADE_URL = "https://student.husc.edu.vn/Statistics/StudyResult"

# Thông tin đăng nhập của bạn (Thay bằng thông tin của bạn)
USERNAME = "23T1020544"
PASSWORD = "tinh15042005"

# Khởi tạo session để duy trì cookies
session = requests.Session()

# Hàm lấy CSRF Token
def get_csrf_token():
    response = requests.get(GRADE_URL, proxies={"http": None, "https": None})
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
    return csrf_token

# Hàm đăng nhập
def login():
    csrf_token = get_csrf_token()
    login_data = {
        '__RequestVerificationToken': csrf_token,
        'loginID': USERNAME,
        'password': PASSWORD,
    }

    # Gửi yêu cầu POST để đăng nhập
    response = session.post(LOGIN_URL, data=login_data)

    if response.status_code == 200 and 'Mã sinh viên' not in response.text:
        return True
    else:
        return False

def Lay_Diem():
    if login():
        response = session.get(GRADE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        grades = soup.find_all('td')
        return grades

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# Hàm xử lý lệnh /Diem
async def scores(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Update:
    grade = Lay_Diem()
    for i in grade:
        await update.message.reply_text(f"{i.text}")

# Cấu hình Updater và Dispatcher
app = ApplicationBuilder().token(TOKEN).build()

# Thêm lệnh /scores vào bot
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("Diem", scores))
app.add_handler(CommandHandler("diem", scores))
# Bắt đầu bot
app.run_polling()

        
