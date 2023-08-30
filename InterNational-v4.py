
import os
import csv
import sys
import math

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
        if Country != "IR" and Country != "ZZ" and ":" not in IPSeq[ 0 ] :
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


RangesObj = {}

for EachCIDR in range( 1 , 33 ) :
    RangesObj[ EachCIDR ] = []

Blocks = [ 1 , 2 , 4 , 8 , 16 , 32 , 64 , 128 ]

ClassCCIDRs = [ 32 , 31 , 30 , 29 , 28 , 27 , 26 , 25 ]

def ClassC( ClassCSeq ) :
    
    if ClassCSeq[ 0 ] == ClassCSeq[ 1 ] :
        RangesObj[ 32 ].append( ClassCSeq[ 0 ] )
    else :
        ClassCSeqStart = ClassCSeq[ 0 ][ 3 ]
        ClassCSeqEnd = ClassCSeq[ 1 ][ 3 ]
        if ClassCSeqStart == 0 and ClassCSeqEnd == 255 :
            RangesObj[ 24 ].append( ClassCSeq[ 0 ] )
        else :

            ClassCPrefix = ClassCSeq[ 0 ][ 0 : 3 ]

            while ClassCSeqStart <= ClassCSeqEnd :
                ClassCDistance = ( ClassCSeqEnd - ClassCSeqStart ) + 1

                ClassCBlock = 1
                for Block in Blocks :
                    NextBlock = Block * 2
                    if ClassCSeqStart % NextBlock != 0 or NextBlock > ClassCDistance :
                        ClassCBlock = Block
                        break

                ClassCCIDR = ClassCCIDRs[ Blocks.index( ClassCBlock ) ]

                SubNetRange = [ ClassCPrefix[ 0 ] , ClassCPrefix[ 1 ] , ClassCPrefix[ 2 ] , ClassCSeqStart ]

                RangesObj[ ClassCCIDR ].append( SubNetRange )

                ClassCSeqStart = ClassCSeqStart + ClassCBlock

                
for ClassCSeq in ClassCSeqs :
    ClassC( ClassCSeq )

ClassBCIDRs = [ 24 , 23 , 22 , 21 , 20 , 19 , 18 , 17 ]

def ClassB( ClassBSeq ) :

    ClassBSeqStart = ClassBSeq[ 0 ][ 2 ]
    ClassBSeqEnd = ClassBSeq[ 1 ][ 2 ]
    ClassCSeqStart = ClassBSeq[ 0 ][ 3 ]
    ClassCSeqEnd = ClassBSeq[ 1 ][ 3 ]

    if ( ClassBSeqStart == ClassCSeqStart == 0 ) and ( ClassBSeqEnd == ClassCSeqEnd == 255 ) :
        RangesObj[ 16 ].append( ClassBSeq[ 0 ] )
    else :

        if ClassCSeqStart != 0 :
            ClassCSubSeqStart = ClassBSeq[ 0 ]
            ClassC( [ ClassCSubSeqStart , [ ClassCSubSeqStart[ 0 ] , ClassCSubSeqStart[ 1 ] , ClassCSubSeqStart[ 2 ] , 255 ] ] )
            ClassBSeqStart = ClassBSeqStart + 1

        if ClassCSeqEnd != 255 :
            ClassCSubSeqEnd = ClassBSeq[ 1 ]
            ClassC( [ [ ClassCSubSeqEnd[ 0 ] , ClassCSubSeqEnd[ 1 ] , ClassCSubSeqEnd[ 2 ] , 0 ] , ClassCSubSeqEnd ] )
            ClassBSeqEnd = ClassBSeqEnd - 1
        
        ClassBPrefix = ClassBSeq[ 0 ][ 0 : 2 ]

        while ClassBSeqStart <= ClassBSeqEnd :

            ClassBDistance = ( ClassBSeqEnd - ClassBSeqStart ) + 1

            ClassBBlock = 1
            for Block in Blocks :
                NextBlock = Block * 2
                if ClassBSeqStart % NextBlock != 0 or NextBlock > ClassBDistance :
                    ClassBBlock = Block
                    break

            ClassBCIDR = ClassBCIDRs[ Blocks.index( ClassBBlock ) ]
            RangesObj[ ClassBCIDR ].append( [ ClassBPrefix[ 0 ] , ClassBPrefix[ 1 ] , ClassBSeqStart , 0 ] )
            ClassBSeqStart = ClassBSeqStart + ClassBBlock
                
for ClassBSeq in ClassBSeqs :
    ClassB( ClassBSeq )

ClassACIDRs = [ 16 , 15 , 14 , 13 , 12 , 11 , 10 , 9 ]

def ClassA( ClassASeq ) :
    
    ClassCSeqStart = ClassASeq[ 0 ][ 3 ]
    ClassCSeqEnd = ClassASeq[ 1 ][ 3 ]
    ClassBSeqStart = ClassASeq[ 0 ][ 2 ]
    ClassBSeqEnd = ClassASeq[ 1 ][ 2 ]
    ClassASeqStart = ClassASeq[ 0 ][ 1 ]
    ClassASeqEnd = ClassASeq[ 1 ][ 1 ]

    if ( ClassASeqStart == ClassBSeqStart == ClassCSeqStart == 0 ) and ( ClassASeqEnd == ClassBSeqEnd == ClassCSeqEnd == 255 ) :
        RangesObj[ 8 ].append( ClassASeq[ 0 ] )
    else :

        if ClassBSeqStart != 0 :
            ClassBSubSeqStart = ClassASeq[ 0 ]
            ClassB( [ ClassBSubSeqStart , [ ClassBSubSeqStart[ 0 ] , ClassBSubSeqStart[ 1 ] , 255 , 255 ] ] )
            ClassASeqStart = ClassASeqStart + 1
        
        if ClassBSeqEnd != 255 :
            ClassBSubSeqEnd = ClassASeq[ 1 ]
            ClassB( [ [ ClassBSubSeqEnd[ 0 ] , ClassBSubSeqEnd[ 1 ] , 0 , 0 ] , ClassBSubSeqEnd ] )
            ClassASeqEnd = ClassASeqEnd - 1
        
        ClassAPrefix = ClassASeq[ 0 ][ 0 : 1 ]

        while ClassASeqStart <= ClassASeqEnd :

            ClassADistance = ( ClassASeqEnd - ClassASeqStart ) + 1
            ClassABlock = 1

            for Block in Blocks :
                NextBlock = Block * 2
                if ClassASeqStart % NextBlock != 0 or NextBlock > ClassADistance :
                    ClassABlock = Block
                    break
            
            ClassACIDR = ClassACIDRs[ Blocks.index( ClassABlock ) ]
            RangesObj[ ClassACIDR ].append( [ ClassAPrefix[ 0 ] , ClassASeqStart , 0 , 0 ] )
            ClassASeqStart = ClassASeqStart + ClassABlock

for ClassASeq in ClassASeqs :
    ClassA( ClassASeq )

ClassXCIDRs = [ 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 ]

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
        RangesObj[ ClassXCIDR ].append( [ ClassXSeqStart , 0 , 0 , 0 ] )
        ClassXSeqStart = ClassXSeqStart + ClassXBlock

for ClassXSeq in ClassXSeqs :
    ClassX( ClassXSeq )

print( " Raw Ranges : " )

RawRangesTotal = 0
for RangeCIDR in range( 1 , 33 ) :
    SameCIDRRangesNumber = len( RangesObj[ RangeCIDR ] )
    print( " /" + str( RangeCIDR ) + " Ranges : " + str( SameCIDRRangesNumber ) )
    RawRangesTotal = RawRangesTotal + SameCIDRRangesNumber 

print( " Total Raw Ranges : " + str( RawRangesTotal ) )
print()

for CurrentCIDR in reversed( range( 2 , 33 ) ) :

    SameCIDRRanges = RangesObj[ CurrentCIDR ]

    if CurrentCIDR in [ 32 , 24 , 16 , 8 ] :
        PrefixBytes = math.trunc( CurrentCIDR / 8 ) - 1
        RangeBlock = 1
    else :
        PrefixBytes = math.trunc( CurrentCIDR / 8 )
        RangeBlock = pow( 2 , ( 8 - ( CurrentCIDR % 8 ) ) )

    for CurrentRange in SameCIDRRanges :

        CurrentRangePrefix = CurrentRange[ : PrefixBytes ]
        CurrentRangeID = CurrentRange[ PrefixBytes ]

        for SameCIDRRange in SameCIDRRanges :

            if CurrentRange != SameCIDRRange :

                SameCIDRRangePrefix = SameCIDRRange[ : PrefixBytes ]
                SameCIDRRangeID = SameCIDRRange[ PrefixBytes ]
                SameCIDRRangesDistance = abs( CurrentRangeID - SameCIDRRangeID )

                if CurrentRangeID < SameCIDRRangeID :
                    TargetRange = CurrentRange
                else :
                    TargetRange = SameCIDRRange
                
                TargetRangeID = TargetRange[ PrefixBytes ]

                if CurrentRangePrefix == SameCIDRRangePrefix and SameCIDRRangesDistance == RangeBlock and TargetRangeID % ( RangeBlock * 2 ) == 0 :

                    RangesObj[ CurrentCIDR ].remove( CurrentRange )
                    RangesObj[ CurrentCIDR ].remove( SameCIDRRange )
                    
                    RangesObj[ CurrentCIDR - 1 ].append( TargetRange )
    
    print()
    print( " /" + str( CurrentCIDR ) + " Ranges Optimized !" )
    print( " /" + str( CurrentCIDR ) + " Ranges : " + str( len( RangesObj[ CurrentCIDR ]) ) )

print( " Optimized Ranges : " )

OptimizedRangesTotal = 0
for RangeCIDR in range( 1 , 33 ) :
    SameCIDRRangesNumber = len( RangesObj[ RangeCIDR ] )
    print( " /" + str( RangeCIDR ) + " Ranges : " + str( SameCIDRRangesNumber ) )
    OptimizedRanges = OptimizedRangesTotal + SameCIDRRangesNumber 

print( " Total Optimized Ranges : " + str( OptimizedRangesTotal ) )
print()

Ranges = []

for RangeCIDR in range( 1 , 33 ) :
    for Range in RangesObj[ RangeCIDR ] :
        StringRangeArray = []
        for IntByte in Range :
            StringRange.append( str( IntByte ) )
        StringRange = ".".join( StringRangeArray ) + "/" + str( RangeCIDR )
        Ranges.append( StringRange )

AddressListName = "InterNational-v4-" + DBIPCSVFileName[ -9 : -4 ]

InterNationalV4RSCFileObj = open( AddressListName + ".rsc" ,"w+" )

InterNationalV4RSCFileObj.write( "/ip firewall address-list\n" )

for Range in Ranges :
    InterNationalV4RSCFileObj.write( "add address=" + Range + " list=" + AddressListName + "\n" )

InterNationalV4RSCFileObj.close()  
