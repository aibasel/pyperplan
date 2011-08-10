(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	satellite1
	instrument1
	instrument2
	instrument3
	satellite2
	instrument4
	thermograph2
	spectrograph0
	infrared1
	infrared3
	GroundStation3
	Star1
	Star2
	Star0
	Planet4
	Planet5
	Star6
	Star7
	Phenomenon8
	Star9
	Star10
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 infrared1)
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 Star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon8)
	(satellite satellite1)
	(instrument instrument1)
	(supports instrument1 infrared3)
	(calibration_target instrument1 Star2)
	(instrument instrument2)
	(supports instrument2 infrared1)
	(supports instrument2 infrared3)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 Star2)
	(instrument instrument3)
	(supports instrument3 infrared1)
	(supports instrument3 infrared3)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 Star2)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star6)
	(satellite satellite2)
	(instrument instrument4)
	(supports instrument4 infrared3)
	(calibration_target instrument4 Star0)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star6)
	(mode thermograph2)
	(mode spectrograph0)
	(mode infrared1)
	(mode infrared3)
	(direction GroundStation3)
	(direction Star1)
	(direction Star2)
	(direction Star0)
	(direction Planet4)
	(direction Planet5)
	(direction Star6)
	(direction Star7)
	(direction Phenomenon8)
	(direction Star9)
	(direction Star10)
)
(:goal (and
	(have_image Planet4 thermograph2)
	(have_image Planet5 spectrograph0)
	(have_image Star6 thermograph2)
	(have_image Star7 infrared3)
	(have_image Phenomenon8 spectrograph0)
	(have_image Star9 infrared1)
	(have_image Star10 infrared3)
))

)
