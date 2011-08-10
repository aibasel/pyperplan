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
	satellite3
	instrument7
	satellite4
	instrument8
	instrument9
	instrument10
	spectrograph0
	image3
	image4
	infrared1
	image2
	Star4
	Star3
	GroundStation1
	Star0
	Star2
	Planet5
	Phenomenon6
	Phenomenon7
	Phenomenon8
	Star9
	Planet10
	Planet11
	Phenomenon12
	Phenomenon13
	Star14
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 infrared1)
	(supports instrument0 image4)
	(calibration_target instrument0 Star3)
	(instrument instrument1)
	(supports instrument1 image4)
	(supports instrument1 image2)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 Star4)
	(instrument instrument2)
	(supports instrument2 image2)
	(calibration_target instrument2 Star2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(satellite satellite1)
	(instrument instrument3)
	(supports instrument3 image2)
	(supports instrument3 image3)
	(supports instrument3 image4)
	(calibration_target instrument3 Star2)
	(instrument instrument4)
	(supports instrument4 image3)
	(supports instrument4 image2)
	(calibration_target instrument4 Star3)
	(instrument instrument5)
	(supports instrument5 image4)
	(supports instrument5 infrared1)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 Star3)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet11)
	(satellite satellite2)
	(instrument instrument6)
	(supports instrument6 image2)
	(supports instrument6 spectrograph0)
	(calibration_target instrument6 Star2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Phenomenon6)
	(satellite satellite3)
	(instrument instrument7)
	(supports instrument7 image3)
	(supports instrument7 spectrograph0)
	(supports instrument7 image4)
	(calibration_target instrument7 Star0)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Planet10)
	(satellite satellite4)
	(instrument instrument8)
	(supports instrument8 image4)
	(supports instrument8 infrared1)
	(supports instrument8 image3)
	(calibration_target instrument8 GroundStation1)
	(instrument instrument9)
	(supports instrument9 image4)
	(calibration_target instrument9 Star0)
	(instrument instrument10)
	(supports instrument10 image2)
	(supports instrument10 infrared1)
	(supports instrument10 image4)
	(calibration_target instrument10 Star2)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star9)
	(mode spectrograph0)
	(mode image3)
	(mode image4)
	(mode infrared1)
	(mode image2)
	(direction Star4)
	(direction Star3)
	(direction GroundStation1)
	(direction Star0)
	(direction Star2)
	(direction Planet5)
	(direction Phenomenon6)
	(direction Phenomenon7)
	(direction Phenomenon8)
	(direction Star9)
	(direction Planet10)
	(direction Planet11)
	(direction Phenomenon12)
	(direction Phenomenon13)
	(direction Star14)
)
(:goal (and
	(pointing satellite0 Phenomenon7)
	(pointing satellite3 Star9)
	(pointing satellite4 Planet5)
	(have_image Planet5 image2)
	(have_image Phenomenon6 image3)
	(have_image Phenomenon7 infrared1)
	(have_image Phenomenon8 image2)
	(have_image Star9 image3)
	(have_image Planet10 image4)
	(have_image Planet11 spectrograph0)
	(have_image Phenomenon12 image3)
	(have_image Phenomenon13 spectrograph0)
	(have_image Star14 image4)
))

)
