import pickle
from refresh_data import Game

if __name__=="__main__":
	with open("games.pkl","rb") as f:
		games = pickle.load(f)
	for game_class in games:
        	score = 0
        	if 'Great_comeback' in pref_dict:
                	score += int(pref_dict['Great comeback']) * game_class.comeback

