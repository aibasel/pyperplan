; Transport two-cities-sequential-14nodes-1000size-4degree-100mindistance-3trucks-8packages-2008seed

(define (problem transport-two-cities-sequential-14nodes-1000size-4degree-100mindistance-3trucks-8packages-2008seed)
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
  city-1-loc-11 - location
  city-2-loc-11 - location
  city-1-loc-12 - location
  city-2-loc-12 - location
  city-1-loc-13 - location
  city-2-loc-13 - location
  city-1-loc-14 - location
  city-2-loc-14 - location
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
  
  ; 174,643 -> 273,425
  (road city-1-loc-11 city-1-loc-9)
  
  ; 273,425 -> 174,643
  (road city-1-loc-9 city-1-loc-11)
  
  ; 930,259 -> 890,543
  (road city-1-loc-12 city-1-loc-1)
  
  ; 890,543 -> 930,259
  (road city-1-loc-1 city-1-loc-12)
  
  ; 930,259 -> 748,385
  (road city-1-loc-12 city-1-loc-3)
  
  ; 748,385 -> 930,259
  (road city-1-loc-3 city-1-loc-12)
  
  ; 930,259 -> 742,542
  (road city-1-loc-12 city-1-loc-7)
  
  ; 742,542 -> 930,259
  (road city-1-loc-7 city-1-loc-12)
  
  ; 55,605 -> 273,425
  (road city-1-loc-13 city-1-loc-9)
  
  ; 273,425 -> 55,605
  (road city-1-loc-9 city-1-loc-13)
  
  ; 55,605 -> 174,643
  (road city-1-loc-13 city-1-loc-11)
  
  ; 174,643 -> 55,605
  (road city-1-loc-11 city-1-loc-13)
  
  ; 803,858 -> 890,543
  (road city-1-loc-14 city-1-loc-1)
  
  ; 890,543 -> 803,858
  (road city-1-loc-1 city-1-loc-14)
  
  ; 803,858 -> 912,799
  (road city-1-loc-14 city-1-loc-4)
  
  ; 912,799 -> 803,858
  (road city-1-loc-4 city-1-loc-14)
  
  ; 803,858 -> 977,899
  (road city-1-loc-14 city-1-loc-5)
  
  ; 977,899 -> 803,858
  (road city-1-loc-5 city-1-loc-14)
  
  ; 803,858 -> 742,542
  (road city-1-loc-14 city-1-loc-7)
  
  ; 742,542 -> 803,858
  (road city-1-loc-7 city-1-loc-14)
  
  ; 803,858 -> 564,783
  (road city-1-loc-14 city-1-loc-8)
  
  ; 564,783 -> 803,858
  (road city-1-loc-8 city-1-loc-14)
  
  ; 2257,5 -> 2006,60
  (road city-2-loc-4 city-2-loc-2)
  
  ; 2006,60 -> 2257,5
  (road city-2-loc-2 city-2-loc-4)
  
  ; 2245,346 -> 2257,5
  (road city-2-loc-5 city-2-loc-4)
  
  ; 2257,5 -> 2245,346
  (road city-2-loc-4 city-2-loc-5)
  
  ; 2559,565 -> 2748,863
  (road city-2-loc-6 city-2-loc-1)
  
  ; 2748,863 -> 2559,565
  (road city-2-loc-1 city-2-loc-6)
  
  ; 2559,565 -> 2659,497
  (road city-2-loc-6 city-2-loc-3)
  
  ; 2659,497 -> 2559,565
  (road city-2-loc-3 city-2-loc-6)
  
  ; 2347,149 -> 2006,60
  (road city-2-loc-7 city-2-loc-2)
  
  ; 2006,60 -> 2347,149
  (road city-2-loc-2 city-2-loc-7)
  
  ; 2347,149 -> 2257,5
  (road city-2-loc-7 city-2-loc-4)
  
  ; 2257,5 -> 2347,149
  (road city-2-loc-4 city-2-loc-7)
  
  ; 2347,149 -> 2245,346
  (road city-2-loc-7 city-2-loc-5)
  
  ; 2245,346 -> 2347,149
  (road city-2-loc-5 city-2-loc-7)
  
  ; 2336,475 -> 2659,497
  (road city-2-loc-8 city-2-loc-3)
  
  ; 2659,497 -> 2336,475
  (road city-2-loc-3 city-2-loc-8)
  
  ; 2336,475 -> 2245,346
  (road city-2-loc-8 city-2-loc-5)
  
  ; 2245,346 -> 2336,475
  (road city-2-loc-5 city-2-loc-8)
  
  ; 2336,475 -> 2559,565
  (road city-2-loc-8 city-2-loc-6)
  
  ; 2559,565 -> 2336,475
  (road city-2-loc-6 city-2-loc-8)
  
  ; 2336,475 -> 2347,149
  (road city-2-loc-8 city-2-loc-7)
  
  ; 2347,149 -> 2336,475
  (road city-2-loc-7 city-2-loc-8)
  
  ; 2170,709 -> 2336,475
  (road city-2-loc-9 city-2-loc-8)
  
  ; 2336,475 -> 2170,709
  (road city-2-loc-8 city-2-loc-9)
  
  ; 2521,375 -> 2659,497
  (road city-2-loc-10 city-2-loc-3)
  
  ; 2659,497 -> 2521,375
  (road city-2-loc-3 city-2-loc-10)
  
  ; 2521,375 -> 2245,346
  (road city-2-loc-10 city-2-loc-5)
  
  ; 2245,346 -> 2521,375
  (road city-2-loc-5 city-2-loc-10)
  
  ; 2521,375 -> 2559,565
  (road city-2-loc-10 city-2-loc-6)
  
  ; 2559,565 -> 2521,375
  (road city-2-loc-6 city-2-loc-10)
  
  ; 2521,375 -> 2347,149
  (road city-2-loc-10 city-2-loc-7)
  
  ; 2347,149 -> 2521,375
  (road city-2-loc-7 city-2-loc-10)
  
  ; 2521,375 -> 2336,475
  (road city-2-loc-10 city-2-loc-8)
  
  ; 2336,475 -> 2521,375
  (road city-2-loc-8 city-2-loc-10)
  
  ; 2720,241 -> 2659,497
  (road city-2-loc-12 city-2-loc-3)
  
  ; 2659,497 -> 2720,241
  (road city-2-loc-3 city-2-loc-12)
  
  ; 2720,241 -> 2559,565
  (road city-2-loc-12 city-2-loc-6)
  
  ; 2559,565 -> 2720,241
  (road city-2-loc-6 city-2-loc-12)
  
  ; 2720,241 -> 2521,375
  (road city-2-loc-12 city-2-loc-10)
  
  ; 2521,375 -> 2720,241
  (road city-2-loc-10 city-2-loc-12)
  
  ; 2720,241 -> 2701,0
  (road city-2-loc-12 city-2-loc-11)
  
  ; 2701,0 -> 2720,241
  (road city-2-loc-11 city-2-loc-12)
  
  ; 2630,722 -> 2748,863
  (road city-2-loc-13 city-2-loc-1)
  
  ; 2748,863 -> 2630,722
  (road city-2-loc-1 city-2-loc-13)
  
  ; 2630,722 -> 2659,497
  (road city-2-loc-13 city-2-loc-3)
  
  ; 2659,497 -> 2630,722
  (road city-2-loc-3 city-2-loc-13)
  
  ; 2630,722 -> 2559,565
  (road city-2-loc-13 city-2-loc-6)
  
  ; 2559,565 -> 2630,722
  (road city-2-loc-6 city-2-loc-13)
  
  ; 2120,854 -> 2170,709
  (road city-2-loc-14 city-2-loc-9)
  
  ; 2170,709 -> 2120,854
  (road city-2-loc-9 city-2-loc-14)
  
  ; 930,259 <-> 2006,60
  (road city-1-loc-12 city-2-loc-2)
  
  (road city-2-loc-2 city-1-loc-12)
  
  (at package-1 city-1-loc-6)
  (at package-2 city-1-loc-4)
  (at package-3 city-1-loc-3)
  (at package-4 city-1-loc-8)
  (at package-5 city-1-loc-5)
  (at package-6 city-1-loc-9)
  (at package-7 city-1-loc-6)
  (at package-8 city-1-loc-11)
  (at truck-1 city-2-loc-10)
  (capacity truck-1 capacity-4)
  (at truck-2 city-2-loc-5)
  (capacity truck-2 capacity-3)
  (at truck-3 city-2-loc-6)
  (capacity truck-3 capacity-2)
 )
 (:goal (and
  (at package-1 city-2-loc-9)
  (at package-2 city-2-loc-11)
  (at package-3 city-2-loc-1)
  (at package-4 city-2-loc-4)
  (at package-5 city-2-loc-13)
  (at package-6 city-2-loc-2)
  (at package-7 city-2-loc-1)
  (at package-8 city-2-loc-8)
 ))
 
)
