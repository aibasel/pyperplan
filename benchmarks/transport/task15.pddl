; Transport two-cities-sequential-10nodes-1000size-3degree-100mindistance-2trucks-6packages-2008seed

(define (problem transport-two-cities-sequential-10nodes-1000size-3degree-100mindistance-2trucks-6packages-2008seed)
 (:domain transport)
 (:objects
  city-1-loc-1 - location
  city-2-loc-1 - location
  city-1-loc-2 - location
  city-2-loc-2 - location
  city-1-loc-3 - location
  city-2-loc-3 - location
  city-1-loc-4 - location
  city-2-loc-4 - location
  city-1-loc-5 - location
  city-2-loc-5 - location
  city-1-loc-6 - location
  city-2-loc-6 - location
  city-1-loc-7 - location
  city-2-loc-7 - location
  city-1-loc-8 - location
  city-2-loc-8 - location
  city-1-loc-9 - location
  city-2-loc-9 - location
  city-1-loc-10 - location
  city-2-loc-10 - location
  truck-1 - vehicle
  truck-2 - vehicle
  package-1 - package
  package-2 - package
  package-3 - package
  package-4 - package
  package-5 - package
  package-6 - package
  capacity-0 - capacity-number
  capacity-1 - capacity-number
  capacity-2 - capacity-number
  capacity-3 - capacity-number
  capacity-4 - capacity-number
 )
 (:init
  
  (capacity-predecessor capacity-0 capacity-1)
  (capacity-predecessor capacity-1 capacity-2)
  (capacity-predecessor capacity-2 capacity-3)
  (capacity-predecessor capacity-3 capacity-4)
  ; 748,385 -> 890,543
  (road city-1-loc-3 city-1-loc-1)
  
  ; 890,543 -> 748,385
  (road city-1-loc-1 city-1-loc-3)
  
  ; 912,799 -> 890,543
  (road city-1-loc-4 city-1-loc-1)
  
  ; 890,543 -> 912,799
  (road city-1-loc-1 city-1-loc-4)
  
  ; 977,899 -> 890,543
  (road city-1-loc-5 city-1-loc-1)
  
  ; 890,543 -> 977,899
  (road city-1-loc-1 city-1-loc-5)
  
  ; 977,899 -> 912,799
  (road city-1-loc-5 city-1-loc-4)
  
  ; 912,799 -> 977,899
  (road city-1-loc-4 city-1-loc-5)
  
  ; 456,221 -> 384,50
  (road city-1-loc-6 city-1-loc-2)
  
  ; 384,50 -> 456,221
  (road city-1-loc-2 city-1-loc-6)
  
  ; 456,221 -> 748,385
  (road city-1-loc-6 city-1-loc-3)
  
  ; 748,385 -> 456,221
  (road city-1-loc-3 city-1-loc-6)
  
  ; 742,542 -> 890,543
  (road city-1-loc-7 city-1-loc-1)
  
  ; 890,543 -> 742,542
  (road city-1-loc-1 city-1-loc-7)
  
  ; 742,542 -> 748,385
  (road city-1-loc-7 city-1-loc-3)
  
  ; 748,385 -> 742,542
  (road city-1-loc-3 city-1-loc-7)
  
  ; 742,542 -> 912,799
  (road city-1-loc-7 city-1-loc-4)
  
  ; 912,799 -> 742,542
  (road city-1-loc-4 city-1-loc-7)
  
  ; 564,783 -> 912,799
  (road city-1-loc-8 city-1-loc-4)
  
  ; 912,799 -> 564,783
  (road city-1-loc-4 city-1-loc-8)
  
  ; 564,783 -> 742,542
  (road city-1-loc-8 city-1-loc-7)
  
  ; 742,542 -> 564,783
  (road city-1-loc-7 city-1-loc-8)
  
  ; 273,425 -> 456,221
  (road city-1-loc-9 city-1-loc-6)
  
  ; 456,221 -> 273,425
  (road city-1-loc-6 city-1-loc-9)
  
  ; 566,552 -> 890,543
  (road city-1-loc-10 city-1-loc-1)
  
  ; 890,543 -> 566,552
  (road city-1-loc-1 city-1-loc-10)
  
  ; 566,552 -> 748,385
  (road city-1-loc-10 city-1-loc-3)
  
  ; 748,385 -> 566,552
  (road city-1-loc-3 city-1-loc-10)
  
  ; 566,552 -> 456,221
  (road city-1-loc-10 city-1-loc-6)
  
  ; 456,221 -> 566,552
  (road city-1-loc-6 city-1-loc-10)
  
  ; 566,552 -> 742,542
  (road city-1-loc-10 city-1-loc-7)
  
  ; 742,542 -> 566,552
  (road city-1-loc-7 city-1-loc-10)
  
  ; 566,552 -> 564,783
  (road city-1-loc-10 city-1-loc-8)
  
  ; 564,783 -> 566,552
  (road city-1-loc-8 city-1-loc-10)
  
  ; 566,552 -> 273,425
  (road city-1-loc-10 city-1-loc-9)
  
  ; 273,425 -> 566,552
  (road city-1-loc-9 city-1-loc-10)
  
  ; 2170,709 -> 2336,475
  (road city-2-loc-2 city-2-loc-1)
  
  ; 2336,475 -> 2170,709
  (road city-2-loc-1 city-2-loc-2)
  
  ; 2521,375 -> 2336,475
  (road city-2-loc-3 city-2-loc-1)
  
  ; 2336,475 -> 2521,375
  (road city-2-loc-1 city-2-loc-3)
  
  ; 2316,237 -> 2336,475
  (road city-2-loc-5 city-2-loc-1)
  
  ; 2336,475 -> 2316,237
  (road city-2-loc-1 city-2-loc-5)
  
  ; 2316,237 -> 2521,375
  (road city-2-loc-5 city-2-loc-3)
  
  ; 2521,375 -> 2316,237
  (road city-2-loc-3 city-2-loc-5)
  
  ; 2720,241 -> 2521,375
  (road city-2-loc-6 city-2-loc-3)
  
  ; 2521,375 -> 2720,241
  (road city-2-loc-3 city-2-loc-6)
  
  ; 2720,241 -> 2701,0
  (road city-2-loc-6 city-2-loc-4)
  
  ; 2701,0 -> 2720,241
  (road city-2-loc-4 city-2-loc-6)
  
  ; 2630,722 -> 2521,375
  (road city-2-loc-7 city-2-loc-3)
  
  ; 2521,375 -> 2630,722
  (road city-2-loc-3 city-2-loc-7)
  
  ; 2120,854 -> 2170,709
  (road city-2-loc-8 city-2-loc-2)
  
  ; 2170,709 -> 2120,854
  (road city-2-loc-2 city-2-loc-8)
  
  ; 2171,545 -> 2336,475
  (road city-2-loc-9 city-2-loc-1)
  
  ; 2336,475 -> 2171,545
  (road city-2-loc-1 city-2-loc-9)
  
  ; 2171,545 -> 2170,709
  (road city-2-loc-9 city-2-loc-2)
  
  ; 2170,709 -> 2171,545
  (road city-2-loc-2 city-2-loc-9)
  
  ; 2171,545 -> 2316,237
  (road city-2-loc-9 city-2-loc-5)
  
  ; 2316,237 -> 2171,545
  (road city-2-loc-5 city-2-loc-9)
  
  ; 2171,545 -> 2120,854
  (road city-2-loc-9 city-2-loc-8)
  
  ; 2120,854 -> 2171,545
  (road city-2-loc-8 city-2-loc-9)
  
  ; 2348,607 -> 2336,475
  (road city-2-loc-10 city-2-loc-1)
  
  ; 2336,475 -> 2348,607
  (road city-2-loc-1 city-2-loc-10)
  
  ; 2348,607 -> 2170,709
  (road city-2-loc-10 city-2-loc-2)
  
  ; 2170,709 -> 2348,607
  (road city-2-loc-2 city-2-loc-10)
  
  ; 2348,607 -> 2521,375
  (road city-2-loc-10 city-2-loc-3)
  
  ; 2521,375 -> 2348,607
  (road city-2-loc-3 city-2-loc-10)
  
  ; 2348,607 -> 2630,722
  (road city-2-loc-10 city-2-loc-7)
  
  ; 2630,722 -> 2348,607
  (road city-2-loc-7 city-2-loc-10)
  
  ; 2348,607 -> 2120,854
  (road city-2-loc-10 city-2-loc-8)
  
  ; 2120,854 -> 2348,607
  (road city-2-loc-8 city-2-loc-10)
  
  ; 2348,607 -> 2171,545
  (road city-2-loc-10 city-2-loc-9)
  
  ; 2171,545 -> 2348,607
  (road city-2-loc-9 city-2-loc-10)
  
  ; 977,899 <-> 2120,854
  (road city-1-loc-5 city-2-loc-8)
  
  (road city-2-loc-8 city-1-loc-5)
  
  (at package-1 city-1-loc-4)
  (at package-2 city-1-loc-8)
  (at package-3 city-1-loc-7)
  (at package-4 city-1-loc-7)
  (at package-5 city-1-loc-4)
  (at package-6 city-1-loc-6)
  (at truck-1 city-2-loc-4)
  (capacity truck-1 capacity-2)
  (at truck-2 city-2-loc-6)
  (capacity truck-2 capacity-4)
 )
 (:goal (and
  (at package-1 city-2-loc-1)
  (at package-2 city-2-loc-3)
  (at package-3 city-2-loc-9)
  (at package-4 city-2-loc-2)
  (at package-5 city-2-loc-1)
  (at package-6 city-2-loc-6)
 ))
 
)
