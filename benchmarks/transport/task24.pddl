; Transport three-cities-sequential-4nodes-1000size-2degree-100mindistance-2trucks-5packages-2008seed

(define (problem transport-three-cities-sequential-4nodes-1000size-2degree-100mindistance-2trucks-5packages-2008seed)
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
  truck-1 - vehicle
  truck-2 - vehicle
  package-1 - package
  package-2 - package
  package-3 - package
  package-4 - package
  package-5 - package
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
  ; 742,542 -> 977,899
  (road city-1-loc-3 city-1-loc-1)
  
  ; 977,899 -> 742,542
  (road city-1-loc-1 city-1-loc-3)
  
  ; 742,542 -> 456,221
  (road city-1-loc-3 city-1-loc-2)
  
  ; 456,221 -> 742,542
  (road city-1-loc-2 city-1-loc-3)
  
  ; 564,783 -> 977,899
  (road city-1-loc-4 city-1-loc-1)
  
  ; 977,899 -> 564,783
  (road city-1-loc-1 city-1-loc-4)
  
  ; 564,783 -> 742,542
  (road city-1-loc-4 city-1-loc-3)
  
  ; 742,542 -> 564,783
  (road city-1-loc-3 city-1-loc-4)
  
  ; 2245,346 -> 2257,5
  (road city-2-loc-2 city-2-loc-1)
  
  ; 2257,5 -> 2245,346
  (road city-2-loc-1 city-2-loc-2)
  
  ; 2559,565 -> 2245,346
  (road city-2-loc-3 city-2-loc-2)
  
  ; 2245,346 -> 2559,565
  (road city-2-loc-2 city-2-loc-3)
  
  ; 2347,149 -> 2257,5
  (road city-2-loc-4 city-2-loc-1)
  
  ; 2257,5 -> 2347,149
  (road city-2-loc-1 city-2-loc-4)
  
  ; 2347,149 -> 2245,346
  (road city-2-loc-4 city-2-loc-2)
  
  ; 2245,346 -> 2347,149
  (road city-2-loc-2 city-2-loc-4)
  
  ; 2347,149 -> 2559,565
  (road city-2-loc-4 city-2-loc-3)
  
  ; 2559,565 -> 2347,149
  (road city-2-loc-3 city-2-loc-4)
  
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
  
  ; 977,899 <-> 2245,346
  (road city-1-loc-1 city-2-loc-2)
  
  (road city-2-loc-2 city-1-loc-1)
  
  (road city-1-loc-4 city-3-loc-4)
  
  (road city-3-loc-4 city-1-loc-4)
  
  (road city-2-loc-1 city-3-loc-1)
  
  (road city-3-loc-1 city-2-loc-1)
  
  (at package-1 city-1-loc-1)
  (at package-2 city-3-loc-1)
  (at package-3 city-2-loc-2)
  (at package-4 city-1-loc-3)
  (at package-5 city-2-loc-3)
  (at truck-1 city-1-loc-4)
  (capacity truck-1 capacity-3)
  (at truck-2 city-1-loc-1)
  (capacity truck-2 capacity-3)
 )
 (:goal (and
  (at package-1 city-2-loc-3)
  (at package-2 city-2-loc-3)
  (at package-3 city-2-loc-3)
  (at package-4 city-2-loc-1)
  (at package-5 city-2-loc-4)
 ))
 
)
