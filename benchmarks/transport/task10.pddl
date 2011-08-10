; Transport city-sequential-30nodes-1000size-4degree-100mindistance-3trucks-11packages-2008seed

(define (problem transport-city-sequential-30nodes-1000size-4degree-100mindistance-3trucks-11packages-2008seed)
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
  city-loc-25 - location
  city-loc-26 - location
  city-loc-27 - location
  city-loc-28 - location
  city-loc-29 - location
  city-loc-30 - location
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
  ; 120,854 -> 200,669
  (road city-loc-4 city-loc-2)
  
  ; 200,669 -> 120,854
  (road city-loc-2 city-loc-4)
  
  ; 377,283 -> 490,285
  (road city-loc-5 city-loc-1)
  
  ; 490,285 -> 377,283
  (road city-loc-1 city-loc-5)
  
  ; 171,545 -> 200,669
  (road city-loc-6 city-loc-2)
  
  ; 200,669 -> 171,545
  (road city-loc-2 city-loc-6)
  
  ; 348,607 -> 200,669
  (road city-loc-7 city-loc-2)
  
  ; 200,669 -> 348,607
  (road city-loc-2 city-loc-7)
  
  ; 348,607 -> 171,545
  (road city-loc-7 city-loc-6)
  
  ; 171,545 -> 348,607
  (road city-loc-6 city-loc-7)
  
  ; 395,741 -> 200,669
  (road city-loc-8 city-loc-2)
  
  ; 200,669 -> 395,741
  (road city-loc-2 city-loc-8)
  
  ; 395,741 -> 630,722
  (road city-loc-8 city-loc-3)
  
  ; 630,722 -> 395,741
  (road city-loc-3 city-loc-8)
  
  ; 395,741 -> 348,607
  (road city-loc-8 city-loc-7)
  
  ; 348,607 -> 395,741
  (road city-loc-7 city-loc-8)
  
  ; 69,508 -> 200,669
  (road city-loc-11 city-loc-2)
  
  ; 200,669 -> 69,508
  (road city-loc-2 city-loc-11)
  
  ; 69,508 -> 171,545
  (road city-loc-11 city-loc-6)
  
  ; 171,545 -> 69,508
  (road city-loc-6 city-loc-11)
  
  ; 69,508 -> 71,275
  (road city-loc-11 city-loc-9)
  
  ; 71,275 -> 69,508
  (road city-loc-9 city-loc-11)
  
  ; 203,987 -> 120,854
  (road city-loc-12 city-loc-4)
  
  ; 120,854 -> 203,987
  (road city-loc-4 city-loc-12)
  
  ; 551,602 -> 630,722
  (road city-loc-14 city-loc-3)
  
  ; 630,722 -> 551,602
  (road city-loc-3 city-loc-14)
  
  ; 551,602 -> 348,607
  (road city-loc-14 city-loc-7)
  
  ; 348,607 -> 551,602
  (road city-loc-7 city-loc-14)
  
  ; 551,602 -> 395,741
  (road city-loc-14 city-loc-8)
  
  ; 395,741 -> 551,602
  (road city-loc-8 city-loc-14)
  
  ; 366,457 -> 490,285
  (road city-loc-15 city-loc-1)
  
  ; 490,285 -> 366,457
  (road city-loc-1 city-loc-15)
  
  ; 366,457 -> 377,283
  (road city-loc-15 city-loc-5)
  
  ; 377,283 -> 366,457
  (road city-loc-5 city-loc-15)
  
  ; 366,457 -> 171,545
  (road city-loc-15 city-loc-6)
  
  ; 171,545 -> 366,457
  (road city-loc-6 city-loc-15)
  
  ; 366,457 -> 348,607
  (road city-loc-15 city-loc-7)
  
  ; 348,607 -> 366,457
  (road city-loc-7 city-loc-15)
  
  ; 366,457 -> 551,602
  (road city-loc-15 city-loc-14)
  
  ; 551,602 -> 366,457
  (road city-loc-14 city-loc-15)
  
  ; 453,848 -> 630,722
  (road city-loc-16 city-loc-3)
  
  ; 630,722 -> 453,848
  (road city-loc-3 city-loc-16)
  
  ; 453,848 -> 395,741
  (road city-loc-16 city-loc-8)
  
  ; 395,741 -> 453,848
  (road city-loc-8 city-loc-16)
  
  ; 614,343 -> 490,285
  (road city-loc-17 city-loc-1)
  
  ; 490,285 -> 614,343
  (road city-loc-1 city-loc-17)
  
  ; 614,343 -> 377,283
  (road city-loc-17 city-loc-5)
  
  ; 377,283 -> 614,343
  (road city-loc-5 city-loc-17)
  
  ; 936,210 -> 858,139
  (road city-loc-18 city-loc-10)
  
  ; 858,139 -> 936,210
  (road city-loc-10 city-loc-18)
  
  ; 193,424 -> 200,669
  (road city-loc-19 city-loc-2)
  
  ; 200,669 -> 193,424
  (road city-loc-2 city-loc-19)
  
  ; 193,424 -> 377,283
  (road city-loc-19 city-loc-5)
  
  ; 377,283 -> 193,424
  (road city-loc-5 city-loc-19)
  
  ; 193,424 -> 171,545
  (road city-loc-19 city-loc-6)
  
  ; 171,545 -> 193,424
  (road city-loc-6 city-loc-19)
  
  ; 193,424 -> 348,607
  (road city-loc-19 city-loc-7)
  
  ; 348,607 -> 193,424
  (road city-loc-7 city-loc-19)
  
  ; 193,424 -> 71,275
  (road city-loc-19 city-loc-9)
  
  ; 71,275 -> 193,424
  (road city-loc-9 city-loc-19)
  
  ; 193,424 -> 69,508
  (road city-loc-19 city-loc-11)
  
  ; 69,508 -> 193,424
  (road city-loc-11 city-loc-19)
  
  ; 193,424 -> 366,457
  (road city-loc-19 city-loc-15)
  
  ; 366,457 -> 193,424
  (road city-loc-15 city-loc-19)
  
  ; 480,435 -> 490,285
  (road city-loc-20 city-loc-1)
  
  ; 490,285 -> 480,435
  (road city-loc-1 city-loc-20)
  
  ; 480,435 -> 377,283
  (road city-loc-20 city-loc-5)
  
  ; 377,283 -> 480,435
  (road city-loc-5 city-loc-20)
  
  ; 480,435 -> 348,607
  (road city-loc-20 city-loc-7)
  
  ; 348,607 -> 480,435
  (road city-loc-7 city-loc-20)
  
  ; 480,435 -> 551,602
  (road city-loc-20 city-loc-14)
  
  ; 551,602 -> 480,435
  (road city-loc-14 city-loc-20)
  
  ; 480,435 -> 366,457
  (road city-loc-20 city-loc-15)
  
  ; 366,457 -> 480,435
  (road city-loc-15 city-loc-20)
  
  ; 480,435 -> 614,343
  (road city-loc-20 city-loc-17)
  
  ; 614,343 -> 480,435
  (road city-loc-17 city-loc-20)
  
  ; 918,341 -> 858,139
  (road city-loc-21 city-loc-10)
  
  ; 858,139 -> 918,341
  (road city-loc-10 city-loc-21)
  
  ; 918,341 -> 936,210
  (road city-loc-21 city-loc-18)
  
  ; 936,210 -> 918,341
  (road city-loc-18 city-loc-21)
  
  ; 651,235 -> 490,285
  (road city-loc-22 city-loc-1)
  
  ; 490,285 -> 651,235
  (road city-loc-1 city-loc-22)
  
  ; 651,235 -> 858,139
  (road city-loc-22 city-loc-10)
  
  ; 858,139 -> 651,235
  (road city-loc-10 city-loc-22)
  
  ; 651,235 -> 614,343
  (road city-loc-22 city-loc-17)
  
  ; 614,343 -> 651,235
  (road city-loc-17 city-loc-22)
  
  ; 560,901 -> 630,722
  (road city-loc-23 city-loc-3)
  
  ; 630,722 -> 560,901
  (road city-loc-3 city-loc-23)
  
  ; 560,901 -> 395,741
  (road city-loc-23 city-loc-8)
  
  ; 395,741 -> 560,901
  (road city-loc-8 city-loc-23)
  
  ; 560,901 -> 453,848
  (road city-loc-23 city-loc-16)
  
  ; 453,848 -> 560,901
  (road city-loc-16 city-loc-23)
  
  ; 362,940 -> 395,741
  (road city-loc-24 city-loc-8)
  
  ; 395,741 -> 362,940
  (road city-loc-8 city-loc-24)
  
  ; 362,940 -> 203,987
  (road city-loc-24 city-loc-12)
  
  ; 203,987 -> 362,940
  (road city-loc-12 city-loc-24)
  
  ; 362,940 -> 453,848
  (road city-loc-24 city-loc-16)
  
  ; 453,848 -> 362,940
  (road city-loc-16 city-loc-24)
  
  ; 362,940 -> 560,901
  (road city-loc-24 city-loc-23)
  
  ; 560,901 -> 362,940
  (road city-loc-23 city-loc-24)
  
  ; 941,734 -> 968,863
  (road city-loc-25 city-loc-13)
  
  ; 968,863 -> 941,734
  (road city-loc-13 city-loc-25)
  
  ; 653,507 -> 630,722
  (road city-loc-26 city-loc-3)
  
  ; 630,722 -> 653,507
  (road city-loc-3 city-loc-26)
  
  ; 653,507 -> 551,602
  (road city-loc-26 city-loc-14)
  
  ; 551,602 -> 653,507
  (road city-loc-14 city-loc-26)
  
  ; 653,507 -> 614,343
  (road city-loc-26 city-loc-17)
  
  ; 614,343 -> 653,507
  (road city-loc-17 city-loc-26)
  
  ; 653,507 -> 480,435
  (road city-loc-26 city-loc-20)
  
  ; 480,435 -> 653,507
  (road city-loc-20 city-loc-26)
  
  ; 820,551 -> 918,341
  (road city-loc-27 city-loc-21)
  
  ; 918,341 -> 820,551
  (road city-loc-21 city-loc-27)
  
  ; 820,551 -> 941,734
  (road city-loc-27 city-loc-25)
  
  ; 941,734 -> 820,551
  (road city-loc-25 city-loc-27)
  
  ; 820,551 -> 653,507
  (road city-loc-27 city-loc-26)
  
  ; 653,507 -> 820,551
  (road city-loc-26 city-loc-27)
  
  ; 731,24 -> 858,139
  (road city-loc-28 city-loc-10)
  
  ; 858,139 -> 731,24
  (road city-loc-10 city-loc-28)
  
  ; 731,24 -> 651,235
  (road city-loc-28 city-loc-22)
  
  ; 651,235 -> 731,24
  (road city-loc-22 city-loc-28)
  
  ; 452,192 -> 490,285
  (road city-loc-29 city-loc-1)
  
  ; 490,285 -> 452,192
  (road city-loc-1 city-loc-29)
  
  ; 452,192 -> 377,283
  (road city-loc-29 city-loc-5)
  
  ; 377,283 -> 452,192
  (road city-loc-5 city-loc-29)
  
  ; 452,192 -> 614,343
  (road city-loc-29 city-loc-17)
  
  ; 614,343 -> 452,192
  (road city-loc-17 city-loc-29)
  
  ; 452,192 -> 480,435
  (road city-loc-29 city-loc-20)
  
  ; 480,435 -> 452,192
  (road city-loc-20 city-loc-29)
  
  ; 452,192 -> 651,235
  (road city-loc-29 city-loc-22)
  
  ; 651,235 -> 452,192
  (road city-loc-22 city-loc-29)
  
  ; 205,275 -> 377,283
  (road city-loc-30 city-loc-5)
  
  ; 377,283 -> 205,275
  (road city-loc-5 city-loc-30)
  
  ; 205,275 -> 71,275
  (road city-loc-30 city-loc-9)
  
  ; 71,275 -> 205,275
  (road city-loc-9 city-loc-30)
  
  ; 205,275 -> 366,457
  (road city-loc-30 city-loc-15)
  
  ; 366,457 -> 205,275
  (road city-loc-15 city-loc-30)
  
  ; 205,275 -> 193,424
  (road city-loc-30 city-loc-19)
  
  ; 193,424 -> 205,275
  (road city-loc-19 city-loc-30)
  
  (at package-1 city-loc-4)
  (at package-2 city-loc-23)
  (at package-3 city-loc-9)
  (at package-4 city-loc-7)
  (at package-5 city-loc-6)
  (at package-6 city-loc-13)
  (at package-7 city-loc-1)
  (at package-8 city-loc-16)
  (at package-9 city-loc-11)
  (at package-10 city-loc-12)
  (at package-11 city-loc-19)
  (at truck-1 city-loc-8)
  (capacity truck-1 capacity-2)
  (at truck-2 city-loc-6)
  (capacity truck-2 capacity-4)
  (at truck-3 city-loc-24)
  (capacity truck-3 capacity-4)
 )
 (:goal (and
  (at package-1 city-loc-29)
  (at package-2 city-loc-20)
  (at package-3 city-loc-28)
  (at package-4 city-loc-28)
  (at package-5 city-loc-5)
  (at package-6 city-loc-5)
  (at package-7 city-loc-30)
  (at package-8 city-loc-29)
  (at package-9 city-loc-4)
  (at package-10 city-loc-28)
  (at package-11 city-loc-27)
 ))
 
)
