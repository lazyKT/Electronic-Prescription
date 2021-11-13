from datetime import datetime

medicine = [
	{
		'medName': "Sulfamethoxazole/Trimethoprim",
		'expDate': datetime(2023, 4, 15, 0, 0, 0),
		'price': "14.82",
		'description': "50gm",
		'instructions': "1 Time Daily",
		'quantity': "746"
	},
	{
		'medName': "Ibuprofen (Rx)",
		'expDate': datetime(2023, 8, 15, 0, 0, 0),
		'price': "96.92",
		'description': "60ml",
		'instructions': "5 Times Daily",
		'quantity': "311"
	},
	{
		'medName': "Carisoprodol",
		'expDate': datetime(2023, 4, 17, 0, 0, 0),
		'price': "86.57",
		'description': "50gm",
		'instructions': "5 Times Daily",
		'quantity': "995"
	},
	{
		'medName': "Simvastatin",
		'expDate': datetime(2023, 1, 2, 0, 0, 0),
		'price': "29.42",
		'description': "20 Tablet",
		'instructions': "3 Times Daily",
		'quantity': "613"
	},
	{
		'medName': "Methylprednisolone",
		'expDate': datetime(2023, 10, 23, 0, 0, 0),
		'price': "166.46",
		'description': "20 Tablet",
		'instructions': "5 Times Daily",
		'quantity': "725"
	},
	{
		'medName': "Zetia",
		'expDate': datetime(2023, 3, 30, 0, 0, 0),
		'price': "127.67",
		'description': "20 Tablet",
		'instructions': "5 Times Daily",
		'quantity': "582"
	},
	{
		'medName': "Benicar HCT",
		'expDate': datetime(2023, 5, 27, 0, 0, 0),
		'price': "118.82",
		'description': "15ml",
		'instructions': "5 Times Daily",
		'quantity': "568"
	},
	{
		'medName': "Ciprofloxacin HCl",
		'expDate': datetime(2023, 3, 29, 0, 0, 0),
		'price': "174.99",
		'description': "30gm",
		'instructions': "5 Times Daily",
		'quantity': "857"
	},
	{
		'medName': "Premarin",
		'expDate': datetime(2023, 1, 24, 0, 0, 0),
		'price': "38.63",
		'description': "20 Tablet",
		'instructions': "5 Times Daily",
		'quantity': "657"
	},
	{
		'medName': "Lidoderm",
		'expDate': datetime(2023, 11, 23, 0, 0, 0),
		'price': "184.79",
		'description': "50gm",
		'instructions': "5 Times Daily",
		'quantity': "912"
	},
	{
		'medName': "Spiriva Handihaler",
		'expDate': datetime(2023, 6, 12, 0, 0, 0),
		'price': "26.06",
		'description': "50gm",
		'instructions': "5 Times Daily",
		'quantity': "759"
	},
	{
		'medName': "Glipizide",
		'expDate': datetime(2023, 9, 22, 0, 0, 0),
		'price': "53.21",
		'description': "60ml",
		'instructions': "5 Times Daily",
		'quantity': "989"
	},
	{
		'medName': "Digoxin",
		'expDate': datetime(2023, 1, 8, 0, 0, 0),
		'price': "55.77",
		'description': "30gm",
		'instructions': "1 Time Daily",
		'quantity': "908"
	},
	{
		'medName': "Actos",
		'expDate': datetime(2023, 5, 2, 0, 0, 0),
		'price': "143.77",
		'description': "15ml",
		'instructions': "3 Times Daily",
		'quantity': "706"
	},
	{
		'medName': "Cyclobenzaprin HCl",
		'expDate': datetime(2023, 5, 4, 0, 0, 0),
		'price': "52.12",
		'description': "5 Tablet",
		'instructions': "5 Times Daily",
		'quantity': "411"
	},
	{
		'medName': "Albuterol",
		'expDate': datetime(2023, 8, 1, 0, 0, 0),
		'price': "44.98",
		'description': "10 Tablet",
		'instructions': "5 Times Daily",
		'quantity': "913"
	},
	{
		'medName': "Lantus",
		'expDate': datetime(2023, 11, 13, 0, 0, 0),
		'price': "193.72",
		'description': "75ml",
		'instructions': "1 Time Daily",
		'quantity': "810"
	},
	{
		'medName': "Synthroid",
		'expDate': datetime(2023, 5, 5, 0, 0, 0),
		'price': "141.71",
		'description': "60ml",
		'instructions': "3 Times Daily",
		'quantity': "599"
	},
	{
		'medName': "Lorazepam",
		'expDate': datetime(2023, 9, 7, 0, 0, 0),
		'price': "106.80",
		'description': "100ml",
		'instructions': "1 Time Daily",
		'quantity': "523"
	},
	{
		'medName': "Hydrochlorothiazide",
		'expDate': datetime(2023, 2, 26, 0, 0, 0),
		'price': "39.03",
		'description': "30gm",
		'instructions': "3 Times Daily",
		'quantity': "471"
	},
	{
		'medName': "Fluoxetine HCl",
		'expDate': datetime(2023, 5, 13, 0, 0, 0),
		'price': "120.75",
		'description': "75ml",
		'instructions': "3 Times Daily",
		'quantity': "797"
	},
	{
		'medName': "Losartan Potassium",
		'expDate': datetime(2023, 6, 13, 0, 0, 0),
		'price': "159.40",
		'description': "75ml",
		'instructions': "5 Times Daily",
		'quantity': "481"
	},
	{
		'medName': "Ranitidine HCl",
		'expDate': datetime(2023, 5, 29, 0, 0, 0),
		'price': "151.35",
		'description': "20 Tablet",
		'instructions': "5 Times Daily",
		'quantity': "568"
	},
	{
		'medName': "Paroxetine HCl",
		'expDate': datetime(2023, 1, 17, 0, 0, 0),
		'price': "13.04",
		'description': "20 Tablet",
		'instructions': "1 Time Daily",
		'quantity': "650"
	},
	{
		'medName': "Levaquin",
		'expDate': datetime(2023, 8, 9, 0, 0, 0),
		'price': "72.60",
		'description': "10 Tablet",
		'instructions': "3 Times Daily",
		'quantity': "975"
	},
	{
		'medName': "Alprazolam",
		'expDate': datetime(2023, 10, 3, 0, 0, 0),
		'price': "25.07",
		'description': "5 Tablet",
		'instructions': "3 Times Daily",
		'quantity': "956"
	},
	{
		'medName': "TriNessa",
		'expDate': datetime(2023, 4, 26, 0, 0, 0),
		'price': "192.40",
		'description': "30gm",
		'instructions': "1 Time Daily",
		'quantity': "868"
	},
	{
		'medName': "Gabapentin",
		'expDate': datetime(2023, 3, 29, 0, 0, 0),
		'price': "166.08",
		'description': "20 Tablet",
		'instructions': "3 Times Daily",
		'quantity': "871"
	},
	{
		'medName': "Triamcinolone Acetonide",
		'expDate': datetime(2023, 9, 6, 0, 0, 0),
		'price': "108.91",
		'description': "10 Tablet",
		'instructions': "3 Times Daily",
		'quantity': "673"
	},
	{
		'medName': "Cymbalta",
		'expDate': datetime(2023, 3, 11, 0, 0, 0),
		'price': "110.94",
		'description': "15ml",
		'instructions': "3 Times Daily",
		'quantity': "360"
	},
	{
		'medName': "Nuvaring",
		'expDate': datetime(2023, 7, 25, 0, 0, 0),
		'price': "9.83",
		'description': "5 Tablet",
		'instructions': "5 Times Daily",
		'quantity': "444"
	},
	{
		'medName': "Amlodipine Besylate",
		'expDate': datetime(2023, 9, 24, 0, 0, 0),
		'price': "163.12",
		'description': "100ml",
		'instructions': "5 Times Daily",
		'quantity': "659"
	},
	{
		'medName': "Namenda",
		'expDate': datetime(2023, 10, 27, 0, 0, 0),
		'price': "32.16",
		'description': "15ml",
		'instructions': "3 Times Daily",
		'quantity': "451"
	},
	{
		'medName': "Promethazine HCl",
		'expDate': datetime(2023, 5, 6, 0, 0, 0),
		'price': "120.70",
		'description': "20 Tablet",
		'instructions': "3 Times Daily",
		'quantity': "678"
	},
	{
		'medName': "Azithromycin",
		'expDate': datetime(2023, 5, 7, 0, 0, 0),
		'price': "102.67",
		'description': "100gm",
		'instructions': "5 Times Daily",
		'quantity': "515"
	},
	{
		'medName': "Lovaza",
		'expDate': datetime(2023, 8, 26, 0, 0, 0),
		'price': "42.34",
		'description': "30gm",
		'instructions': "3 Times Daily",
		'quantity': "993"
	},
	{
		'medName': "Gianvi",
		'expDate': datetime(2023, 10, 16, 0, 0, 0),
		'price': "166.61",
		'description': "15ml",
		'instructions': "1 Time Daily",
		'quantity': "534"
	},
	{
		'medName': "Niaspan",
		'expDate': datetime(2023, 9, 7, 0, 0, 0),
		'price': "151.32",
		'description': "75ml",
		'instructions': "1 Time Daily",
		'quantity': "805"
	},
	{
		'medName': "Lexapro",
		'expDate': datetime(2023, 9, 24, 0, 0, 0),
		'price': "99.75",
		'description': "75gm",
		'instructions': "1 Time Daily",
		'quantity': "853"
	},
	{
		'medName': "Zyprexa",
		'expDate': datetime(2023, 12, 31, 0, 0, 0),
		'price': "68.81",
		'description': "15ml",
		'instructions': "3 Times Daily",
		'quantity': "841"
	},
	{
		'medName': "Allopurinol",
		'expDate': datetime(2023, 8, 6, 0, 0, 0),
		'price': "150.02",
		'description': "50gm",
		'instructions': "5 Times Daily",
		'quantity': "473"
	},
	{
		'medName': "Oxycodone/APAP",
		'expDate': datetime(2023, 9, 15, 0, 0, 0),
		'price': "12.63",
		'description': "10 Tablet",
		'instructions': "1 Time Daily",
		'quantity': "812"
	},
	{
		'medName': "Atenolol",
		'expDate': datetime(2023, 7, 8, 0, 0, 0),
		'price': "40.36",
		'description': "100ml",
		'instructions': "3 Times Daily",
		'quantity': "562"
	}
]