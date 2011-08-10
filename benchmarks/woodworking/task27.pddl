; woodworking task with 9 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 825203

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
    black blue mauve red white green - acolour
    pine oak - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 - part
    b0 b1 b2 - board
    s0 s1 s2 s3 s4 - aboardsize
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
    (has-colour glazer0 green)
    (has-colour glazer0 white)
    (has-colour glazer0 natural)
    (has-colour glazer0 red)
    (has-colour immersion-varnisher0 green)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 green)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 small)
    
    
    
    
    (unused p1)
    (goalsize p1 medium)
    
    
    
    
    (unused p2)
    (goalsize p2 medium)
    
    
    
    
    (unused p3)
    (goalsize p3 medium)
    
    
    
    
    (unused p4)
    (goalsize p4 small)
    
    
    
    
    (available p5)
    (colour p5 black)
    (wood p5 pine)
    (surface-condition p5 smooth)
    (treatment p5 colourfragments)
    (goalsize p5 large)
    
    
    
    
    (unused p6)
    (goalsize p6 small)
    
    
    
    
    (unused p7)
    (goalsize p7 medium)
    
    
    
    
    (unused p8)
    (goalsize p8 small)
    
    
    
    
    (boardsize b0 s4)
    (wood b0 oak)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s4)
    (wood b1 pine)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s4)
    (wood b2 pine)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (colour p0 green)
      (wood p0 oak)
      (treatment p0 glazed)
      (available p1)
      (wood p1 pine)
      (surface-condition p1 smooth)
      (available p2)
      (wood p2 pine)
      (treatment p2 glazed)
      (available p3)
      (colour p3 red)
      (wood p3 oak)
      (treatment p3 varnished)
      (available p4)
      (colour p4 natural)
      (wood p4 oak)
      (surface-condition p4 smooth)
      (treatment p4 glazed)
      (available p5)
      (colour p5 green)
      (wood p5 pine)
      (available p6)
      (colour p6 red)
      (wood p6 pine)
      (surface-condition p6 smooth)
      (available p7)
      (colour p7 white)
      (wood p7 pine)
      (surface-condition p7 verysmooth)
      (treatment p7 glazed)
      (available p8)
      (wood p8 pine)
      (surface-condition p8 smooth)
      (treatment p8 varnished)
    )
  )
  
)
