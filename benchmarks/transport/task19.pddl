; Transport two-cities-sequential-18nodes-1000size-4degree-100mindistance-3trucks-10packages-2008seed

(define (problem transport-two-cities-sequential-18nodes-1000size-4degree-100mindistance-3trucks-10packages-2008seed)
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
  city-1-loc-15 - location
  city-2-loc-15 - location
  city-1-loc-16 - location
  city-2-loc-16 - location
  city-1-loc-17 - location
  city-2-loc-17 - location
  city-1-loc-18 - location
  city-2-loc-18 - location
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
  
  ; 564,783 -> 742,542
  (road city-1-loc-8 city-1-loc-7)
  
  ; 742,542 -> 564,783
  (road city-1-loc-7 city-1-loc-8)
  
  ; 273,425 -> 456,221
  (road city-1-loc-9 city-1-loc-6)
  
  ; 456,221 -> 273,425
  (road city-1-loc-6 city-1-loc-9)
  
  ; 566,552 -> 748,385
  (road city-1-loc-10 city-1-loc-3)
  
  ; 748,385 -> 566,552
  (road city-1-loc-3 city-1-loc-10)
  
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
  
  ; 55,605 -> 273,425
  (road city-1-loc-13 city-1-loc-9)
  
  ; 273,425 -> 55,605
  (road city-1-loc-9 city-1-loc-13)
  
  ; 55,605 -> 174,643
  (road city-1-loc-13 city-1-loc-11)
  
  ; 174,643 -> 55,605
  (road city-1-loc-11 city-1-loc-13)
  
  ; 803,858 -> 912,799
  (road city-1-loc-14 city-1-loc-4)
  
  ; 912,799 -> 803,858
  (road city-1-loc-4 city-1-loc-14)
  
  ; 803,858 -> 977,899
  (road city-1-loc-14 city-1-loc-5)
  
  ; 977,899 -> 803,858
  (road city-1-loc-5 city-1-loc-14)
  
  ; 803,858 -> 564,783
  (road city-1-loc-14 city-1-loc-8)
  
  ; 564,783 -> 803,858
  (road city-1-loc-8 city-1-loc-14)
  
  ; 263,567 -> 273,425
  (road city-1-loc-15 city-1-loc-9)
  
  ; 273,425 -> 263,567
  (road city-1-loc-9 city-1-loc-15)
  
  ; 263,567 -> 566,552
  (road city-1-loc-15 city-1-loc-10)
  
  ; 566,552 -> 263,567
  (road city-1-loc-10 city-1-loc-15)
  
  ; 263,567 -> 174,643
  (road city-1-loc-15 city-1-loc-11)
  
  ; 174,643 -> 263,567
  (road city-1-loc-11 city-1-loc-15)
  
  ; 263,567 -> 55,605
  (road city-1-loc-15 city-1-loc-13)
  
  ; 55,605 -> 263,567
  (road city-1-loc-13 city-1-loc-15)
  
  ; 128,791 -> 174,643
  (road city-1-loc-16 city-1-loc-11)
  
  ; 174,643 -> 128,791
  (road city-1-loc-11 city-1-loc-16)
  
  ; 128,791 -> 55,605
  (road city-1-loc-16 city-1-loc-13)
  
  ; 55,605 -> 128,791
  (road city-1-loc-13 city-1-loc-16)
  
  ; 128,791 -> 263,567
  (road city-1-loc-16 city-1-loc-15)
  
  ; 263,567 -> 128,791
  (road city-1-loc-15 city-1-loc-16)
  
  ; 426,706 -> 564,783
  (road city-1-loc-17 city-1-loc-8)
  
  ; 564,783 -> 426,706
  (road city-1-loc-8 city-1-loc-17)
  
  ; 426,706 -> 566,552
  (road city-1-loc-17 city-1-loc-10)
  
  ; 566,552 -> 426,706
  (road city-1-loc-10 city-1-loc-17)
  
  ; 426,706 -> 174,643
  (road city-1-loc-17 city-1-loc-11)
  
  ; 174,643 -> 426,706
  (road city-1-loc-11 city-1-loc-17)
  
  ; 426,706 -> 263,567
  (road city-1-loc-17 city-1-loc-15)
  
  ; 263,567 -> 426,706
  (road city-1-loc-15 city-1-loc-17)
  
  ; 426,706 -> 128,791
  (road city-1-loc-17 city-1-loc-16)
  
  ; 128,791 -> 426,706
  (road city-1-loc-16 city-1-loc-17)
  
  ; 36,368 -> 273,425
  (road city-1-loc-18 city-1-loc-9)
  
  ; 273,425 -> 36,368
  (road city-1-loc-9 city-1-loc-18)
  
  ; 36,368 -> 174,643
  (road city-1-loc-18 city-1-loc-11)
  
  ; 174,643 -> 36,368
  (road city-1-loc-11 city-1-loc-18)
  
  ; 36,368 -> 55,605
  (road city-1-loc-18 city-1-loc-13)
  
  ; 55,605 -> 36,368
  (road city-1-loc-13 city-1-loc-18)
  
  ; 36,368 -> 263,567
  (road city-1-loc-18 city-1-loc-15)
  
  ; 263,567 -> 36,368
  (road city-1-loc-15 city-1-loc-18)
  
  ; 2936,210 -> 2872,63
  (road city-2-loc-4 city-2-loc-1)
  
  ; 2872,63 -> 2936,210
  (road city-2-loc-1 city-2-loc-4)
  
  ; 2480,435 -> 2614,343
  (road city-2-loc-6 city-2-loc-3)
  
  ; 2614,343 -> 2480,435
  (road city-2-loc-3 city-2-loc-6)
  
  ; 2480,435 -> 2193,424
  (road city-2-loc-6 city-2-loc-5)
  
  ; 2193,424 -> 2480,435
  (road city-2-loc-5 city-2-loc-6)
  
  ; 2918,341 -> 2872,63
  (road city-2-loc-7 city-2-loc-1)
  
  ; 2872,63 -> 2918,341
  (road city-2-loc-1 city-2-loc-7)
  
  ; 2918,341 -> 2614,343
  (road city-2-loc-7 city-2-loc-3)
  
  ; 2614,343 -> 2918,341
  (road city-2-loc-3 city-2-loc-7)
  
  ; 2918,341 -> 2936,210
  (road city-2-loc-7 city-2-loc-4)
  
  ; 2936,210 -> 2918,341
  (road city-2-loc-4 city-2-loc-7)
  
  ; 2651,235 -> 2872,63
  (road city-2-loc-8 city-2-loc-1)
  
  ; 2872,63 -> 2651,235
  (road city-2-loc-1 city-2-loc-8)
  
  ; 2651,235 -> 2614,343
  (road city-2-loc-8 city-2-loc-3)
  
  ; 2614,343 -> 2651,235
  (road city-2-loc-3 city-2-loc-8)
  
  ; 2651,235 -> 2936,210
  (road city-2-loc-8 city-2-loc-4)
  
  ; 2936,210 -> 2651,235
  (road city-2-loc-4 city-2-loc-8)
  
  ; 2651,235 -> 2480,435
  (road city-2-loc-8 city-2-loc-6)
  
  ; 2480,435 -> 2651,235
  (road city-2-loc-6 city-2-loc-8)
  
  ; 2651,235 -> 2918,341
  (road city-2-loc-8 city-2-loc-7)
  
  ; 2918,341 -> 2651,235
  (road city-2-loc-7 city-2-loc-8)
  
  ; 2560,901 -> 2645,721
  (road city-2-loc-9 city-2-loc-2)
  
  ; 2645,721 -> 2560,901
  (road city-2-loc-2 city-2-loc-9)
  
  ; 2447,732 -> 2645,721
  (road city-2-loc-10 city-2-loc-2)
  
  ; 2645,721 -> 2447,732
  (road city-2-loc-2 city-2-loc-10)
  
  ; 2447,732 -> 2480,435
  (road city-2-loc-10 city-2-loc-6)
  
  ; 2480,435 -> 2447,732
  (road city-2-loc-6 city-2-loc-10)
  
  ; 2447,732 -> 2560,901
  (road city-2-loc-10 city-2-loc-9)
  
  ; 2560,901 -> 2447,732
  (road city-2-loc-9 city-2-loc-10)
  
  ; 2362,940 -> 2560,901
  (road city-2-loc-11 city-2-loc-9)
  
  ; 2560,901 -> 2362,940
  (road city-2-loc-9 city-2-loc-11)
  
  ; 2362,940 -> 2447,732
  (road city-2-loc-11 city-2-loc-10)
  
  ; 2447,732 -> 2362,940
  (road city-2-loc-10 city-2-loc-11)
  
  ; 2941,734 -> 2645,721
  (road city-2-loc-12 city-2-loc-2)
  
  ; 2645,721 -> 2941,734
  (road city-2-loc-2 city-2-loc-12)
  
  ; 2653,507 -> 2645,721
  (road city-2-loc-13 city-2-loc-2)
  
  ; 2645,721 -> 2653,507
  (road city-2-loc-2 city-2-loc-13)
  
  ; 2653,507 -> 2614,343
  (road city-2-loc-13 city-2-loc-3)
  
  ; 2614,343 -> 2653,507
  (road city-2-loc-3 city-2-loc-13)
  
  ; 2653,507 -> 2480,435
  (road city-2-loc-13 city-2-loc-6)
  
  ; 2480,435 -> 2653,507
  (road city-2-loc-6 city-2-loc-13)
  
  ; 2653,507 -> 2918,341
  (road city-2-loc-13 city-2-loc-7)
  
  ; 2918,341 -> 2653,507
  (road city-2-loc-7 city-2-loc-13)
  
  ; 2653,507 -> 2651,235
  (road city-2-loc-13 city-2-loc-8)
  
  ; 2651,235 -> 2653,507
  (road city-2-loc-8 city-2-loc-13)
  
  ; 2653,507 -> 2447,732
  (road city-2-loc-13 city-2-loc-10)
  
  ; 2447,732 -> 2653,507
  (road city-2-loc-10 city-2-loc-13)
  
  ; 2820,551 -> 2645,721
  (road city-2-loc-14 city-2-loc-2)
  
  ; 2645,721 -> 2820,551
  (road city-2-loc-2 city-2-loc-14)
  
  ; 2820,551 -> 2614,343
  (road city-2-loc-14 city-2-loc-3)
  
  ; 2614,343 -> 2820,551
  (road city-2-loc-3 city-2-loc-14)
  
  ; 2820,551 -> 2918,341
  (road city-2-loc-14 city-2-loc-7)
  
  ; 2918,341 -> 2820,551
  (road city-2-loc-7 city-2-loc-14)
  
  ; 2820,551 -> 2941,734
  (road city-2-loc-14 city-2-loc-12)
  
  ; 2941,734 -> 2820,551
  (road city-2-loc-12 city-2-loc-14)
  
  ; 2820,551 -> 2653,507
  (road city-2-loc-14 city-2-loc-13)
  
  ; 2653,507 -> 2820,551
  (road city-2-loc-13 city-2-loc-14)
  
  ; 2437,605 -> 2645,721
  (road city-2-loc-15 city-2-loc-2)
  
  ; 2645,721 -> 2437,605
  (road city-2-loc-2 city-2-loc-15)
  
  ; 2437,605 -> 2614,343
  (road city-2-loc-15 city-2-loc-3)
  
  ; 2614,343 -> 2437,605
  (road city-2-loc-3 city-2-loc-15)
  
  ; 2437,605 -> 2193,424
  (road city-2-loc-15 city-2-loc-5)
  
  ; 2193,424 -> 2437,605
  (road city-2-loc-5 city-2-loc-15)
  
  ; 2437,605 -> 2480,435
  (road city-2-loc-15 city-2-loc-6)
  
  ; 2480,435 -> 2437,605
  (road city-2-loc-6 city-2-loc-15)
  
  ; 2437,605 -> 2447,732
  (road city-2-loc-15 city-2-loc-10)
  
  ; 2447,732 -> 2437,605
  (road city-2-loc-10 city-2-loc-15)
  
  ; 2437,605 -> 2653,507
  (road city-2-loc-15 city-2-loc-13)
  
  ; 2653,507 -> 2437,605
  (road city-2-loc-13 city-2-loc-15)
  
  ; 2497,244 -> 2614,343
  (road city-2-loc-16 city-2-loc-3)
  
  ; 2614,343 -> 2497,244
  (road city-2-loc-3 city-2-loc-16)
  
  ; 2497,244 -> 2480,435
  (road city-2-loc-16 city-2-loc-6)
  
  ; 2480,435 -> 2497,244
  (road city-2-loc-6 city-2-loc-16)
  
  ; 2497,244 -> 2651,235
  (road city-2-loc-16 city-2-loc-8)
  
  ; 2651,235 -> 2497,244
  (road city-2-loc-8 city-2-loc-16)
  
  ; 2497,244 -> 2653,507
  (road city-2-loc-16 city-2-loc-13)
  
  ; 2653,507 -> 2497,244
  (road city-2-loc-13 city-2-loc-16)
  
  ; 2305,509 -> 2193,424
  (road city-2-loc-17 city-2-loc-5)
  
  ; 2193,424 -> 2305,509
  (road city-2-loc-5 city-2-loc-17)
  
  ; 2305,509 -> 2480,435
  (road city-2-loc-17 city-2-loc-6)
  
  ; 2480,435 -> 2305,509
  (road city-2-loc-6 city-2-loc-17)
  
  ; 2305,509 -> 2447,732
  (road city-2-loc-17 city-2-loc-10)
  
  ; 2447,732 -> 2305,509
  (road city-2-loc-10 city-2-loc-17)
  
  ; 2305,509 -> 2437,605
  (road city-2-loc-17 city-2-loc-15)
  
  ; 2437,605 -> 2305,509
  (road city-2-loc-15 city-2-loc-17)
  
  ; 2731,24 -> 2872,63
  (road city-2-loc-18 city-2-loc-1)
  
  ; 2872,63 -> 2731,24
  (road city-2-loc-1 city-2-loc-18)
  
  ; 2731,24 -> 2936,210
  (road city-2-loc-18 city-2-loc-4)
  
  ; 2936,210 -> 2731,24
  (road city-2-loc-4 city-2-loc-18)
  
  ; 2731,24 -> 2651,235
  (road city-2-loc-18 city-2-loc-8)
  
  ; 2651,235 -> 2731,24
  (road city-2-loc-8 city-2-loc-18)
  
  ; 930,259 <-> 2193,424
  (road city-1-loc-12 city-2-loc-5)
  
  (road city-2-loc-5 city-1-loc-12)
  
  (at package-1 city-1-loc-9)
  (at package-2 city-1-loc-4)
  (at package-3 city-1-loc-9)
  (at package-4 city-1-loc-17)
  (at package-5 city-1-loc-9)
  (at package-6 city-1-loc-14)
  (at package-7 city-1-loc-10)
  (at package-8 city-1-loc-6)
  (at package-9 city-1-loc-16)
  (at package-10 city-1-loc-10)
  (at truck-1 city-2-loc-8)
  (capacity truck-1 capacity-4)
  (at truck-2 city-2-loc-6)
  (capacity truck-2 capacity-4)
  (at truck-3 city-2-loc-4)
  (capacity truck-3 capacity-2)
 )
 (:goal (and
  (at package-1 city-2-loc-3)
  (at package-2 city-2-loc-14)
  (at package-3 city-2-loc-5)
  (at package-4 city-2-loc-4)
  (at package-5 city-2-loc-4)
  (at package-6 city-2-loc-8)
  (at package-7 city-2-loc-1)
  (at package-8 city-2-loc-10)
  (at package-9 city-2-loc-7)
  (at package-10 city-2-loc-8)
 ))
 
)
