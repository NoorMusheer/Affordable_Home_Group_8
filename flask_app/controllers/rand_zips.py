import random

zip_codes =  [64036, 42349, 80046, 28138, 30260, 46312, 99124, 43219, 27909, 47865, 57752, 45672, 23412, 89705, 94538, 37229, 12584, 79401, 90039, 80206, 12257, 42762, 81046, 98837, 33981, 55110, 23952, 48381, 53003, 33127, 75372, 40618, 95894, 67762, 58779, 20233, 16410, 11715, 59074, 28105, 15676, 95836, 28166, 41093, 28232, 30306, 93950, 41001, 72583, 58735, 27377, 87323, 40285, 98577, 34293, 38066, 43333, 24993, 30276, 15865, 57629, 73301, 94938, 84656, 27106, 14683, 76856, 19074, 92376, 38391, 49017, 10011, 37219, 72031, 58278, 97914, 20011, 72802, 56340, 97042, 43347, 12967, 90012, 73045, 94945, 66416, 58795, 62035, 40160, 97731, 76028, 65250, 60974, 38668, 36135, 32607, 21201, 44809, 30439, 96121]

def get_random_zip():
    rndm_zip = random.choice(zip_codes)
    return rndm_zip

# print (get_random_zip(zip_codes))