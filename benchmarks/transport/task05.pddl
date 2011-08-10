; Transport city-sequential-15nodes-1000size-3degree-100mindistance-2trucks-6packages-2008seed

(define (problem transport-city-sequential-15nodes-1000size-3degree-100mindistance-2trucks-6packages-2008seed)
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
  ; 347,149 -> 257,5
  (road city-loc-4 city-loc-1)
  
  ; 257,5 -> 347,149
  (road city-loc-1 city-loc-4)
  
  ; 347,149 -> 245,346
  (road city-loc-4 city-loc-2)
  
  ; 245,346 -> 347,149
  (road city-loc-2 city-loc-4)
  
  ; 336,475 -> 245,346
  (road city-loc-5 city-loc-2)
  
  ; 245,346 -> 336,475
  (road city-loc-2 city-loc-5)
  
  ; 336,475 -> 559,565
  (road city-loc-5 city-loc-3)
  
  ; 559,565 -> 336,475
  (road city-loc-3 city-loc-5)
  
  ; 170,709 -> 336,475
  (road city-loc-6 city-loc-5)
  
  ; 336,475 -> 170,709
  (road city-loc-5 city-loc-6)
  
  ; 521,375 -> 245,346
  (road city-loc-7 city-loc-2)
  
  ; 245,346 -> 521,375
  (road city-loc-2 city-loc-7)
  
  ; 521,375 -> 559,565
  (road city-loc-7 city-loc-3)
  
  ; 559,565 -> 521,375
  (road city-loc-3 city-loc-7)
  
  ; 521,375 -> 347,149
  (road city-loc-7 city-loc-4)
  
  ; 347,149 -> 521,375
  (road city-loc-4 city-loc-7)
  
  ; 521,375 -> 336,475
  (road city-loc-7 city-loc-5)
  
  ; 336,475 -> 521,375
  (road city-loc-5 city-loc-7)
  
  ; 720,241 -> 521,375
  (road city-loc-9 city-loc-7)
  
  ; 521,375 -> 720,241
  (road city-loc-7 city-loc-9)
  
  ; 720,241 -> 701,0
  (road city-loc-9 city-loc-8)
  
  ; 701,0 -> 720,241
  (road city-loc-8 city-loc-9)
  
  ; 630,722 -> 559,565
  (road city-loc-10 city-loc-3)
  
  ; 559,565 -> 630,722
  (road city-loc-3 city-loc-10)
  
  ; 120,854 -> 170,709
  (road city-loc-11 city-loc-6)
  
  ; 170,709 -> 120,854
  (road city-loc-6 city-loc-11)
  
  ; 377,283 -> 245,346
  (road city-loc-12 city-loc-2)
  
  ; 245,346 -> 377,283
  (road city-loc-2 city-loc-12)
  
  ; 377,283 -> 347,149
  (road city-loc-12 city-loc-4)
  
  ; 347,149 -> 377,283
  (road city-loc-4 city-loc-12)
  
  ; 377,283 -> 336,475
  (road city-loc-12 city-loc-5)
  
  ; 336,475 -> 377,283
  (road city-loc-5 city-loc-12)
  
  ; 377,283 -> 521,375
  (road city-loc-12 city-loc-7)
  
  ; 521,375 -> 377,283
  (road city-loc-7 city-loc-12)
  
  ; 171,545 -> 245,346
  (road city-loc-13 city-loc-2)
  
  ; 245,346 -> 171,545
  (road city-loc-2 city-loc-13)
  
  ; 171,545 -> 336,475
  (road city-loc-13 city-loc-5)
  
  ; 336,475 -> 171,545
  (road city-loc-5 city-loc-13)
  
  ; 171,545 -> 170,709
  (road city-loc-13 city-loc-6)
  
  ; 170,709 -> 171,545
  (road city-loc-6 city-loc-13)
  
  ; 348,607 -> 245,346
  (road city-loc-14 city-loc-2)
  
  ; 245,346 -> 348,607
  (road city-loc-2 city-loc-14)
  
  ; 348,607 -> 559,565
  (road city-loc-14 city-loc-3)
  
  ; 559,565 -> 348,607
  (road city-loc-3 city-loc-14)
  
  ; 348,607 -> 336,475
  (road city-loc-14 city-loc-5)
  
  ; 336,475 -> 348,607
  (road city-loc-5 city-loc-14)
  
  ; 348,607 -> 170,709
  (road city-loc-14 city-loc-6)
  
  ; 170,709 -> 348,607
  (road city-loc-6 city-loc-14)
  
  ; 348,607 -> 521,375
  (road city-loc-14 city-loc-7)
  
  ; 521,375 -> 348,607
  (road city-loc-7 city-loc-14)
  
  ; 348,607 -> 171,545
  (road city-loc-14 city-loc-13)
  
  ; 171,545 -> 348,607
  (road city-loc-13 city-loc-14)
  
  ; 395,741 -> 559,565
  (road city-loc-15 city-loc-3)
  
  ; 559,565 -> 395,741
  (road city-loc-3 city-loc-15)
  
  ; 395,741 -> 336,475
  (road city-loc-15 city-loc-5)
  
  ; 336,475 -> 395,741
  (road city-loc-5 city-loc-15)
  
  ; 395,741 -> 170,709
  (road city-loc-15 city-loc-6)
  
  ; 170,709 -> 395,741
  (road city-loc-6 city-loc-15)
  
  ; 395,741 -> 630,722
  (road city-loc-15 city-loc-10)
  
  ; 630,722 -> 395,741
  (road city-loc-10 city-loc-15)
  
  ; 395,741 -> 120,854
  (road city-loc-15 city-loc-11)
  
  ; 120,854 -> 395,741
  (road city-loc-11 city-loc-15)
  
  ; 395,741 -> 171,545
  (road city-loc-15 city-loc-13)
  
  ; 171,545 -> 395,741
  (road city-loc-13 city-loc-15)
  
  ; 395,741 -> 348,607
  (road city-loc-15 city-loc-14)
  
  ; 348,607 -> 395,741
  (road city-loc-14 city-loc-15)
  
  (at package-1 city-loc-10)
  (at package-2 city-loc-11)
  (at package-3 city-loc-5)
  (at package-4 city-loc-9)
  (at package-5 city-loc-6)
  (at package-6 city-loc-4)
  (at truck-1 city-loc-12)
  (capacity truck-1 capacity-3)
  (at truck-2 city-loc-5)
  (capacity truck-2 capacity-2)
 )
 (:goal (and
  (at package-1 city-loc-13)
  (at package-2 city-loc-3)
  (at package-3 city-loc-2)
  (at package-4 city-loc-8)
  (at package-5 city-loc-4)
  (at package-6 city-loc-15)
 ))
 
)
