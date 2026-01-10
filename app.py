from flask import Flask, render_template, request, flash, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_sqlalchemy import SQLAlchemy
from stash.faq import FAQ_ITEMS
import os

app = Flask(__name__)
app.secret_key = "block-stash-booking-reading-twilight"

# --- Данные интерфейса ---
NAV_MENU = [
    {'name': 'О нас', 'url': '#about'},
    {'name': 'Каталог', 'url': '#catalog'},
    {'name': 'FAQ', 'url': '#faq'},
]

FOOTER_DATA = {
    'description': 'Создаем уникальные цифровые и печатные арты для истинных ценителей аниме-культуры.',
    'owner': 'ИП Котельников Родион Дмитриевич',
    'inn': '123456789012',
    'ogrnip': '321654987000012',
    'location': 'Россия, г. Москва',
    'year_range': '2024-2026'
}

# --- Настройка Базы Данных ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1mgtgOb9_mD6rucPHrIc4M_Y6e_McQIYcWkChQk3t0HE/edit"
WORKSHEET_NAME = "Для сайта"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sheet_id = db.Column(db.String(50))
    title = db.Column(db.String(200))
    fandom = db.Column(db.String(100))
    tags = db.Column(db.Text)
    price = db.Column(db.String(50))
    image = db.Column(db.Text)
    status = db.Column(db.String(50))
    stock = db.Column(db.String(100))
    delivery = db.Column(db.String(100))


# Функция синхронизации
def sync_with_google():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("stash/credentials.json", scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_url(SHEET_URL)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        data = worksheet.get_all_records()

        with app.app_context():
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


@app.route('/')
def index():
    db_products = Product.query.all()
    products_list = []

    for p in db_products:
        st = p.status.lower()
        # Автоматический подбор цвета для статуса
        status_class = "bg-success" if "налич" in st else "bg-warning" if "заказ" in st else "bg-secondary"

        products_list.append({
            'title': p.title,
            'fandom': p.fandom,
            'tags': [t.strip() for t in p.tags.split(',')] if p.tags else [],
            'price': f"{p.price} ₽" if p.price.isdigit() else p.price,
            'image': p.image,
            'status': p.status,
            'status_class': status_class,
            'stock': p.stock,
            'delivery': p.delivery
        })

    return render_template(
        'index.html',
        products=products_list,
        faq=FAQ_ITEMS,
        nav=NAV_MENU,
        footer=FOOTER_DATA
    )


@app.route('/sync')
def sync():
    if sync_with_google():
        flash("success_sync")
    else:
        flash("error_sync")
    return redirect(url_for('index'))


@app.route('/order', methods=['POST'])
def order():
    # Логика сбора данных из вашей новой формы
    form_data = {
        "name": request.form.get('name'),
        "contact": request.form.get('contact'),
        "idea": request.form.get('idea'),
        "ref": request.form.get('ref'),
        "size": request.form.get('size', 'Не указан')
    }
    # Здесь можно добавить отправку в Telegram или ту же Google Таблицу
    print(f"ПОЛУЧЕН ЗАКАЗ: {form_data}")
    flash("success_order")
    return redirect(url_for('index', _anchor='custom-section'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)