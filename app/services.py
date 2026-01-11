import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import current_app
from .extensions import db
from .models import Product


def sync_with_google():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Путь к credentials теперь относительно корня или абсолютный
        creds = ServiceAccountCredentials.from_json_keyfile_name("stash/credentials.json", scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_url(current_app.config['SHEET_URL'])
        worksheet = spreadsheet.worksheet(current_app.config['WORKSHEET_NAME'])
        data = worksheet.get_all_records()

        # Удаляем старые и добавляем новые (в рамках текущего контекста приложения)
        db.session.query(Product).delete()
        for item in data:
            new_item = Product(
                sheet_id=str(item.get('id', '')),
                title=item.get('title', 'Без названия'),
                fandom=item.get('fandom', ''),
                tags=str(item.get('tags', '')),
                price=str(item.get('price', '')),
                image=item.get('image', ''),
                status=item.get('status', ''),
                stock=item.get('stock', ''),
                delivery=item.get('delivery', '')
            )
            db.session.add(new_item)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Ошибка синхронизации: {e}")
        return False


def send_telegram_order(data, file=None):
    """Отправка заказа в Telegram"""
    token = current_app.config['TG_BOT_TOKEN']
    chat_id = current_app.config['TG_CHAT_ID']

    message_text = (
        f"<b>🔥 НОВЫЙ ЗАКАЗ (ANICRAFT)</b>\n\n"
        f"👤 <b>Имя:</b> {data['name']}\n"
        f"📱 <b>Связь:</b> {data['contact']}\n"
        f"📏 <b>Размер:</b> {data['size']}\n"
        f"📝 <b>Идея/Описание:</b>\n{data['idea']}"
    )

    try:
        if file and file.filename:
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            files = {'photo': (file.filename, file.stream, file.content_type)}
            payload = {'chat_id': chat_id, 'caption': message_text, 'parse_mode': 'HTML'}
            requests.post(url, data=payload, files=files)
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {'chat_id': chat_id, 'text': message_text, 'parse_mode': 'HTML'}
            requests.post(url, data=payload)
        return True
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False