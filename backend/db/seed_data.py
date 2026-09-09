"""
Seed data for BIS Saathi SQLite Database.
Contains 20+ Tier A Indian Standards with rich synonyms, 
Tier B verbatim deep-clause content for 2 flagship standards,
certification steps, mock verification registry, laboratories, and FAQs.
"""

STANDARDS_SEED = [
    {
        "is_code": "IS 9873 (Part 1):2019",
        "title": "Safety of Toys - Part 1: Safety Aspects Related to Mechanical and Physical Properties",
        "division": "Mechanical Engineering / Consumer Products",
        "qco_status": "Mandatory",
        "qco_reference": "Toys (Quality Control) Order, 2020 (S.O. 853(E) dated 25.02.2020)",
        "related_standards": "IS 9873 (Part 2):2017, IS 9873 (Part 3):2017, IS 15644:2006",
        "synonyms": "toys, children toy, plastic toys, stuffed toys, teddy bear, toy cars, dolls, kids play, baby rattle, mechanical toy",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "is_code": "IS 17803:2022",
        "title": "Stainless Steel Vacuum Flasks and Insulated Flask Containers - Specification",
        "division": "Metallurgical Engineering / Consumer Products",
        "qco_status": "Mandatory",
        "qco_reference": "Cookware, Utensils and Cans for Foods and Beverages (Quality Control) Order, 2023",
        "related_standards": "IS 5522:2014, IS 6911:2017, IS 3025",
        "synonyms": "stainless steel bottle, vacuum flask, thermos, insulated water bottle, kids bottle, school bottle, steel sipper, hot and cold bottle",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-flasks-2023"
    },
    {
        "is_code": "IS 16046 (Part 2):2018",
        "title": "Secondary Cells and Batteries Containing Alkaline or Other Non-Acid Electrolytes - Safety Requirements: Part 2 Lithium Systems",
        "division": "Electronics & Information Technology (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Compulsory Registration Scheme (CRO Order Phase-II & III)",
        "related_standards": "IS 13252 (Part 1):2010, IEC 62133-2:2017",
        "synonyms": "lithium ion battery, power bank, mobile battery, laptop battery, rechargeable battery, li-ion cell, ev battery cell, portable battery pack, electronic battery, electronics",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 13252 (Part 1):2010",
        "title": "Information Technology Equipment - Safety - General Requirements",
        "division": "Electronics & Information Technology (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Electronics & IT Goods (Requirements for Compulsory Registration) Order, 2012",
        "related_standards": "IS 16046 (Part 2):2018, IEC 60950-1",
        "synonyms": "electronics, electronic goods, consumer electronics, electronic devices, it goods, laptop, computer, tablet, pos terminal, electronic cash register, it equipment, server, notebook, wifi router",
        "source_url": "https://www.crsbis.in/BIS/about-crs.do"
    },
    {
        "is_code": "IS 4151:2015",
        "title": "Protective Helmets for Motorcycle Riders - Specification (Fourth Revision)",
        "division": "Transport Engineering",
        "qco_status": "Mandatory",
        "qco_reference": "Protective Helmets for Two Wheeler Riders (Quality Control) Order, 2020",
        "related_standards": "IS 9944:1992, IS 1699:1995",
        "synonyms": "helmet, bike helmet, motorcycle helmet, two wheeler helmet, safety helmet, headgear, rider head protection, full face helmet",
        "source_url": "https://morth.nic.in/helmets-qco-notification"
    },
    {
        "is_code": "IS 14543:2016",
        "title": "Packaged Drinking Water (Other than Packaged Natural Mineral Water) - Specification",
        "division": "Food & Agriculture",
        "qco_status": "Mandatory",
        "qco_reference": "Food Safety and Standards (Packaging and Labelling) Regulations & BIS Mandatory List",
        "related_standards": "IS 13428:2005, IS 10500:2012, IS 3025",
        "synonyms": "packaged drinking water, bottled water, mineral water jar, purified water, 20 litre water can, RO water bottle, packaged water",
        "source_url": "https://www.bis.gov.in/product-certification/products-under-mandatory-certification/"
    },
    {
        "is_code": "IS 1417:2016",
        "title": "Gold and Gold Alloys, Jewellery/Artefacts - Fineness and Marking - Specification",
        "division": "Hallmarking / Metallurgical Engineering",
        "qco_status": "Mandatory",
        "qco_reference": "Hallmarking of Gold Jewellery and Artefacts Order, 2020 (enforced mandatory in recognized districts)",
        "related_standards": "IS 15820:2009, IS 2790:1999",
        "synonyms": "gold jewellery, gold hallmark, 22k gold, 18k gold, 916 gold, HUID, jewellery marking, gold coin, gold chain, gold bangles",
        "source_url": "https://www.bis.gov.in/hallmarking/overview/"
    },
    {
        "is_code": "IS 1489 (Part 1):2015",
        "title": "Portland Pozzolana Cement - Specification - Part 1: Fly Ash Based",
        "division": "Civil Engineering",
        "qco_status": "Mandatory",
        "qco_reference": "Cement (Quality Control) Order, 2003",
        "related_standards": "IS 269:2015, IS 8112:2013, IS 12269:2013",
        "synonyms": "cement, ppc cement, construction cement, flyash cement, concrete cement, building cement, cement bag",
        "source_url": "https://www.bis.gov.in/mandatory-certification-cement/"
    },
    {
        "is_code": "IS 1786:2008",
        "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement - Specification",
        "division": "Civil Engineering / Metallurgical",
        "qco_status": "Mandatory",
        "qco_reference": "Steel and Steel Products (Quality Control) Order, 2020",
        "related_standards": "IS 432:1982, IS 2062:2011",
        "synonyms": "tmt steel bar, rebars, tmt saria, reinforcement steel, construction steel rod, fe500d, fe550, iron rod",
        "source_url": "https://steel.gov.in/quality-control-orders"
    },
    {
        "is_code": "IS 16102 (Part 1):2012",
        "title": "Self-Ballasted LED Lamps for General Lighting Services - Part 1: Safety Requirements",
        "division": "Electronics & IT (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Compulsory Registration Order Phase-II",
        "related_standards": "IS 16102 (Part 2):2012, IS 15885 (Part 2/Sec 13)",
        "synonyms": "led bulb, led lamp, lighting bulb, home led, led light, b22 led, e27 led, self-ballasted lamp",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 694:2010",
        "title": "Polyvinyl Chloride Insulated Unsheathed and Sheathed Cables/Cords with Rigid and Flexible Conductors",
        "division": "Electrotechnical",
        "qco_status": "Mandatory",
        "qco_reference": "Electrical Wires and Cables (Quality Control) Order, 2023",
        "related_standards": "IS 1554 (Part 1):1988, IS 7098 (Part 1):1988",
        "synonyms": "electric wire, copper wire, house wiring cable, pvc wire, flexible wire, 1.5 sq mm wire, 2.5 sq mm wire, home cable",
        "source_url": "https://www.bis.gov.in/qco-wires-cables-2023"
    },
    {
        "is_code": "IS 15844:2010",
        "title": "Sports Footwear - Specification",
        "division": "Chemical & Leather",
        "qco_status": "Mandatory",
        "qco_reference": "Footwear made from Leather and other Materials (Quality Control) Order, 2020",
        "related_standards": "IS 15844 (Part 1):2023, IS 15844 (Part 2):2023",
        "synonyms": "shoes, sports shoes, sneakers, running shoes, gym footwear, athletic shoes, tennis shoes",
        "source_url": "https://www.bis.gov.in/qco-footwear-leather-rubber/"
    },
    {
        "is_code": "IS 15644:2006",
        "title": "Safety of Electric Toys - Specification",
        "division": "Electrotechnical / Mechanical",
        "qco_status": "Mandatory",
        "qco_reference": "Toys (Quality Control) Order, 2020",
        "related_standards": "IS 9873 (Part 1):2019, IEC 62115",
        "synonyms": "electric toy, remote control car, rc car, battery operated toy, electronic kids toy, robotic toy, drone toy",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "is_code": "IS 14625:1999",
        "title": "Feeding Bottles - Specification",
        "division": "Consumer Products / Plastic",
        "qco_status": "Mandatory",
        "qco_reference": "Infant Milk Substitutes, Feeding Bottles and Infant Foods Act & BIS Mandatory Scheme",
        "related_standards": "IS 3462, IS 9845",
        "synonyms": "feeding bottle, baby bottle, milk bottle for infants, baby milk container, bpa free baby bottle, infant feeder",
        "source_url": "https://www.bis.gov.in/product-certification/products-under-mandatory-certification/"
    },
    {
        "is_code": "IS 302 (Part 2/Sec 3):2007",
        "title": "Safety of Household and Similar Electrical Appliances: Particular Requirements for Electric Irons",
        "division": "Electrotechnical",
        "qco_status": "Mandatory",
        "qco_reference": "Electrical Appliances (Quality Control) Order, 2023",
        "related_standards": "IS 302 (Part 1):2008, IS 366:1991",
        "synonyms": "electric iron, dry iron, steam iron, clothes iron, press, garment iron, electric press",
        "source_url": "https://www.bis.gov.in/qco-electrical-appliances-2023"
    },
    {
        "is_code": "IS 13428:2005",
        "title": "Packaged Natural Mineral Water - Specification (Second Revision)",
        "division": "Food & Agriculture",
        "qco_status": "Mandatory",
        "qco_reference": "Food Safety and Standards Act & BIS Mandatory Certification",
        "related_standards": "IS 14543:2016, IS 10500:2012",
        "synonyms": "natural mineral water, spring water, himalayan water, bottled spring water, natural water, sparkling mineral water",
        "source_url": "https://www.bis.gov.in/product-certification/products-under-mandatory-certification/"
    },
    {
        "is_code": "IS 10500:2012",
        "title": "Drinking Water - Specification (Second Revision)",
        "division": "Civil Engineering / Public Health",
        "qco_status": "Voluntary",
        "qco_reference": "Benchmark quality standard for municipal and tap water supply (Jal Jeevan Mission guideline)",
        "related_standards": "IS 14543:2016, IS 3025",
        "synonyms": "tap water, municipal drinking water, water purity standard, tds limit, potable water, piped water quality, water testing benchmark",
        "source_url": "https://www.bis.gov.in/standards/civil-engineering/"
    },
    {
        "is_code": "IS 269:2015",
        "title": "Ordinary Portland Cement - Specification (Sixth Revision)",
        "division": "Civil Engineering",
        "qco_status": "Mandatory",
        "qco_reference": "Cement (Quality Control) Order, 2003",
        "related_standards": "IS 1489 (Part 1):2015, IS 8112:2013",
        "synonyms": "opc cement, ordinary portland cement, 43 grade cement, 53 grade cement, heavy construction cement",
        "source_url": "https://www.bis.gov.in/mandatory-certification-cement/"
    },
    {
        "is_code": "IS 2062:2011",
        "title": "Hot Rolled Medium and High Tensile Structural Steel - Specification",
        "division": "Metallurgical Engineering",
        "qco_status": "Mandatory",
        "qco_reference": "Steel and Steel Products (Quality Control) Order, 2020",
        "related_standards": "IS 1786:2008, IS 808:1989",
        "synonyms": "structural steel, steel beams, steel angles, steel plates, industrial steel, i-beam, channel steel, ms angle",
        "source_url": "https://steel.gov.in/quality-control-orders"
    },
    {
        "is_code": "IS 15885 (Part 2/Sec 13):2012",
        "title": "Lamp Controlgear Part 2: Particular Requirements - Section 13: D.C. or A.C. Supplied Electronic Controlgear for LED Modules",
        "division": "Electronics & IT (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Compulsory Registration Scheme Phase-II",
        "related_standards": "IS 16102 (Part 1):2012, IEC 61347-2-13",
        "synonyms": "led driver, led power supply, led ballast, electronic controlgear, constant current led driver",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 6911:2017",
        "title": "Stainless Steel Plate, Sheet and Strip - Specification",
        "division": "Metallurgical Engineering (MTD)",
        "qco_status": "Mandatory",
        "qco_reference": "Stainless Steel and Nickel Alloy (Quality Control) Order, 2020",
        "related_standards": "IS 17803:2022, IS 5522:2014",
        "synonyms": "stainless steel sheet, stainless steel plate, grade 304, grade 316, food grade stainless steel, raw material steel",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-2020"
    },
    {
        "is_code": "IS 5522:2014",
        "title": "Stainless Steel Sheets and Strips for Utensils - Specification",
        "division": "Metallurgical Engineering (MTD)",
        "qco_status": "Mandatory",
        "qco_reference": "Stainless Steel and Nickel Alloy (Quality Control) Order, 2020",
        "related_standards": "IS 17803:2022, IS 6911:2017",
        "synonyms": "stainless steel utensils, utensil sheet, kitchenware steel, steel containers",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-2020"
    },
    {
        "is_code": "IS 2347:2017",
        "title": "Domestic Pressure Cookers - Specification (Fifth Revision)",
        "division": "Mechanical Engineering / Consumer Products",
        "qco_status": "Mandatory",
        "qco_reference": "Domestic Pressure Cooker (Quality Control) Order, 2020 (S.O. 297(E) dated 21.01.2020)",
        "related_standards": "IS 21:1992, IS 6911:2017, IS 13983",
        "synonyms": "pressure cooker, domestic cooker, hawkins cooker, prestige cooker, aluminium cooker, stainless steel cooker, kitchen cooker, steam cooker, food cooker",
        "source_url": "https://www.bis.gov.in/qco-pressure-cookers-2020"
    },
    {
        "is_code": "IS 4246:2002",
        "title": "Domestic Gas Stoves for Use with Liquefied Petroleum Gases - Specification (Fifth Revision)",
        "division": "Mechanical Engineering / Energy",
        "qco_status": "Mandatory",
        "qco_reference": "Domestic Gas Stoves (Quality Control) Order, 2023",
        "related_standards": "IS 5116, IS 10584",
        "synonyms": "gas stove, lpg stove, cooking stove, gas burner, domestic gas stove, chulha, kitchen stove, 2 burner stove, 3 burner stove, gas cooktop",
        "source_url": "https://www.bis.gov.in/qco-gas-stoves-2023"
    },
    {
        "is_code": "IS 15392:2003",
        "title": "Aluminium and Aluminium Alloy Bare Foil for Food Packaging - Specification",
        "division": "Metallurgical Engineering / Consumer Products",
        "qco_status": "Mandatory",
        "qco_reference": "Aluminium and Aluminium Alloy Products (Quality Control) Order, 2023 (S.O. 4333(E))",
        "related_standards": "IS 737:2008, IS 10258",
        "synonyms": "aluminium foil, foil paper, food wrapping foil, kitchen foil, silver foil, food pack foil",
        "source_url": "https://www.bis.gov.in/qco-aluminium-foil"
    },
    {
        "is_code": "IS 10325:2000",
        "title": "Square Tins for Solid and Semi-Solid Foodstuffs - Specification (Second Revision)",
        "division": "Mechanical Engineering / Food Packaging",
        "qco_status": "Mandatory",
        "qco_reference": "Metal Containers (Quality Control) Order, 2020",
        "related_standards": "IS 1993:2006, IS 2508",
        "synonyms": "oil tin, ghee tin, 15 kg tin, edible oil container, vanaspati tin, square tin, ghee can, packaging tin",
        "source_url": "https://www.bis.gov.in/qco-metal-containers"
    },
    {
        "is_code": "IS 12269:2013",
        "title": "Ordinary Portland Cement, 53 Grade - Specification (First Revision)",
        "division": "Civil Engineering",
        "qco_status": "Mandatory",
        "qco_reference": "Cement (Quality Control) Order, 2003",
        "related_standards": "IS 269:2015, IS 1489 (Part 1):2015, IS 4031",
        "synonyms": "53 grade cement, high strength cement, opc 53, ultra strong cement, structural concrete cement, heavy bridge cement, ultratech cement",
        "source_url": "https://www.bis.gov.in/mandatory-certification-cement/"
    },
    {
        "is_code": "IS 303:1989",
        "title": "Plywood for General Purposes - Specification (Third Revision)",
        "division": "Civil Engineering / Wood Products",
        "qco_status": "Mandatory",
        "qco_reference": "Wood and Wooden Products (Quality Control) Order, 2023 (S.O. 3871(E))",
        "related_standards": "IS 710:2010, IS 1734, IS 5509",
        "synonyms": "plywood, commercial plywood, mr grade plywood, bwp plywood, wooden board, furniture ply, marine ply, shuttering ply, wood sheet",
        "source_url": "https://dpiit.gov.in/qco-wood-products-2023"
    },
    {
        "is_code": "IS 4985:2021",
        "title": "Unplasticized Polyvinyl Chloride (PVC-U) Pipes for Potable Water Supplies - Specification",
        "division": "Civil Engineering / Plastic Piping",
        "qco_status": "Mandatory",
        "qco_reference": "Pipes and Fittings (Quality Control) Order, 2023",
        "related_standards": "IS 7634, IS 12235, IS 12818",
        "synonyms": "pvc pipe, upvc pipe, water supply pipe, plumbing pipe, agricultural pipe, borewell pipe, drainage pvc pipe, water line tube, astral pipe, ashirvad pipe",
        "source_url": "https://www.bis.gov.in/qco-pvc-pipes"
    },
    {
        "is_code": "IS 2202 (Part 1):1999",
        "title": "Wooden Flush Door Shutters (Solid Core Type) - Part 1: Plywood Face Panels - Specification",
        "division": "Civil Engineering / Timber",
        "qco_status": "Mandatory",
        "qco_reference": "Door Shutters (Quality Control) Order, 2023",
        "related_standards": "IS 303:1989, IS 1003 (Part 1):2003",
        "synonyms": "flush door, wooden door, solid core door, room door, plywood door shutter, main door shutter, flush shutter",
        "source_url": "https://dpiit.gov.in/qco-door-shutters"
    },
    {
        "is_code": "IS 2553 (Part 2):2019",
        "title": "Safety Glass - Specification - Part 2: For Road Transport (Third Revision)",
        "division": "Transport Engineering / Glass",
        "qco_status": "Mandatory",
        "qco_reference": "Safety Glass (Quality Control) Order, 2020 (MoRTH S.O. 1122(E))",
        "related_standards": "IS 2553 (Part 1):2018, AIS 037",
        "synonyms": "car windshield, safety glass, laminated glass, tempered glass for cars, automotive glass, rear windscreen, bus window glass, vehicle glass",
        "source_url": "https://morth.nic.in/safety-glass-qco"
    },
    {
        "is_code": "IS 15633:2005",
        "title": "Automotive Vehicles - Pneumatic Tyres for Commercial Vehicles - Diagonal and Radial Ply",
        "division": "Transport Engineering / Rubber",
        "qco_status": "Mandatory",
        "qco_reference": "Pneumatic Tyres and Tubes for Automotive Vehicles (Quality Control) Order, 2009",
        "related_standards": "IS 15636:2012, IS 13098:2012",
        "synonyms": "truck tyre, commercial tyre, bus tyre, radial tyre, commercial vehicle tyre, lorry tyre, truck tire",
        "source_url": "https://morth.nic.in/pneumatic-tyres-order"
    },
    {
        "is_code": "IS 15636:2012",
        "title": "Automotive Vehicles - Pneumatic Tyres for Passenger Car Vehicles - Diagonal and Radial Ply",
        "division": "Transport Engineering / Rubber",
        "qco_status": "Mandatory",
        "qco_reference": "Pneumatic Tyres and Tubes for Automotive Vehicles (Quality Control) Order, 2009",
        "related_standards": "IS 15633:2005, ISO 10191",
        "synonyms": "car tyre, passenger tyre, tubeless car tyre, radial car tyre, automobile tyre, suv tyre, mrf tyre, ceat tyre, car tire",
        "source_url": "https://morth.nic.in/pneumatic-tyres-passenger"
    },
    {
        "is_code": "IS 15683:2018",
        "title": "Portable Fire Extinguishers - Performance and Construction - Specification (First Revision)",
        "division": "Civil Engineering / Fire Safety",
        "qco_status": "Mandatory",
        "qco_reference": "Fire Safety Equipment (Quality Control) Order, 2023",
        "related_standards": "IS 2190:2010, IS 13849",
        "synonyms": "fire extinguisher, portable fire cylinder, abc powder extinguisher, co2 extinguisher, foam extinguisher, fire safety cylinder, fire equipment, ceasefire extinguisher",
        "source_url": "https://www.bis.gov.in/qco-fire-extinguishers"
    },
    {
        "is_code": "IS 9473:2002",
        "title": "Respiratory Protective Devices - Filtering Half Masks to Protect Against Particles - Specification",
        "division": "Chemical & Personal Safety",
        "qco_status": "Mandatory",
        "qco_reference": "Personal Protective Equipment (Quality Control) Order, 2022",
        "related_standards": "IS 14166:1994, EN 149",
        "synonyms": "n95 mask, ffp2 mask, respiratory mask, face mask, pollution mask, particulate mask, dust mask, protective safety mask",
        "source_url": "https://www.bis.gov.in/qco-respiratory-ppe"
    },
    {
        "is_code": "IS 15298 (Part 2):2016",
        "title": "Personal Protective Equipment - Part 2: Safety Footwear (Second Revision)",
        "division": "Chemical & Leather",
        "qco_status": "Mandatory",
        "qco_reference": "Footwear made from Leather and other Materials (Quality Control) Order, 2020",
        "related_standards": "IS 15844:2010, ISO 20345:2011",
        "synonyms": "safety shoes, steel toe boots, industrial shoes, factory footwear, safety boots, site shoes, protective work shoes, steel toe shoes",
        "source_url": "https://www.bis.gov.in/qco-footwear-leather-rubber/"
    },
    {
        "is_code": "IS 616:2017",
        "title": "Audio, Video and Similar Electronic Apparatus - Safety Requirements",
        "division": "Electronics & IT (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Electronics & IT Goods (Compulsory Registration) Order Phase-I & III",
        "related_standards": "IS 13252 (Part 1):2010, IEC 60065",
        "synonyms": "smart tv, television, led tv, audio system, soundbar, home theatre, amplifier, music system, crs tv, 4k tv",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 16333 (Part 3):2022",
        "title": "Mobile Phone Handsets - Part 3: Indian Language Support for Mobile Phone Handsets",
        "division": "Electronics & IT (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Indian Language Support for Mobile Phone Handsets Order, 2016",
        "related_standards": "IS 13252 (Part 1):2010, IS 16046",
        "synonyms": "mobile phone, smartphone, android phone, iphone, cell phone, handset, 5g phone, feature phone, telephone",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 16242 (Part 1):2014",
        "title": "Uninterruptible Power Systems (UPS) - Part 1: General and Safety Requirements for UPS",
        "division": "Electronics & IT (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Compulsory Registration Scheme Phase-II",
        "related_standards": "IS 13252 (Part 1):2010, IEC 62040-1",
        "synonyms": "ups, inverter ups, backup power, computer ups, online ups, battery inverter, home ups, power backup",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 252:2013",
        "title": "Caustic Soda, Pure and Technical - Specification (Fifth Revision)",
        "division": "Chemical",
        "qco_status": "Mandatory",
        "qco_reference": "Caustic Soda (Quality Control) Order, 2018 (S.O. 1475(E))",
        "related_standards": "IS 10112, IS 283",
        "synonyms": "caustic soda, sodium hydroxide, naoh, lye, industrial chemical, chemical flakes, caustic lye",
        "source_url": "https://chemicals.gov.in/qco-caustic-soda"
    },
    {
        "is_code": "IS 10146:1982",
        "title": "Polyethylene for Its Safe Use in Contact with Foodstuffs, Pharmaceuticals and Drinking Water",
        "division": "Chemical & Plastics",
        "qco_status": "Mandatory",
        "qco_reference": "Plastics for Food Contact Applications (Quality Control) Order, 2021",
        "related_standards": "IS 9845, IS 10141",
        "synonyms": "food grade plastic, polyethylene food contact, water container plastic, ldpe food bag, hdpe food grade container, pharma plastic",
        "source_url": "https://chemicals.gov.in/qco-plastics-food-contact"
    },
    {
        "is_code": "IS 14286:2010",
        "title": "Crystalline Silicon Terrestrial Photovoltaic (PV) Modules - Design Qualification and Type Approval",
        "division": "Electronics & IT (CRS / Solar Energy)",
        "qco_status": "Mandatory",
        "qco_reference": "Solar Photovoltaics, Systems, Devices and Components Goods (Requirements for Compulsory Registration) Order, 2017 (MNRE Order)",
        "related_standards": "IS/IEC 61730 (Part 1):2004, IS/IEC 61730 (Part 2):2004, IS 16221 (Part 2):2015",
        "synonyms": "solar panel, solar panels, solar pv module, photovoltaic module, solar cell, solar power panel, rooftop solar, solar module, crystalline solar panel, solar pv, solar power system, solar electricity panel",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS/IEC 61730 (Part 1):2004",
        "title": "Photovoltaic (PV) Module Safety Qualification - Part 1: Requirements for Construction",
        "division": "Electronics & IT (CRS / Solar Energy)",
        "qco_status": "Mandatory",
        "qco_reference": "Solar Photovoltaics, Systems, Devices and Components Goods (Requirements for Compulsory Registration) Order, 2017",
        "related_standards": "IS 14286:2010, IS/IEC 61730 (Part 2):2004",
        "synonyms": "solar module safety, pv module construction, solar panel construction, pv safety qualification, solar panel safety",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 16221 (Part 2):2015",
        "title": "Safety of Power Converters for Use in Photovoltaic Power Systems - Part 2: Particular Requirements for Inverters",
        "division": "Electronics & IT (CRS / Solar Energy)",
        "qco_status": "Mandatory",
        "qco_reference": "Solar Photovoltaics, Systems, Devices and Components Goods (Requirements for Compulsory Registration) Order, 2017",
        "related_standards": "IS 14286:2010, IEC 62109-2",
        "synonyms": "solar inverter, pv inverter, grid tie inverter, solar power converter, rooftop solar inverter, solar power conditioner",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    }
]

# Tier B Flagship Deep-Clause Curated Chunks (Paraphrased technical summaries of official standards)
CHUNKS_SEED = [
    # Flagship 1: IS 9873 (Part 1):2019 / IS 17803:2022 (Child & Consumer Safety)
    {
        "chunk_id": "IS9873-P1-C4.1",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "4.1",
        "sub_clause": "4.1.1",
        "page": 7,
        "content": "Mechanical & Physical Safety Summary: Mandates that toys withstand anticipated normal use and reasonably foreseeable abuse by children without presenting mechanical risks. Cross-references Clause 5 physical abuse simulation testing protocols.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Safety of Toys (Technical Summary)",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS9873-P1-C4.2",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "4.2",
        "sub_clause": "4.2.1",
        "page": 8,
        "content": "Choking Hazard & Small Parts Summary: Restricts toys and detachable components intended for children under 36 months from fitting completely inside the standardized small parts test cylinder, including fragments liberated post drop and torque testing.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Safety of Toys (Technical Summary)",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS9873-P1-C4.7",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "4.7",
        "sub_clause": "4.7.1",
        "page": 11,
        "content": "Accessible Edges & Points Summary: Prohibits sharp metal or glass edges on toys intended for children under 96 months. Requires rolling, curling, or permanent protective guards that endure drop and impact testing.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Safety of Toys (Technical Summary)",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS9873-P1-C7",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "7.1",
        "sub_clause": "7.1.2",
        "page": 18,
        "content": "Marking & Licence Display Summary: Mandates clear and indelible display of the standard ISI Mark accompanied by the unique 7-digit CM/L licence number, manufacturer identity, and mandatory age-grading safety warnings.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Marking Requirements (Technical Summary)",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS17803-C4.1",
        "standard_id": "IS 17803:2022",
        "clause": "4.1",
        "sub_clause": "4.1.1",
        "page": 3,
        "content": "Material Food-Contact Safety Summary: Specifies that the inner container and potable water contact surfaces must use food-grade austenitic stainless steel (Grade 304 / Grade 316 per IS 6911) ensuring non-toxicity and chemical corrosion resistance.",
        "source": "Bureau of Indian Standards: IS 17803:2022 Stainless Steel Flasks (Technical Summary)",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-flasks-2023"
    },
    {
        "chunk_id": "IS17803-C5.2",
        "standard_id": "IS 17803:2022",
        "clause": "5.2",
        "sub_clause": "5.2.3",
        "page": 5,
        "content": "Thermal Retention Performance Summary: Requires insulated flasks (capacity >= 500 ml) filled with 95°C boiling water to maintain water temperature at or above 60°C after 6 hours in a 20°C ± 2°C ambient testing environment.",
        "source": "Bureau of Indian Standards: IS 17803:2022 Thermal Testing (Technical Summary)",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-flasks-2023"
    },
    {
        "chunk_id": "IS17803-C6.1",
        "standard_id": "IS 17803:2022",
        "clause": "6.1",
        "sub_clause": "6.1.1",
        "page": 6,
        "content": "Impact & Drop Resistance Summary: Mandates that flasks filled to rated capacity survive two consecutive drops from a height of 1.0 meter onto flat concrete without structural rupture, leakage, or loss of internal vacuum.",
        "source": "Bureau of Indian Standards: IS 17803:2022 Mechanical Integrity (Technical Summary)",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-flasks-2023"
    },
    # Flagship 2: IS 16046 (Part 2):2018 / IS 13252 (Part 1):2010 (Electronics & CRS)
    {
        "chunk_id": "IS16046-P2-C5.3",
        "standard_id": "IS 16046 (Part 2):2018",
        "clause": "5.3",
        "sub_clause": "5.3.1",
        "page": 9,
        "content": "Continuous Charging Safety Summary: Requires fully discharged cells to endure 7 days of continuous charging at manufacturer rated voltage/current without fire, explosion, or chemical venting.",
        "source": "Bureau of Indian Standards: IS 16046 (Part 2):2018 Secondary Cells Safety (Technical Summary)",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "chunk_id": "IS16046-P2-C7.2",
        "standard_id": "IS 16046 (Part 2):2018",
        "clause": "7.2",
        "sub_clause": "7.2.2",
        "page": 14,
        "content": "External Short Circuit Safety Summary: Requires fully charged cells and battery packs short-circuited with 80 mΩ external resistance at 55°C to stabilize safely without catching fire or exploding.",
        "source": "Bureau of Indian Standards: IS 16046 (Part 2):2018 Short Circuit Requirements (Technical Summary)",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "chunk_id": "IS16046-P2-C9.1",
        "standard_id": "IS 16046 (Part 2):2018",
        "clause": "9.1",
        "sub_clause": "9.1.1",
        "page": 19,
        "content": "Compulsory Registration Scheme (CRS) Marking Summary: Mandates the BIS CRS mark formatted as 'Self-Declaration - Conforming to IS 16046 (Part 2):2018, R-XXXXXXXX' with the registered 8-digit R-number.",
        "source": "Bureau of Indian Standards: CRS Marking Guidelines (Technical Summary)",
        "source_url": "https://www.crsbis.in/BIS/about-crs.do"
    },
    {
        "chunk_id": "IS13252-P1-C1.5",
        "standard_id": "IS 13252 (Part 1):2010",
        "clause": "1.5",
        "sub_clause": "1.5.1",
        "page": 12,
        "content": "Electrical Insulation & Clearance Summary: Mandates prescribed physical clearance and creepage distances around hazardous voltage circuitry to protect operators from electric shock and thermal hazards under normal and fault conditions.",
        "source": "Bureau of Indian Standards: IS 13252 (Part 1):2010 IT Safety (Technical Summary)",
        "source_url": "https://www.crsbis.in/BIS/about-crs.do"
    },
    # Flagship 3: IS 2347:2017 (Domestic Pressure Cookers)
    {
        "chunk_id": "IS2347-C4.1",
        "standard_id": "IS 2347:2017",
        "clause": "4.1",
        "sub_clause": "4.1.1",
        "page": 4,
        "content": "Material Quality & Food Contact Safety: Wrought aluminium alloy used for cooker body and lid shall conform to IS 21 (Grade 4000 or 5000), or stainless steel shall conform to Grade 304/316 of IS 6911. Gaskets shall be food-grade synthetic or natural rubber conforming to IS 7466 without toxic lead or phthalate leaching.",
        "source": "Bureau of Indian Standards: IS 2347:2017 Material Requirements",
        "source_url": "https://www.bis.gov.in/qco-pressure-cookers-2020"
    },
    {
        "chunk_id": "IS2347-C5.3",
        "standard_id": "IS 2347:2017",
        "clause": "5.3",
        "sub_clause": "5.3.2",
        "page": 6,
        "content": "Operating Pressure & Vent Weight Performance: The primary pressure regulating device (weight valve) shall operate smoothly to maintain internal steam operating pressure at nominal 100 kPa ± 10 kPa during normal cooking cycle.",
        "source": "Bureau of Indian Standards: IS 2347:2017 Pressure Regulation",
        "source_url": "https://www.bis.gov.in/qco-pressure-cookers-2020"
    },
    {
        "chunk_id": "IS2347-C6.1",
        "standard_id": "IS 2347:2017",
        "clause": "6.1",
        "sub_clause": "6.1.1",
        "page": 7,
        "content": "Hydraulic Proof Pressure Safety Test: Every assembled pressure cooker body and lid shall withstand an internal hydrostatic proof pressure of 200 kPa without permanent plastic deformation, rupture, joint opening, or hydraulic fluid leakage.",
        "source": "Bureau of Indian Standards: IS 2347:2017 Proof Pressure Test",
        "source_url": "https://www.bis.gov.in/qco-pressure-cookers-2020"
    },
    {
        "chunk_id": "IS2347-C7.2",
        "standard_id": "IS 2347:2017",
        "clause": "7.2",
        "sub_clause": "7.2.1",
        "page": 9,
        "content": "Secondary Safety Relief Device (Fusible Plug / Spring Valve): If the primary vent pipe is artificially blocked, the secondary safety relief device must blow off and safely vent internal pressure between 130 kPa and 200 kPa before explosive pressure levels are reached.",
        "source": "Bureau of Indian Standards: IS 2347:2017 Secondary Safety Mechanism",
        "source_url": "https://www.bis.gov.in/qco-pressure-cookers-2020"
    },
    {
        "chunk_id": "IS2347-C9.1",
        "standard_id": "IS 2347:2017",
        "clause": "9.1",
        "sub_clause": "9.1.2",
        "page": 12,
        "content": "Mandatory Certification Marking: Cooker body and outer packaging must be visibly and indelibly stamped with the standard ISI Mark, 7-digit CM/L licence number, manufacturer identity, nominal capacity in litres, and maximum operating pressure.",
        "source": "Bureau of Indian Standards: IS 2347:2017 Marking Guidelines",
        "source_url": "https://www.bis.gov.in/qco-pressure-cookers-2020"
    },
    # Flagship 4: IS 1786:2008 (High Strength TMT Reinforcement Steel Bars)
    {
        "chunk_id": "IS1786-C4.2",
        "standard_id": "IS 1786:2008",
        "clause": "4.2",
        "sub_clause": "4.2.1",
        "page": 3,
        "content": "Chemical Composition Limits (Fe 500D Grade): Maximum permissible limits by ladle analysis shall be Carbon: 0.25%, Sulphur: 0.040%, Phosphorus: 0.040%, and combined Sulphur + Phosphorus: 0.075%, ensuring high earthquake ductility and weldability.",
        "source": "Bureau of Indian Standards: IS 1786:2008 Chemical Limits",
        "source_url": "https://steel.gov.in/quality-control-orders"
    },
    {
        "chunk_id": "IS1786-C8.1",
        "standard_id": "IS 1786:2008",
        "clause": "8.1",
        "sub_clause": "8.1.1",
        "page": 6,
        "content": "Tensile and Elongation Requirements (Fe 500D): Minimum 0.2 percent proof stress / yield strength shall be 500.0 N/mm², tensile strength minimum 565 N/mm² (TS/YS ratio >= 1.10), and total elongation at maximum force not less than 5.0%.",
        "source": "Bureau of Indian Standards: IS 1786:2008 Mechanical Properties",
        "source_url": "https://steel.gov.in/quality-control-orders"
    },
    {
        "chunk_id": "IS1786-C11.2",
        "standard_id": "IS 1786:2008",
        "clause": "11.2",
        "sub_clause": "11.2.2",
        "page": 10,
        "content": "Rolling Identification Marks: Every deformed bar and wire shall carry distinct rolled-on identification marks at repeated intervals not exceeding 1.5 meters along its length, displaying the manufacturer's brand logo, grade Fe 500D, and nominal diameter.",
        "source": "Bureau of Indian Standards: IS 1786:2008 Rolling Marks",
        "source_url": "https://steel.gov.in/quality-control-orders"
    },
    # Flagship 5: IS 1489 (Part 1):2015 (Portland Pozzolana Cement - Fly Ash Based)
    {
        "chunk_id": "IS1489-C5.1",
        "standard_id": "IS 1489 (Part 1):2015",
        "clause": "5.1",
        "sub_clause": "5.1.1",
        "page": 3,
        "content": "Pozzolanic Constituent Proportion: The fly ash constituent conforming to IS 3812 (Part 1) shall be homogeneously interground or blended with clinker such that fly ash is not less than 15 percent and not more than 35 percent by mass of the final Portland Pozzolana Cement.",
        "source": "Bureau of Indian Standards: IS 1489 (Part 1):2015 Raw Materials",
        "source_url": "https://www.bis.gov.in/mandatory-certification-cement/"
    },
    {
        "chunk_id": "IS1489-C6.1",
        "standard_id": "IS 1489 (Part 1):2015",
        "clause": "6.1",
        "sub_clause": "6.1.1",
        "page": 5,
        "content": "Compressive Strength Requirements: Standard cement-sand mortar cubes shall exhibit compressive strength not less than 16 MPa at 72 ± 1 hours (3 days), not less than 22 MPa at 168 ± 2 hours (7 days), and not less than 33 MPa at 672 ± 4 hours (28 days).",
        "source": "Bureau of Indian Standards: IS 1489 (Part 1):2015 Physical Requirements",
        "source_url": "https://www.bis.gov.in/mandatory-certification-cement/"
    },
    # Flagship 6: IS 15683:2018 (Portable Fire Extinguishers)
    {
        "chunk_id": "IS15683-C6.1",
        "standard_id": "IS 15683:2018",
        "clause": "6.1",
        "sub_clause": "6.1.2",
        "page": 7,
        "content": "Discharge Duration & Throw Efficiency: When fully charged at 27°C ± 5°C, portable dry powder fire extinguishers of 4 kg capacity or higher shall maintain continuous effective discharge for not less than 13 seconds, discharging at least 85% of total extinguishing chemical charge.",
        "source": "Bureau of Indian Standards: IS 15683:2018 Discharge Performance",
        "source_url": "https://www.bis.gov.in/qco-fire-extinguishers"
    },
    {
        "chunk_id": "IS15683-C7.2",
        "standard_id": "IS 15683:2018",
        "clause": "7.2",
        "sub_clause": "7.2.1",
        "page": 11,
        "content": "Hydrostatic Burst Pressure Safety: Every extinguisher cylinder body shall be hydraulically tested to 2.5 times maximum service pressure (minimum 3.0 MPa) for 60 seconds without rupture, permanent deformation, or pinhole leakage.",
        "source": "Bureau of Indian Standards: IS 15683:2018 Pressure Safety",
        "source_url": "https://www.bis.gov.in/qco-fire-extinguishers"
    },
    # Flagship 7: IS 4151:2015 (Protective Helmets for Two-Wheeler Motorcycle Riders)
    {
        "chunk_id": "IS4151-C4.1",
        "standard_id": "IS 4151:2015",
        "clause": "4.1",
        "sub_clause": "4.1.2",
        "page": 5,
        "content": "Protective Outer Shell & Impact Buffer Liner: Outer shell must be moulded from virgin high-impact engineering thermoplastic (ABS or Polycarbonate) or glass/carbon fiber composite. Inner protective liner must use expanded polystyrene (EPS) with minimum density of 24 kg/m³ to absorb kinetic crash energy.",
        "source": "Bureau of Indian Standards: IS 4151:2015 Shell and Liner Construction",
        "source_url": "https://morth.nic.in/helmets-qco-notification"
    },
    {
        "chunk_id": "IS4151-C5.2",
        "standard_id": "IS 4151:2015",
        "clause": "5.2",
        "sub_clause": "5.2.1",
        "page": 8,
        "content": "Impact Absorption Dynamic Test: When subjected to guided drop impact at 7.5 m/s velocity onto flat and hemispherical steel anvils under ambient, heat, cold (-10°C), and water-submersion conditioning, peak headform acceleration shall not exceed 300g and cumulative duration exceeding 150g shall be under 5 ms.",
        "source": "Bureau of Indian Standards: IS 4151:2015 Impact Test Protocols",
        "source_url": "https://morth.nic.in/helmets-qco-notification"
    },
    {
        "chunk_id": "IS4151-C7.1",
        "standard_id": "IS 4151:2015",
        "clause": "7.1",
        "sub_clause": "7.1.3",
        "page": 12,
        "content": "Retention System (Chin Strap) Dynamic Test: Under dynamic shock load of 1500 N, the retention system elongation shall not exceed 35 mm and residual displacement shall not exceed 25 mm, guaranteeing that the helmet will not dislodge from rider head during collision.",
        "source": "Bureau of Indian Standards: IS 4151:2015 Retention Test",
        "source_url": "https://morth.nic.in/helmets-qco-notification"
    },
    # Flagship 8: IS 14286:2010 (Crystalline Silicon Terrestrial Photovoltaic PV Modules)
    {
        "chunk_id": "IS14286-C10.11",
        "standard_id": "IS 14286:2010",
        "clause": "10.11",
        "sub_clause": "10.11.1",
        "page": 14,
        "content": "Thermal Cycling Endurance Test: PV modules must undergo 200 continuous thermal cycles between -40°C and +85°C with current injection at maximum power point to verify resistance to thermal fatigue, cell cracking, and solder interconnect delamination.",
        "source": "Bureau of Indian Standards: IS 14286:2010 Thermal Cycling Protocol",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "chunk_id": "IS14286-C10.13",
        "standard_id": "IS 14286:2010",
        "clause": "10.13",
        "sub_clause": "10.13.2",
        "page": 16,
        "content": "Damp Heat Environmental Test: Modules shall be subjected to 85°C ± 2°C and 85% ± 5% relative humidity for 1000 hours without moisture penetration, EVA encapsulant browning, backsheet peeling, or insulation resistance drop below 40 MΩ·m².",
        "source": "Bureau of Indian Standards: IS 14286:2010 Damp Heat Protocol",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "chunk_id": "IS14286-C12.1",
        "standard_id": "IS 14286:2010",
        "clause": "12.1",
        "sub_clause": "12.1.2",
        "page": 22,
        "content": "CRS Registration Marking & Solar Identification: Modules must bear indelible nameplate displaying manufacturer identity, model designation, unique serial number, nominal rated power output (Pmax), open circuit voltage (Voc), short circuit current (Isc), and the official BIS Compulsory Registration Scheme mark with 8-digit R-number.",
        "source": "Bureau of Indian Standards: IS 14286:2010 Marking Guidelines",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    }
]

# Structured Certification Steps for Scheme-I, CRS, and FMCS
CERTIFICATION_STEPS_SEED = [
    # Scheme-I (Domestic - ISI Mark)
    {
        "step_id": "SCH1-S1",
        "scheme": "Scheme-I",
        "step_number": 1,
        "title": "Identify Applicable Standard & Confirm QCO",
        "description": "Determine the exact Indian Standard (e.g. IS 9873 for toys, IS 17803 for flasks). Verify whether the product falls under a mandatory Quality Control Order (QCO) issued by the relevant Ministry.",
        "applies_to": "domestic",
        "indicative_timeline": "1–3 days",
        "source": "BIS Manak Online Portal / Conformity Assessment Regulations, 2018"
    },
    {
        "step_id": "SCH1-S2",
        "scheme": "Scheme-I",
        "step_number": 2,
        "title": "Sample Testing at NABL / BIS Recognized Laboratory",
        "description": "Manufacture prototypes or pilot production samples and submit them to a BIS-recognized or NABL-accredited laboratory for complete testing against the prescribed standard parameters.",
        "applies_to": "domestic",
        "indicative_timeline": "15–30 days (depends on product test cycles)",
        "source": "BIS Laboratory Recognition Scheme (LRS)"
    },
    {
        "step_id": "SCH1-S3",
        "scheme": "Scheme-I",
        "step_number": 3,
        "title": "Online Application Submission via Manak Online (Form V)",
        "description": "File Form V on www.manakonline.in. Upload in-house manufacturing machinery list, testing equipment calibration certificates, factory layout, manufacturing process flowchart, and initial test reports.",
        "applies_to": "domestic",
        "indicative_timeline": "3–5 days",
        "source": "BIS Manak Online Operating Manual"
    },
    {
        "step_id": "SCH1-S4",
        "scheme": "Scheme-I",
        "step_number": 4,
        "title": "Application & Marking Fee Payment (MSME Concessions Apply)",
        "description": "Pay the statutory application fee and annual minimum marking fees. Micro enterprises receive a 50% concession, and small enterprises / women entrepreneurs receive a 20% concession on application and annual licence fees.",
        "applies_to": "domestic",
        "indicative_timeline": "Instant online payment",
        "source": "BIS Gazette Notification on Concessions for MSMEs & Startups"
    },
    {
        "step_id": "SCH1-S5",
        "scheme": "Scheme-I",
        "step_number": 5,
        "title": "On-Site Factory Inspection & Verification Audit",
        "description": "A designated BIS technical inspecting officer visits the manufacturing premises to verify in-house quality control testing capability, calibration of equipment, and draws counter-samples for independent testing.",
        "applies_to": "domestic",
        "indicative_timeline": "10–20 days from application acceptance",
        "source": "BIS Conformity Assessment Manual, Scheme-I"
    },
    {
        "step_id": "SCH1-S6",
        "scheme": "Scheme-I",
        "step_number": 6,
        "title": "Grant of Licence (CM/L Number) & ISI Mark Authorization",
        "description": "Upon successful verification audit and passing lab test reports, BIS grants a 7-digit Certification Marks Licence (CM/L-XXXXXXX). The manufacturer is legally authorized to apply the standard ISI mark on products.",
        "applies_to": "domestic",
        "indicative_timeline": "35–65 days total indicative process",
        "source": "BIS Act 2016, Section 13"
    },

    # Compulsory Registration Scheme (CRS) - Electronics & IT
    {
        "step_id": "CRS-S1",
        "scheme": "CRS",
        "step_number": 1,
        "title": "Confirm Product Coverage in MeitY / BIS CRO Schedule",
        "description": "Verify product category under the Electronics and Information Technology Goods (Compulsory Registration) Order (e.g. power banks under IS 16046 Part 2, LED lamps under IS 16102 Part 1).",
        "applies_to": "all",
        "indicative_timeline": "1–2 days",
        "source": "crsbis.in MeitY Product Schedule"
    },
    {
        "step_id": "CRS-S2",
        "scheme": "CRS",
        "step_number": 2,
        "title": "Appoint Authorized Indian Representative (AIR) (For Foreign Mfrs)",
        "description": "Foreign manufacturers must legally nominate an Authorized Indian Representative (AIR) residing in India who acts as liaison and accepts legal compliance responsibility.",
        "applies_to": "foreign",
        "indicative_timeline": "3–7 days",
        "source": "BIS CRS Guidelines for Foreign Entities"
    },
    {
        "step_id": "CRS-S3",
        "scheme": "CRS",
        "step_number": 3,
        "title": "Mandatory Testing at BIS-Recognized Indian Laboratory",
        "description": "Sample testing must be conducted exclusively at a BIS-recognized laboratory located in India. Test reports are valid for 90 days for filing registration.",
        "applies_to": "all",
        "indicative_timeline": "15–25 days",
        "source": "CRS Lab Testing Protocol"
    },
    {
        "step_id": "CRS-S4",
        "scheme": "CRS",
        "step_number": 4,
        "title": "Portal Submission of Self-Declaration of Conformity (SDoC)",
        "description": "File application online on crsbis.in with test reports, undertaking, brand authorization, and statutory fees. No physical factory audit is required under CRS (Purely Paperless SDoC).",
        "applies_to": "all",
        "indicative_timeline": "3–5 days",
        "source": "crsbis.in Self-Declaration Guidelines"
    },
    {
        "step_id": "CRS-S5",
        "scheme": "CRS",
        "step_number": 5,
        "title": "Issuance of Unique Registration Number (R-Number)",
        "description": "BIS issues an 8-digit Registration Number (e.g. R-41001234). Products can be imported/sold bearing the CRS logo and 'Self-Declaration - Conforming to IS XXXXX, R-XXXXXXXX'.",
        "applies_to": "all",
        "indicative_timeline": "15–20 days from report upload",
        "source": "BIS Act 2016 Section 15"
    },

    # Foreign Manufacturers Certification Scheme (FMCS)
    {
        "step_id": "FMCS-S1",
        "scheme": "FMCS",
        "step_number": 1,
        "title": "Application via FMCD Portal & Appointment of AIR",
        "description": "Foreign applicant files online through the Foreign Manufacturers Certification Department (FMCD) portal and formally registers an Authorized Indian Representative (AIR).",
        "applies_to": "foreign",
        "indicative_timeline": "5–10 days",
        "source": "FMCD Operational Manual"
    },
    {
        "step_id": "FMCS-S2",
        "scheme": "FMCS",
        "step_number": 2,
        "title": "Overseas Factory Physical Audit by BIS Delegation",
        "description": "A team of BIS auditors travels to the foreign manufacturing facility to verify manufacturing infrastructure, quality control systems, and draw random samples.",
        "applies_to": "foreign",
        "indicative_timeline": "30–60 days (depends on visa/travel coordination)",
        "source": "BIS FMCS Guidelines"
    },
    {
        "step_id": "FMCS-S3",
        "scheme": "FMCS",
        "step_number": 3,
        "title": "Testing of Drawn Samples in India & Performance Guarantee Bond",
        "description": "Samples drawn during overseas audit are tested in BIS laboratories in India. The applicant submits a Performance Bank Guarantee (PBG) and pays annual marking fees.",
        "applies_to": "foreign",
        "indicative_timeline": "20–30 days",
        "source": "FMCS Regulations"
    },
    {
        "step_id": "FMCS-S4",
        "scheme": "FMCS",
        "step_number": 4,
        "title": "Grant of FMCS CM/L Licence",
        "description": "Upon satisfactory audit and test results, FMCS licence is granted allowing use of standard ISI mark for goods exported to the Indian market.",
        "applies_to": "foreign",
        "indicative_timeline": "90–120 days total indicative timeline",
        "source": "BIS Foreign Certification Regulations"
    }
]

# Verification Registry (Mock BIS CM/L, HUID, CRS Data)
VERIFICATION_REGISTRY_SEED = [
    # CM/L (Scheme-I Domestic & FMCS)
    {
        "number_type": "CML",
        "number_val": "CML1234567",
        "licensee_name": "Hamilton Housewares Pvt. Ltd. (Milton)",
        "brand": "Milton",
        "product_category": "Stainless Steel Vacuum Flasks and Bottles",
        "is_code": "IS 17803:2022",
        "status": "Active",
        "validity_date": "2027-03-31",
        "details": "Factory: Plot 42, GIDC Industrial Estate, Silvassa, D&NH. Scope: Vacuum insulated flasks up to 2000 ml."
    },
    {
        "number_type": "CML",
        "number_val": "CML7654321",
        "licensee_name": "Steelbird Hi-Tech India Ltd.",
        "brand": "Steelbird",
        "product_category": "Protective Helmets for Motorcycle Riders",
        "is_code": "IS 4151:2015",
        "status": "Active",
        "validity_date": "2026-12-15",
        "details": "Factory: Baddi Industrial Area, Solan, Himachal Pradesh. Scope: Full-face and open-face helmets with visors."
    },
    {
        "number_type": "CML",
        "number_val": "CML9988776",
        "licensee_name": "AquaPure Beverages Ltd.",
        "brand": "AquaPure",
        "product_category": "Packaged Drinking Water",
        "is_code": "IS 14543:2016",
        "status": "Suspended",
        "validity_date": "2025-06-30",
        "details": "Licence suspended due to microbiological non-conformity during market surveillance sampling."
    },
    {
        "number_type": "CML",
        "number_val": "CML5544332",
        "licensee_name": "Funskool India Limited",
        "brand": "Funskool",
        "product_category": "Safety of Toys (Mechanical and Physical)",
        "is_code": "IS 9873 (Part 1):2019",
        "status": "Active",
        "validity_date": "2028-01-15",
        "details": "Factory: Ranipet, Vellore District, Tamil Nadu. Scope: Non-battery toys and building blocks for 0-14 years."
    },

    # HUID (Hallmark Unique Identification Number - 6 Alphanumeric Characters stored as TEXT)
    {
        "number_type": "HUID",
        "number_val": "AB1234",
        "licensee_name": "Titan Company Limited (Tanishq)",
        "brand": "Tanishq",
        "product_category": "Gold Jewellery - 22 Karat (916 Fineness)",
        "is_code": "IS 1417:2016",
        "status": "Operative",
        "validity_date": "Verified Lifetime Hallmark",
        "details": "Assaying & Hallmarking Centre: National Gold Assaying Center (AHC-0102). Article: Gold Necklace 22K (91.6% Pure Gold)."
    },
    {
        "number_type": "HUID",
        "number_val": "XY9876",
        "licensee_name": "Kalyan Jewellers India Limited",
        "brand": "Kalyan Jewellers",
        "product_category": "Gold Jewellery - 18 Karat (750 Fineness)",
        "is_code": "IS 1417:2016",
        "status": "Operative",
        "validity_date": "Verified Lifetime Hallmark",
        "details": "Assaying & Hallmarking Centre: Southern Assay Lab, Thrissur (AHC-0455). Article: Diamond-studded 18K Gold Ring."
    },
    {
        "number_type": "HUID",
        "number_val": "K7M2P9",
        "licensee_name": "Malabar Gold & Diamonds",
        "brand": "Malabar Gold",
        "product_category": "Gold Jewellery - 22 Karat (916 Fineness)",
        "is_code": "IS 1417:2016",
        "status": "Operative",
        "validity_date": "Verified Lifetime Hallmark",
        "details": "Assaying & Hallmarking Centre: Calicut Assay Lab (AHC-0789). Article: Traditional Gold Bangle pair."
    },

    # CRS (Compulsory Registration Scheme - R-Numbers)
    {
        "number_type": "CRS",
        "number_val": "R-41001234",
        "licensee_name": "Samsung Electronics Co. Ltd.",
        "brand": "Samsung",
        "product_category": "Secondary Lithium-Ion Battery Packs",
        "is_code": "IS 16046 (Part 2):2018",
        "status": "Active",
        "validity_date": "2027-08-20",
        "details": "Factory: Samsung SDI, Cheonan Plant, South Korea. AIR: Samsung India Electronics Pvt. Ltd., Gurugram, India."
    },
    {
        "number_type": "CRS",
        "number_val": "R-41005678",
        "licensee_name": "Xiaomi Communications Co., Ltd.",
        "brand": "Mi / Xiaomi",
        "product_category": "Portable Power Bank",
        "is_code": "IS 16046 (Part 2):2018",
        "status": "Active",
        "validity_date": "2026-11-10",
        "details": "Factory: DBG Technology India Pvt. Ltd., Bawal, Haryana. Model: Mi 20000mAh 3i Power Bank."
    },
    {
        "number_type": "CML",
        "number_val": "CML1122334",
        "licensee_name": "Hawkins Cookers Limited",
        "brand": "Hawkins",
        "product_category": "Domestic Pressure Cookers (Aluminium & Hard Anodized)",
        "is_code": "IS 2347:2017",
        "status": "Active",
        "validity_date": "2028-04-30",
        "details": "Factory: Hoshiarpur Plant, Punjab. Scope: Inner lid pressure cookers from 1.5L to 12L capacity."
    },
    {
        "number_type": "CML",
        "number_val": "CML2233445",
        "licensee_name": "TTK Prestige Limited",
        "brand": "Prestige",
        "product_category": "Domestic Pressure Cookers (Stainless Steel & Clip-on)",
        "is_code": "IS 2347:2017",
        "status": "Active",
        "validity_date": "2027-10-31",
        "details": "Factory: Hosur Unit, Krishnagiri District, Tamil Nadu. Scope: Outer lid and clip-on stainless steel cookers."
    },
    {
        "number_type": "CML",
        "number_val": "CML3344556",
        "licensee_name": "Tata Steel Limited",
        "brand": "Tata Tiscon",
        "product_category": "High Strength Deformed Steel Bars (Fe 500D / Fe 550D)",
        "is_code": "IS 1786:2008",
        "status": "Active",
        "validity_date": "2029-01-31",
        "details": "Works: Jamshedpur Steel Plant, Jharkhand. Scope: Earthquake-resistant TMT rebars 8mm to 32mm diameter."
    },
    {
        "number_type": "CML",
        "number_val": "CML4455667",
        "licensee_name": "UltraTech Cement Limited",
        "brand": "UltraTech",
        "product_category": "Portland Pozzolana Cement (Fly Ash Based)",
        "is_code": "IS 1489 (Part 1):2015",
        "status": "Active",
        "validity_date": "2028-08-31",
        "details": "Works: Awarpur Cement Works, Chandrapur, Maharashtra. Scope: High durability PPC in 50 kg HDPE bags."
    },
    {
        "number_type": "CML",
        "number_val": "CML5566778",
        "licensee_name": "Ceasefire Industries Pvt. Ltd.",
        "brand": "Ceasefire",
        "product_category": "Portable Fire Extinguishers (ABC Powder & Clean Agent)",
        "is_code": "IS 15683:2018",
        "status": "Active",
        "validity_date": "2027-05-15",
        "details": "Factory: Roorkee Industrial Area, Haridwar, Uttarakhand. Scope: 2kg, 4kg, 6kg, and 9kg stored pressure extinguishers."
    },
    {
        "number_type": "CML",
        "number_val": "CML6677889",
        "licensee_name": "Vega Auto Accessories Pvt. Ltd.",
        "brand": "Vega",
        "product_category": "Protective Helmets for Motorcycle Riders",
        "is_code": "IS 4151:2015",
        "status": "Active",
        "validity_date": "2028-02-28",
        "details": "Factory: Belagavi Plant, Karnataka. Scope: Full face and modular helmets with quick-release chin buckle."
    },
    {
        "number_type": "CML",
        "number_val": "CML7788990",
        "licensee_name": "MRF Limited",
        "brand": "MRF",
        "product_category": "Automotive Vehicles - Pneumatic Tyres for Passenger Cars",
        "is_code": "IS 15636:2012",
        "status": "Active",
        "validity_date": "2027-12-31",
        "details": "Factory: Medak Plant, Telangana. Scope: Tubeless steel-belted passenger car radial tyres (ZLX, Wanderer series)."
    },
    {
        "number_type": "CRS",
        "number_val": "R-41009988",
        "licensee_name": "Sony India Pvt. Ltd.",
        "brand": "Sony Bravia",
        "product_category": "Television Sets - 4K Ultra HD Smart LED TV",
        "is_code": "IS 616:2017",
        "status": "Active",
        "validity_date": "2027-09-30",
        "details": "Factory: Foxconn India Hon Hai, Sriperumbudur, Tamil Nadu. Model: Bravia 55-inch 4K Google TV."
    },
    {
        "number_type": "CRS",
        "number_val": "R-41007711",
        "licensee_name": "Apple India Private Limited",
        "brand": "Apple",
        "product_category": "Mobile Phone Handsets with Indian Language Support",
        "is_code": "IS 16333 (Part 3):2022",
        "status": "Active",
        "validity_date": "2028-06-30",
        "details": "Factory: Pegatron India, Chengalpattu, Tamil Nadu. Scope: iPhone 15 & 16 Series with 22 Indian Official Languages."
    },
    {
        "number_type": "CRS",
        "number_val": "R-41003322",
        "licensee_name": "Schneider Electric IT Business India Pvt. Ltd.",
        "brand": "APC by Schneider",
        "product_category": "Uninterruptible Power Systems (UPS)",
        "is_code": "IS 16242 (Part 1):2014",
        "status": "Active",
        "validity_date": "2027-03-31",
        "details": "Factory: Jigani Industrial Area, Bengaluru, Karnataka. Scope: APC Back-UPS 600VA to 2000VA."
    },
    {
        "number_type": "CRS",
        "number_val": "R-41008899",
        "licensee_name": "Tata Power Solar Systems Limited",
        "brand": "Tata Solar",
        "product_category": "Crystalline Silicon Terrestrial Photovoltaic (PV) Modules",
        "is_code": "IS 14286:2010",
        "status": "Active",
        "validity_date": "2028-11-30",
        "details": "Manufacturing Plant: Electronic City, Bengaluru, Karnataka. Scope: Monocrystalline & Polycrystalline PV modules up to 550W."
    },
    {
        "number_type": "CRS",
        "number_val": "R-41006655",
        "licensee_name": "Waaree Energies Limited",
        "brand": "Waaree",
        "product_category": "Photovoltaic (PV) Modules & Solar Panels",
        "is_code": "IS 14286:2010",
        "status": "Active",
        "validity_date": "2028-05-15",
        "details": "Works: Chikhli Plant, Navsari District, Gujarat. Scope: Bifacial and TOPCon solar panels conforming to IS 14286 and IS/IEC 61730."
    }
]

# Testing Laboratories (Central, Regional, Recognized)
TESTING_LABS_SEED = [
    {
        "lab_id": "LAB-CL-01",
        "lab_name": "BIS Central Laboratory (CL Sahibabad)",
        "lab_type": "Central",
        "address": "Plot No. 20/9, Site IV, Sahibabad Industrial Area",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "contact_email": "cl@bis.gov.in",
        "phone": "+91-120-2770030",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-WRL-01",
        "lab_name": "BIS Western Regional Laboratory (WRL)",
        "lab_type": "Regional",
        "address": "Manakalaya, E9, MIDC, Andheri (East)",
        "city": "Mumbai",
        "state": "Maharashtra",
        "contact_email": "wrl@bis.gov.in",
        "phone": "+91-22-28329295",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-NRL-01",
        "lab_name": "BIS Northern Regional Laboratory (NRL)",
        "lab_type": "Regional",
        "address": "Plot No. 4-A, Sector 27-B, Madhya Marg",
        "city": "Chandigarh",
        "state": "Chandigarh",
        "contact_email": "nrl@bis.gov.in",
        "phone": "+91-172-2650290",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-SRL-01",
        "lab_name": "BIS Southern Regional Laboratory (SRL)",
        "lab_type": "Regional",
        "address": "CIT Campus, IV Cross Road, Taramani",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "contact_email": "srl@bis.gov.in",
        "phone": "+91-44-22541442",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-ERL-01",
        "lab_name": "BIS Eastern Regional Laboratory (ERL)",
        "lab_type": "Regional",
        "address": "1/14 C.I.T. Scheme VII M, V.I.P. Road, Kankurgachi",
        "city": "Kolkata",
        "state": "West Bengal",
        "contact_email": "erl@bis.gov.in",
        "phone": "+91-33-23553243",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-01",
        "lab_name": "Shriram Institute for Industrial Research (SIIR)",
        "lab_type": "Recognized",
        "address": "19, University Road, Block A, Timarpur",
        "city": "Delhi",
        "state": "Delhi",
        "contact_email": "customercare@shriraminstitute.org",
        "phone": "+91-11-27667267",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-02",
        "lab_name": "TUV India Testing & Certification Center",
        "lab_type": "Recognized",
        "address": "Survey No. 42/3/1, Baner Road",
        "city": "Pune",
        "state": "Maharashtra",
        "contact_email": "pune-lab@tuv-nord.com",
        "phone": "+91-20-67900000",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-03",
        "lab_name": "National Test House (NTH Bengaluru)",
        "lab_type": "Recognized",
        "address": "F-10, Industrial Estate, Rajajinagar",
        "city": "Bengaluru",
        "state": "Karnataka",
        "contact_email": "nth-blr@gov.in",
        "phone": "+91-80-23382740",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-04",
        "lab_name": "Automotive Research Association of India (ARAI)",
        "lab_type": "Recognized",
        "address": "Survey No. 102, Vetal Hill, Off Paud Road, Kothrud",
        "city": "Pune",
        "state": "Maharashtra",
        "contact_email": "director@araiindia.com",
        "phone": "+91-20-30231111",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-05",
        "lab_name": "Central Institute of Petrochemicals Engineering & Technology (CIPET)",
        "lab_type": "Recognized",
        "address": "Plot No. 630, Phase-IV, GIDC Vatva",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "contact_email": "ahmedabad@cipet.gov.in",
        "phone": "+91-79-40103900",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-06",
        "lab_name": "National Test House (NTH Alipore)",
        "lab_type": "Recognized",
        "address": "11/1, Judges Court Road, Alipore",
        "city": "Kolkata",
        "state": "West Bengal",
        "contact_email": "nth-alipore@gov.in",
        "phone": "+91-33-24791219",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-07",
        "lab_name": "CSIR - Central Building Research Institute (CBRI)",
        "lab_type": "Recognized",
        "address": "Roorkee, Haridwar District",
        "city": "Roorkee",
        "state": "Uttarakhand",
        "contact_email": "director@cbri.res.in",
        "phone": "+91-1332-272243",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-08",
        "lab_name": "National Institute of Solar Energy (NISE)",
        "lab_type": "Recognized",
        "address": "Gwal Pahari, Faridabad-Gurugram Road",
        "city": "Gurugram",
        "state": "Haryana",
        "contact_email": "director@nise.res.in",
        "phone": "+91-124-2853060",
        "is_nabl_accredited": 1
    },
    {
        "lab_id": "LAB-REC-09",
        "lab_name": "UL India Testing & Certification Centre (Solar Lab)",
        "lab_type": "Recognized",
        "address": "Kalyani Platina, Block I, EPIP Zone, Whitefield",
        "city": "Bengaluru",
        "state": "Karnataka",
        "contact_email": "solar.india@ul.com",
        "phone": "+91-80-41384400",
        "is_nabl_accredited": 1
    }
]

# Lab to Standard Mapping (Many-to-Many Join Table)
LAB_STANDARD_MAP_SEED = [
    # BIS Central Lab (Ghaziabad) tests all nationwide flagship standards
    {"lab_id": "LAB-CL-01", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 17803:2022"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 16046 (Part 2):2018"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 13252 (Part 1):2010"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 4151:2015"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 14543:2016"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 1489 (Part 1):2015"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 2347:2017"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 4246:2002"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 15683:2018"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 12269:2013"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 303:1989"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 4985:2021"},
    {"lab_id": "LAB-CL-01", "standard_id": "IS 14286:2010"},

    # Western Regional Lab (Mumbai)
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 17803:2022"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 4151:2015"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 14543:2016"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 16102 (Part 1):2012"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 694:2010"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 2347:2017"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 4246:2002"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 15683:2018"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 15636:2012"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 14286:2010"},

    # Northern Regional Lab (Chandigarh)
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 1489 (Part 1):2015"},
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 1786:2008"},
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 2347:2017"},
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 12269:2013"},

    # Southern Regional Lab (Chennai)
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 16046 (Part 2):2018"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 14543:2016"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 2347:2017"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 4985:2021"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 616:2017"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 16333 (Part 3):2022"},

    # Eastern Regional Lab (Kolkata)
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 1786:2008"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 1489 (Part 1):2015"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 14543:2016"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 2347:2017"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 12269:2013"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 10325:2000"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 303:1989"},

    # Shriram Institute (Delhi)
    {"lab_id": "LAB-REC-01", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-REC-01", "standard_id": "IS 17803:2022"},
    {"lab_id": "LAB-REC-01", "standard_id": "IS 14543:2016"},
    {"lab_id": "LAB-REC-01", "standard_id": "IS 15392:2003"},
    {"lab_id": "LAB-REC-01", "standard_id": "IS 10146:1982"},

    # TUV India (Pune)
    {"lab_id": "LAB-REC-02", "standard_id": "IS 16046 (Part 2):2018"},
    {"lab_id": "LAB-REC-02", "standard_id": "IS 13252 (Part 1):2010"},
    {"lab_id": "LAB-REC-02", "standard_id": "IS 16102 (Part 1):2012"},
    {"lab_id": "LAB-REC-02", "standard_id": "IS 616:2017"},
    {"lab_id": "LAB-REC-02", "standard_id": "IS 16242 (Part 1):2014"},

    # National Test House (Bengaluru)
    {"lab_id": "LAB-REC-03", "standard_id": "IS 13252 (Part 1):2010"},
    {"lab_id": "LAB-REC-03", "standard_id": "IS 694:2010"},
    {"lab_id": "LAB-REC-03", "standard_id": "IS 16046 (Part 2):2018"},
    {"lab_id": "LAB-REC-03", "standard_id": "IS 4985:2021"},

    # Automotive Research Association of India (ARAI Pune)
    {"lab_id": "LAB-REC-04", "standard_id": "IS 4151:2015"},
    {"lab_id": "LAB-REC-04", "standard_id": "IS 2553 (Part 2):2019"},
    {"lab_id": "LAB-REC-04", "standard_id": "IS 15633:2005"},
    {"lab_id": "LAB-REC-04", "standard_id": "IS 15636:2012"},

    # CIPET (Ahmedabad)
    {"lab_id": "LAB-REC-05", "standard_id": "IS 4985:2021"},
    {"lab_id": "LAB-REC-05", "standard_id": "IS 10146:1982"},
    {"lab_id": "LAB-REC-05", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-REC-05", "standard_id": "IS 9473:2002"},

    # National Test House (Kolkata Alipore)
    {"lab_id": "LAB-REC-06", "standard_id": "IS 2347:2017"},
    {"lab_id": "LAB-REC-06", "standard_id": "IS 1489 (Part 1):2015"},
    {"lab_id": "LAB-REC-06", "standard_id": "IS 1786:2008"},
    {"lab_id": "LAB-REC-06", "standard_id": "IS 15298 (Part 2):2016"},

    # CBRI (Roorkee)
    {"lab_id": "LAB-REC-07", "standard_id": "IS 15683:2018"},
    {"lab_id": "LAB-REC-07", "standard_id": "IS 303:1989"},
    {"lab_id": "LAB-REC-07", "standard_id": "IS 2202 (Part 1):1999"},
    {"lab_id": "LAB-REC-07", "standard_id": "IS 12269:2013"},

    # NISE (Gurugram) - Apex Solar Test Center
    {"lab_id": "LAB-REC-08", "standard_id": "IS 14286:2010"},
    {"lab_id": "LAB-REC-08", "standard_id": "IS/IEC 61730 (Part 1):2004"},
    {"lab_id": "LAB-REC-08", "standard_id": "IS 16221 (Part 2):2015"},

    # UL India (Bengaluru) - Solar Testing Lab
    {"lab_id": "LAB-REC-09", "standard_id": "IS 14286:2010"},
    {"lab_id": "LAB-REC-09", "standard_id": "IS/IEC 61730 (Part 1):2004"}
]

# FAQs covering Consumer Affairs, Standards Clubs, MSME Concessions, Grievance Portals
FAQ_SEED = [
    {
        "faq_id": "FAQ-01",
        "category": "Consumer",
        "question": "How can a consumer file a complaint against fake ISI mark or hallmarked jewellery?",
        "answer": "Consumers can file complaints directly through the official 'BIS Care App' (available on Android & iOS) or via the online portal www.manakonline.in under 'Consumer Grievance'. You can report counterfeit ISI marks, misuse of registration numbers, or suboptimal quality. BIS officers investigate complaints, conduct search-and-seizure raids, and take penal action under Section 29 of the BIS Act 2016.",
        "source_url": "https://www.bis.gov.in/consumer-affairs/grievance-redressal/"
    },
    {
        "faq_id": "FAQ-02",
        "category": "MSME",
        "question": "Are there special fee concessions for MSMEs, startups, and women entrepreneurs in BIS certification?",
        "answer": "Yes! To promote domestic manufacturing, BIS provides: (1) 50% concession on application fee, annual licence fee, and minimum marking fee for Micro Enterprises registered under Udyam; (2) 20% concession for Small Scale Enterprises; (3) 20% concession for Startups recognized by DPIIT; and (4) Special concessions for women-led enterprises. These benefits can be claimed during Form V submission on Manak Online.",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2021/04/MSME-Concessions.pdf"
    },
    {
        "faq_id": "FAQ-03",
        "category": "StandardsClubs",
        "question": "What is the BIS Standards Clubs initiative in schools and colleges?",
        "answer": "BIS has established over 10,000 Standards Clubs across high schools, polytechnics, and engineering colleges across India. The objective is to sensitize students ('Young Standard Protectors') towards quality, safety, and standardization through learning science via standards, quiz competitions, industrial visits to BIS labs, and consumer awareness drives. BIS provides financial grants of up to Rs. 10,000 for club activities and laboratory exposure visits.",
        "source_url": "https://www.bis.gov.in/standards-clubs/"
    },
    {
        "faq_id": "FAQ-04",
        "category": "Hallmarking",
        "question": "How can I verify the purity of gold jewellery before buying?",
        "answer": "Always verify that the gold jewellery carries three mandatory marks: (1) BIS Standard Logo (a triangle); (2) Purity / Fineness mark (e.g. 22K916 for 22 Karat 91.6% purity, 18K750 for 18 Karat 75.0% purity, 14K585 for 14 Karat); and (3) 6-character alphanumeric Hallmark Unique Identification (HUID) code. You can instantly enter the 6-character HUID in the BIS Care App or in BIS Saathi's Verification Panel to verify the registered jeweller, assaying center, and article type.",
        "source_url": "https://www.bis.gov.in/hallmarking/overview/"
    },
    {
        "faq_id": "FAQ-05",
        "category": "NITS",
        "question": "What training does the National Institute of Training for Standardization (NITS) provide?",
        "answer": "NITS is the premier training arm of BIS located in Noida. It provides specialized training courses for industry quality managers, laboratory personnel, testing technicians, auditors, and international delegates on implementation of ISO/IS standards, laboratory management (ISO/IEC 17025), and total quality management.",
        "source_url": "https://www.bis.gov.in/nits/"
    },
    {
        "faq_id": "FAQ-06",
        "category": "Organization",
        "question": "What is the Bureau of Indian Standards (BIS)?",
        "answer": "The Bureau of Indian Standards (BIS) is the National Standard Body of India established under the BIS Act 2016 (originally founded as the Indian Standards Institution - ISI in 1947). Operating under the Ministry of Consumer Affairs, Food & Public Distribution, BIS is responsible for harmonious development of standardization, product quality certification (ISI Mark, CRS), gold and silver hallmarking, laboratory testing, and consumer protection across India.",
        "source_url": "https://www.bis.gov.in/the-bureau/about-bis/"
    },
    {
        "faq_id": "FAQ-07",
        "category": "MobileApp",
        "question": "Is there an official BIS mobile app for consumers?",
        "answer": "Yes! The official mobile application is the 'BIS Care App', available for free on both Android (Google Play Store) and iOS (Apple App Store). The app empowers citizens to: (1) Verify ISI mark authenticity by entering the 7-digit CM/L number; (2) Verify Gold Hallmark purity and assaying centre by entering the 6-character HUID code; (3) Verify electronic goods registration by entering the 8-digit CRS R-number; (4) Check validity of testing laboratories; and (5) Lodge quality complaints with photo evidence directly to BIS enforcement officers.",
        "source_url": "https://www.bis.gov.in/consumer-affairs/bis-care-app/"
    },
    {
        "faq_id": "FAQ-08",
        "category": "Portal",
        "question": "What is Manak Online (manakonline.in)?",
        "answer": "Manak Online (www.manakonline.in) is the flagship e-governance portal of the Bureau of Indian Standards. It provides an end-to-end digital platform for manufacturers and citizens: online submission of Form V for Scheme-I certification, fee payments, booking conformity audits, surveillance tracking, standards sales (Manak Copy), and consumer grievance registration.",
        "source_url": "https://www.manakonline.in"
    },
    {
        "faq_id": "FAQ-09",
        "category": "ISIMark",
        "question": "What is the ISI Mark and what does it indicate?",
        "answer": "The ISI mark is the official conformity mark for industrial and consumer products in India under BIS Scheme-I. It certifies that the product complies with the relevant Indian Standard (IS) for safety, quality, and reliability. Products under mandatory Quality Control Orders (QCOs) must carry the ISI mark alongside a unique 7-digit CM/L (Certification Marks Licence) number identifying the licensed manufacturing factory.",
        "source_url": "https://www.bis.gov.in/product-certification/overview/"
    }
]
