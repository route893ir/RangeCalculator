
from datetime import datetime
import os
import csv
import sys

CurrentDirectoryFiles = os.listdir()

DBIPCSVFileName = ""

for FileName in CurrentDirectoryFiles :
    if FileName.endswith( ".csv" ):
        DBIPCSVFileName = FileName

if DBIPCSVFileName == "" :
    print()
    sys.exit( " DB IP CSV File Not Found ! \n" )

Seqs = []

with open( DBIPCSVFileName ) as DBIPCSVFileObj :
    CSVReader = csv.reader( DBIPCSVFileObj , delimiter = "," )
    for CSVRow in CSVReader :
        Country = CSVRow[ 2 ]
        IPSeq = CSVRow[ 0 : 2 ]
        if Country == "IR" and ":" not in IPSeq[ 0 ] :
            Seqs.append( IPSeq )

ClassXSeqs = []
ClassASeqs = []
ClassBSeqs = []
ClassCSeqs = []

for Seq in Seqs :

    StringSeqStart = Seq[ 0 ].split( "." )
    SeqStart = []
    for StringElement in StringSeqStart :
        SeqStart.append( int( StringElement ) )

    StringSeqEnd = Seq[ 1 ].split( "." )
    SeqEnd = []
    for StringElement in StringSeqEnd :
        SeqEnd.append( int( StringElement ) )

    if SeqStart[ 0 ] != SeqEnd[ 0 ] :
        ClassXSeqs.append( [ SeqStart , SeqEnd ] )
    else :
        if SeqStart[ 1 ] != SeqEnd[ 1 ] :
            ClassASeqs.append( [ SeqStart , SeqEnd ] )
        else :
            if SeqStart[ 2 ] != SeqEnd[ 2 ] :
                ClassBSeqs.append( [ SeqStart , SeqEnd ] )
            else :
                ClassCSeqs.append( [ SeqStart , SeqEnd ] )

Blocks = [ 1 , 2 , 4 , 8 , 16 , 32 , 64 , 128 ]

ClassCCIDRs = [ "32" , "31" , "30" , "29" , "28" , "27" , "26" , "25" ]

ClassCRanges = []

def ClassC( ClassCSeq ) :
    StringClassCSeqStart = []
    for IntElement in ClassCSeq[ 0 ] :
        StringClassCSeqStart.append( str( IntElement ) )
    if ClassCSeq[ 0 ] == ClassCSeq[ 1 ] :
        ClassCRanges.append( ".".join( StringClassCSeqStart ) + "/32" )
    else :
        ClassCSeqStart = ClassCSeq[ 0 ][ 3 ]
        ClassCSeqEnd = ClassCSeq[ 1 ][ 3 ]
        if ClassCSeqStart == 0 and ClassCSeqEnd == 255 :
            ClassCRanges.append( ".".join( StringClassCSeqStart ) + "/24" )
        else :
            ClassCPrefix = ( "." ).join( StringClassCSeqStart[ 0 : 3 ] ) + "."
            while ClassCSeqStart <= ClassCSeqEnd :
                ClassCDistance = ( ClassCSeqEnd - ClassCSeqStart ) + 1

                ClassCBlock = 1
                for Block in Blocks :
                    NextBlock = Block * 2
                    if ClassCSeqStart % NextBlock != 0 or NextBlock > ClassCDistance :
                        ClassCBlock = Block
                        break

                ClassCCIDR = ClassCCIDRs[ Blocks.index( ClassCBlock ) ]
                ClassCRanges.append( ClassCPrefix + str( ClassCSeqStart ) + "/" + ClassCCIDR )
                ClassCSeqStart = ClassCSeqStart + ClassCBlock

                
for ClassCSeq in ClassCSeqs :
    ClassC( ClassCSeq )

ClassBCIDRs = [ "24" , "23" , "22" , "21" , "20" , "19" , "18" , "17" ]

ClassBRanges = []

def ClassB( ClassBSeq ) :
    StringClassBSeqStart = []
    for IntElement in ClassBSeq[ 0 ] :
        StringClassBSeqStart.append( str( IntElement ) )
    ClassBSeqStart = ClassBSeq[ 0 ][ 2 ]
    ClassBSeqEnd = ClassBSeq[ 1 ][ 2 ]
    ClassCSeqStart = ClassBSeq[ 0 ][ 3 ]
    ClassCSeqEnd = ClassBSeq[ 1 ][ 3 ]
    if ( ClassBSeqStart == ClassCSeqStart == 0 ) and ( ClassBSeqEnd == ClassCSeqEnd == 255 ) :
        ClassBRanges.append( ( "." ).join( StringClassBSeqStart ) + "/16" )
    else :
        if ClassCSeqStart != 0 :
            ClassCSubSeqStart = ClassBSeq[ 0 ]
            ClassC( [ ClassCSubSeqStart , [ ClassCSubSeqStart[ 0 ] , ClassCSubSeqStart[ 1 ] , ClassCSubSeqStart[ 2 ] , 255 ] ] )
            ClassBSeqStart = ClassBSeqStart + 1

        if ClassCSeqEnd != 255 :
            ClassCSubSeqEnd = ClassBSeq[ 1 ]
            ClassC( [ [ ClassCSubSeqEnd[ 0 ] , ClassCSubSeqEnd[ 1 ] , ClassCSubSeqEnd[ 2 ] , 0 ] , ClassCSubSeqEnd ] )
            ClassBSeqEnd = ClassBSeqEnd - 1

        ClassBPrefix = ( "." ).join( StringClassBSeqStart[ 0 : 2 ] ) + "."

        while ClassBSeqStart <= ClassBSeqEnd :

            ClassBDistance = ( ClassBSeqEnd - ClassBSeqStart ) + 1

            ClassBBlock = 1
            for Block in Blocks :
                NextBlock = Block * 2
                if ClassBSeqStart % NextBlock != 0 or NextBlock > ClassBDistance :
                    ClassBBlock = Block
                    break

            ClassBCIDR = ClassBCIDRs[ Blocks.index( ClassBBlock ) ]
            ClassBRanges.append( ClassBPrefix + str( ClassBSeqStart ) + ".0" + "/" + ClassBCIDR )
            ClassBSeqStart = ClassBSeqStart + ClassBBlock

for ClassBSeq in ClassBSeqs :
    ClassB( ClassBSeq )

ClassACIDRs = [ "16" , "15" , "14" , "13" , "12" , "11" , "10" , "9" ]
ClassARanges = []

def ClassA( ClassASeq ) :

    StringClassASeqStart = []
    for IntElement in ClassASeq[ 0 ] :
        StringClassASeqStart.append( str( IntElement ) )
    
    ClassCSeqStart = ClassASeq[ 0 ][ 3 ]
    ClassCSeqEnd = ClassASeq[ 1 ][ 3 ]
    ClassBSeqStart = ClassASeq[ 0 ][ 2 ]
    ClassBSeqEnd = ClassASeq[ 1 ][ 2 ]
    ClassASeqStart = ClassASeq[ 0 ][ 1 ]
    ClassASeqEnd = ClassASeq[ 1 ][ 1 ]

    if ( ClassASeqStart == ClassBSeqStart == ClassCSeqStart == 0 ) and ( ClassASeqEnd == ClassBSeqEnd == ClassCSeqEnd == 255 ) :
        ClassARanges.append( ( "." ).join( StringClassASeqStart ) + "/8" )
    else :

        if ClassBSeqStart != 0 :
            ClassBSubSeqStart = ClassASeq[ 0 ]

            ClassB( [ ClassBSubSeqStart , [ ClassBSubSeqStart[ 0 ] , ClassBSubSeqStart[ 1 ] , 255 , 255 ] ] )
            ClassASeqStart = ClassASeqStart + 1
        
        if ClassBSeqEnd != 255 :
            ClassBSubSeqEnd = ClassASeq[ 1 ]
            ClassB( [ [ ClassBSubSeqEnd[ 0 ] , ClassBSubSeqEnd[ 1 ] , 0 , 0 ] , ClassBSubSeqEnd ] )
            ClassASeqEnd = ClassASeqEnd - 1
        
        ClassAPrefix = ( "." ).join( StringClassASeqStart[ 0 : 1 ] ) + "."

        while ClassASeqStart <= ClassASeqEnd :

            ClassADistance = ( ClassASeqEnd - ClassASeqStart ) + 1
            ClassABlock = 1

            for Block in Blocks :
                NextBlock = Block * 2
                if ClassASeqStart % NextBlock != 0 or NextBlock > ClassADistance :
                    ClassABlock = Block
                    break
            
            ClassACIDR = ClassACIDRs[ Blocks.index( ClassABlock ) ]
            ClassARanges.append( ClassAPrefix + str( ClassASeqStart ) + ".0.0" + "/" + ClassACIDR )
            ClassASeqStart = ClassASeqStart + ClassABlock

for ClassASeq in ClassASeqs :
    ClassA( ClassASeq )

ClassXCIDRs = [ "7" , "6" , "5" , "4" , "3" , "2" , "1" ]
ClassXRanges = []

def ClassX( ClassXSeq ) :
    
    ClassASeqStart = ClassXSeq[ 0 ][ 1 ]
    ClassASeqEnd = ClassXSeq[ 1 ][ 1 ]
    ClassXSeqStart = ClassXSeq[ 0 ][ 0 ]
    ClassXSeqEnd = ClassXSeq[ 1 ][ 0 ]


    if ClassASeqStart != 0 :
        ClassASubSeqStart = ClassXSeq[ 0 ]
        ClassA( [ ClassASubSeqStart , [ ClassASubSeqStart[ 0 ] , 255 , 255 , 255 ] ] )
        ClassXSeqStart = ClassXSeqStart + 1
        
    if ClassASeqEnd != 255 :
        ClassASubSeqEnd = ClassXSeq[ 1 ]
        ClassA( [ [ ClassASubSeqEnd[ 0 ] , 0 , 0 , 0 ] , ClassASubSeqEnd ] )
        ClassXSeqEnd = ClassXSeqEnd - 1
        

    while ClassXSeqStart <= ClassXSeqEnd :

        ClassXDistance = ( ClassXSeqEnd - ClassXSeqStart ) + 1
        ClassXBlock = 1

        for Block in Blocks :
            NextBlock = Block * 2
            if ClassXSeqStart % NextBlock != 0 or NextBlock > ClassXDistance :
                ClassXBlock = Block
                break
            
        ClassXCIDR = ClassXCIDRs[ Blocks.index( ClassXBlock ) ]
        ClassXRanges.append( str( ClassXSeqStart ) + ".0.0.0" + "/" + ClassXCIDR )
        ClassXSeqStart = ClassXSeqStart + ClassXBlock

for ClassXSeq in ClassXSeqs :
    ClassX( ClassXSeq )

Ranges = []

Ranges.extend( ClassXRanges )

Ranges.extend( ClassARanges )

Ranges.extend( ClassBRanges )

Ranges.extend( ClassCRanges )

def RangeCIDR( Range ) :
    CIDR = int( ( Range.split( "/" ) )[ 1 ] )
    return ( CIDR )

Ranges.sort( key=RangeCIDR )

AddressListName = "Iran-v4-" + DBIPCSVFileName[ -9 : -4 ]

IranV4RSCFileObj = open( AddressListName + ".rsc" ,"w+" )

IranV4RSCFileObj.write( "/ip firewall address-list\n" )

for Range in Ranges :
    IranV4RSCFileObj.write( "add address=" + Range + " list=" + AddressListName + "\n" )

IranV4RSCFileObj.close()
