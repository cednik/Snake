import socket
from Communication.exceptions import *
from codecs import getincrementalencoder, getincrementaldecoder, IncrementalEncoder, IncrementalDecoder
from queue import Queue
from sys import exc_info

class transparent_coder(IncrementalEncoder, IncrementalDecoder):
    def encode(self, object, final = False):
        return object
    def decode(self, object, final = False):
        return object

class Client:
    def __init__(self, addr = None, port = 1234, timeout = None, encoding = 'utf8', decoding = None, noexcept = True, read_error_retval = None):
        self.__error_queue = Queue()
        self.__socket = None
        self.__addr = addr
        self.__port = Client.check_port(port)
        self.__timeout = timeout
        self.encoder = encoding
        self.decoder = decoding
        self.__init_recbuff()
        self.__bufsize = 4096
        self.__noexcept = noexcept
        self.__read_error_retval = read_error_retval
        if self.__addr != None:
            self.connect()

    def connect(self, addr = None, port = None):
        if self.connected:
            if addr == self.__addr and port == self.__port:
                return
            seld.disconnect()
        if addr != None:
            self.__addr = addr
        elif self.__addr == None:
            return self.__error(ValueError('Address not specified.'), False)
        if port != None:
            self.__port = Client.check_port(port)
        try:
            self.__socket = socket.create_connection((self.__addr, self.__port), self.__timeout)
        except:
            return self.__error(None, False)
        self.__readable = True
        self.__writable = True
        return True

    def disconnect(self):
        if self.connected:
            self.shutdown(True, True)
            self.__socket.close()
            self.__socket = None
            self.__init_recbuff()

    def shutdown(self, write = True, read = False):
        if self.__socket == None:
            return self.__error(PortClosedError('Operation on closed port (shutdown).'), False)
        if write:
            how = socket.SHUT_RDWR if read else socket.SHUT_WR
        elif read:
            how = socket.SHUT_RD
        else:
            return True
        self.__readable &= ~read
        self.__writable &= ~write
        self.__socket.shutdown(how)
        return True
            

    def read(self, size = 1):
        if self.__socket == None:
            return self.__error(PortClosedError('Operation on closed port (read).'), self.__read_error_retval)
        if not self.__readable:
            return self.__error(ConnectionBrokenError(), self.__read_error_retval)
        while len(self.__recbuff) < size:
            try:
                v = self.__socket.recv(self.__bufsize)
            except (socket.timeout, BlockingIOError):
                break
            except ConnectionResetError:
                self.__readable = False
                return self.__error(None, self.__read_error_retval)
            if not v:
                self.__readable = False
                return self.__error(ConnectionBrokenError(), self.__read_error_retval)
            self.__recbuff += self.__decoder.decode(v)
        ret = self.__recbuff[0:size]
        if len(self.__recbuff) > size:
            self.__recbuff = self.__recbuff[size:]
        else:
            self.__init_recbuff()
        return ret

    def write(self, value):
        if self.__socket == None:
            return self.__error(PortClosedError('Operation on closed port (write).'), 0)
        if not self.__writable: raise ConnectionBrokenError()
        if self.__force_encode or isinstance(value, str):
            value = self.__encoder.encode(value)
        else:
            value = bytes(value)
        sent = 0
        all = len(value)
        while sent != all:
            try:
                v = self.__socket.send(value[sent:])
            except:
                return self.__error(None, sent)
            if v == 0:
                self.__writable = False
                return self.__error(ConnectionBrokenError(), sent)
            sent += v
        return sent

    @property
    def connected(self):
        return self.__socket != None

    @property
    def readable(self):
        return self.__readable

    @property
    def writable(self):
        return self.__writable

    @property
    def address(self):
        return self.__addr

    @property
    def port(self):
        return self.__port

    @property
    def timeout(self):
        return self.__timeout
    @timeout.setter
    def timeout(self, value):
        if self.__socket != None:
            self.__socket.settimeout(value)
        self.__timeout = value

    @property
    def encoder(self):
        return self.__encoder
    @encoder.setter
    def encoder(self, value):
        self.__encoder = Client.resolve_coder(value, getincrementalencoder)
        self.__force_encode = self.__encoder == value

    @property
    def decoder(self):
        return self.__decoder
    @decoder.setter
    def decoder(self, value):
        self.__decoder = Client.resolve_coder(value, getincrementaldecoder)

    @property
    def read_type(self):
        return b'' if isinstance(self.__decoder, transparent_coder) else ''

    @property
    def noexcept(self):
        return self.__noexcept
    @noexcept.setter
    def noexcept(self, value):
        self.__noexcept = bool(value)

    @property
    def was_error(self):
        return not self.__error_queue.empty()

    @property
    def error(self):
        if self.__error_queue.empty():
            return None
        err = self.__error_queue.get()
        self.__error_queue.task_done()
        return err

    def __enter__(self):
        return self

    def __exit__(self, *exception):
        self.disconnect()
        return False

    def __repr__(self):
        if self.connected:
            state = '{}, {}'.format(self.__addr, self.__port)
        else:
            state = 'disconnected'
            if self.__addr != None:
                state += '[{}, {}]'.format(self.__addr, self.__port)
        return '<tcp.Client({}) at 0x{:08X}>'.format(state, id(self))

    open = connect
    close = disconnect

    def _from_server(self, socket, addr, timeout):
        self.__socket = socket
        self.__addr = addr
        self.__readable = True
        self.__writable = True
        self.timeout = timeout
        return self

    def __error(self, exception = None, retval = False):
        if self.__noexcept:
            if exception == None:
                exc_type, exc_value, exc_traceback = exc_info()
                exception = exc_value
            self.__error_queue.put(exception)
            return retval
        if exception == None:
            raise
        raise exception

    def __init_recbuff(self):
        self.__recbuff = self.read_type

    @staticmethod
    def check_port(port):
        if not isinstance(port, int):
            raise TypeError('Port has to be int, {} given.'.format(type(port)))
        if port < 0 or port > 65535:
            raise ValueError('Port has to be in range 0 to 65536, {} given.'.format(port))
        return port

    @staticmethod
    def resolve_coder(codings, getter):
        if codings == None: return transparent_coder()
        if isinstance(codings, str): return getter(codings)()
        return codings


class Server:
    def __init__(self,
                 addr = '',
                 port = 1234,
                 timeout = None,
                 family = socket.AF_INET,
                 type = socket.SOCK_STREAM,
                 proto = 0,
                 max_con = 1,
                 client_timeout = None,
                 encoding = 'utf8',
                 decoding = None,
                 noexcept = True,
                 read_error_retval = None):
        self.__port = Client.check_port(port)
        self.__client_timeout = client_timeout
        self.__encoding = encoding
        self.__decoding = decoding
        self.__socket = socket.socket(family, type, proto)
        self.__socket.bind((addr, self.__port))
        self.__socket.listen(max_con)
        self.__socket.settimeout(timeout)
        self.__noexcept = noexcept
        self.__read_error_retval = read_error_retval

    def accept(self):
        try:
            sock, addr = self.__socket.accept()
        except (socket.timeout, BlockingIOError):
            return None
        except:
            raise
        else:
            return Client(
                port = self.__port,
                encoding = self.__encoding,
                decoding = self.__decoding,
                noexcept = self.__noexcept,
                read_error_retval = self.__read_error_retval)._from_server(sock, addr, self.__client_timeout)

    def close(self):
        self.__socket.close()
