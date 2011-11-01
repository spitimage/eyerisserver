from pyQR import *

qr = QRCode(10, QRErrorCorrectLevel.M)
# 213 is the max length for this setting and encoding
# See http://www.denso-wave.com/qrcode/vertable1-e.html
data = '7' * 213
print data
print len(data)
qr.addData(data)
qr.make()

im = qr.makeImage()

im.save('out.jpg')

#im.show()
