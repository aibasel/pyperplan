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
	satellite2
	instrument5
	satellite3
	instrument6
	satellite4
	instrument7
	instrument8
	instrument9
	thermograph2
	infrared0
	infrared1
	spectrograph4
	infrared3
	Star0
	Star3
	GroundStation1
	Star2
	Star4
	Planet5
	Phenomenon6
	Star7
	Planet8
	Star9
	Planet10
	Planet11
	Star12
	Phenomenon13
	Star14
	Star15
	Planet16
	Phenomenon17
	Star18
	Star19
	Planet20
	Phenomenon21
	Star22
	Star23
	Phenomenon24
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 infrared1)
	(supports instrument0 spectrograph4)
	(calibration_target instrument0 Star0)
	(instrument instrument1)
	(supports instrument1 infrared1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 Star2)
	(instrument instrument2)
	(supports instrument2 infrared1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 Star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet16)
	(satellite satellite1)
	(instrument instrument3)
	(supports instrument3 infrared0)
	(supports instrument3 spectrograph4)
	(calibration_target instrument3 Star4)
	(instrument instrument4)
	(supports instrument4 infrared0)
	(supports instrument4 infrared3)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 Star4)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star4)
	(satellite satellite2)
	(instrument instrument5)
	(supports instrument5 infrared1)
	(calibration_target instrument5 GroundStation1)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star15)
	(satellite satellite3)
	(instrument instrument6)
	(supports instrument6 infrared1)
	(calibration_target instrument6 Star4)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon6)
	(satellite satellite4)
	(instrument instrument7)
	(supports instrument7 infrared1)
	(supports instrument7 infrared3)
	(calibration_target instrument7 Star2)
	(instrument instrument8)
	(supports instrument8 infrared0)
	(supports instrument8 infrared3)
	(supports instrument8 spectrograph4)
	(calibration_target instrument8 Star2)
	(instrument instrument9)
	(supports instrument9 infrared3)
	(supports instrument9 spectrograph4)
	(supports instrument9 infrared1)
	(calibration_target instrument9 Star4)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star14)
	(mode thermograph2)
	(mode infrared0)
	(mode infrared1)
	(mode spectrograph4)
	(mode infrared3)
	(direction Star0)
	(direction Star3)
	(direction GroundStation1)
	(direction Star2)
	(direction Star4)
	(direction Planet5)
	(direction Phenomenon6)
	(direction Star7)
	(direction Planet8)
	(direction Star9)
	(direction Planet10)
	(direction Planet11)
	(direction Star12)
	(direction Phenomenon13)
	(direction Star14)
	(direction Star15)
	(direction Planet16)
	(direction Phenomenon17)
	(direction Star18)
	(direction Star19)
	(direction Planet20)
	(direction Phenomenon21)
	(direction Star22)
	(direction Star23)
	(direction Phenomenon24)
)
(:goal (and
	(have_image Planet5 infrared0)
	(have_image Phenomenon6 spectrograph4)
	(have_image Star7 infrared0)
	(have_image Planet8 infrared1)
	(have_image Star9 spectrograph4)
	(have_image Planet10 thermograph2)
	(have_image Planet11 infrared3)
	(have_image Phenomenon13 spectrograph4)
	(have_image Star14 thermograph2)
	(have_image Star15 infrared3)
	(have_image Planet16 infrared1)
	(have_image Phenomenon17 spectrograph4)
	(have_image Star18 spectrograph4)
	(have_image Star19 thermograph2)
	(have_image Planet20 thermograph2)
	(have_image Phenomenon21 thermograph2)
	(have_image Star22 infrared1)
	(have_image Star23 spectrograph4)
	(have_image Phenomenon24 infrared0)
))

)
