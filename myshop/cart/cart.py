from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    def __init__(self,request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Product."""
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    # для вывода количества товаров в корзине
    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    # посчет общей стоимости корзины
    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    # функция очистки корзины
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
