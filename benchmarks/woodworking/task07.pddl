; woodworking task with 9 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 166664

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
    black mauve green red blue white - acolour
    pine cherry - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 - part
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
    (has-colour glazer0 green)
    (has-colour glazer0 white)
    (has-colour glazer0 black)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 green)
    (has-colour immersion-varnisher0 white)
    (has-colour immersion-varnisher0 black)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 green)
    (has-colour spray-varnisher0 white)
    (has-colour spray-varnisher0 black)
    (unused p0)
    (goalsize p0 large)
    
    
    
    
    (unused p1)
    (goalsize p1 medium)
    
    
    
    
    (unused p2)
    (goalsize p2 small)
    
    
    
    
    (available p3)
    (colour p3 mauve)
    (wood p3 cherry)
    (surface-condition p3 rough)
    (treatment p3 glazed)
    (goalsize p3 small)
    
    
    
    
    (available p4)
    (colour p4 natural)
    (wood p4 cherry)
    (surface-condition p4 verysmooth)
    (treatment p4 varnished)
    (goalsize p4 large)
    
    
    
    
    (unused p5)
    (goalsize p5 small)
    
    
    
    
    (unused p6)
    (goalsize p6 large)
    
    
    
    
    (available p7)
    (colour p7 natural)
    (wood p7 pine)
    (surface-condition p7 smooth)
    (treatment p7 colourfragments)
    (goalsize p7 small)
    
    
    
    
    (unused p8)
    (goalsize p8 large)
    
    
    
    
    (boardsize b0 s6)
    (wood b0 cherry)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s7)
    (wood b1 pine)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s6)
    (wood b2 pine)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (colour p0 green)
      (surface-condition p0 smooth)
      (available p1)
      (colour p1 black)
      (wood p1 pine)
      (treatment p1 glazed)
      (available p2)
      (wood p2 cherry)
      (surface-condition p2 verysmooth)
      (treatment p2 varnished)
      (available p3)
      (colour p3 black)
      (surface-condition p3 verysmooth)
      (available p4)
      (colour p4 white)
      (wood p4 cherry)
      (surface-condition p4 smooth)
      (available p5)
      (colour p5 green)
      (wood p5 pine)
      (available p6)
      (colour p6 white)
      (wood p6 cherry)
      (surface-condition p6 smooth)
      (treatment p6 glazed)
      (available p7)
      (colour p7 blue)
      (wood p7 pine)
      (surface-condition p7 smooth)
      (treatment p7 varnished)
      (available p8)
      (colour p8 white)
      (surface-condition p8 smooth)
    )
  )
  
)
