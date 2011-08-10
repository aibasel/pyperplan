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
	satellite3
	instrument8
	instrument9
	thermograph2
	image0
	thermograph1
	spectrograph3
	Star2
	GroundStation1
	Star0
	Star3
	Star4
	Phenomenon5
	Star6
	Star7
	Phenomenon8
	Phenomenon9
	Star10
	Planet11
	Phenomenon12
	Phenomenon13
	Phenomenon14
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 thermograph1)
	(supports instrument0 image0)
	(calibration_target instrument0 Star3)
	(instrument instrument1)
	(supports instrument1 spectrograph3)
	(supports instrument1 thermograph2)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 Star2)
	(instrument instrument2)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 Star4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon14)
	(satellite satellite1)
	(instrument instrument3)
	(supports instrument3 thermograph2)
	(supports instrument3 image0)
	(calibration_target instrument3 GroundStation1)
	(instrument instrument4)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 Star4)
	(instrument instrument5)
	(supports instrument5 thermograph2)
	(supports instrument5 thermograph1)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 Star0)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star4)
	(satellite satellite2)
	(instrument instrument6)
	(supports instrument6 thermograph1)
	(supports instrument6 thermograph2)
	(calibration_target instrument6 Star3)
	(instrument instrument7)
	(supports instrument7 thermograph2)
	(supports instrument7 thermograph1)
	(supports instrument7 image0)
	(calibration_target instrument7 Star0)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star6)
	(satellite satellite3)
	(instrument instrument8)
	(supports instrument8 image0)
	(calibration_target instrument8 Star3)
	(instrument instrument9)
	(supports instrument9 spectrograph3)
	(supports instrument9 thermograph1)
	(supports instrument9 image0)
	(calibration_target instrument9 Star4)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon5)
	(mode thermograph2)
	(mode image0)
	(mode thermograph1)
	(mode spectrograph3)
	(direction Star2)
	(direction GroundStation1)
	(direction Star0)
	(direction Star3)
	(direction Star4)
	(direction Phenomenon5)
	(direction Star6)
	(direction Star7)
	(direction Phenomenon8)
	(direction Phenomenon9)
	(direction Star10)
	(direction Planet11)
	(direction Phenomenon12)
	(direction Phenomenon13)
	(direction Phenomenon14)
)
(:goal (and
	(have_image Phenomenon5 thermograph1)
	(have_image Star6 thermograph1)
	(have_image Star7 spectrograph3)
	(have_image Phenomenon8 image0)
	(have_image Phenomenon9 image0)
	(have_image Star10 spectrograph3)
	(have_image Planet11 thermograph2)
	(have_image Phenomenon12 image0)
	(have_image Phenomenon13 thermograph1)
	(have_image Phenomenon14 thermograph2)
))

)
