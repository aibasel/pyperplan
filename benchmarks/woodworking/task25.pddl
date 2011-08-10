; woodworking task with 7 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 173831

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
    blue mauve green red black - acolour
    beech mahogany - awood
    p0 p1 p2 p3 p4 p5 p6 - part
    b0 b1 b2 - board
    s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 - aboardsize
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
    (boardsize-successor s8 s9)
    (boardsize-successor s9 s10)
    (has-colour glazer0 blue)
    (has-colour glazer0 black)
    (has-colour glazer0 red)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 natural)
    (has-colour immersion-varnisher0 black)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 natural)
    (has-colour spray-varnisher0 black)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 medium)
    
    
    
    
    (unused p1)
    (goalsize p1 small)
    
    
    
    
    (unused p2)
    (goalsize p2 large)
    
    
    
    
    (unused p3)
    (goalsize p3 small)
    
    
    
    
    (unused p4)
    (goalsize p4 large)
    
    
    
    
    (unused p5)
    (goalsize p5 small)
    
    
    
    
    (unused p6)
    (goalsize p6 large)
    
    
    
    
    (boardsize b0 s10)
    (wood b0 beech)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s2)
    (wood b1 beech)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s2)
    (wood b2 mahogany)
    (surface-condition b2 rough)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (colour p0 blue)
      (surface-condition p0 verysmooth)
      (available p1)
      (colour p1 natural)
      (treatment p1 varnished)
      (available p2)
      (colour p2 black)
      (wood p2 beech)
      (treatment p2 glazed)
      (available p3)
      (surface-condition p3 verysmooth)
      (treatment p3 varnished)
      (available p4)
      (colour p4 black)
      (wood p4 beech)
      (treatment p4 varnished)
      (available p5)
      (surface-condition p5 verysmooth)
      (treatment p5 varnished)
      (available p6)
      (colour p6 red)
      (surface-condition p6 verysmooth)
    )
  )
  
)
