(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	instrument1
	satellite1
	instrument2
	instrument3
	satellite2
	instrument4
	instrument5
	satellite3
	instrument6
	instrument7
	satellite4
	instrument8
	instrument9
	instrument10
	infrared0
	spectrograph1
	infrared3
	image4
	image2
	Star1
	GroundStation3
	Star4
	Star2
	Star0
	Planet5
	Star6
	Star7
	Phenomenon8
	Planet9
	Planet10
	Star11
	Star12
	Phenomenon13
	Phenomenon14
	Star15
	Star16
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 image4)
	(calibration_target instrument0 Star1)
	(instrument instrument1)
	(supports instrument1 infrared0)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 GroundStation3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(satellite satellite1)
	(instrument instrument2)
	(supports instrument2 infrared0)
	(supports instrument2 image2)
	(calibration_target instrument2 GroundStation3)
	(instrument instrument3)
	(supports instrument3 infrared3)
	(supports instrument3 infrared0)
	(calibration_target instrument3 Star4)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star4)
	(satellite satellite2)
	(instrument instrument4)
	(supports instrument4 spectrograph1)
	(supports instrument4 image4)
	(supports instrument4 infrared0)
	(calibration_target instrument4 Star2)
	(instrument instrument5)
	(supports instrument5 image2)
	(supports instrument5 infrared0)
	(supports instrument5 infrared3)
	(calibration_target instrument5 Star0)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star1)
	(satellite satellite3)
	(instrument instrument6)
	(supports instrument6 infrared0)
	(supports instrument6 infrared3)
	(calibration_target instrument6 GroundStation3)
	(instrument instrument7)
	(supports instrument7 image4)
	(supports instrument7 spectrograph1)
	(supports instrument7 infrared3)
	(calibration_target instrument7 Star4)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 GroundStation3)
	(satellite satellite4)
	(instrument instrument8)
	(supports instrument8 spectrograph1)
	(supports instrument8 image4)
	(calibration_target instrument8 Star4)
	(instrument instrument9)
	(supports instrument9 infrared3)
	(calibration_target instrument9 Star2)
	(instrument instrument10)
	(supports instrument10 image2)
	(supports instrument10 image4)
	(calibration_target instrument10 Star0)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Planet10)
	(mode infrared0)
	(mode spectrograph1)
	(mode infrared3)
	(mode image4)
	(mode image2)
	(direction Star1)
	(direction GroundStation3)
	(direction Star4)
	(direction Star2)
	(direction Star0)
	(direction Planet5)
	(direction Star6)
	(direction Star7)
	(direction Phenomenon8)
	(direction Planet9)
	(direction Planet10)
	(direction Star11)
	(direction Star12)
	(direction Phenomenon13)
	(direction Phenomenon14)
	(direction Star15)
	(direction Star16)
)
(:goal (and
	(pointing satellite4 Planet9)
	(have_image Planet5 image4)
	(have_image Star6 infrared3)
	(have_image Star7 image4)
	(have_image Phenomenon8 image4)
	(have_image Planet9 infrared0)
	(have_image Planet10 infrared3)
	(have_image Star12 image4)
	(have_image Phenomenon13 image4)
	(have_image Phenomenon14 spectrograph1)
	(have_image Star15 spectrograph1)
	(have_image Star16 image2)
))

)
