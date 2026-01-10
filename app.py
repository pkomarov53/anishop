from flask import Flask, render_template, request, flash, redirect, url_for
from stash import faq
from stash.faq import FAQ_ITEMS

app = Flask(__name__)
app.secret_key = "anime_art_secret"

# База данных товаров
products = [
    {
        "id": 1,
        "title": "Узумаки: Режим Мудреца",
        "fandom": "Naruto",
        "tags": ["Неон", "Портрет"],
        "price": "2 500 ₽",
        "image": "https://images.unsplash.com/photo-1614728263952-84ea256f9679?q=80&w=500",
        "status": "В наличии",
        "stock": "Осталось 2 шт.",
        "delivery": "1-3 дня"
    },
    {
        "id": 2,
        "title": "Кибер-Самурай",
        "fandom": "Original",
        "tags": ["Киберпанк", "Full Art"],
        "price": "3 200 ₽",
        "image": "https://images.unsplash.com/photo-1614728263952-84ea256f9679?q=80&w=500",
        "status": "Под заказ",
        "stock": "Печать за 5 дней",
        "delivery": "Отправка РФ/ЕС"
    },
    {
        "id": 3,
        "title": "Призрак в доспехах",
        "fandom": "GITS",
        "tags": ["Минимализм", "Интерьер"],
        "price": "2 800 ₽",
        "image": "https://images.unsplash.com/photo-1614728263952-84ea256f9679?q=80&w=500",
        "status": "В наличии",
        "stock": "Популярный выбор",
        "delivery": "2-4 дня"
    }
]


@app.route('/')
def index():
    return render_template(
        'index.html',
        products=products,
        faq=FAQ_ITEMS
    )

@app.route('/order', methods=['POST'])
def order():
    # Сбор всех данных из формы
    form_data = {
        "name": request.form.get('name'),
        "contact": request.form.get('contact'),
        "idea": request.form.get('idea'),
        "ref": request.form.get('ref'),
        "size": request.form.get('size', 'Не указан')
    }

    # Логика обработки (например, формирование строки для логов или Telegram)
    log_message = (
        f"ЗАКАЗ: {form_data['name']} | "
        f"Связь: {form_data['contact']} | "
        f"Размер: {form_data['size']} | "
        f"Идея: {form_data['idea']} | "
        f"Реф: {form_data['ref']}"
    )
    print(log_message)

    flash("Заявка успешно отправлена! Мы свяжемся с вами в течение часа.")
    return redirect(url_for('index', _anchor='custom-section'))

if __name__ == '__main__':
    app.run(debug=True)