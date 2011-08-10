; woodworking task with 12 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 987123

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
    white red mauve black green blue - acolour
    oak pine beech - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 - part
    b0 b1 b2 b3 b4 - board
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
    (has-colour glazer0 natural)
    (has-colour glazer0 black)
    (has-colour glazer0 mauve)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 black)
    (has-colour immersion-varnisher0 green)
    (has-colour immersion-varnisher0 natural)
    (has-colour immersion-varnisher0 mauve)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 black)
    (has-colour spray-varnisher0 green)
    (has-colour spray-varnisher0 natural)
    (has-colour spray-varnisher0 mauve)
    (unused p0)
    (goalsize p0 large)
    
    
    
    
    (available p1)
    (colour p1 black)
    (wood p1 pine)
    (surface-condition p1 verysmooth)
    (treatment p1 varnished)
    (goalsize p1 large)
    
    
    
    
    (available p2)
    (colour p2 blue)
    (wood p2 beech)
    (surface-condition p2 smooth)
    (treatment p2 varnished)
    (goalsize p2 large)
    
    
    
    
    (unused p3)
    (goalsize p3 small)
    
    
    
    
    (unused p4)
    (goalsize p4 medium)
    
    
    
    
    (unused p5)
    (goalsize p5 medium)
    
    
    
    
    (unused p6)
    (goalsize p6 large)
    
    
    
    
    (unused p7)
    (goalsize p7 large)
    
    
    
    
    (unused p8)
    (goalsize p8 medium)
    
    
    
    
    (unused p9)
    (goalsize p9 small)
    
    
    
    
    (unused p10)
    (goalsize p10 large)
    
    
    
    
    (unused p11)
    (goalsize p11 large)
    
    
    
    
    (boardsize b0 s9)
    (wood b0 beech)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s10)
    (wood b1 oak)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s3)
    (wood b2 oak)
    (surface-condition b2 smooth)
    (available b2)
    (boardsize b3 s9)
    (wood b3 pine)
    (surface-condition b3 smooth)
    (available b3)
    (boardsize b4 s3)
    (wood b4 pine)
    (surface-condition b4 rough)
    (available b4)
  )
  (:goal
    (and
      (available p0)
      (colour p0 blue)
      (surface-condition p0 smooth)
      (available p1)
      (colour p1 natural)
      (surface-condition p1 smooth)
      (available p2)
      (surface-condition p2 verysmooth)
      (treatment p2 varnished)
      (available p3)
      (wood p3 pine)
      (surface-condition p3 smooth)
      (treatment p3 varnished)
      (available p4)
      (colour p4 black)
      (treatment p4 varnished)
      (available p5)
      (surface-condition p5 verysmooth)
      (treatment p5 varnished)
      (available p6)
      (wood p6 pine)
      (treatment p6 varnished)
      (available p7)
      (colour p7 green)
      (wood p7 oak)
      (surface-condition p7 verysmooth)
      (treatment p7 varnished)
      (available p8)
      (colour p8 black)
      (wood p8 beech)
      (available p9)
      (colour p9 blue)
      (wood p9 beech)
      (surface-condition p9 smooth)
      (treatment p9 glazed)
      (available p10)
      (colour p10 natural)
      (surface-condition p10 verysmooth)
      (available p11)
      (colour p11 mauve)
      (wood p11 oak)
      (surface-condition p11 smooth)
    )
  )
  
)
