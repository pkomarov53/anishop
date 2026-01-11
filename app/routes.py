from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Product
from .config import NAV_MENU, FOOTER_DATA, FAQ_ITEMS
from .services import sync_with_google, send_telegram_order

main = Blueprint('main', __name__)

@main.route('/')
def index():
    db_products = Product.query.all()
    products_list = []

    for p in db_products:
        st = p.status.lower()
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

@main.route('/sync')
def sync():
    if sync_with_google():
        flash("success_sync")
    else:
        flash("error_sync")
    return redirect(url_for('main.index'))

@main.route('/order', methods=['POST'])
def order():
    name = request.form.get('name')
    contact = request.form.get('contact')
    idea = request.form.get('idea')
    size = request.form.get('size', 'Не указан')
    ref_image = request.files.get('ref_image')

    order_data = {
        "name": name,
        "contact": contact,
        "idea": idea,
        "size": size
    }

    send_telegram_order(order_data, ref_image)
    flash("success_order")
    return redirect(url_for('main.index', _anchor='custom-section'))