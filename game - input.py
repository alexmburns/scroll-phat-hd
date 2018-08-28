import signal
import time
import scrollphathd as sphd

name = raw_input("What is your name? ")
location = raw_input("Where do you live? ")
colour = raw_input("What is your favourite colour? ")

sphd.write_string("  Ah, so your name is %s, you come from %s " \
"and your favourite colour is %s." % (name, location, colour))

while True:
    sphd.show()
    sphd.scroll(1)
    time.sleep(0.05)
