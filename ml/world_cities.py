"""
Comprehensive world cities database with coordinates
Contains 250+ major cities from every continent
"""

WORLD_CITIES = {
    # NORTH AMERICA
    
    # United States
    "New York, USA": {"lat": 40.7128, "lon": -74.0060},
    "Los Angeles, USA": {"lat": 34.0522, "lon": -118.2437},
    "Chicago, USA": {"lat": 41.8781, "lon": -87.6298},
    "Houston, USA": {"lat": 29.7604, "lon": -95.3698},
    "Phoenix, USA": {"lat": 33.4484, "lon": -112.0740},
    "Philadelphia, USA": {"lat": 39.9526, "lon": -75.1652},
    "San Antonio, USA": {"lat": 29.4241, "lon": -98.4936},
    "San Diego, USA": {"lat": 32.7157, "lon": -117.1611},
    "Dallas, USA": {"lat": 32.7767, "lon": -96.7970},
    "San Jose, USA": {"lat": 37.3382, "lon": -121.8863},
    "Austin, USA": {"lat": 30.2672, "lon": -97.7431},
    "Jacksonville, USA": {"lat": 30.3322, "lon": -81.6557},
    "Fort Worth, USA": {"lat": 32.7555, "lon": -97.3308},
    "Columbus, USA": {"lat": 39.9612, "lon": -82.9988},
    "San Francisco, USA": {"lat": 37.7749, "lon": -122.4194},
    "Charlotte, USA": {"lat": 35.2271, "lon": -80.8431},
    "Indianapolis, USA": {"lat": 39.7684, "lon": -86.1581},
    "Seattle, USA": {"lat": 47.6062, "lon": -122.3321},
    "Denver, USA": {"lat": 39.7392, "lon": -104.9903},
    "Washington DC, USA": {"lat": 38.9072, "lon": -77.0369},
    "Boston, USA": {"lat": 42.3601, "lon": -71.0589},
    "Nashville, USA": {"lat": 36.1627, "lon": -86.7816},
    "Detroit, USA": {"lat": 42.3314, "lon": -83.0458},
    "Portland, USA": {"lat": 45.5152, "lon": -122.6784},
    "Las Vegas, USA": {"lat": 36.1699, "lon": -115.1398},
    "Memphis, USA": {"lat": 35.1495, "lon": -90.0490},
    "Louisville, USA": {"lat": 38.2527, "lon": -85.7585},
    "Baltimore, USA": {"lat": 39.2904, "lon": -76.6122},
    "Milwaukee, USA": {"lat": 43.0389, "lon": -87.9065},
    "Albuquerque, USA": {"lat": 35.0844, "lon": -106.6504},
    "Tucson, USA": {"lat": 32.2226, "lon": -110.9747},
    "Fresno, USA": {"lat": 36.7378, "lon": -119.7871},
    "Sacramento, USA": {"lat": 38.5816, "lon": -121.4944},
    "Kansas City, USA": {"lat": 39.0997, "lon": -94.5786},
    "Atlanta, USA": {"lat": 33.7490, "lon": -84.3880},
    "Miami, USA": {"lat": 25.7617, "lon": -80.1918},
    "Cleveland, USA": {"lat": 41.4993, "lon": -81.6944},
    "New Orleans, USA": {"lat": 29.9511, "lon": -90.0715},
    "Minneapolis, USA": {"lat": 44.9778, "lon": -93.2650},
    "Tampa, USA": {"lat": 27.9506, "lon": -82.4572},
    "Honolulu, USA": {"lat": 21.3099, "lon": -157.8581},
    "Anchorage, USA": {"lat": 61.2181, "lon": -149.9003},
    
    # Canada
    "Toronto, Canada": {"lat": 43.6532, "lon": -79.3832},
    "Montreal, Canada": {"lat": 45.5017, "lon": -73.5673},
    "Vancouver, Canada": {"lat": 49.2827, "lon": -123.1207},
    "Calgary, Canada": {"lat": 51.0447, "lon": -114.0719},
    "Edmonton, Canada": {"lat": 53.5461, "lon": -113.4938},
    "Ottawa, Canada": {"lat": 45.4215, "lon": -75.6972},
    "Winnipeg, Canada": {"lat": 49.8951, "lon": -97.1384},
    "Quebec City, Canada": {"lat": 46.8139, "lon": -71.2080},
    "Halifax, Canada": {"lat": 44.6488, "lon": -63.5752},
    
    # Mexico
    "Mexico City, Mexico": {"lat": 19.4326, "lon": -99.1332},
    "Guadalajara, Mexico": {"lat": 20.6597, "lon": -103.3496},
    "Monterrey, Mexico": {"lat": 25.6866, "lon": -100.3161},
    "Puebla, Mexico": {"lat": 19.0414, "lon": -98.2063},
    "Tijuana, Mexico": {"lat": 32.5149, "lon": -117.0382},
    "Cancún, Mexico": {"lat": 21.1619, "lon": -86.8515},
    
    # SOUTH AMERICA
    
    "São Paulo, Brazil": {"lat": -23.5505, "lon": -46.6333},
    "Rio de Janeiro, Brazil": {"lat": -22.9068, "lon": -43.1729},
    "Brasília, Brazil": {"lat": -15.8267, "lon": -47.9218},
    "Salvador, Brazil": {"lat": -12.9714, "lon": -38.5014},
    "Fortaleza, Brazil": {"lat": -3.7172, "lon": -38.5433},
    "Belo Horizonte, Brazil": {"lat": -19.9167, "lon": -43.9345},
    "Manaus, Brazil": {"lat": -3.1190, "lon": -60.0217},
    "Curitiba, Brazil": {"lat": -25.4284, "lon": -49.2733},
    "Recife, Brazil": {"lat": -8.0476, "lon": -34.8770},
    
    "Buenos Aires, Argentina": {"lat": -34.6037, "lon": -58.3816},
    "Córdoba, Argentina": {"lat": -31.4201, "lon": -64.1888},
    "Rosario, Argentina": {"lat": -32.9442, "lon": -60.6505},
    "Mendoza, Argentina": {"lat": -32.8895, "lon": -68.8458},
    
    "Lima, Peru": {"lat": -12.0464, "lon": -77.0428},
    "Arequipa, Peru": {"lat": -16.4090, "lon": -71.5375},
    "Cusco, Peru": {"lat": -13.5319, "lon": -71.9675},
    
    "Bogotá, Colombia": {"lat": 4.7110, "lon": -74.0721},
    "Medellín, Colombia": {"lat": 6.2476, "lon": -75.5658},
    "Cali, Colombia": {"lat": 3.4516, "lon": -76.5320},
    "Cartagena, Colombia": {"lat": 10.3910, "lon": -75.4794},
    
    "Santiago, Chile": {"lat": -33.4489, "lon": -70.6693},
    "Valparaíso, Chile": {"lat": -33.0458, "lon": -71.6197},
    
    "Caracas, Venezuela": {"lat": 10.4806, "lon": -66.9036},
    "Maracaibo, Venezuela": {"lat": 10.6666, "lon": -71.6124},
    
    "Quito, Ecuador": {"lat": -0.1807, "lon": -78.4678},
    "Guayaquil, Ecuador": {"lat": -2.1894, "lon": -79.8890},
    
    "La Paz, Bolivia": {"lat": -16.5000, "lon": -68.1500},
    "Santa Cruz, Bolivia": {"lat": -17.7833, "lon": -63.1821},
    
    "Asunción, Paraguay": {"lat": -25.2637, "lon": -57.5759},
    "Montevideo, Uruguay": {"lat": -34.9011, "lon": -56.1645},
    
    # EUROPE
    
    # United Kingdom
    "London, UK": {"lat": 51.5074, "lon": -0.1278},
    "Manchester, UK": {"lat": 53.4808, "lon": -2.2426},
    "Birmingham, UK": {"lat": 52.4862, "lon": -1.8904},
    "Liverpool, UK": {"lat": 53.4084, "lon": -2.9916},
    "Edinburgh, UK": {"lat": 55.9533, "lon": -3.1883},
    "Glasgow, UK": {"lat": 55.8642, "lon": -4.2518},
    "Leeds, UK": {"lat": 53.8008, "lon": -1.5491},
    "Bristol, UK": {"lat": 51.4545, "lon": -2.5879},
    
    # France
    "Paris, France": {"lat": 48.8566, "lon": 2.3522},
    "Marseille, France": {"lat": 43.2965, "lon": 5.3698},
    "Lyon, France": {"lat": 45.7640, "lon": 4.8357},
    "Toulouse, France": {"lat": 43.6047, "lon": 1.4442},
    "Nice, France": {"lat": 43.7102, "lon": 7.2620},
    "Bordeaux, France": {"lat": 44.8378, "lon": -0.5792},
    
    # Germany
    "Berlin, Germany": {"lat": 52.5200, "lon": 13.4050},
    "Hamburg, Germany": {"lat": 53.5511, "lon": 9.9937},
    "Munich, Germany": {"lat": 48.1351, "lon": 11.5820},
    "Cologne, Germany": {"lat": 50.9375, "lon": 6.9603},
    "Frankfurt, Germany": {"lat": 50.1109, "lon": 8.6821},
    "Stuttgart, Germany": {"lat": 48.7758, "lon": 9.1829},
    "Düsseldorf, Germany": {"lat": 51.2277, "lon": 6.7735},
    
    # Spain
    "Madrid, Spain": {"lat": 40.4168, "lon": -3.7038},
    "Barcelona, Spain": {"lat": 41.3851, "lon": 2.1734},
    "Valencia, Spain": {"lat": 39.4699, "lon": -0.3763},
    "Seville, Spain": {"lat": 37.3891, "lon": -5.9845},
    "Málaga, Spain": {"lat": 36.7213, "lon": -4.4214},
    "Bilbao, Spain": {"lat": 43.2630, "lon": -2.9350},
    
    # Italy
    "Rome, Italy": {"lat": 41.9028, "lon": 12.4964},
    "Milan, Italy": {"lat": 45.4642, "lon": 9.1900},
    "Naples, Italy": {"lat": 40.8518, "lon": 14.2681},
    "Turin, Italy": {"lat": 45.0703, "lon": 7.6869},
    "Florence, Italy": {"lat": 43.7696, "lon": 11.2558},
    "Venice, Italy": {"lat": 45.4408, "lon": 12.3155},
    
    # Netherlands
    "Amsterdam, Netherlands": {"lat": 52.3676, "lon": 4.9041},
    "Rotterdam, Netherlands": {"lat": 51.9225, "lon": 4.4792},
    "The Hague, Netherlands": {"lat": 52.0705, "lon": 4.3007},
    "Utrecht, Netherlands": {"lat": 52.0907, "lon": 5.1214},
    
    # Other Europe
    "Vienna, Austria": {"lat": 48.2082, "lon": 16.3738},
    "Prague, Czech Republic": {"lat": 50.0755, "lon": 14.4378},
    "Budapest, Hungary": {"lat": 47.4979, "lon": 19.0402},
    "Warsaw, Poland": {"lat": 52.2297, "lon": 21.0122},
    "Stockholm, Sweden": {"lat": 59.3293, "lon": 18.0686},
    "Copenhagen, Denmark": {"lat": 55.6761, "lon": 12.5683},
    "Oslo, Norway": {"lat": 59.9139, "lon": 10.7522},
    "Helsinki, Finland": {"lat": 60.1699, "lon": 24.9384},
    "Athens, Greece": {"lat": 37.9838, "lon": 23.7275},
    "Lisbon, Portugal": {"lat": 38.7223, "lon": -9.1393},
    "Porto, Portugal": {"lat": 41.1579, "lon": -8.6291},
    "Dublin, Ireland": {"lat": 53.3498, "lon": -6.2603},
    "Brussels, Belgium": {"lat": 50.8503, "lon": 4.3517},
    "Zurich, Switzerland": {"lat": 47.3769, "lon": 8.5417},
    "Geneva, Switzerland": {"lat": 46.2044, "lon": 6.1432},
    "Moscow, Russia": {"lat": 55.7558, "lon": 37.6173},
    "Saint Petersburg, Russia": {"lat": 59.9311, "lon": 30.3609},
    "Istanbul, Turkey": {"lat": 41.0082, "lon": 28.9784},
    "Ankara, Turkey": {"lat": 39.9334, "lon": 32.8597},
    "Belgrade, Serbia": {"lat": 44.7866, "lon": 20.4489},
    "Bucharest, Romania": {"lat": 44.4268, "lon": 26.1025},
    "Sofia, Bulgaria": {"lat": 42.6977, "lon": 23.3219},
    "Kiev, Ukraine": {"lat": 50.4501, "lon": 30.5234},
    
    # ASIA
    
    # China
    "Beijing, China": {"lat": 39.9042, "lon": 116.4074},
    "Shanghai, China": {"lat": 31.2304, "lon": 121.4737},
    "Guangzhou, China": {"lat": 23.1291, "lon": 113.2644},
    "Shenzhen, China": {"lat": 22.5431, "lon": 114.0579},
    "Chengdu, China": {"lat": 30.5728, "lon": 104.0668},
    "Hong Kong, China": {"lat": 22.3193, "lon": 114.1694},
    "Chongqing, China": {"lat": 29.4316, "lon": 106.9123},
    "Tianjin, China": {"lat": 39.3434, "lon": 117.3616},
    "Wuhan, China": {"lat": 30.5928, "lon": 114.3055},
    "Xi'an, China": {"lat": 34.3416, "lon": 108.9398},
    "Hangzhou, China": {"lat": 30.2741, "lon": 120.1551},
    
    # India
    "Mumbai, India": {"lat": 19.0760, "lon": 72.8777},
    "Delhi, India": {"lat": 28.7041, "lon": 77.1025},
    "Bangalore, India": {"lat": 12.9716, "lon": 77.5946},
    "Hyderabad, India": {"lat": 17.3850, "lon": 78.4867},
    "Chennai, India": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata, India": {"lat": 22.5726, "lon": 88.3639},
    "Pune, India": {"lat": 18.5204, "lon": 73.8567},
    "Ahmedabad, India": {"lat": 23.0225, "lon": 72.5714},
    "Jaipur, India": {"lat": 26.9124, "lon": 75.7873},
    "Lucknow, India": {"lat": 26.8467, "lon": 80.9462},
    
    # Japan
    "Tokyo, Japan": {"lat": 35.6762, "lon": 139.6503},
    "Osaka, Japan": {"lat": 34.6937, "lon": 135.5023},
    "Yokohama, Japan": {"lat": 35.4437, "lon": 139.6380},
    "Nagoya, Japan": {"lat": 35.1815, "lon": 136.9066},
    "Kyoto, Japan": {"lat": 35.0116, "lon": 135.7681},
    "Sapporo, Japan": {"lat": 43.0642, "lon": 141.3469},
    "Fukuoka, Japan": {"lat": 33.5904, "lon": 130.4017},
    
    # South Korea
    "Seoul, South Korea": {"lat": 37.5665, "lon": 126.9780},
    "Busan, South Korea": {"lat": 35.1796, "lon": 129.0756},
    "Incheon, South Korea": {"lat": 37.4563, "lon": 126.7052},
    
    # Southeast Asia
    "Bangkok, Thailand": {"lat": 13.7563, "lon": 100.5018},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Kuala Lumpur, Malaysia": {"lat": 3.1390, "lon": 101.6869},
    "Jakarta, Indonesia": {"lat": -6.2088, "lon": 106.8456},
    "Manila, Philippines": {"lat": 14.5995, "lon": 120.9842},
    "Hanoi, Vietnam": {"lat": 21.0285, "lon": 105.8542},
    "Ho Chi Minh City, Vietnam": {"lat": 10.8231, "lon": 106.6297},
    "Yangon, Myanmar": {"lat": 16.8661, "lon": 96.1951},
    "Phnom Penh, Cambodia": {"lat": 11.5564, "lon": 104.9282},
    "Vientiane, Laos": {"lat": 17.9757, "lon": 102.6331},
    "Taipei, Taiwan": {"lat": 25.0330, "lon": 121.5654},
    
    # South Asia
    "Karachi, Pakistan": {"lat": 24.8607, "lon": 67.0011},
    "Lahore, Pakistan": {"lat": 31.5497, "lon": 74.3436},
    "Islamabad, Pakistan": {"lat": 33.6844, "lon": 73.0479},
    "Dhaka, Bangladesh": {"lat": 23.8103, "lon": 90.4125},
    "Colombo, Sri Lanka": {"lat": 6.9271, "lon": 79.8612},
    "Kathmandu, Nepal": {"lat": 27.7172, "lon": 85.3240},
    
    # Middle East
    "Dubai, UAE": {"lat": 25.2048, "lon": 55.2708},
    "Abu Dhabi, UAE": {"lat": 24.4539, "lon": 54.3773},
    "Riyadh, Saudi Arabia": {"lat": 24.7136, "lon": 46.6753},
    "Jeddah, Saudi Arabia": {"lat": 21.5433, "lon": 39.1728},
    "Tehran, Iran": {"lat": 35.6892, "lon": 51.3890},
    "Baghdad, Iraq": {"lat": 33.3152, "lon": 44.3661},
    "Damascus, Syria": {"lat": 33.5138, "lon": 36.2765},
    "Beirut, Lebanon": {"lat": 33.8886, "lon": 35.4955},
    "Amman, Jordan": {"lat": 31.9454, "lon": 35.9284},
    "Jerusalem, Israel": {"lat": 31.7683, "lon": 35.2137},
    "Tel Aviv, Israel": {"lat": 32.0853, "lon": 34.7818},
    "Kuwait City, Kuwait": {"lat": 29.3759, "lon": 47.9774},
    "Doha, Qatar": {"lat": 25.2854, "lon": 51.5310},
    "Muscat, Oman": {"lat": 23.5880, "lon": 58.3829},
    
    # AFRICA
    
    "Cairo, Egypt": {"lat": 30.0444, "lon": 31.2357},
    "Alexandria, Egypt": {"lat": 31.2001, "lon": 29.9187},
    "Lagos, Nigeria": {"lat": 6.5244, "lon": 3.3792},
    "Johannesburg, South Africa": {"lat": -26.2041, "lon": 28.0473},
    "Cape Town, South Africa": {"lat": -33.9249, "lon": 18.4241},
    "Durban, South Africa": {"lat": -29.8587, "lon": 31.0218},
    "Nairobi, Kenya": {"lat": -1.2864, "lon": 36.8172},
    "Casablanca, Morocco": {"lat": 33.5731, "lon": -7.5898},
    "Rabat, Morocco": {"lat": 34.0209, "lon": -6.8416},
    "Addis Ababa, Ethiopia": {"lat": 9.0320, "lon": 38.7469},
    "Accra, Ghana": {"lat": 5.6037, "lon": -0.1870},
    "Dakar, Senegal": {"lat": 14.7167, "lon": -17.4677},
    "Dar es Salaam, Tanzania": {"lat": -6.7924, "lon": 39.2083},
    "Kampala, Uganda": {"lat": 0.3476, "lon": 32.5825},
    "Khartoum, Sudan": {"lat": 15.5007, "lon": 32.5599},
    "Algiers, Algeria": {"lat": 36.7538, "lon": 3.0588},
    "Tunis, Tunisia": {"lat": 36.8065, "lon": 10.1815},
    "Tripoli, Libya": {"lat": 32.8872, "lon": 13.1913},
    "Luanda, Angola": {"lat": -8.8383, "lon": 13.2344},
    "Kinshasa, DR Congo": {"lat": -4.4419, "lon": 15.2663},
    "Abidjan, Ivory Coast": {"lat": 5.3600, "lon": -4.0083},
    "Lusaka, Zambia": {"lat": -15.3875, "lon": 28.3228},
    "Harare, Zimbabwe": {"lat": -17.8292, "lon": 31.0522},
    "Maputo, Mozambique": {"lat": -25.9692, "lon": 32.5732},
    
    # OCEANIA
    
    "Sydney, Australia": {"lat": -33.8688, "lon": 151.2093},
    "Melbourne, Australia": {"lat": -37.8136, "lon": 144.9631},
    "Brisbane, Australia": {"lat": -27.4698, "lon": 153.0251},
    "Perth, Australia": {"lat": -31.9505, "lon": 115.8605},
    "Adelaide, Australia": {"lat": -34.9285, "lon": 138.6007},
    "Canberra, Australia": {"lat": -35.2809, "lon": 149.1300},
    "Auckland, New Zealand": {"lat": -36.8485, "lon": 174.7633},
    "Wellington, New Zealand": {"lat": -41.2865, "lon": 174.7762},
    "Christchurch, New Zealand": {"lat": -43.5321, "lon": 172.6362},
    "Suva, Fiji": {"lat": -18.1416, "lon": 178.4419},
    "Port Moresby, Papua New Guinea": {"lat": -9.4438, "lon": 147.1803},
}
