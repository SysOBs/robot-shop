import os
import random

from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span
from transport import http_transport

from locust import HttpUser, task, between
from random import choice
from random import randint


class UserBehavior(HttpUser):
    wait_time = between(2, 10)

    # source: https://tools.tracemyip.org/search--ip/list
    fake_ip_addresses = [
        # white house
        "156.33.241.5",
        # Hollywood
        "34.196.93.245",
        # Chicago
        "98.142.103.241",
        # Los Angeles
        "192.241.230.151",
        # Berlin
        "46.114.35.116",
        # Singapore
        "52.77.99.130",
        # Sydney
        "60.242.161.215"
    ]


    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print('Starting')

    @task
    def login(self):
        fake_ip = random.choice(self.fake_ip_addresses)
        headers = create_http_headers_for_new_span() | {'x-forwarded-for': fake_ip}
        credentials = {
            'name': 'user',
            'password': 'password'
        }
        res = self.client.post(
            '/api/user/login', json=credentials, headers=headers)
        print('login {}'.format(res.status_code))

    @task
    def load(self):
        with zipkin_span(
                service_name='locust-client',
                span_name='load',
                transport_handler=http_transport,
                port=30494,
                sample_rate=100,
        ):
            fake_ip = random.choice(self.fake_ip_addresses)
            headers = create_http_headers_for_new_span() | {'x-forwarded-for': fake_ip}
            self.client.get('/',headers=headers)
            user = self.client.get('/api/user/uniqueid',
                                  headers=headers).json()
            uniqueid = user['uuid']
            print('User {}'.format(uniqueid))

            self.client.get('/api/catalogue/categories',
                           headers=headers)
            # all products in catalogue
            products = self.client.get(
                '/api/catalogue/products',headers=headers).json()
            for i in range(2):
                item = None
                while True:
                    item = choice(products)
                    if item['instock'] != 0:
                        break

                # vote for item
                if randint(1, 10) <= 3:
                    self.client.put('/api/ratings/api/rate/{}/{}'.format(
                        item['sku'], randint(1, 5)),headers=headers)

                self.client.get(
                    '/api/catalogue/product/{}'.format(item['sku']),headers=headers)
                self.client.get(
                    '/api/ratings/api/fetch/{}'.format(item['sku']),headers=headers)
                self.client.get('/api/cart/add/{}/{}/1'.format(uniqueid,
                                item['sku']),headers=headers)

            cart = self.client.get(
                '/api/cart/cart/{}'.format(uniqueid),headers=headers).json()
            item = choice(cart['items'])
            self.client.get('/api/cart/update/{}/{}/2'.format(uniqueid,
                            item['sku']),headers=headers)

            # country codes
            code = choice(self.client.get('/api/shipping/codes',
                                         headers=headers).json())
            city = choice(self.client.get('/api/shipping/cities/{}'.format(
                code['code']),headers=headers).json())
            print('code {} city {}'.format(code, city))
            shipping = self.client.get(
                '/api/shipping/calc/{}'.format(city['uuid']),headers=headers).json()
            shipping['location'] = '{} {}'.format(code['name'], city['name'])
            print('Shipping {}'.format(shipping))
            # POST
            cart = self.client.post('/api/shipping/confirm/{}'.format(uniqueid),
                                    json=shipping,headers=headers).json()
            print('Final cart {}'.format(cart))

            order = self.client.post('/api/payment/pay/{}'.format(uniqueid),
                                     json=cart,headers=headers).json()
            print('Order {}'.format(order))

    @task
    def error(self):
        if os.environ.get('ERROR') == '1':
            print('Error request')
            cart = {'total': 0, 'tax': 0}
            self.client.post('/api/payment/pay/partner-57',
                             json=cart, headers=create_http_headers_for_new_span() | {'x-forwarded-for': fake_ip})
