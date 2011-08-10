(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	instrument1
	instrument2
	satellite1
	instrument3
	instrument4
	instrument5
	satellite2
	instrument6
	instrument7
	instrument8
	thermograph0
	image2
	spectrograph1
	GroundStation2
	GroundStation1
	GroundStation0
	Star3
	Star4
	Phenomenon5
	Phenomenon6
	Star7
	Phenomenon8
	Planet9
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 image2)
	(supports instrument0 thermograph0)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 GroundStation2)
	(instrument instrument1)
	(supports instrument1 thermograph0)
	(supports instrument1 spectrograph1)
	(supports instrument1 image2)
	(calibration_target instrument1 GroundStation1)
	(instrument instrument2)
	(supports instrument2 image2)
	(calibration_target instrument2 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon8)
	(satellite satellite1)
	(instrument instrument3)
	(supports instrument3 spectrograph1)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 GroundStation0)
	(instrument instrument4)
	(supports instrument4 image2)
	(supports instrument4 spectrograph1)
	(calibration_target instrument4 GroundStation2)
	(instrument instrument5)
	(supports instrument5 image2)
	(supports instrument5 spectrograph1)
	(supports instrument5 thermograph0)
	(calibration_target instrument5 GroundStation1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation2)
	(satellite satellite2)
	(instrument instrument6)
	(supports instrument6 image2)
	(calibration_target instrument6 GroundStation1)
	(instrument instrument7)
	(supports instrument7 image2)
	(supports instrument7 thermograph0)
	(calibration_target instrument7 GroundStation1)
	(instrument instrument8)
	(supports instrument8 spectrograph1)
	(supports instrument8 image2)
	(supports instrument8 thermograph0)
	(calibration_target instrument8 GroundStation0)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(on_board instrument8 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Phenomenon5)
	(mode thermograph0)
	(mode image2)
	(mode spectrograph1)
	(direction GroundStation2)
	(direction GroundStation1)
	(direction GroundStation0)
	(direction Star3)
	(direction Star4)
	(direction Phenomenon5)
	(direction Phenomenon6)
	(direction Star7)
	(direction Phenomenon8)
	(direction Planet9)
)
(:goal (and
	(pointing satellite0 Phenomenon5)
	(pointing satellite1 GroundStation2)
	(have_image Star3 thermograph0)
	(have_image Phenomenon5 image2)
	(have_image Phenomenon6 image2)
	(have_image Star7 thermograph0)
	(have_image Phenomenon8 image2)
	(have_image Planet9 spectrograph1)
))

)
