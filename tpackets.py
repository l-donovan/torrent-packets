import flask
from random import randint
app = flask.Flask(__name__)

TPACK_DATA_SIZE = 1024 # 1 KiB
ACTIVE_FILE = None

@app.route('/t/<file_name>/<int:packet_num>')
def torrent_packet(file_name, packet_num):
    global ACTIVE_FILE

    if ACTIVE_FILE is None or ACTIVE_FILE.name != file_name:
        ACTIVE_FILE = open(file_name, 'rb')
    ACTIVE_FILE.seek(TPACK_DATA_SIZE * packet_num)
    data = bytearray(ACTIVE_FILE.read(TPACK_DATA_SIZE))

    outArray = []
    c = 0
    d = 0b00000000

    for b in data:
        if (b & 0b10000000 == 1):
            b -= 0b10000000
            d += 2**c
        outArray.append(b)
        c += 1
        if (c > 6):
            outArray.append(d)
            c = 0
            d = 0

    if (c < 7): outArray.append(d)
    outArray = ''.join([chr(i) for i in outArray])

    resp = flask.make_response(outArray)
    resp.headers['TPACK_NUM'] = packet_num
    resp.headers['TPACK_DATA_SIZE'] = TPACK_DATA_SIZE
    resp.headers['TPACK_RESP_SIZE'] = len(outArray)
    resp.headers['ACTIVE_FILE_NAME'] = ACTIVE_FILE.name

    return resp

if __name__ == "__main__":
    app.run()
