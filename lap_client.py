from tornado import gen
from tornado import ioloop, websocket, httpclient
import clipboard

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 6

class WebSocketClient():
    """Base for web socket clients.
    """
 
    def __init__(self, *, connect_timeout=DEFAULT_CONNECT_TIMEOUT,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT):

        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout

    def connect(self, url):
        """Connect to the server.
        :param str url: server URL.
        """

        # headers = httputil.HTTPHeaders({'Content-Type': APPLICATION_JSON})
        request = httpclient.HTTPRequest(url=url,
                                         connect_timeout=self.connect_timeout,
                                         request_timeout=self.request_timeout)
        # ws_conn = websocket.WebSocketClientConnection(ioloop.IOLoop.current(),
        #                                               request)
        # ws_conn.connect_future.add_done_callback(self._connect_callback)
        self._ws_connection = websocket.WebSocketClientConnection(request)
        print(self._ws_connection)
        self._on_connection_success()
        self._read_messages()
                        # print(ws_conn._ws_connection)
    def send(self, data):
        """Send message to the server
        :param str data: message.
        """
        if not self._ws_connection:
            raise RuntimeError('Web socket connection is closed.')

        self._ws_connection.write_message(data)

    def close(self):
        """Close connection.
        """

        if not self._ws_connection:
            raise RuntimeError('Web socket connection is already closed.')

        self._ws_connection.close()

    def _connect_callback(self, future):
        if future.exception() is None:
            self.var = 2
            self._ws_connection = future.result()
            self._on_connection_success()
            self._read_messages()
        else:
            self._on_connection_error(future.exception())

    @gen.coroutine
    def _read_messages(self):
        while True:
            msg = yield self._ws_connection.read_message()
            if msg is None:
                self._on_connection_close()
                break

            self._on_message(msg)

    # @gen.coroutine
    # def send(self, msg):
    #     while True:



    def _on_message(self, msg):
        print(msg)
        clipboard.copy(msg)
        # deadline = time.time() + 1
        # ioloop.IOLoop().instance().add_timeout(
        #     deadline, functools.partial(self.send, str(int(time.time()))))

    def _on_connection_success(self):
        print('Connected!')
        # self.send('eek')
        # self.send(str(int(time.time())))

    def _on_connection_close(self):
        print('Connection closed!')

    def _on_connection_error(self, exception):
        print('Connection error: %s', exception)



    

def main():
    client = WebSocketClient()
    client.connect('ws://localhost:8888/ws')

    try:
        ioloop.IOLoop.current().start() 

    except KeyboardInterrupt:
        client.close()




if __name__ == '__main__':
    main()
