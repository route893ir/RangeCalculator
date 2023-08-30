
from datetime import datetime
import sys
import os

CurrentDirectoryFiles = os.listdir() 

if "cidr.txt" not in CurrentDirectoryFiles :
    print()
    print( sys.exit( " Telegram CIDR File Not Found !\n" ) )

TelegramRangesFileObj = open( "cidr.txt" , "r" )

TelegramRangeLines = TelegramRangesFileObj.readlines()

TelegramRanges = []

for TelegramRangeLine in TelegramRangeLines :
    if ":" not in TelegramRangeLine :
        TelegramRanges.append( TelegramRangeLine )

TimeStamp = datetime.today().strftime( "%Y-%m" )

AddressListName = "Telegram-v4-" + TimeStamp

TelegramV4RSCFileObj = open( AddressListName + ".rsc" ,"w+" )

TelegramV4RSCFileObj.write( "/ip firewall address-list\n" )

def TelegramRangeCIDR( TelegramRange ) :
    return int( ( TelegramRange.split( "/" ) )[ 1 ] )

TelegramRanges.sort( key=TelegramRangeCIDR )

for TelegramRange in TelegramRanges :
    TelegramV4RSCFileObj.write( "add address=" + TelegramRange.rstrip( "\n\r" ) + " list=" + AddressListName + "\n" )

TelegramV4RSCFileObj.close()
