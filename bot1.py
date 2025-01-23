from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

def get_news():
    url = 'https://baomoi.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_dict = soup.find_all('h3', class_='font-semibold block')
    news_list = []

    # Duyệt qua tất cả các thẻ <h3> chứa tin tức
    for new in news_dict:
        news_data = {}
        # Lấy tiêu đề và liên kết
        title = new.a.get('title') if new.a else None
        link = new.a.get('href') if new.a else None

        # Lưu vào danh sách
        news_data['title'] = title
        news_data['link'] = link
        news_list.append(news_data)
    return news_list

# Hàm xử lý lệnh /hello
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# Hàm xử lý lệnh /news (cập nhật tin tức)
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Update:
    news_list = get_news()  # Giả sử bạn đã có hàm get_news()
    So_TT = 1
    for item in news_list[:5]:
        # Gửi tin tức đầu tiên 10 tin đã lấy
        title = item['title'] if item['title'] else None
        link = item['link'] if item['link'] else None
        # link truy cap
        await update.message.reply_text(f"Tin tức số {So_TT}: {title}")
        await update.message.reply_text(f"Link: baomoi.com/{link}")
        await update.message.reply_text("------------------------------------")
        # Tăng số thứ tự tin tức
        So_TT += 1
# Khởi tạo ứng dụng
TOKEN = "7601455848:AAFyTFGa1F3R4Ev75csu4GUjidfWsr4NIA0"
app = ApplicationBuilder().token(TOKEN).build()

# Thêm các handler
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("news", news))

# Chạy bot
app.run_polling()
