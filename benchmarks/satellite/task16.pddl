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
	satellite5
	instrument11
	instrument12
	instrument13
	satellite6
	instrument14
	instrument15
	instrument16
	satellite7
	instrument17
	instrument18
	satellite8
	instrument19
	instrument20
	instrument21
	satellite9
	instrument22
	image0
	image2
	infrared4
	thermograph1
	spectrograph3
	GroundStation0
	Star3
	GroundStation4
	Star2
	GroundStation1
	Phenomenon5
	Planet6
	Planet7
	Planet8
	Phenomenon9
	Planet10
	Planet11
	Star12
	Star13
	Star14
	Star15
	Star16
	Phenomenon17
	Phenomenon18
	Planet19
	Star20
	Planet21
	Planet22
	Phenomenon23
	Star24
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 infrared4)
	(calibration_target instrument0 Star3)
	(instrument instrument1)
	(supports instrument1 spectrograph3)
	(calibration_target instrument1 GroundStation0)
	(instrument instrument2)
	(supports instrument2 image0)
	(supports instrument2 thermograph1)
	(supports instrument2 image2)
	(calibration_target instrument2 GroundStation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star15)
	(satellite satellite1)
	(instrument instrument3)
	(supports instrument3 thermograph1)
	(supports instrument3 image0)
	(calibration_target instrument3 GroundStation4)
	(instrument instrument4)
	(supports instrument4 image2)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 Star3)
	(instrument instrument5)
	(supports instrument5 spectrograph3)
	(supports instrument5 thermograph1)
	(supports instrument5 image2)
	(calibration_target instrument5 GroundStation4)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet10)
	(satellite satellite2)
	(instrument instrument6)
	(supports instrument6 image0)
	(calibration_target instrument6 GroundStation1)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star24)
	(satellite satellite3)
	(instrument instrument7)
	(supports instrument7 infrared4)
	(calibration_target instrument7 Star3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon9)
	(satellite satellite4)
	(instrument instrument8)
	(supports instrument8 spectrograph3)
	(calibration_target instrument8 GroundStation0)
	(instrument instrument9)
	(supports instrument9 image0)
	(supports instrument9 image2)
	(supports instrument9 thermograph1)
	(calibration_target instrument9 Star3)
	(instrument instrument10)
	(supports instrument10 image0)
	(supports instrument10 image2)
	(supports instrument10 spectrograph3)
	(calibration_target instrument10 Star2)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Planet19)
	(satellite satellite5)
	(instrument instrument11)
	(supports instrument11 image0)
	(calibration_target instrument11 Star3)
	(instrument instrument12)
	(supports instrument12 infrared4)
	(supports instrument12 image0)
	(calibration_target instrument12 GroundStation4)
	(instrument instrument13)
	(supports instrument13 spectrograph3)
	(calibration_target instrument13 Star2)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(on_board instrument13 satellite5)
	(power_avail satellite5)
	(pointing satellite5 Planet10)
	(satellite satellite6)
	(instrument instrument14)
	(supports instrument14 spectrograph3)
	(supports instrument14 thermograph1)
	(supports instrument14 image0)
	(calibration_target instrument14 Star3)
	(instrument instrument15)
	(supports instrument15 image0)
	(supports instrument15 thermograph1)
	(supports instrument15 image2)
	(calibration_target instrument15 GroundStation4)
	(instrument instrument16)
	(supports instrument16 spectrograph3)
	(supports instrument16 image2)
	(calibration_target instrument16 GroundStation0)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(on_board instrument16 satellite6)
	(power_avail satellite6)
	(pointing satellite6 Planet11)
	(satellite satellite7)
	(instrument instrument17)
	(supports instrument17 thermograph1)
	(supports instrument17 image2)
	(supports instrument17 image0)
	(calibration_target instrument17 GroundStation4)
	(instrument instrument18)
	(supports instrument18 image2)
	(supports instrument18 thermograph1)
	(calibration_target instrument18 Star3)
	(on_board instrument17 satellite7)
	(on_board instrument18 satellite7)
	(power_avail satellite7)
	(pointing satellite7 Planet11)
	(satellite satellite8)
	(instrument instrument19)
	(supports instrument19 thermograph1)
	(supports instrument19 infrared4)
	(calibration_target instrument19 Star2)
	(instrument instrument20)
	(supports instrument20 thermograph1)
	(calibration_target instrument20 GroundStation4)
	(instrument instrument21)
	(supports instrument21 thermograph1)
	(calibration_target instrument21 Star2)
	(on_board instrument19 satellite8)
	(on_board instrument20 satellite8)
	(on_board instrument21 satellite8)
	(power_avail satellite8)
	(pointing satellite8 GroundStation4)
	(satellite satellite9)
	(instrument instrument22)
	(supports instrument22 spectrograph3)
	(supports instrument22 thermograph1)
	(supports instrument22 infrared4)
	(calibration_target instrument22 GroundStation1)
	(on_board instrument22 satellite9)
	(power_avail satellite9)
	(pointing satellite9 Planet11)
	(mode image0)
	(mode image2)
	(mode infrared4)
	(mode thermograph1)
	(mode spectrograph3)
	(direction GroundStation0)
	(direction Star3)
	(direction GroundStation4)
	(direction Star2)
	(direction GroundStation1)
	(direction Phenomenon5)
	(direction Planet6)
	(direction Planet7)
	(direction Planet8)
	(direction Phenomenon9)
	(direction Planet10)
	(direction Planet11)
	(direction Star12)
	(direction Star13)
	(direction Star14)
	(direction Star15)
	(direction Star16)
	(direction Phenomenon17)
	(direction Phenomenon18)
	(direction Planet19)
	(direction Star20)
	(direction Planet21)
	(direction Planet22)
	(direction Phenomenon23)
	(direction Star24)
)
(:goal (and
	(pointing satellite5 Planet6)
	(pointing satellite7 Star3)
	(pointing satellite8 Star15)
	(pointing satellite9 Star16)
	(have_image Phenomenon5 thermograph1)
	(have_image Planet6 infrared4)
	(have_image Planet7 image0)
	(have_image Planet8 thermograph1)
	(have_image Phenomenon9 image2)
	(have_image Planet10 image0)
	(have_image Planet11 infrared4)
	(have_image Star12 image0)
	(have_image Star13 image0)
	(have_image Star14 thermograph1)
	(have_image Star15 image0)
	(have_image Star16 thermograph1)
	(have_image Phenomenon17 infrared4)
	(have_image Phenomenon18 spectrograph3)
	(have_image Star20 image0)
	(have_image Planet21 thermograph1)
	(have_image Planet22 image2)
	(have_image Phenomenon23 image0)
	(have_image Star24 infrared4)
))

)
