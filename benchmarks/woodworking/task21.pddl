; woodworking task with 3 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 20683

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
    red blue - acolour
    oak beech - awood
    p0 p1 p2 - part
    b0 - board
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
    (has-colour glazer0 red)
    (has-colour immersion-varnisher0 natural)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 natural)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 small)
    
    
    
    
    (available p1)
    (colour p1 blue)
    (wood p1 oak)
    (surface-condition p1 rough)
    (treatment p1 varnished)
    (goalsize p1 large)
    
    
    
    
    (unused p2)
    (goalsize p2 large)
    
    
    
    
    (boardsize b0 s4)
    (wood b0 oak)
    (surface-condition b0 smooth)
    (available b0)
  )
  (:goal
    (and
      (available p0)
      (colour p0 natural)
      (treatment p0 varnished)
      (available p1)
      (wood p1 oak)
      (surface-condition p1 smooth)
      (available p2)
      (colour p2 red)
      (wood p2 oak)
      (surface-condition p2 smooth)
      (treatment p2 varnished)
    )
  )
  
)
