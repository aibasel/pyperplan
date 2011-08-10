; Transport city-sequential-24nodes-1000size-4degree-100mindistance-3trucks-9packages-2008seed

(define (problem transport-city-sequential-24nodes-1000size-4degree-100mindistance-3trucks-9packages-2008seed)
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
  city-loc-10 - location
  city-loc-11 - location
  city-loc-12 - location
  city-loc-13 - location
  city-loc-14 - location
  city-loc-15 - location
  city-loc-16 - location
  city-loc-17 - location
  city-loc-18 - location
  city-loc-19 - location
  city-loc-20 - location
  city-loc-21 - location
  city-loc-22 - location
  city-loc-23 - location
  city-loc-24 - location
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
  (road city-loc-3 city-loc-1)
  
  ; 890,543 -> 748,385
  (road city-loc-1 city-loc-3)
  
  ; 912,799 -> 890,543
  (road city-loc-4 city-loc-1)
  
  ; 890,543 -> 912,799
  (road city-loc-1 city-loc-4)
  
  ; 977,899 -> 912,799
  (road city-loc-5 city-loc-4)
  
  ; 912,799 -> 977,899
  (road city-loc-4 city-loc-5)
  
  ; 456,221 -> 384,50
  (road city-loc-6 city-loc-2)
  
  ; 384,50 -> 456,221
  (road city-loc-2 city-loc-6)
  
  ; 742,542 -> 890,543
  (road city-loc-7 city-loc-1)
  
  ; 890,543 -> 742,542
  (road city-loc-1 city-loc-7)
  
  ; 742,542 -> 748,385
  (road city-loc-7 city-loc-3)
  
  ; 748,385 -> 742,542
  (road city-loc-3 city-loc-7)
  
  ; 273,425 -> 456,221
  (road city-loc-9 city-loc-6)
  
  ; 456,221 -> 273,425
  (road city-loc-6 city-loc-9)
  
  ; 566,552 -> 748,385
  (road city-loc-10 city-loc-3)
  
  ; 748,385 -> 566,552
  (road city-loc-3 city-loc-10)
  
  ; 566,552 -> 742,542
  (road city-loc-10 city-loc-7)
  
  ; 742,542 -> 566,552
  (road city-loc-7 city-loc-10)
  
  ; 566,552 -> 564,783
  (road city-loc-10 city-loc-8)
  
  ; 564,783 -> 566,552
  (road city-loc-8 city-loc-10)
  
  ; 174,643 -> 273,425
  (road city-loc-11 city-loc-9)
  
  ; 273,425 -> 174,643
  (road city-loc-9 city-loc-11)
  
  ; 930,259 -> 748,385
  (road city-loc-12 city-loc-3)
  
  ; 748,385 -> 930,259
  (road city-loc-3 city-loc-12)
  
  ; 55,605 -> 174,643
  (road city-loc-13 city-loc-11)
  
  ; 174,643 -> 55,605
  (road city-loc-11 city-loc-13)
  
  ; 803,858 -> 912,799
  (road city-loc-14 city-loc-4)
  
  ; 912,799 -> 803,858
  (road city-loc-4 city-loc-14)
  
  ; 803,858 -> 977,899
  (road city-loc-14 city-loc-5)
  
  ; 977,899 -> 803,858
  (road city-loc-5 city-loc-14)
  
  ; 803,858 -> 564,783
  (road city-loc-14 city-loc-8)
  
  ; 564,783 -> 803,858
  (road city-loc-8 city-loc-14)
  
  ; 263,567 -> 273,425
  (road city-loc-15 city-loc-9)
  
  ; 273,425 -> 263,567
  (road city-loc-9 city-loc-15)
  
  ; 263,567 -> 174,643
  (road city-loc-15 city-loc-11)
  
  ; 174,643 -> 263,567
  (road city-loc-11 city-loc-15)
  
  ; 263,567 -> 55,605
  (road city-loc-15 city-loc-13)
  
  ; 55,605 -> 263,567
  (road city-loc-13 city-loc-15)
  
  ; 128,791 -> 174,643
  (road city-loc-16 city-loc-11)
  
  ; 174,643 -> 128,791
  (road city-loc-11 city-loc-16)
  
  ; 128,791 -> 55,605
  (road city-loc-16 city-loc-13)
  
  ; 55,605 -> 128,791
  (road city-loc-13 city-loc-16)
  
  ; 128,791 -> 263,567
  (road city-loc-16 city-loc-15)
  
  ; 263,567 -> 128,791
  (road city-loc-15 city-loc-16)
  
  ; 426,706 -> 564,783
  (road city-loc-17 city-loc-8)
  
  ; 564,783 -> 426,706
  (road city-loc-8 city-loc-17)
  
  ; 426,706 -> 566,552
  (road city-loc-17 city-loc-10)
  
  ; 566,552 -> 426,706
  (road city-loc-10 city-loc-17)
  
  ; 426,706 -> 174,643
  (road city-loc-17 city-loc-11)
  
  ; 174,643 -> 426,706
  (road city-loc-11 city-loc-17)
  
  ; 426,706 -> 263,567
  (road city-loc-17 city-loc-15)
  
  ; 263,567 -> 426,706
  (road city-loc-15 city-loc-17)
  
  ; 36,368 -> 273,425
  (road city-loc-18 city-loc-9)
  
  ; 273,425 -> 36,368
  (road city-loc-9 city-loc-18)
  
  ; 36,368 -> 55,605
  (road city-loc-18 city-loc-13)
  
  ; 55,605 -> 36,368
  (road city-loc-13 city-loc-18)
  
  ; 806,18 -> 930,259
  (road city-loc-19 city-loc-12)
  
  ; 930,259 -> 806,18
  (road city-loc-12 city-loc-19)
  
  ; 138,109 -> 384,50
  (road city-loc-20 city-loc-2)
  
  ; 384,50 -> 138,109
  (road city-loc-2 city-loc-20)
  
  ; 392,433 -> 456,221
  (road city-loc-21 city-loc-6)
  
  ; 456,221 -> 392,433
  (road city-loc-6 city-loc-21)
  
  ; 392,433 -> 273,425
  (road city-loc-21 city-loc-9)
  
  ; 273,425 -> 392,433
  (road city-loc-9 city-loc-21)
  
  ; 392,433 -> 566,552
  (road city-loc-21 city-loc-10)
  
  ; 566,552 -> 392,433
  (road city-loc-10 city-loc-21)
  
  ; 392,433 -> 263,567
  (road city-loc-21 city-loc-15)
  
  ; 263,567 -> 392,433
  (road city-loc-15 city-loc-21)
  
  ; 392,433 -> 426,706
  (road city-loc-21 city-loc-17)
  
  ; 426,706 -> 392,433
  (road city-loc-17 city-loc-21)
  
  ; 231,881 -> 174,643
  (road city-loc-22 city-loc-11)
  
  ; 174,643 -> 231,881
  (road city-loc-11 city-loc-22)
  
  ; 231,881 -> 128,791
  (road city-loc-22 city-loc-16)
  
  ; 128,791 -> 231,881
  (road city-loc-16 city-loc-22)
  
  ; 231,881 -> 426,706
  (road city-loc-22 city-loc-17)
  
  ; 426,706 -> 231,881
  (road city-loc-17 city-loc-22)
  
  ; 682,8 -> 806,18
  (road city-loc-23 city-loc-19)
  
  ; 806,18 -> 682,8
  (road city-loc-19 city-loc-23)
  
  ; 989,457 -> 890,543
  (road city-loc-24 city-loc-1)
  
  ; 890,543 -> 989,457
  (road city-loc-1 city-loc-24)
  
  ; 989,457 -> 748,385
  (road city-loc-24 city-loc-3)
  
  ; 748,385 -> 989,457
  (road city-loc-3 city-loc-24)
  
  ; 989,457 -> 742,542
  (road city-loc-24 city-loc-7)
  
  ; 742,542 -> 989,457
  (road city-loc-7 city-loc-24)
  
  ; 989,457 -> 930,259
  (road city-loc-24 city-loc-12)
  
  ; 930,259 -> 989,457
  (road city-loc-12 city-loc-24)
  
  (at package-1 city-loc-2)
  (at package-2 city-loc-19)
  (at package-3 city-loc-24)
  (at package-4 city-loc-5)
  (at package-5 city-loc-15)
  (at package-6 city-loc-19)
  (at package-7 city-loc-2)
  (at package-8 city-loc-4)
  (at package-9 city-loc-9)
  (at truck-1 city-loc-18)
  (capacity truck-1 capacity-4)
  (at truck-2 city-loc-1)
  (capacity truck-2 capacity-4)
  (at truck-3 city-loc-16)
  (capacity truck-3 capacity-2)
 )
 (:goal (and
  (at package-1 city-loc-12)
  (at package-2 city-loc-7)
  (at package-3 city-loc-1)
  (at package-4 city-loc-6)
  (at package-5 city-loc-9)
  (at package-6 city-loc-14)
  (at package-7 city-loc-14)
  (at package-8 city-loc-9)
  (at package-9 city-loc-4)
 ))
 
)
