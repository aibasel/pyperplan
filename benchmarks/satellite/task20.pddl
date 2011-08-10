(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	instrument1
	instrument2
	instrument3
	instrument4
	instrument5
	instrument6
	instrument7
	instrument8
	instrument9
	satellite1
	instrument10
	instrument11
	instrument12
	instrument13
	instrument14
	instrument15
	satellite2
	instrument16
	instrument17
	instrument18
	instrument19
	satellite3
	instrument20
	instrument21
	satellite4
	instrument22
	instrument23
	instrument24
	instrument25
	instrument26
	instrument27
	instrument28
	spectrograph6
	infrared1
	thermograph8
	infrared5
	image3
	infrared9
	image2
	thermograph7
	image4
	spectrograph0
	Star0
	Star2
	Star4
	GroundStation3
	GroundStation1
	Phenomenon5
	Star6
	Planet7
	Phenomenon8
	Planet9
	Star10
	Star11
	Phenomenon12
	Planet13
	Phenomenon14
	Planet15
	Star16
	Planet17
	Planet18
	Phenomenon19
	Star20
	Phenomenon21
	Planet22
	Star23
	Star24
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 image3)
	(calibration_target instrument0 Star2)
	(instrument instrument1)
	(supports instrument1 infrared9)
	(calibration_target instrument1 Star4)
	(instrument instrument2)
	(supports instrument2 thermograph8)
	(supports instrument2 image2)
	(supports instrument2 image4)
	(calibration_target instrument2 Star4)
	(instrument instrument3)
	(supports instrument3 infrared9)
	(calibration_target instrument3 Star0)
	(instrument instrument4)
	(supports instrument4 image3)
	(supports instrument4 thermograph8)
	(calibration_target instrument4 GroundStation3)
	(instrument instrument5)
	(supports instrument5 infrared9)
	(supports instrument5 image4)
	(calibration_target instrument5 GroundStation3)
	(instrument instrument6)
	(supports instrument6 infrared1)
	(calibration_target instrument6 GroundStation3)
	(instrument instrument7)
	(supports instrument7 thermograph8)
	(supports instrument7 spectrograph6)
	(calibration_target instrument7 GroundStation1)
	(instrument instrument8)
	(supports instrument8 spectrograph0)
	(supports instrument8 infrared9)
	(supports instrument8 thermograph7)
	(calibration_target instrument8 Star2)
	(instrument instrument9)
	(supports instrument9 thermograph7)
	(calibration_target instrument9 Star4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(on_board instrument3 satellite0)
	(on_board instrument4 satellite0)
	(on_board instrument5 satellite0)
	(on_board instrument6 satellite0)
	(on_board instrument7 satellite0)
	(on_board instrument8 satellite0)
	(on_board instrument9 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation1)
	(satellite satellite1)
	(instrument instrument10)
	(supports instrument10 infrared1)
	(supports instrument10 thermograph8)
	(supports instrument10 spectrograph6)
	(calibration_target instrument10 Star4)
	(instrument instrument11)
	(supports instrument11 image4)
	(supports instrument11 thermograph7)
	(supports instrument11 infrared1)
	(calibration_target instrument11 GroundStation3)
	(instrument instrument12)
	(supports instrument12 infrared9)
	(supports instrument12 thermograph8)
	(supports instrument12 infrared5)
	(calibration_target instrument12 GroundStation3)
	(instrument instrument13)
	(supports instrument13 image2)
	(supports instrument13 infrared1)
	(calibration_target instrument13 Star4)
	(instrument instrument14)
	(supports instrument14 image3)
	(calibration_target instrument14 GroundStation3)
	(instrument instrument15)
	(supports instrument15 thermograph7)
	(calibration_target instrument15 Star2)
	(on_board instrument10 satellite1)
	(on_board instrument11 satellite1)
	(on_board instrument12 satellite1)
	(on_board instrument13 satellite1)
	(on_board instrument14 satellite1)
	(on_board instrument15 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon19)
	(satellite satellite2)
	(instrument instrument16)
	(supports instrument16 infrared9)
	(supports instrument16 image2)
	(calibration_target instrument16 Star4)
	(instrument instrument17)
	(supports instrument17 infrared5)
	(calibration_target instrument17 Star0)
	(instrument instrument18)
	(supports instrument18 infrared9)
	(calibration_target instrument18 GroundStation1)
	(instrument instrument19)
	(supports instrument19 infrared5)
	(supports instrument19 image2)
	(calibration_target instrument19 GroundStation3)
	(on_board instrument16 satellite2)
	(on_board instrument17 satellite2)
	(on_board instrument18 satellite2)
	(on_board instrument19 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Phenomenon14)
	(satellite satellite3)
	(instrument instrument20)
	(supports instrument20 image2)
	(supports instrument20 image3)
	(supports instrument20 image4)
	(calibration_target instrument20 GroundStation1)
	(instrument instrument21)
	(supports instrument21 image3)
	(supports instrument21 thermograph8)
	(supports instrument21 infrared5)
	(calibration_target instrument21 Star2)
	(on_board instrument20 satellite3)
	(on_board instrument21 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star10)
	(satellite satellite4)
	(instrument instrument22)
	(supports instrument22 thermograph8)
	(supports instrument22 infrared5)
	(calibration_target instrument22 Star4)
	(instrument instrument23)
	(supports instrument23 thermograph8)
	(supports instrument23 image3)
	(calibration_target instrument23 Star2)
	(instrument instrument24)
	(supports instrument24 thermograph8)
	(calibration_target instrument24 Star2)
	(instrument instrument25)
	(supports instrument25 infrared5)
	(calibration_target instrument25 Star2)
	(instrument instrument26)
	(supports instrument26 image3)
	(calibration_target instrument26 Star4)
	(instrument instrument27)
	(supports instrument27 image2)
	(supports instrument27 infrared9)
	(calibration_target instrument27 GroundStation3)
	(instrument instrument28)
	(supports instrument28 spectrograph0)
	(supports instrument28 image4)
	(supports instrument28 thermograph7)
	(calibration_target instrument28 GroundStation1)
	(on_board instrument22 satellite4)
	(on_board instrument23 satellite4)
	(on_board instrument24 satellite4)
	(on_board instrument25 satellite4)
	(on_board instrument26 satellite4)
	(on_board instrument27 satellite4)
	(on_board instrument28 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star16)
	(mode spectrograph6)
	(mode infrared1)
	(mode thermograph8)
	(mode infrared5)
	(mode image3)
	(mode infrared9)
	(mode image2)
	(mode thermograph7)
	(mode image4)
	(mode spectrograph0)
	(direction Star0)
	(direction Star2)
	(direction Star4)
	(direction GroundStation3)
	(direction GroundStation1)
	(direction Phenomenon5)
	(direction Star6)
	(direction Planet7)
	(direction Phenomenon8)
	(direction Planet9)
	(direction Star10)
	(direction Star11)
	(direction Phenomenon12)
	(direction Planet13)
	(direction Phenomenon14)
	(direction Planet15)
	(direction Star16)
	(direction Planet17)
	(direction Planet18)
	(direction Phenomenon19)
	(direction Star20)
	(direction Phenomenon21)
	(direction Planet22)
	(direction Star23)
	(direction Star24)
)
(:goal (and
	(pointing satellite1 Phenomenon19)
	(have_image Phenomenon5 thermograph8)
	(have_image Phenomenon5 spectrograph0)
	(have_image Phenomenon5 image3)
	(have_image Star6 spectrograph0)
	(have_image Star6 spectrograph6)
	(have_image Star6 image3)
	(have_image Planet7 spectrograph6)
	(have_image Planet7 infrared5)
	(have_image Planet7 image2)
	(have_image Phenomenon8 spectrograph6)
	(have_image Phenomenon8 infrared5)
	(have_image Phenomenon8 thermograph7)
	(have_image Planet9 spectrograph6)
	(have_image Star10 spectrograph6)
	(have_image Star11 thermograph7)
	(have_image Star11 image4)
	(have_image Star11 image3)
	(have_image Phenomenon12 image4)
	(have_image Planet13 infrared5)
	(have_image Planet13 spectrograph6)
	(have_image Planet13 image2)
	(have_image Phenomenon14 thermograph7)
	(have_image Planet15 image3)
	(have_image Star16 image3)
	(have_image Star16 image4)
	(have_image Planet18 infrared9)
	(have_image Planet18 infrared5)
	(have_image Planet18 thermograph7)
	(have_image Phenomenon19 image2)
	(have_image Phenomenon19 image4)
	(have_image Star20 spectrograph0)
	(have_image Phenomenon21 image4)
	(have_image Phenomenon21 image2)
	(have_image Phenomenon21 thermograph7)
	(have_image Planet22 image2)
	(have_image Planet22 spectrograph6)
	(have_image Star23 image2)
	(have_image Star23 infrared9)
	(have_image Star24 spectrograph6)
	(have_image Star24 infrared5)
))

)
