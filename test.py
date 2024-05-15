import tmk3qr as custqr



def test(string_to_test):
    qr = custqr.makeqr(string_to_test,4)
    custqr.create_image_from_array(qr,'tmpqr.png')
    qr,_,_ = custqr.image_to_2d_arrays('tmpqr.png')
    qr = custqr.read_qr('tmpqr.png')
    if string_to_test == qr:
        return 'OK'
    else:
        print(string_to_test,qr)
        return 'ERR'


for i in range(10):
    print(test(str(i)))
    