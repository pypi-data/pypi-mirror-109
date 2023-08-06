import copy
import time
import typing
from http.client import HTTPConnection, HTTPResponse
import socket
import nb_log

from universal_object_pool import ObjectPool, AbstractObject
from threadpool_executor_shrink_able import BoundedThreadPoolExecutor
import decorator_libs


class CustomHTTPResponse(HTTPResponse):  # 为了ide补全
    text: str = None


class HttpOperator(AbstractObject):
    """ 这个请求速度暴击requests，可以自行测试请求nginx网关本身"""

    def __init__(self, host, port=None, timeout=5,
                 source_address=None):
        self.conn = HTTPConnection(host=host, port=port, timeout=timeout, source_address=source_address, )
        self.core_obj = self.conn

    def clean_up(self):
        self.conn.close()

    def before_back_to_queue(self, exc_type, exc_val, exc_tb):
        pass

    def request_and_getresponse(self, method, url, body=None, headers={}, *,
                                encode_chunked=False) -> CustomHTTPResponse:
        self.conn.request(method, url, body=body, headers=headers,
                          encode_chunked=encode_chunked)
        resp = self.conn.getresponse()
        resp.text = resp.read()
        return resp  # noqa


if __name__ == '__main__':
    http_pool = ObjectPool(object_type=HttpOperator, object_pool_size=100, object_init_kwargs=dict(host='127.0.0.1'), max_idle_seconds=60)

    import requests

    ss = requests.session()


    def test_request():
        # ss.get('http://127.0.0.1')

        # requests.get('http://127.0.0.1')

        with http_pool.get() as conn:  # type: typing.Union[HttpOperator,HTTPConnection]  # http对象池的请求速度暴击requests的session和直接requests.get
            r1 = conn.request_and_getresponse('GET', '/')
            print(r1.text[:100])


    thread_pool = BoundedThreadPoolExecutor(200)
    with decorator_libs.TimerContextManager():
        for x in range(30000):
            thread_pool.submit(test_request, )
            # thread_pool.submit(test_update_multi_threads_use_one_conn, x)
        thread_pool.shutdown()
    time.sleep(10000)
