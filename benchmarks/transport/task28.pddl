; Transport three-cities-sequential-8nodes-1000size-4degree-100mindistance-3trucks-9packages-2008seed

(define (problem transport-three-cities-sequential-8nodes-1000size-4degree-100mindistance-3trucks-9packages-2008seed)
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
  
  ; 742,542 -> 456,221
  (road city-1-loc-7 city-1-loc-6)
  
  ; 456,221 -> 742,542
  (road city-1-loc-6 city-1-loc-7)
  
  ; 564,783 -> 890,543
  (road city-1-loc-8 city-1-loc-1)
  
  ; 890,543 -> 564,783
  (road city-1-loc-1 city-1-loc-8)
  
  ; 564,783 -> 748,385
  (road city-1-loc-8 city-1-loc-3)
  
  ; 748,385 -> 564,783
  (road city-1-loc-3 city-1-loc-8)
  
  ; 564,783 -> 912,799
  (road city-1-loc-8 city-1-loc-4)
  
  ; 912,799 -> 564,783
  (road city-1-loc-4 city-1-loc-8)
  
  ; 564,783 -> 977,899
  (road city-1-loc-8 city-1-loc-5)
  
  ; 977,899 -> 564,783
  (road city-1-loc-5 city-1-loc-8)
  
  ; 564,783 -> 742,542
  (road city-1-loc-8 city-1-loc-7)
  
  ; 742,542 -> 564,783
  (road city-1-loc-7 city-1-loc-8)
  
  ; 2566,552 -> 2273,425
  (road city-2-loc-2 city-2-loc-1)
  
  ; 2273,425 -> 2566,552
  (road city-2-loc-1 city-2-loc-2)
  
  ; 2174,643 -> 2273,425
  (road city-2-loc-3 city-2-loc-1)
  
  ; 2273,425 -> 2174,643
  (road city-2-loc-1 city-2-loc-3)
  
  ; 2174,643 -> 2566,552
  (road city-2-loc-3 city-2-loc-2)
  
  ; 2566,552 -> 2174,643
  (road city-2-loc-2 city-2-loc-3)
  
  ; 2930,259 -> 2566,552
  (road city-2-loc-5 city-2-loc-2)
  
  ; 2566,552 -> 2930,259
  (road city-2-loc-2 city-2-loc-5)
  
  ; 2055,605 -> 2273,425
  (road city-2-loc-6 city-2-loc-1)
  
  ; 2273,425 -> 2055,605
  (road city-2-loc-1 city-2-loc-6)
  
  ; 2055,605 -> 2174,643
  (road city-2-loc-6 city-2-loc-3)
  
  ; 2174,643 -> 2055,605
  (road city-2-loc-3 city-2-loc-6)
  
  ; 2803,858 -> 2566,552
  (road city-2-loc-7 city-2-loc-2)
  
  ; 2566,552 -> 2803,858
  (road city-2-loc-2 city-2-loc-7)
  
  ; 2803,858 -> 2946,916
  (road city-2-loc-7 city-2-loc-4)
  
  ; 2946,916 -> 2803,858
  (road city-2-loc-4 city-2-loc-7)
  
  ; 2263,567 -> 2273,425
  (road city-2-loc-8 city-2-loc-1)
  
  ; 2273,425 -> 2263,567
  (road city-2-loc-1 city-2-loc-8)
  
  ; 2263,567 -> 2566,552
  (road city-2-loc-8 city-2-loc-2)
  
  ; 2566,552 -> 2263,567
  (road city-2-loc-2 city-2-loc-8)
  
  ; 2263,567 -> 2174,643
  (road city-2-loc-8 city-2-loc-3)
  
  ; 2174,643 -> 2263,567
  (road city-2-loc-3 city-2-loc-8)
  
  ; 2263,567 -> 2055,605
  (road city-2-loc-8 city-2-loc-6)
  
  ; 2055,605 -> 2263,567
  (road city-2-loc-6 city-2-loc-8)
  
  ; 1748,2863 -> 1362,2862
  (road city-3-loc-2 city-3-loc-1)
  
  ; 1362,2862 -> 1748,2863
  (road city-3-loc-1 city-3-loc-2)
  
  ; 1659,2497 -> 1362,2862
  (road city-3-loc-4 city-3-loc-1)
  
  ; 1362,2862 -> 1659,2497
  (road city-3-loc-1 city-3-loc-4)
  
  ; 1659,2497 -> 1748,2863
  (road city-3-loc-4 city-3-loc-2)
  
  ; 1748,2863 -> 1659,2497
  (road city-3-loc-2 city-3-loc-4)
  
  ; 1257,2005 -> 1006,2060
  (road city-3-loc-5 city-3-loc-3)
  
  ; 1006,2060 -> 1257,2005
  (road city-3-loc-3 city-3-loc-5)
  
  ; 1245,2346 -> 1006,2060
  (road city-3-loc-6 city-3-loc-3)
  
  ; 1006,2060 -> 1245,2346
  (road city-3-loc-3 city-3-loc-6)
  
  ; 1245,2346 -> 1659,2497
  (road city-3-loc-6 city-3-loc-4)
  
  ; 1659,2497 -> 1245,2346
  (road city-3-loc-4 city-3-loc-6)
  
  ; 1245,2346 -> 1257,2005
  (road city-3-loc-6 city-3-loc-5)
  
  ; 1257,2005 -> 1245,2346
  (road city-3-loc-5 city-3-loc-6)
  
  ; 1559,2565 -> 1362,2862
  (road city-3-loc-7 city-3-loc-1)
  
  ; 1362,2862 -> 1559,2565
  (road city-3-loc-1 city-3-loc-7)
  
  ; 1559,2565 -> 1748,2863
  (road city-3-loc-7 city-3-loc-2)
  
  ; 1748,2863 -> 1559,2565
  (road city-3-loc-2 city-3-loc-7)
  
  ; 1559,2565 -> 1659,2497
  (road city-3-loc-7 city-3-loc-4)
  
  ; 1659,2497 -> 1559,2565
  (road city-3-loc-4 city-3-loc-7)
  
  ; 1559,2565 -> 1245,2346
  (road city-3-loc-7 city-3-loc-6)
  
  ; 1245,2346 -> 1559,2565
  (road city-3-loc-6 city-3-loc-7)
  
  ; 1347,2149 -> 1006,2060
  (road city-3-loc-8 city-3-loc-3)
  
  ; 1006,2060 -> 1347,2149
  (road city-3-loc-3 city-3-loc-8)
  
  ; 1347,2149 -> 1659,2497
  (road city-3-loc-8 city-3-loc-4)
  
  ; 1659,2497 -> 1347,2149
  (road city-3-loc-4 city-3-loc-8)
  
  ; 1347,2149 -> 1257,2005
  (road city-3-loc-8 city-3-loc-5)
  
  ; 1257,2005 -> 1347,2149
  (road city-3-loc-5 city-3-loc-8)
  
  ; 1347,2149 -> 1245,2346
  (road city-3-loc-8 city-3-loc-6)
  
  ; 1245,2346 -> 1347,2149
  (road city-3-loc-6 city-3-loc-8)
  
  ; 1347,2149 -> 1559,2565
  (road city-3-loc-8 city-3-loc-7)
  
  ; 1559,2565 -> 1347,2149
  (road city-3-loc-7 city-3-loc-8)
  
  ; 977,899 <-> 2055,605
  (road city-1-loc-5 city-2-loc-6)
  
  (road city-2-loc-6 city-1-loc-5)
  
  (road city-1-loc-1 city-3-loc-1)
  
  (road city-3-loc-1 city-1-loc-1)
  
  (road city-2-loc-1 city-3-loc-1)
  
  (road city-3-loc-1 city-2-loc-1)
  
  (at package-1 city-2-loc-4)
  (at package-2 city-1-loc-6)
  (at package-3 city-1-loc-6)
  (at package-4 city-2-loc-4)
  (at package-5 city-3-loc-1)
  (at package-6 city-1-loc-2)
  (at package-7 city-3-loc-2)
  (at package-8 city-2-loc-3)
  (at package-9 city-1-loc-6)
  (at truck-1 city-2-loc-6)
  (capacity truck-1 capacity-2)
  (at truck-2 city-3-loc-4)
  (capacity truck-2 capacity-2)
  (at truck-3 city-1-loc-5)
  (capacity truck-3 capacity-3)
 )
 (:goal (and
  (at package-1 city-3-loc-6)
  (at package-2 city-3-loc-3)
  (at package-3 city-2-loc-3)
  (at package-4 city-1-loc-5)
  (at package-5 city-1-loc-7)
  (at package-6 city-1-loc-1)
  (at package-7 city-2-loc-2)
  (at package-8 city-3-loc-3)
  (at package-9 city-2-loc-4)
 ))
 
)
