
PrivateIPv6Ranges = [
    "fc00::/7" ,
    "ff00::/8" ,
    "fe80::/10" ,
    "::1/128"
]

PrivateV6RSCFileObj = open( r"Private-v6.rsc" ,"w+" )

PrivateV6RSCFileObj.write( "/ipv6 firewall address-list\n" )

AddressListName = "Private-v6"

for PrivateIPv6Range in PrivateIPv6Ranges :
    PrivateV6RSCFileObj.write( "add address=" + PrivateIPv6Range + " list=" + AddressListName + "\n" )

PrivateV6RSCFileObj.close()
