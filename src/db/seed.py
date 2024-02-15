import random

from yachalk import chalk
import factory
from cuid2 import cuid_wrapper
import faker_commerce
import factory.random
from factory import alchemy

from connection import db_session
from schema import User, Restaurants, Products, OrderItems, Orders


def array_elements(array, min_qtd, max_qtd):
    """
    Retorna um subconjunto aleatório de uma lista com um número mínimo e máximo de elementos.
    
    :param array: A lista de onde um subconjunto aleatório será selecionado.
    :type array: list
    :param min_qtd: A quantidade mínima de elementos no subconjunto.
    :type min_qtd: int
    :param max_qtd: A quantidade máxima de elementos no subconjunto.
    :type max_qtd: int
    :return: Um subconjunto aleatório da lista fornecida.
    """
    if not array:
        raise ValueError("A lista fornecida está vazia.")
    if min_qtd < 0 or max_qtd < 0:
        raise ValueError("A quantidade mínima e máxima de elementos devem ser não-negativas.")
    if min_qtd > max_qtd:
        raise ValueError("A quantidade mínima de elementos não pode ser maior que a quantidade máxima.")
    
    qtd_elementos = random.randint(min_qtd, max_qtd)
    return random.sample(array, qtd_elementos)


factory.random.reseed_random(40)
factory.faker.Faker.add_provider(faker_commerce.Provider)

db_session.query(User).delete()
db_session.commit()

print(chalk.yellow('✔ Database reset'))

class CustomerFactory(alchemy.SQLAlchemyModelFactory):
  class Meta:
    model = User
    sqlalchemy_session = db_session

  name = factory.faker.Faker('name',locale='pt-br')
  phone = factory.faker.Faker('phone_number',locale='pt-br')
  email = factory.faker.Faker('email',locale='pt-br')

user1 = CustomerFactory(role='customer').create()
user2 = CustomerFactory(role='customer').create()

print(chalk.yellow('✔ Created customers'))

class ManagerFactory(alchemy.SQLAlchemyModelFactory):
  class Meta:
    model = User
    sqlalchemy_session = db_session

  name = factory.faker.Faker('name',locale='pt-br')
  phone = factory.faker.Faker('phone_number',locale='pt-br')
  email = factory.faker.Faker('email',locale='pt-br')

manager = ManagerFactory(email="tulioneedforspeed@gmail.com",role="manager").create()

print(chalk.yellow('✔ Created manager'))

class RestaurantFactory(alchemy.SQLAlchemyModelFactory):
  class Meta:
    model = Restaurants
    sqlalchemy_session = db_session

  name = factory.faker.Faker('company',locale='pt-br')
  description = factory.faker.Faker('paragraph')
  manager_id = manager.id

restaurant = RestaurantFactory.create()
db_session.add(restaurant)
db_session.commit()

print(chalk.yellow('✔ Created restaurant'))

class ProductFactory(alchemy.SQLAlchemyModelFactory):
  class Meta:
    model = Products
    sqlalchemy_session = db_session

  name = factory.faker.Faker('ecommerce_name')
  price_in_cents = factory.faker.Faker('ecommerce_price')
  description = factory.faker.Faker('ecommerce_price')
  restaurant_id = restaurant.id

products = ProductFactory.create_batch(10)

db_session.add_all(products)
db_session.commit()

print(chalk.yellow('✔ Created products'))


class OrdersFactory(alchemy.SQLAlchemyModelFactory):
  class Meta:
    model = Orders
    sqlalchemy_session = db_session

class OrderItemsFactory(alchemy.SQLAlchemyModelFactory):
  class Meta:
    model = OrderItems
    sqlalchemy_session = db_session

orders_to_insert = []
order_items_to_push = []
                         
for i in range(200):
  cuid_generator = cuid_wrapper()
  order_id = cuid_generator()

  order_products = array_elements(products,max_qtd=3,min_qtd=1)

  total_in_cents = 0

  for order_product in order_products:
     quantity = random.randint(1,3)

     total_in_cents += order_product.price_in_cents * quantity

     order_items_to_push.append(OrderItemsFactory(**{
        "order_id": order_id,
        "product_id": order_product.id,
        "price_in_cents": order_product.price_in_cents,
        "quantity": quantity
     }))
  
  orders_to_insert.append(OrdersFactory(**{
     "id": order_id,
     "customer_id": random.choice([user1.id,user2.id]),
      "restaurant_id": restaurant.id,
    "status": random.choice([
      'pending',
      'canceled',
      'processing',
      'delivering',
      'delivered',
    ]),
    "total_in_cents": total_in_cents,
    "created_at": factory.faker.Faker('date_time_between',start_date="-40d")

  }))


db_session.add_all(orders_to_insert)
db_session.add_all(order_items_to_push)
db_session.commit()

print(chalk.yellow('✔ Created orders'))

db_session.close()

print(chalk.green_bright('Database seeded successfully!'))