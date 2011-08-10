; woodworking task with 8 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 960077

(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    grinder0 - grinder
    glazer0 - glazer
    immersion-varnisher0 - immersion-varnisher
    planer0 - planer
    highspeed-saw0 - highspeed-saw
    spray-varnisher0 - spray-varnisher
    saw0 - saw
    black white blue red green mauve - acolour
    teak pine - awood
    p0 p1 p2 p3 p4 p5 p6 p7 - part
    b0 b1 b2 - board
    s0 s1 s2 s3 s4 s5 s6 s7 - aboardsize
  )
  (:init
    (grind-treatment-change varnished colourfragments)
    (grind-treatment-change glazed untreated)
    (grind-treatment-change untreated untreated)
    (grind-treatment-change colourfragments untreated)
    (is-smooth smooth)
    (is-smooth verysmooth)
    
    (boardsize-successor s0 s1)
    (boardsize-successor s1 s2)
    (boardsize-successor s2 s3)
    (boardsize-successor s3 s4)
    (boardsize-successor s4 s5)
    (boardsize-successor s5 s6)
    (boardsize-successor s6 s7)
    (has-colour glazer0 blue)
    (has-colour glazer0 white)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 white)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 white)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 large)
    
    
    
    
    (unused p1)
    (goalsize p1 small)
    
    
    
    
    (unused p2)
    (goalsize p2 small)
    
    
    
    
    (unused p3)
    (goalsize p3 medium)
    
    
    
    
    (available p4)
    (colour p4 green)
    (wood p4 teak)
    (surface-condition p4 rough)
    (treatment p4 colourfragments)
    (goalsize p4 small)
    
    
    
    
    (unused p5)
    (goalsize p5 large)
    
    
    
    
    (unused p6)
    (goalsize p6 medium)
    
    
    
    
    (unused p7)
    (goalsize p7 medium)
    
    
    
    
    (boardsize b0 s7)
    (wood b0 teak)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s4)
    (wood b1 teak)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s3)
    (wood b2 pine)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (wood p0 teak)
      (surface-condition p0 smooth)
      (available p1)
      (wood p1 teak)
      (surface-condition p1 smooth)
      (treatment p1 varnished)
      (available p2)
      (colour p2 red)
      (wood p2 teak)
      (treatment p2 varnished)
      (available p3)
      (colour p3 blue)
      (wood p3 teak)
      (surface-condition p3 smooth)
      (treatment p3 glazed)
      (available p4)
      (colour p4 white)
      (wood p4 teak)
      (surface-condition p4 smooth)
      (available p5)
      (wood p5 pine)
      (treatment p5 varnished)
      (available p6)
      (wood p6 teak)
      (surface-condition p6 verysmooth)
      (available p7)
      (colour p7 blue)
      (treatment p7 varnished)
    )
  )
  
)
