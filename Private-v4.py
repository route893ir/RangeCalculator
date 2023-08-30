
# 172.16.0.0/12
PrivateIPv4Ranges = [
    "192.168.0.0/16" ,
    "172.16.0.0/16" ,
    "10.0.0.0/8" ,
    "169.254.0.0/16" ,
    "100.64.0.0/10" ,
    "224.0.0.0/4" ,
    "127.0.0.0/8" ,
    "0.0.0.0/8"
]

PrivateV4RSCFileObj = open( r"Private-v4.rsc" ,"w+" )

PrivateV4RSCFileObj.write( "/ip firewall address-list\n" )

AddressListName = "Private-v4"

for PrivateIPv4Range in PrivateIPv4Ranges :
    PrivateV4RSCFileObj.write( "add address=" + PrivateIPv4Range + " list=" + AddressListName + "\n" )

PrivateV4RSCFileObj.close()
