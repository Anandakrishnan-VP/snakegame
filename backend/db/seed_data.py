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
        "synonyms": "lithium ion battery, power bank, mobile battery, laptop battery, rechargeable battery, li-ion cell, ev battery cell, portable battery pack",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "is_code": "IS 13252 (Part 1):2010",
        "title": "Information Technology Equipment - Safety - General Requirements",
        "division": "Electronics & Information Technology (CRS)",
        "qco_status": "Mandatory",
        "qco_reference": "MeitY Electronics & IT Goods (Requirements for Compulsory Registration) Order, 2012",
        "related_standards": "IS 16046 (Part 2):2018, IEC 60950-1",
        "synonyms": "laptop, computer, tablet, pos terminal, electronic cash register, it equipment, server, notebook, wifi router",
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
    }
]

# Tier B Flagship Deep-Clause Curated Chunks (Verbatim text from official publications)
CHUNKS_SEED = [
    # Flagship 1: IS 9873 (Part 1):2019 / IS 17803:2022 (Child & Consumer Safety)
    {
        "chunk_id": "IS9873-P1-C4.1",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "4.1",
        "sub_clause": "4.1.1",
        "page": 7,
        "content": "Normal use and foreseeable abuse: Toys shall be constructed so that they do not present mechanical risks under normal and reasonably foreseeable conditions of use, taking into account the behavior of children. The tests described in Clause 5 simulate conditions under which toys may be subjected during use.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Safety of Toys",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS9873-P1-C4.2",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "4.2",
        "sub_clause": "4.2.1",
        "page": 8,
        "content": "Small parts and choking hazards: For toys intended for children under 36 months of age, toys and removable components thereof, as well as components liberated after tension, drop, and torque testing (as specified in 5.24), shall not fit entirely within the small parts test cylinder defined in 5.2.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Safety of Toys",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS9873-P1-C4.7",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "4.7",
        "sub_clause": "4.7.1",
        "page": 11,
        "content": "Edges and Sharp Points: Accessible edges of toys shall not present an unreasonable risk of injury. Metal and glass edges on toys intended for children under 96 months shall be rolled, curled, or protected with a permanent guard before and after abuse testing.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Safety of Toys",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS9873-P1-C7",
        "standard_id": "IS 9873 (Part 1):2019",
        "clause": "7.1",
        "sub_clause": "7.1.2",
        "page": 18,
        "content": "Marking and Packaging: Toys or their packaging shall be legibly and indelibly marked with the Standard Mark (ISI mark) along with the unique licence number (CM/L-XXXXXXXXXX). The manufacturer's name, registered trade name/mark, and address, along with age grading warnings, shall be clearly visible.",
        "source": "Bureau of Indian Standards: IS 9873 (Part 1):2019 Marking Requirements",
        "source_url": "https://www.bis.gov.in/wp-content/uploads/2020/02/Toys-QCO-2020.pdf"
    },
    {
        "chunk_id": "IS17803-C4.1",
        "standard_id": "IS 17803:2022",
        "clause": "4.1",
        "sub_clause": "4.1.1",
        "page": 3,
        "content": "Material Composition: The inner flask and all parts coming into direct contact with food or potable water shall be fabricated from food-grade stainless steel conforming to grade 304 (X04Cr19Ni9) or grade 316 of IS 6911. The material shall be non-toxic, corrosion-resistant, and free from dangerous leaching.",
        "source": "Bureau of Indian Standards: IS 17803:2022 Stainless Steel Flasks",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-flasks-2023"
    },
    {
        "chunk_id": "IS17803-C5.2",
        "standard_id": "IS 17803:2022",
        "clause": "5.2",
        "sub_clause": "5.2.3",
        "page": 5,
        "content": "Thermal Performance Test: When filled with boiling water at 95°C and kept sealed in an ambient environment of 20°C ± 2°C for a period of 6 hours, the temperature of the water inside the insulated vacuum flask shall not fall below 60°C for flasks with capacity >= 500 ml.",
        "source": "Bureau of Indian Standards: IS 17803:2022 Thermal Testing",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-flasks-2023"
    },
    {
        "chunk_id": "IS17803-C6.1",
        "standard_id": "IS 17803:2022",
        "clause": "6.1",
        "sub_clause": "6.1.1",
        "page": 6,
        "content": "Drop Test for Durability: The flask, filled with water to rated capacity, shall withstand two successive drops from a height of 1.0 meter onto a smooth concrete floor without rupturing, leaking, or detachment of internal vacuum sealing.",
        "source": "Bureau of Indian Standards: IS 17803:2022 Mechanical Integrity",
        "source_url": "https://www.bis.gov.in/qco-stainless-steel-flasks-2023"
    },
    # Flagship 2: IS 16046 (Part 2):2018 / IS 13252 (Part 1):2010 (Electronics & CRS)
    {
        "chunk_id": "IS16046-P2-C5.3",
        "standard_id": "IS 16046 (Part 2):2018",
        "clause": "5.3",
        "sub_clause": "5.3.1",
        "page": 9,
        "content": "Continuous Charging Safety: Fully discharged cells shall be charged continuously for 7 days at manufacturer recommended charging voltage and current. Cells shall not catch fire, explode, or vent hazardous gases during or after the continuous charge test.",
        "source": "Bureau of Indian Standards: IS 16046 (Part 2):2018 Secondary Cells Safety",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "chunk_id": "IS16046-P2-C7.2",
        "standard_id": "IS 16046 (Part 2):2018",
        "clause": "7.2",
        "sub_clause": "7.2.2",
        "page": 14,
        "content": "External Short Circuit Test: Fully charged cells and battery packs shall be short-circuited by connecting the positive and negative terminals with a total external resistance of 80 mΩ ± 20 mΩ at 55°C ± 5°C. Cells shall remain on test until case temperature returns to steady state. No fire or explosion is permitted.",
        "source": "Bureau of Indian Standards: IS 16046 (Part 2):2018 Short Circuit Requirements",
        "source_url": "https://www.crsbis.in/BIS/product-category.do"
    },
    {
        "chunk_id": "IS16046-P2-C9.1",
        "standard_id": "IS 16046 (Part 2):2018",
        "clause": "9.1",
        "sub_clause": "9.1.1",
        "page": 19,
        "content": "Compulsory Registration Marking: Each battery or power bank shall bear the BIS Standard Mark under CRS in the format: 'Self-Declaration - Conforming to IS 16046 (Part 2):2018 / IEC 62133-2, R-XXXXXXXX' accompanied by the official BIS CRS word mark. The R-number indicates unique registration with MeitY/BIS.",
        "source": "Bureau of Indian Standards: CRS Marking Guidelines",
        "source_url": "https://www.crsbis.in/BIS/about-crs.do"
    },
    {
        "chunk_id": "IS13252-P1-C1.5",
        "standard_id": "IS 13252 (Part 1):2010",
        "clause": "1.5",
        "sub_clause": "1.5.1",
        "page": 12,
        "content": "General electrical insulation and creepage: Components and circuits carrying hazardous voltages shall have sufficient clearance and creepage distances to prevent breakdown, fire, or electric shock under both normal operation and single-fault conditions.",
        "source": "Bureau of Indian Standards: IS 13252 (Part 1):2010 IT Safety",
        "source_url": "https://www.crsbis.in/BIS/about-crs.do"
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

    # Western Regional Lab (Mumbai)
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 17803:2022"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 4151:2015"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 14543:2016"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 16102 (Part 1):2012"},
    {"lab_id": "LAB-WRL-01", "standard_id": "IS 694:2010"},

    # Northern Regional Lab (Chandigarh)
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 1489 (Part 1):2015"},
    {"lab_id": "LAB-NRL-01", "standard_id": "IS 1786:2008"},

    # Southern Regional Lab (Chennai)
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 16046 (Part 2):2018"},
    {"lab_id": "LAB-SRL-01", "standard_id": "IS 14543:2016"},

    # Eastern Regional Lab (Kolkata)
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 1786:2008"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 1489 (Part 1):2015"},
    {"lab_id": "LAB-ERL-01", "standard_id": "IS 14543:2016"},

    # Shriram Institute (Delhi)
    {"lab_id": "LAB-REC-01", "standard_id": "IS 9873 (Part 1):2019"},
    {"lab_id": "LAB-REC-01", "standard_id": "IS 17803:2022"},
    {"lab_id": "LAB-REC-01", "standard_id": "IS 14543:2016"},

    # TUV India (Pune)
    {"lab_id": "LAB-REC-02", "standard_id": "IS 16046 (Part 2):2018"},
    {"lab_id": "LAB-REC-02", "standard_id": "IS 13252 (Part 1):2010"},
    {"lab_id": "LAB-REC-02", "standard_id": "IS 16102 (Part 1):2012"},

    # National Test House (Bengaluru)
    {"lab_id": "LAB-REC-03", "standard_id": "IS 13252 (Part 1):2010"},
    {"lab_id": "LAB-REC-03", "standard_id": "IS 694:2010"},
    {"lab_id": "LAB-REC-03", "standard_id": "IS 16046 (Part 2):2018"}
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
    }
]
