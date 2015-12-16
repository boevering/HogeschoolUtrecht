from pysimplesoap.client import SoapClient, SoapFault

# create a simple consumer
client = SoapClient(
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    ns = False)

# call a few remote methods
r1=str(client.get_value(number=1).resultaat)
print "sys.platform =1 :", r1

r2=str(client.get_value(number=2).resultaat)
print "sys.getdefaultencoding() =2 :", r2

r3=str(client.get_value(number=3).resultaat)
print "Doet helemaal niks =3 :", int(r3) # r3 is a number!

r4=str(client.get_value(number=4).resultaat)
print "Aantal processen =4 :", r4.rstrip() # This is a multiline: strip the newline from the result!

r5=str(client.get_value(number=5).resultaat)
print "Aantal services =5 :", r5.rstrip()

r10=str(client.get_value(number=10).resultaat)
print "psutil.cpu_percent =10 :", float(r10)

r11=str(client.get_value(number=11).resultaat)
print "psutil.cpu_times().system =11 :", r11

r20=str(client.get_value(number=20).resultaat)
print "psutil.virtual_memory().percent =20 :", float(r20)