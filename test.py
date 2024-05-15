import tmk3qr as custqr
import random


def test(s1,s2,s3):
    custqr.enc(s1,s2,s3,'tmpqr.png',ver=4,s=False)
    d1,d2,d3 = custqr.dec('tmpqr.png',s=False)
    if (s1 == d1) and (s2 == d2) and (s3 == d3):
        return 'PASS'
    else:
        print(s1 == d1)
        print(s2 == d2)
        print(s3 == d3)
        print(s1,s2,s3,d1,d2,d3)
        return 'FAIL'



for i in range(10):
    print(test(str(random.randint(0,1000000)),str(random.randint(0,1000000)),str(random.randint(0,1000000))))
    