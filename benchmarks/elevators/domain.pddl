(define (domain elevators-sequencedstrips)
  (:requirements :typing )
  (:types 	elevator - object 
			slow-elevator fast-elevator - elevator
   			passenger - object
          	count - object
         )

(:predicates 
	(passenger-at ?person - passenger ?floor - count)
	(boarded ?person - passenger ?lift - elevator)
	(lift-at ?lift - elevator ?floor - count)
	(reachable-floor ?lift - elevator ?floor - count)
	(above ?floor1 - count ?floor2 - count)
	(passengers ?lift - elevator ?n - count)
	(can-hold ?lift - elevator ?n - count)
	(next ?n1 - count ?n2 - count)
)



(:action move-up-slow
  :parameters (?lift - slow-elevator ?f1 - count ?f2 - count )
  :precondition (and (lift-at ?lift ?f1) (above ?f1 ?f2 ) (reachable-floor ?lift ?f2) )
  :effect (and (lift-at ?lift ?f2) (not (lift-at ?lift ?f1)) ))

(:action move-down-slow
  :parameters (?lift - slow-elevator ?f1 - count ?f2 - count )
  :precondition (and (lift-at ?lift ?f1) (above ?f2 ?f1 ) (reachable-floor ?lift ?f2) )
  :effect (and (lift-at ?lift ?f2) (not (lift-at ?lift ?f1)) ))

(:action move-up-fast
  :parameters (?lift - fast-elevator ?f1 - count ?f2 - count )
  :precondition (and (lift-at ?lift ?f1) (above ?f1 ?f2 ) (reachable-floor ?lift ?f2) )
  :effect (and (lift-at ?lift ?f2) (not (lift-at ?lift ?f1)) ))

(:action move-down-fast
  :parameters (?lift - fast-elevator ?f1 - count ?f2 - count )
  :precondition (and (lift-at ?lift ?f1) (above ?f2 ?f1 ) (reachable-floor ?lift ?f2) )
  :effect (and (lift-at ?lift ?f2) (not (lift-at ?lift ?f1)) ))

(:action board
  :parameters (?p - passenger ?lift - elevator ?f - count ?n1 - count ?n2 - count)
  :precondition (and  (lift-at ?lift ?f) (passenger-at ?p ?f) (passengers ?lift ?n1) (next ?n1 ?n2) (can-hold ?lift ?n2) )
  :effect (and (not (passenger-at ?p ?f)) (boarded ?p ?lift) (not (passengers ?lift ?n1)) (passengers ?lift ?n2) ))

(:action leave 
  :parameters (?p - passenger ?lift - elevator ?f - count ?n1 - count ?n2 - count)
  :precondition (and  (lift-at ?lift ?f) (boarded ?p ?lift) (passengers ?lift ?n1) (next ?n2 ?n1) )
  :effect (and (passenger-at ?p ?f) (not (boarded ?p ?lift)) (not (passengers ?lift ?n1)) (passengers ?lift ?n2) ))
  
)

