#global variables the program uses
background_label = None
bg_image = None
current_bg_path = None
'''
played:
1, 10, 50, 100
completed:
1, 10, 50, 100
wrote entries:
1, 10, 20, 50, 100
spin wheel x times
1, 10, 50, 100, 1000
use wheel x times without picking game
1, 5, 10, 20, 50, 100
complete x games without starting a new one in between
1, 10, 20, 50
complete a game within x days of starting it
1 (day), 7 (week), 30 (month)
change currently playing game X times in a day
1, 2, 5, 10, 20
add game with no image
1
'''
achiement_num = 37
achievements = [0] * achiement_num
num_played = 0
num_completed = 0
num_written = 0
num_spin = 0
#games completed without starting new in between
cur_no_game = 0
max_no_game = 0
#have we spun the wheel x times without picking a game?
cur_no_choose = 0
max_no_choose = 0
