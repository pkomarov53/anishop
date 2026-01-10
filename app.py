from flask import Flask, render_template, request, flash, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_sqlalchemy import SQLAlchemy
from stash.faq import FAQ_ITEMS
import os

app = Flask(__name__)
app.secret_key = "block-stash-booking-reading-twilight"

# --- Настройка Базы Данных (SQLite) ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1mgtgOb9_mD6rucPHrIc4M_Y6e_McQIYcWkChQk3t0HE/edit"
WORKSHEET_NAME = "Для сайта"


# --- Модель товара в БД ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Это внутренний ID базы
    sheet_id = db.Column(db.String(50))  # ID из вашей таблицы
    title = db.Column(db.String(200))
    fandom = db.Column(db.String(100))
    tags = db.Column(db.Text)  # Храним как строку через запятую
    price = db.Column(db.String(50))
    image = db.Column(db.Text)
    status = db.Column(db.String(50))
    stock = db.Column(db.String(100))
    delivery = db.Column(db.String(100))


# Создаем таблицу при запуске
with app.app_context():
    db.create_all()


# --- Логика синхронизации ---
def sync_with_google():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("stash/credentials.json", scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_url(SHEET_URL)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

        data = worksheet.get_all_records()

        # Очищаем старые данные и записываем новые
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
    # Берем данные ТОЛЬКО из базы данных
    db_products = Product.query.all()

    # Превращаем объекты БД в список словарей для шаблона (чтобы не менять логику тегов в HTML)
    products_list = []
    for p in db_products:
        products_list.append({
            'title': p.title,
            'fandom': p.fandom,
            'tags': [t.strip() for t in p.tags.split(',')] if p.tags else [],
            'price': p.price,
            'image': p.image,
            'status': p.status,
            'stock': p.stock,
            'delivery': p.delivery
        })

    return render_template(
        'index.html',
        products=products_list,
        faq=FAQ_ITEMS
    )


@app.route('/sync')
def sync():
    if sync_with_google():
        flash("Каталог успешно обновлен из облака!")
    else:
        flash("Ошибка при обновлении каталога.")
    return redirect(url_for('index'))


@app.route('/order', methods=['POST'])
def order():
    # Ваша логика заказа без изменений
    form_data = {
        "name": request.form.get('name'),
        "contact": request.form.get('contact'),
        "idea": request.form.get('idea'),
        "ref": request.form.get('ref'),
        "size": request.form.get('size', 'Не указан')
    }
    print(f"ЗАКАЗ: {form_data}")
    flash("Заявка успешно отправлена!")
    return redirect(url_for('index', _anchor='custom-section'))


if __name__ == '__main__':
    app.run(debug=True)