; woodworking task with 7 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 42617

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
    blue red white green black - acolour
    mahogany teak - awood
    p0 p1 p2 p3 p4 p5 p6 - part
    b0 b1 b2 - board
    s0 s1 s2 s3 s4 s5 s6 s7 s8 - aboardsize
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
    (boardsize-successor s7 s8)
    (has-colour glazer0 blue)
    (has-colour glazer0 green)
    (has-colour glazer0 natural)
    (has-colour glazer0 black)
    (has-colour immersion-varnisher0 black)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 black)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 large)
    
    
    
    
    (unused p1)
    (goalsize p1 large)
    
    
    
    
    (unused p2)
    (goalsize p2 small)
    
    
    
    
    (unused p3)
    (goalsize p3 small)
    
    
    
    
    (unused p4)
    (goalsize p4 small)
    
    
    
    
    (available p5)
    (colour p5 white)
    (wood p5 teak)
    (surface-condition p5 rough)
    (treatment p5 varnished)
    (goalsize p5 large)
    
    
    
    
    (unused p6)
    (goalsize p6 medium)
    
    
    
    
    (boardsize b0 s3)
    (wood b0 teak)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s8)
    (wood b1 mahogany)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s5)
    (wood b2 mahogany)
    (surface-condition b2 smooth)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (wood p0 mahogany)
      (treatment p0 glazed)
      (available p1)
      (surface-condition p1 smooth)
      (treatment p1 varnished)
      (available p2)
      (colour p2 green)
      (wood p2 teak)
      (treatment p2 glazed)
      (available p3)
      (colour p3 blue)
      (wood p3 mahogany)
      (surface-condition p3 verysmooth)
      (treatment p3 glazed)
      (available p4)
      (colour p4 red)
      (wood p4 teak)
      (surface-condition p4 smooth)
      (treatment p4 varnished)
      (available p5)
      (colour p5 natural)
      (treatment p5 glazed)
      (available p6)
      (colour p6 black)
      (wood p6 mahogany)
    )
  )
  
)
