; Transport three-cities-sequential-5nodes-1000size-3degree-100mindistance-2trucks-6packages-2008seed

(define (problem transport-three-cities-sequential-5nodes-1000size-3degree-100mindistance-2trucks-6packages-2008seed)
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
  
  ; 2742,542 -> 2456,221
  (road city-2-loc-2 city-2-loc-1)
  
  ; 2456,221 -> 2742,542
  (road city-2-loc-1 city-2-loc-2)
  
  ; 2564,783 -> 2742,542
  (road city-2-loc-3 city-2-loc-2)
  
  ; 2742,542 -> 2564,783
  (road city-2-loc-2 city-2-loc-3)
  
  ; 2273,425 -> 2456,221
  (road city-2-loc-4 city-2-loc-1)
  
  ; 2456,221 -> 2273,425
  (road city-2-loc-1 city-2-loc-4)
  
  ; 2273,425 -> 2742,542
  (road city-2-loc-4 city-2-loc-2)
  
  ; 2742,542 -> 2273,425
  (road city-2-loc-2 city-2-loc-4)
  
  ; 2273,425 -> 2564,783
  (road city-2-loc-4 city-2-loc-3)
  
  ; 2564,783 -> 2273,425
  (road city-2-loc-3 city-2-loc-4)
  
  ; 2566,552 -> 2456,221
  (road city-2-loc-5 city-2-loc-1)
  
  ; 2456,221 -> 2566,552
  (road city-2-loc-1 city-2-loc-5)
  
  ; 2566,552 -> 2742,542
  (road city-2-loc-5 city-2-loc-2)
  
  ; 2742,542 -> 2566,552
  (road city-2-loc-2 city-2-loc-5)
  
  ; 2566,552 -> 2564,783
  (road city-2-loc-5 city-2-loc-3)
  
  ; 2564,783 -> 2566,552
  (road city-2-loc-3 city-2-loc-5)
  
  ; 2566,552 -> 2273,425
  (road city-2-loc-5 city-2-loc-4)
  
  ; 2273,425 -> 2566,552
  (road city-2-loc-4 city-2-loc-5)
  
  ; 1174,2643 -> 1616,2621
  (road city-3-loc-2 city-3-loc-1)
  
  ; 1616,2621 -> 1174,2643
  (road city-3-loc-1 city-3-loc-2)
  
  ; 1946,2916 -> 1616,2621
  (road city-3-loc-3 city-3-loc-1)
  
  ; 1616,2621 -> 1946,2916
  (road city-3-loc-1 city-3-loc-3)
  
  ; 1930,2259 -> 1616,2621
  (road city-3-loc-4 city-3-loc-1)
  
  ; 1616,2621 -> 1930,2259
  (road city-3-loc-1 city-3-loc-4)
  
  ; 1055,2605 -> 1174,2643
  (road city-3-loc-5 city-3-loc-2)
  
  ; 1174,2643 -> 1055,2605
  (road city-3-loc-2 city-3-loc-5)
  
  ; 977,899 <-> 2273,425
  (road city-1-loc-5 city-2-loc-4)
  
  (road city-2-loc-4 city-1-loc-5)
  
  (road city-1-loc-5 city-3-loc-4)
  
  (road city-3-loc-4 city-1-loc-5)
  
  (road city-2-loc-1 city-3-loc-1)
  
  (road city-3-loc-1 city-2-loc-1)
  
  (at package-1 city-3-loc-5)
  (at package-2 city-1-loc-3)
  (at package-3 city-1-loc-4)
  (at package-4 city-2-loc-4)
  (at package-5 city-1-loc-2)
  (at package-6 city-3-loc-1)
  (at truck-1 city-1-loc-1)
  (capacity truck-1 capacity-3)
  (at truck-2 city-2-loc-5)
  (capacity truck-2 capacity-4)
 )
 (:goal (and
  (at package-1 city-1-loc-5)
  (at package-2 city-1-loc-5)
  (at package-3 city-1-loc-2)
  (at package-4 city-3-loc-1)
  (at package-5 city-3-loc-3)
  (at package-6 city-1-loc-4)
 ))
 
)
