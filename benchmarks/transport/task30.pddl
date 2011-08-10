; Transport three-cities-sequential-10nodes-1000size-4degree-100mindistance-3trucks-11packages-2008seed

(define (problem transport-three-cities-sequential-10nodes-1000size-4degree-100mindistance-3trucks-11packages-2008seed)
 (:domain transport)
 (:objects
  city-1-loc-1 - location
  city-2-loc-1 - location
  city-3-loc-1 - location
  city-1-loc-2 - location
  city-2-loc-2 - location
  city-3-loc-2 - location
  city-1-loc-3 - location
  city-2-loc-3 - location
  city-3-loc-3 - location
  city-1-loc-4 - location
  city-2-loc-4 - location
  city-3-loc-4 - location
  city-1-loc-5 - location
  city-2-loc-5 - location
  city-3-loc-5 - location
  city-1-loc-6 - location
  city-2-loc-6 - location
  city-3-loc-6 - location
  city-1-loc-7 - location
  city-2-loc-7 - location
  city-3-loc-7 - location
  city-1-loc-8 - location
  city-2-loc-8 - location
  city-3-loc-8 - location
  city-1-loc-9 - location
  city-2-loc-9 - location
  city-3-loc-9 - location
  city-1-loc-10 - location
  city-2-loc-10 - location
  city-3-loc-10 - location
  truck-1 - vehicle
  truck-2 - vehicle
  truck-3 - vehicle
  package-1 - package
  package-2 - package
  package-3 - package
  package-4 - package
  package-5 - package
  package-6 - package
  package-7 - package
  package-8 - package
  package-9 - package
  package-10 - package
  package-11 - package
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
  
  ; 742,542 -> 977,899
  (road city-1-loc-7 city-1-loc-5)
  
  ; 977,899 -> 742,542
  (road city-1-loc-5 city-1-loc-7)
  
  ; 564,783 -> 890,543
  (road city-1-loc-8 city-1-loc-1)
  
  ; 890,543 -> 564,783
  (road city-1-loc-1 city-1-loc-8)
  
  ; 564,783 -> 912,799
  (road city-1-loc-8 city-1-loc-4)
  
  ; 912,799 -> 564,783
  (road city-1-loc-4 city-1-loc-8)
  
  ; 564,783 -> 742,542
  (road city-1-loc-8 city-1-loc-7)
  
  ; 742,542 -> 564,783
  (road city-1-loc-7 city-1-loc-8)
  
  ; 273,425 -> 384,50
  (road city-1-loc-9 city-1-loc-2)
  
  ; 384,50 -> 273,425
  (road city-1-loc-2 city-1-loc-9)
  
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
  
  ; 566,552 -> 912,799
  (road city-1-loc-10 city-1-loc-4)
  
  ; 912,799 -> 566,552
  (road city-1-loc-4 city-1-loc-10)
  
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
  
  ; 2362,862 -> 2589,754
  (road city-2-loc-3 city-2-loc-1)
  
  ; 2589,754 -> 2362,862
  (road city-2-loc-1 city-2-loc-3)
  
  ; 2748,863 -> 2589,754
  (road city-2-loc-4 city-2-loc-1)
  
  ; 2589,754 -> 2748,863
  (road city-2-loc-1 city-2-loc-4)
  
  ; 2748,863 -> 2362,862
  (road city-2-loc-4 city-2-loc-3)
  
  ; 2362,862 -> 2748,863
  (road city-2-loc-3 city-2-loc-4)
  
  ; 2006,60 -> 2053,153
  (road city-2-loc-5 city-2-loc-2)
  
  ; 2053,153 -> 2006,60
  (road city-2-loc-2 city-2-loc-5)
  
  ; 2659,497 -> 2589,754
  (road city-2-loc-6 city-2-loc-1)
  
  ; 2589,754 -> 2659,497
  (road city-2-loc-1 city-2-loc-6)
  
  ; 2659,497 -> 2748,863
  (road city-2-loc-6 city-2-loc-4)
  
  ; 2748,863 -> 2659,497
  (road city-2-loc-4 city-2-loc-6)
  
  ; 2257,5 -> 2053,153
  (road city-2-loc-7 city-2-loc-2)
  
  ; 2053,153 -> 2257,5
  (road city-2-loc-2 city-2-loc-7)
  
  ; 2257,5 -> 2006,60
  (road city-2-loc-7 city-2-loc-5)
  
  ; 2006,60 -> 2257,5
  (road city-2-loc-5 city-2-loc-7)
  
  ; 2245,346 -> 2053,153
  (road city-2-loc-8 city-2-loc-2)
  
  ; 2053,153 -> 2245,346
  (road city-2-loc-2 city-2-loc-8)
  
  ; 2245,346 -> 2006,60
  (road city-2-loc-8 city-2-loc-5)
  
  ; 2006,60 -> 2245,346
  (road city-2-loc-5 city-2-loc-8)
  
  ; 2245,346 -> 2257,5
  (road city-2-loc-8 city-2-loc-7)
  
  ; 2257,5 -> 2245,346
  (road city-2-loc-7 city-2-loc-8)
  
  ; 2559,565 -> 2589,754
  (road city-2-loc-9 city-2-loc-1)
  
  ; 2589,754 -> 2559,565
  (road city-2-loc-1 city-2-loc-9)
  
  ; 2559,565 -> 2362,862
  (road city-2-loc-9 city-2-loc-3)
  
  ; 2362,862 -> 2559,565
  (road city-2-loc-3 city-2-loc-9)
  
  ; 2559,565 -> 2748,863
  (road city-2-loc-9 city-2-loc-4)
  
  ; 2748,863 -> 2559,565
  (road city-2-loc-4 city-2-loc-9)
  
  ; 2559,565 -> 2659,497
  (road city-2-loc-9 city-2-loc-6)
  
  ; 2659,497 -> 2559,565
  (road city-2-loc-6 city-2-loc-9)
  
  ; 2559,565 -> 2245,346
  (road city-2-loc-9 city-2-loc-8)
  
  ; 2245,346 -> 2559,565
  (road city-2-loc-8 city-2-loc-9)
  
  ; 2347,149 -> 2053,153
  (road city-2-loc-10 city-2-loc-2)
  
  ; 2053,153 -> 2347,149
  (road city-2-loc-2 city-2-loc-10)
  
  ; 2347,149 -> 2006,60
  (road city-2-loc-10 city-2-loc-5)
  
  ; 2006,60 -> 2347,149
  (road city-2-loc-5 city-2-loc-10)
  
  ; 2347,149 -> 2257,5
  (road city-2-loc-10 city-2-loc-7)
  
  ; 2257,5 -> 2347,149
  (road city-2-loc-7 city-2-loc-10)
  
  ; 2347,149 -> 2245,346
  (road city-2-loc-10 city-2-loc-8)
  
  ; 2245,346 -> 2347,149
  (road city-2-loc-8 city-2-loc-10)
  
  ; 1170,2709 -> 1336,2475
  (road city-3-loc-2 city-3-loc-1)
  
  ; 1336,2475 -> 1170,2709
  (road city-3-loc-1 city-3-loc-2)
  
  ; 1521,2375 -> 1336,2475
  (road city-3-loc-3 city-3-loc-1)
  
  ; 1336,2475 -> 1521,2375
  (road city-3-loc-1 city-3-loc-3)
  
  ; 1701,2000 -> 1521,2375
  (road city-3-loc-4 city-3-loc-3)
  
  ; 1521,2375 -> 1701,2000
  (road city-3-loc-3 city-3-loc-4)
  
  ; 1316,2237 -> 1336,2475
  (road city-3-loc-5 city-3-loc-1)
  
  ; 1336,2475 -> 1316,2237
  (road city-3-loc-1 city-3-loc-5)
  
  ; 1316,2237 -> 1521,2375
  (road city-3-loc-5 city-3-loc-3)
  
  ; 1521,2375 -> 1316,2237
  (road city-3-loc-3 city-3-loc-5)
  
  ; 1720,2241 -> 1521,2375
  (road city-3-loc-6 city-3-loc-3)
  
  ; 1521,2375 -> 1720,2241
  (road city-3-loc-3 city-3-loc-6)
  
  ; 1720,2241 -> 1701,2000
  (road city-3-loc-6 city-3-loc-4)
  
  ; 1701,2000 -> 1720,2241
  (road city-3-loc-4 city-3-loc-6)
  
  ; 1720,2241 -> 1316,2237
  (road city-3-loc-6 city-3-loc-5)
  
  ; 1316,2237 -> 1720,2241
  (road city-3-loc-5 city-3-loc-6)
  
  ; 1630,2722 -> 1336,2475
  (road city-3-loc-7 city-3-loc-1)
  
  ; 1336,2475 -> 1630,2722
  (road city-3-loc-1 city-3-loc-7)
  
  ; 1630,2722 -> 1521,2375
  (road city-3-loc-7 city-3-loc-3)
  
  ; 1521,2375 -> 1630,2722
  (road city-3-loc-3 city-3-loc-7)
  
  ; 1120,2854 -> 1170,2709
  (road city-3-loc-8 city-3-loc-2)
  
  ; 1170,2709 -> 1120,2854
  (road city-3-loc-2 city-3-loc-8)
  
  ; 1171,2545 -> 1336,2475
  (road city-3-loc-9 city-3-loc-1)
  
  ; 1336,2475 -> 1171,2545
  (road city-3-loc-1 city-3-loc-9)
  
  ; 1171,2545 -> 1170,2709
  (road city-3-loc-9 city-3-loc-2)
  
  ; 1170,2709 -> 1171,2545
  (road city-3-loc-2 city-3-loc-9)
  
  ; 1171,2545 -> 1521,2375
  (road city-3-loc-9 city-3-loc-3)
  
  ; 1521,2375 -> 1171,2545
  (road city-3-loc-3 city-3-loc-9)
  
  ; 1171,2545 -> 1316,2237
  (road city-3-loc-9 city-3-loc-5)
  
  ; 1316,2237 -> 1171,2545
  (road city-3-loc-5 city-3-loc-9)
  
  ; 1171,2545 -> 1120,2854
  (road city-3-loc-9 city-3-loc-8)
  
  ; 1120,2854 -> 1171,2545
  (road city-3-loc-8 city-3-loc-9)
  
  ; 1348,2607 -> 1336,2475
  (road city-3-loc-10 city-3-loc-1)
  
  ; 1336,2475 -> 1348,2607
  (road city-3-loc-1 city-3-loc-10)
  
  ; 1348,2607 -> 1170,2709
  (road city-3-loc-10 city-3-loc-2)
  
  ; 1170,2709 -> 1348,2607
  (road city-3-loc-2 city-3-loc-10)
  
  ; 1348,2607 -> 1521,2375
  (road city-3-loc-10 city-3-loc-3)
  
  ; 1521,2375 -> 1348,2607
  (road city-3-loc-3 city-3-loc-10)
  
  ; 1348,2607 -> 1316,2237
  (road city-3-loc-10 city-3-loc-5)
  
  ; 1316,2237 -> 1348,2607
  (road city-3-loc-5 city-3-loc-10)
  
  ; 1348,2607 -> 1630,2722
  (road city-3-loc-10 city-3-loc-7)
  
  ; 1630,2722 -> 1348,2607
  (road city-3-loc-7 city-3-loc-10)
  
  ; 1348,2607 -> 1120,2854
  (road city-3-loc-10 city-3-loc-8)
  
  ; 1120,2854 -> 1348,2607
  (road city-3-loc-8 city-3-loc-10)
  
  ; 1348,2607 -> 1171,2545
  (road city-3-loc-10 city-3-loc-9)
  
  ; 1171,2545 -> 1348,2607
  (road city-3-loc-9 city-3-loc-10)
  
  ; 890,543 <-> 2006,60
  (road city-1-loc-1 city-2-loc-5)
  
  (road city-2-loc-5 city-1-loc-1)
  
  (road city-1-loc-10 city-3-loc-2)
  
  (road city-3-loc-2 city-1-loc-10)
  
  (road city-2-loc-2 city-3-loc-5)
  
  (road city-3-loc-5 city-2-loc-2)
  
  (at package-1 city-2-loc-8)
  (at package-2 city-2-loc-7)
  (at package-3 city-1-loc-6)
  (at package-4 city-2-loc-3)
  (at package-5 city-2-loc-8)
  (at package-6 city-1-loc-3)
  (at package-7 city-3-loc-2)
  (at package-8 city-1-loc-6)
  (at package-9 city-1-loc-10)
  (at package-10 city-1-loc-7)
  (at package-11 city-2-loc-3)
  (at truck-1 city-3-loc-9)
  (capacity truck-1 capacity-3)
  (at truck-2 city-2-loc-4)
  (capacity truck-2 capacity-3)
  (at truck-3 city-1-loc-9)
  (capacity truck-3 capacity-3)
 )
 (:goal (and
  (at package-1 city-3-loc-9)
  (at package-2 city-1-loc-4)
  (at package-3 city-2-loc-5)
  (at package-4 city-3-loc-9)
  (at package-5 city-1-loc-7)
  (at package-6 city-3-loc-7)
  (at package-7 city-2-loc-10)
  (at package-8 city-1-loc-2)
  (at package-9 city-2-loc-7)
  (at package-10 city-3-loc-5)
  (at package-11 city-2-loc-10)
 ))
 
)
