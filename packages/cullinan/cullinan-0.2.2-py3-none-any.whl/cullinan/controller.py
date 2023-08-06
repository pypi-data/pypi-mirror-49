# -*- coding: utf-8 -*-
# @File   : controller.py
# @license: Copyright(C) 2019 FNEP-Tech
# @Author : hansion, fox
# @Date   : 2019-02-15
# @Desc   : controller
import tornado.web
import types
import functools
from cullinan.service import service_list

url_list = []


class Encapsulation_Handler_func(object):
    @classmethod
    def set_fragment_method(cls, cls_name, func):
        @functools.wraps(func)
        def dummy(self, *args, **kwargs):
            func(self, *args, **kwargs)

        setattr(cls_name, func.__name__, dummy)

    @staticmethod
    def add_url(**kwargs):

        def inner(f):
            url = kwargs['url']
            servlet = type('Servlet' + url.replace('/', ''), (Handler,),
                           {"set_instance_method": Encapsulation_Handler_func.set_fragment_method})
            if url_list.__len__() == 0:
                servlet.set_instance_method(servlet, f)
                servlet.f = types.MethodType(f, servlet)
                url_list.append((url, servlet))
                return servlet
            else:
                for item in url_list:
                    if url == item[0]:
                        item[1].set_instance_method(item[1], f)
                        item[1].f = types.MethodType(f, item[1])
                        return item[1]
                else:
                    servlet.set_instance_method(servlet, f)
                    servlet.f = types.MethodType(f, servlet)
                    url_list.append((url, servlet))
                    return servlet

        return inner


class Handler(tornado.web.RequestHandler):

    # def initialize(self):
    #     # 这里将子类对象传入session中, 则以后生成的session对象中就包含处理器的实例对象
    #     self.session = Session(self)

    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        # 用来解决跨域问题
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-type, contenttype")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PATCH, PUT, OPTIONS')

    def options(self):
        pass


def get_api(**kwargs):
    def inner(func):
        @Encapsulation_Handler_func.add_url(url=kwargs['url'])
        def get(self):
            request = self.request
            service = service_list[kwargs['service']]
            print("\t|||request_header", end="")
            print(request)
            response = func(self, request, service)
            if response.get_is_static is True:
                self.render(response.get_body())
            if response.get_headers().__len__() > 0:
                for header in response.get_headers():
                    self.set_header(header[0], header[1])
            self.write(response.get_body())

        return get

    return inner


def post_api(**kwargs):
    def inner(func):
        @Encapsulation_Handler_func.add_url(url=kwargs['url'])
        def post(self):
            request = self.request
            service = service_list[kwargs['service']]
            print("\t|||request_header", end="")
            print(request)
            response = func(self, request, service)
            if response.get_headers().__len__() > 0:
                for header in response.get_headers():
                    self.set_header(header[0], header[1])
            self.write(response.get_body())

        return post

    return inner


def patch_api(**kwargs):
    def inner(func):
        @Encapsulation_Handler_func.add_url(url=kwargs['url'])
        def patch(self):
            request = self.request
            service = service_list[kwargs['service']]
            print("\t|||request_header", end="")
            print(request)
            response = func(self, request, service)
            if response.get_headers().__len__() > 0:
                for header in response.get_headers():
                    self.set_header(header[0], header[1])
            self.write(response.get_body())

        return patch

    return inner


def delete_api(**kwargs):
    def inner(func):
        @Encapsulation_Handler_func.add_url(url=kwargs['url'])
        def delete(self):
            request = self.request
            service = service_list[kwargs['service']]
            print("\t|||request_header", end="")
            print(request)
            response = func(self, request, service)
            if response.get_headers().__len__() > 0:
                for header in response.get_headers():
                    self.set_header(header[0], header[1])
            self.write(response.get_body())

        return delete

    return inner


def put_api(**kwargs):
    def inner(func):
        @Encapsulation_Handler_func.add_url(url=kwargs['url'])
        def put(self):
            request = self.request
            service = service_list[kwargs['service']]
            print("\t|||request_header", end="")
            print(request)
            response = func(self, request, service)
            if response.get_headers().__len__() > 0:
                for header in response.get_headers():
                    self.set_header(header[0], header[1])
            self.write(response.get_body())

        return put

    return inner
