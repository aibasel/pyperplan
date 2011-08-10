; woodworking task with 11 parts and 100% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 623538

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
    red green black mauve white blue - acolour
    teak pine walnut - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 - part
    b0 b1 b2 b3 - board
    s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 - aboardsize
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
    (has-colour glazer0 green)
    (has-colour glazer0 black)
    (has-colour glazer0 natural)
    (has-colour glazer0 red)
    (has-colour glazer0 mauve)
    (has-colour immersion-varnisher0 mauve)
    (has-colour immersion-varnisher0 white)
    (has-colour immersion-varnisher0 natural)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 mauve)
    (has-colour spray-varnisher0 white)
    (has-colour spray-varnisher0 natural)
    (unused p0)
    (goalsize p0 medium)
    
    
    
    
    (unused p1)
    (goalsize p1 medium)
    
    
    
    
    (unused p2)
    (goalsize p2 small)
    
    
    
    
    (unused p3)
    (goalsize p3 large)
    
    
    
    
    (unused p4)
    (goalsize p4 large)
    
    
    
    
    (unused p5)
    (goalsize p5 large)
    
    
    
    
    (available p6)
    (colour p6 natural)
    (wood p6 walnut)
    (surface-condition p6 verysmooth)
    (treatment p6 varnished)
    (goalsize p6 large)
    
    
    
    
    (unused p7)
    (goalsize p7 medium)
    
    
    
    
    (unused p8)
    (goalsize p8 medium)
    
    
    
    
    (unused p9)
    (goalsize p9 medium)
    
    
    
    
    (unused p10)
    (goalsize p10 small)
    
    
    
    
    (boardsize b0 s9)
    (wood b0 teak)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s0)
    (wood b1 teak)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s8)
    (wood b2 pine)
    (surface-condition b2 rough)
    (available b2)
    (boardsize b3 s4)
    (wood b3 walnut)
    (surface-condition b3 rough)
    (available b3)
  )
  (:goal
    (and
      (available p0)
      (colour p0 red)
      (wood p0 walnut)
      (treatment p0 glazed)
      (available p1)
      (colour p1 green)
      (treatment p1 glazed)
      (available p2)
      (colour p2 natural)
      (surface-condition p2 verysmooth)
      (available p3)
      (surface-condition p3 verysmooth)
      (treatment p3 varnished)
      (available p4)
      (colour p4 black)
      (treatment p4 glazed)
      (available p5)
      (colour p5 white)
      (wood p5 pine)
      (surface-condition p5 smooth)
      (treatment p5 varnished)
      (available p6)
      (colour p6 mauve)
      (wood p6 walnut)
      (available p7)
      (surface-condition p7 smooth)
      (treatment p7 glazed)
      (available p8)
      (wood p8 pine)
      (surface-condition p8 verysmooth)
      (treatment p8 varnished)
      (available p9)
      (surface-condition p9 smooth)
      (treatment p9 varnished)
      (available p10)
      (wood p10 walnut)
      (surface-condition p10 smooth)
    )
  )
  
)
