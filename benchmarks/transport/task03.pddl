; Transport city-sequential-9nodes-1000size-3degree-100mindistance-2trucks-4packages-2008seed

(define (problem transport-city-sequential-9nodes-1000size-3degree-100mindistance-2trucks-4packages-2008seed)
 (:domain transport)
 (:objects
  city-loc-1 - location
  city-loc-2 - location
  city-loc-3 - location
  city-loc-4 - location
  city-loc-5 - location
  city-loc-6 - location
  city-loc-7 - location
  city-loc-8 - location
  city-loc-9 - location
  truck-1 - vehicle
  truck-2 - vehicle
  package-1 - package
  package-2 - package
  package-3 - package
  package-4 - package
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
  (road city-loc-3 city-loc-1)
  
  ; 890,543 -> 748,385
  (road city-loc-1 city-loc-3)
  
  ; 912,799 -> 890,543
  (road city-loc-4 city-loc-1)
  
  ; 890,543 -> 912,799
  (road city-loc-1 city-loc-4)
  
  ; 977,899 -> 890,543
  (road city-loc-5 city-loc-1)
  
  ; 890,543 -> 977,899
  (road city-loc-1 city-loc-5)
  
  ; 977,899 -> 912,799
  (road city-loc-5 city-loc-4)
  
  ; 912,799 -> 977,899
  (road city-loc-4 city-loc-5)
  
  ; 456,221 -> 384,50
  (road city-loc-6 city-loc-2)
  
  ; 384,50 -> 456,221
  (road city-loc-2 city-loc-6)
  
  ; 456,221 -> 748,385
  (road city-loc-6 city-loc-3)
  
  ; 748,385 -> 456,221
  (road city-loc-3 city-loc-6)
  
  ; 742,542 -> 890,543
  (road city-loc-7 city-loc-1)
  
  ; 890,543 -> 742,542
  (road city-loc-1 city-loc-7)
  
  ; 742,542 -> 748,385
  (road city-loc-7 city-loc-3)
  
  ; 748,385 -> 742,542
  (road city-loc-3 city-loc-7)
  
  ; 742,542 -> 912,799
  (road city-loc-7 city-loc-4)
  
  ; 912,799 -> 742,542
  (road city-loc-4 city-loc-7)
  
  ; 564,783 -> 912,799
  (road city-loc-8 city-loc-4)
  
  ; 912,799 -> 564,783
  (road city-loc-4 city-loc-8)
  
  ; 564,783 -> 742,542
  (road city-loc-8 city-loc-7)
  
  ; 742,542 -> 564,783
  (road city-loc-7 city-loc-8)
  
  ; 273,425 -> 384,50
  (road city-loc-9 city-loc-2)
  
  ; 384,50 -> 273,425
  (road city-loc-2 city-loc-9)
  
  ; 273,425 -> 456,221
  (road city-loc-9 city-loc-6)
  
  ; 456,221 -> 273,425
  (road city-loc-6 city-loc-9)
  
  (at package-1 city-loc-6)
  (at package-2 city-loc-5)
  (at package-3 city-loc-6)
  (at package-4 city-loc-6)
  (at truck-1 city-loc-6)
  (capacity truck-1 capacity-2)
  (at truck-2 city-loc-9)
  (capacity truck-2 capacity-4)
 )
 (:goal (and
  (at package-1 city-loc-9)
  (at package-2 city-loc-3)
  (at package-3 city-loc-1)
  (at package-4 city-loc-8)
 ))
 
)
