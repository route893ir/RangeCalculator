
from datetime import datetime
import sys
import os

CurrentDirectoryFiles = os.listdir() 

if "cidr.txt" not in CurrentDirectoryFiles :
    print()
    print( sys.exit( " Telegram CIDR File Not Found !\n" ) )

TelegramRangesFileObj = open( "cidr.txt" , "r" )

TelegramRangesLines = TelegramRangesFileObj.readlines()

TelegramIPv6Ranges = []

for TelegramRangeLine in TelegramRangesLines :
    if ":" in TelegramRangeLine :
        TelegramIPv6Ranges.append( TelegramRangeLine )

TimeStamp = datetime.today().strftime( "%Y-%m" )

AddressListName = "Telegram-v6-" + TimeStamp

TelegramV6RSCFileObj = open( AddressListName + ".rsc" ,"w+" )

TelegramV6RSCFileObj.write( "/ipv6 firewall address-list\n" )

def TelegramRangeCIDR( TelegramRange ) :
    return int( ( TelegramRange.split( "/" ) )[ 1 ] )

TelegramIPv6Ranges.sort( key=TelegramRangeCIDR )

for TelegramIPv6Range in TelegramIPv6Ranges :
    TelegramV6RSCFileObj.write( "add address=" + TelegramIPv6Range.rstrip( "\n\r" ) + " list=" + AddressListName + "\n" )

TelegramV6RSCFileObj.close()
