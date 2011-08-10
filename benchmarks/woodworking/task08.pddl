; woodworking task with 10 parts and 140% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 302921

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
    green mauve white black red blue - acolour
    cherry oak mahogany - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 - part
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
    (has-colour glazer0 black)
    (has-colour glazer0 green)
    (has-colour glazer0 red)
    (has-colour glazer0 mauve)
    (has-colour immersion-varnisher0 white)
    (has-colour immersion-varnisher0 black)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 white)
    (has-colour spray-varnisher0 black)
    (has-colour spray-varnisher0 red)
    (available p0)
    (colour p0 mauve)
    (wood p0 cherry)
    (surface-condition p0 smooth)
    (treatment p0 colourfragments)
    (goalsize p0 small)
    
    
    
    
    (unused p1)
    (goalsize p1 large)
    
    
    
    
    (available p2)
    (colour p2 red)
    (wood p2 oak)
    (surface-condition p2 rough)
    (treatment p2 colourfragments)
    (goalsize p2 small)
    
    
    
    
    (available p3)
    (colour p3 black)
    (wood p3 mahogany)
    (surface-condition p3 verysmooth)
    (treatment p3 glazed)
    (goalsize p3 medium)
    
    
    
    
    (unused p4)
    (goalsize p4 large)
    
    
    
    
    (unused p5)
    (goalsize p5 medium)
    
    
    
    
    (unused p6)
    (goalsize p6 large)
    
    
    
    
    (unused p7)
    (goalsize p7 large)
    
    
    
    
    (unused p8)
    (goalsize p8 small)
    
    
    
    
    (unused p9)
    (goalsize p9 medium)
    
    
    
    
    (boardsize b0 s9)
    (wood b0 cherry)
    (surface-condition b0 smooth)
    (available b0)
    (boardsize b1 s3)
    (wood b1 cherry)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s10)
    (wood b2 mahogany)
    (surface-condition b2 smooth)
    (available b2)
    (boardsize b3 s2)
    (wood b3 mahogany)
    (surface-condition b3 rough)
    (available b3)
    (boardsize b4 s2)
    (wood b4 oak)
    (surface-condition b4 rough)
    (available b4)
  )
  (:goal
    (and
      (available p0)
      (surface-condition p0 verysmooth)
      (treatment p0 glazed)
      (available p1)
      (wood p1 cherry)
      (surface-condition p1 verysmooth)
      (available p2)
      (colour p2 black)
      (wood p2 oak)
      (surface-condition p2 smooth)
      (treatment p2 varnished)
      (available p3)
      (colour p3 white)
      (wood p3 mahogany)
      (surface-condition p3 verysmooth)
      (treatment p3 varnished)
      (available p4)
      (colour p4 black)
      (treatment p4 glazed)
      (available p5)
      (wood p5 mahogany)
      (surface-condition p5 verysmooth)
      (available p6)
      (surface-condition p6 smooth)
      (treatment p6 glazed)
      (available p7)
      (colour p7 green)
      (wood p7 mahogany)
      (surface-condition p7 verysmooth)
      (treatment p7 glazed)
      (available p8)
      (colour p8 red)
      (wood p8 oak)
      (surface-condition p8 smooth)
      (available p9)
      (colour p9 mauve)
      (treatment p9 glazed)
    )
  )
  
)
