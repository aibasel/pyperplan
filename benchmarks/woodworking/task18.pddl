; woodworking task with 10 parts and 120% wood
; Machines:
;   1 grinder
;   1 glazer
;   1 immersion-varnisher
;   1 planer
;   1 highspeed-saw
;   1 spray-varnisher
;   1 saw
; random seed: 879948

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
    black white red green mauve blue - acolour
    walnut beech teak - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 - part
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
    (has-colour glazer0 mauve)
    (has-colour glazer0 white)
    (has-colour glazer0 green)
    (has-colour glazer0 red)
    (has-colour immersion-varnisher0 mauve)
    (has-colour immersion-varnisher0 red)
    (empty highspeed-saw0)
    (has-colour spray-varnisher0 mauve)
    (has-colour spray-varnisher0 red)
    (unused p0)
    (goalsize p0 large)
    
    
    
    
    (unused p1)
    (goalsize p1 small)
    
    
    
    
    (unused p2)
    (goalsize p2 medium)
    
    
    
    
    (unused p3)
    (goalsize p3 medium)
    
    
    
    
    (unused p4)
    (goalsize p4 small)
    
    
    
    
    (unused p5)
    (goalsize p5 medium)
    
    
    
    
    (unused p6)
    (goalsize p6 medium)
    
    
    
    
    (unused p7)
    (goalsize p7 small)
    
    
    
    
    (available p8)
    (colour p8 white)
    (wood p8 walnut)
    (surface-condition p8 rough)
    (treatment p8 colourfragments)
    (goalsize p8 large)
    
    
    
    
    (unused p9)
    (goalsize p9 small)
    
    
    
    
    (boardsize b0 s8)
    (wood b0 beech)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s6)
    (wood b1 teak)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s5)
    (wood b2 walnut)
    (surface-condition b2 smooth)
    (available b2)
  )
  (:goal
    (and
      (available p0)
      (colour p0 mauve)
      (surface-condition p0 smooth)
      (available p1)
      (surface-condition p1 verysmooth)
      (treatment p1 glazed)
      (available p2)
      (wood p2 teak)
      (treatment p2 glazed)
      (available p3)
      (wood p3 teak)
      (surface-condition p3 smooth)
      (treatment p3 glazed)
      (available p4)
      (wood p4 teak)
      (surface-condition p4 verysmooth)
      (available p5)
      (colour p5 white)
      (wood p5 walnut)
      (surface-condition p5 verysmooth)
      (treatment p5 glazed)
      (available p6)
      (colour p6 green)
      (wood p6 beech)
      (treatment p6 glazed)
      (available p7)
      (surface-condition p7 verysmooth)
      (treatment p7 glazed)
      (available p8)
      (wood p8 walnut)
      (surface-condition p8 verysmooth)
      (available p9)
      (colour p9 red)
      (surface-condition p9 smooth)
    )
  )
  
)
