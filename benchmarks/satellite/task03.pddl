(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	instrument1
	instrument2
	satellite1
	instrument3
	image1
	infrared0
	spectrograph2
	Star1
	Star2
	Star0
	Star3
	Star4
	Phenomenon5
	Phenomenon6
	Phenomenon7
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 spectrograph2)
	(supports instrument0 infrared0)
	(calibration_target instrument0 Star1)
	(instrument instrument1)
	(supports instrument1 image1)
	(calibration_target instrument1 Star2)
	(instrument instrument2)
	(supports instrument2 infrared0)
	(supports instrument2 image1)
	(calibration_target instrument2 Star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star4)
	(satellite satellite1)
	(instrument instrument3)
	(supports instrument3 spectrograph2)
	(supports instrument3 infrared0)
	(supports instrument3 image1)
	(calibration_target instrument3 Star0)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star0)
	(mode image1)
	(mode infrared0)
	(mode spectrograph2)
	(direction Star1)
	(direction Star2)
	(direction Star0)
	(direction Star3)
	(direction Star4)
	(direction Phenomenon5)
	(direction Phenomenon6)
	(direction Phenomenon7)
)
(:goal (and
	(pointing satellite0 Phenomenon5)
	(have_image Star3 infrared0)
	(have_image Star4 spectrograph2)
	(have_image Phenomenon5 spectrograph2)
	(have_image Phenomenon7 spectrograph2)
))

)
