; Transport three-cities-sequential-6nodes-1000size-4degree-100mindistance-3trucks-7packages-2008seed

(define (problem transport-three-cities-sequential-6nodes-1000size-4degree-100mindistance-3trucks-7packages-2008seed)
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
  
  ; 748,385 -> 384,50
  (road city-1-loc-3 city-1-loc-2)
  
  ; 384,50 -> 748,385
  (road city-1-loc-2 city-1-loc-3)
  
  ; 912,799 -> 890,543
  (road city-1-loc-4 city-1-loc-1)
  
  ; 890,543 -> 912,799
  (road city-1-loc-1 city-1-loc-4)
  
  ; 912,799 -> 748,385
  (road city-1-loc-4 city-1-loc-3)
  
  ; 748,385 -> 912,799
  (road city-1-loc-3 city-1-loc-4)
  
  ; 977,899 -> 890,543
  (road city-1-loc-5 city-1-loc-1)
  
  ; 890,543 -> 977,899
  (road city-1-loc-1 city-1-loc-5)
  
  ; 977,899 -> 912,799
  (road city-1-loc-5 city-1-loc-4)
  
  ; 912,799 -> 977,899
  (road city-1-loc-4 city-1-loc-5)
  
  ; 456,221 -> 890,543
  (road city-1-loc-6 city-1-loc-1)
  
  ; 890,543 -> 456,221
  (road city-1-loc-1 city-1-loc-6)
  
  ; 456,221 -> 384,50
  (road city-1-loc-6 city-1-loc-2)
  
  ; 384,50 -> 456,221
  (road city-1-loc-2 city-1-loc-6)
  
  ; 456,221 -> 748,385
  (road city-1-loc-6 city-1-loc-3)
  
  ; 748,385 -> 456,221
  (road city-1-loc-3 city-1-loc-6)
  
  ; 2564,783 -> 2742,542
  (road city-2-loc-2 city-2-loc-1)
  
  ; 2742,542 -> 2564,783
  (road city-2-loc-1 city-2-loc-2)
  
  ; 2273,425 -> 2742,542
  (road city-2-loc-3 city-2-loc-1)
  
  ; 2742,542 -> 2273,425
  (road city-2-loc-1 city-2-loc-3)
  
  ; 2273,425 -> 2564,783
  (road city-2-loc-3 city-2-loc-2)
  
  ; 2564,783 -> 2273,425
  (road city-2-loc-2 city-2-loc-3)
  
  ; 2566,552 -> 2742,542
  (road city-2-loc-4 city-2-loc-1)
  
  ; 2742,542 -> 2566,552
  (road city-2-loc-1 city-2-loc-4)
  
  ; 2566,552 -> 2564,783
  (road city-2-loc-4 city-2-loc-2)
  
  ; 2564,783 -> 2566,552
  (road city-2-loc-2 city-2-loc-4)
  
  ; 2566,552 -> 2273,425
  (road city-2-loc-4 city-2-loc-3)
  
  ; 2273,425 -> 2566,552
  (road city-2-loc-3 city-2-loc-4)
  
  ; 2174,643 -> 2564,783
  (road city-2-loc-5 city-2-loc-2)
  
  ; 2564,783 -> 2174,643
  (road city-2-loc-2 city-2-loc-5)
  
  ; 2174,643 -> 2273,425
  (road city-2-loc-5 city-2-loc-3)
  
  ; 2273,425 -> 2174,643
  (road city-2-loc-3 city-2-loc-5)
  
  ; 2174,643 -> 2566,552
  (road city-2-loc-5 city-2-loc-4)
  
  ; 2566,552 -> 2174,643
  (road city-2-loc-4 city-2-loc-5)
  
  ; 2946,916 -> 2742,542
  (road city-2-loc-6 city-2-loc-1)
  
  ; 2742,542 -> 2946,916
  (road city-2-loc-1 city-2-loc-6)
  
  ; 2946,916 -> 2564,783
  (road city-2-loc-6 city-2-loc-2)
  
  ; 2564,783 -> 2946,916
  (road city-2-loc-2 city-2-loc-6)
  
  ; 2946,916 -> 2566,552
  (road city-2-loc-6 city-2-loc-4)
  
  ; 2566,552 -> 2946,916
  (road city-2-loc-4 city-2-loc-6)
  
  ; 1245,2346 -> 1257,2005
  (road city-3-loc-2 city-3-loc-1)
  
  ; 1257,2005 -> 1245,2346
  (road city-3-loc-1 city-3-loc-2)
  
  ; 1559,2565 -> 1245,2346
  (road city-3-loc-3 city-3-loc-2)
  
  ; 1245,2346 -> 1559,2565
  (road city-3-loc-2 city-3-loc-3)
  
  ; 1347,2149 -> 1257,2005
  (road city-3-loc-4 city-3-loc-1)
  
  ; 1257,2005 -> 1347,2149
  (road city-3-loc-1 city-3-loc-4)
  
  ; 1347,2149 -> 1245,2346
  (road city-3-loc-4 city-3-loc-2)
  
  ; 1245,2346 -> 1347,2149
  (road city-3-loc-2 city-3-loc-4)
  
  ; 1347,2149 -> 1559,2565
  (road city-3-loc-4 city-3-loc-3)
  
  ; 1559,2565 -> 1347,2149
  (road city-3-loc-3 city-3-loc-4)
  
  ; 1336,2475 -> 1257,2005
  (road city-3-loc-5 city-3-loc-1)
  
  ; 1257,2005 -> 1336,2475
  (road city-3-loc-1 city-3-loc-5)
  
  ; 1336,2475 -> 1245,2346
  (road city-3-loc-5 city-3-loc-2)
  
  ; 1245,2346 -> 1336,2475
  (road city-3-loc-2 city-3-loc-5)
  
  ; 1336,2475 -> 1559,2565
  (road city-3-loc-5 city-3-loc-3)
  
  ; 1559,2565 -> 1336,2475
  (road city-3-loc-3 city-3-loc-5)
  
  ; 1336,2475 -> 1347,2149
  (road city-3-loc-5 city-3-loc-4)
  
  ; 1347,2149 -> 1336,2475
  (road city-3-loc-4 city-3-loc-5)
  
  ; 1170,2709 -> 1245,2346
  (road city-3-loc-6 city-3-loc-2)
  
  ; 1245,2346 -> 1170,2709
  (road city-3-loc-2 city-3-loc-6)
  
  ; 1170,2709 -> 1559,2565
  (road city-3-loc-6 city-3-loc-3)
  
  ; 1559,2565 -> 1170,2709
  (road city-3-loc-3 city-3-loc-6)
  
  ; 1170,2709 -> 1336,2475
  (road city-3-loc-6 city-3-loc-5)
  
  ; 1336,2475 -> 1170,2709
  (road city-3-loc-5 city-3-loc-6)
  
  ; 977,899 <-> 2174,643
  (road city-1-loc-5 city-2-loc-5)
  
  (road city-2-loc-5 city-1-loc-5)
  
  (road city-1-loc-4 city-3-loc-3)
  
  (road city-3-loc-3 city-1-loc-4)
  
  (road city-2-loc-3 city-3-loc-5)
  
  (road city-3-loc-5 city-2-loc-3)
  
  (at package-1 city-1-loc-4)
  (at package-2 city-2-loc-3)
  (at package-3 city-3-loc-1)
  (at package-4 city-1-loc-2)
  (at package-5 city-3-loc-2)
  (at package-6 city-2-loc-2)
  (at package-7 city-1-loc-5)
  (at truck-1 city-2-loc-5)
  (capacity truck-1 capacity-2)
  (at truck-2 city-3-loc-3)
  (capacity truck-2 capacity-2)
  (at truck-3 city-1-loc-4)
  (capacity truck-3 capacity-3)
 )
 (:goal (and
  (at package-1 city-2-loc-3)
  (at package-2 city-3-loc-4)
  (at package-3 city-3-loc-2)
  (at package-4 city-2-loc-3)
  (at package-5 city-1-loc-4)
  (at package-6 city-3-loc-1)
  (at package-7 city-1-loc-6)
 ))
 
)
