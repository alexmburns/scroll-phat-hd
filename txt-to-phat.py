#prints the contents of test.txt into Scroll pHat HD, remember to change directory to be valid.
import signal
import time

import scrollphathd

print("""
This should be reading your .txt file
Press Ctrl+C to exit!
""")

# Uncomment the below if your display is upside down
#scrollphathd.rotate(degrees=180)

scrollphathd.write_string(''.join(file('/home/pi/test.txt')), brightness=0.5)

# Auto scroll using a while + time mechanism (no thread)
while True:
    # Show the buffer
    scrollphathd.show()
    # Scroll the buffer content
    scrollphathd.scroll()
    # Wait for 0.1s
    time.sleep(0.1)
