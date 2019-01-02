# Takes a CSV of a spreadsheet of recorded games and consolidates it into
# readable data
#
# Line o1 of the spreadsheet should be the Category titles with each consecutive
# line should contain the data for each game
#
# The code here is customized to the format of my particular sheet but changing
# some key variables should get it to work pretty easily with a different
# customization

from prettytable import PrettyTable

RANKS = {'B4': 1, 'B3': 2, 'B2': 3, 'B1': 4,
		 'S4': 5, 'S3': 6, 'S2': 7, 'S1': 8,
		 'G4': 9, 'G3': 10, 'G2': 11, 'G1': 12,
		 'P4': 13, 'P3': 14, 'P2': 15, 'P1': 16,
		 'D4': 17, 'D3': 18, 'D2': 19, 'D1': 20,
		 'M': 21}
TOTAL_GAMES = 336
TOTAL_WINS = 201
TOTAL_LOSSES = 135
WIN_PCT = TOTAL_WINS/(TOTAL_WINS+TOTAL_LOSSES)
NUM_CATEGORIES = 13
WIN_STREAK = 0
LOSE_STREAK = 0
PLAY_STREAK = 0
DRAW_STREAK = 0

b_pe, b_pu, b_pd = 0, 0, 0
s_pe, s_pu, s_pd = 0, 0, 0
g_pe, g_pu, g_pd = 0, 0, 0
p_pe, p_pu, p_pd = 0, 0, 0
d_pe, d_pu, d_pd = 0, 0, 0
b_games, b_wins, b_losses = 0, 0, 0
s_games, s_wins, s_losses = 0, 0, 0
g_games, g_wins, g_losses = 0, 0, 0
p_games, p_wins, p_losses = 0, 0, 0
d_games, d_wins, d_losses = 0, 0, 0
flood_w, flood_l = 0, 0
screw_w, screw_l = 0, 0
normal_w, normal_l = 0, 0
frenzy_w, frenzy_l = 0, 0
play_w, play_l = 0, 0
draw_w, draw_l = 0, 0
mull_w, mull_l = 0, 0
mull_opw, mull_opl = 0, 0

# Additional requested metrics
frenzy_l6, frenzy_w6 = 0, 0
flood_w6, flood_l6, screw_w6, screw_l6, normal_w6, normal_l6 = 0, 0, 0, 0, 0, 0

deck_table = PrettyTable()
deck_table.field_names = ['Deck', 'Matches', 'Wins', 'Losses', 'Win %',
						  'Play Wins', 'Play Losses', 'Play Win %',
						  'Draw Wins', 'Draw Losses', 'Draw Win %']
rank_table = PrettyTable()
rank_table.field_names = ['Rank', 'Paired Evenly', 'Paired Up', 'Paired Down',
						  'Wins', 'Losses', 'Win %', 'Games to Next Rank']
misc_table = PrettyTable()
misc_table.field_names = ['Scenario', 'Games', 'Wins', 'Losses', 'Win %',
						  '% of Matches']


f = 'Road to Mythic RDW - Standard.csv'
csv = open(f, 'r').read().split('\n')

categories = csv[0].split(',')[0:NUM_CATEGORIES]

# Remove the categories line of the csv
del csv[0]

# Get the indices of each item that is not a game
indices = []
for i in range(0, len(csv)):
	if len(csv[i].split(',')) < NUM_CATEGORIES:
		indices.append(i)

# Remove the items that
indices.reverse()
for i in indices:
	del csv[i]

# Break down the decks and data about each game
matches = dict()
decklists = set()
d_streak = 0
l_streak = 0
p_streak = 0
w_streak = 0

for i in range(0, len(csv)):
	match = 'game%s' % (i+1)
	data = csv[i].split(',')
	match_data = dict()
	for j in range(0, NUM_CATEGORIES):
		matches[match] = dict()
		match_data[categories[j]] = data[j]

	r = match_data['Rank/New Rank']
	# Begin gathering useful data
	if match_data['Result'] == 'W':
		w_streak += 1
		l_streak = 0
		# Get win streak data
		if w_streak > WIN_STREAK:
			WIN_STREAK = w_streak
		# Get games data where Frenzy was played
		if 'Frenzy' in match_data['Notes']:
			frenzy_w += 1
			if float(match_data['Starting Hand']) < 7:
				frenzy_w6 += 1
		# Get data when on the play
		if match_data['Play/Draw'] == 'Play':
			play_w += 1
		else:
			draw_w += 1
		# Get win/land relationship data
		if float(match_data['Land %']) > .42:
			flood_w += 1
			if float(match_data['Starting Hand']) < 7:
				flood_w6 += 1
		elif float(match_data['Land %']) < .27:
			screw_w += 1
			if float(match_data['Starting Hand']) < 7:
				screw_w6 += 1
		else:
			normal_w += 1
			if float(match_data['Starting Hand']) < 7:
				normal_w6 += 1
		# Get mulligan data
		if float(match_data['Starting Hand']) < 7:
			mull_w += 1
		if float(match_data['Opponent Hand']) < 7:
			mull_opw += 1
		# Get data related to rank
		if r.startswith('B'):
			b_wins += 1
			b_games += 1
		if r.startswith('S'):
			s_wins += 1
			s_games += 1
		if r.startswith('G'):
			g_wins += 1
			g_games += 1
		if r.startswith('P'):
			p_wins += 1
			p_games += 1
		if r.startswith('D'):
			d_wins += 1
			d_games += 1
	else:
		l_streak += 1
		w_streak = 0
		if l_streak > LOSE_STREAK:
			LOSE_STREAK = l_streak
		if 'Frenzy' in match_data['Notes']:
			frenzy_l += 1
			if float(match_data['Starting Hand']) < 7:
				frenzy_l6 += 1
		if match_data['Play/Draw'] == 'Play':
			play_l += 1
		else:
			draw_l += 1
		if float(match_data['Land %']) > .42:
			flood_l += 1
			if float(match_data['Starting Hand']) < 7:
				flood_l6 += 1
		elif float(match_data['Land %']) < .27:
			screw_l += 1
			if float(match_data['Starting Hand']) < 7:
				screw_l6 += 1
		else:
			normal_l += 1
			if float(match_data['Starting Hand']) < 7:
				normal_l6 += 1
		if float(match_data['Starting Hand']) < 7:
			mull_l += 1
		if float(match_data['Opponent Hand']) < 7:
			mull_opl += 1
		if r.startswith('B'):
			b_losses += 1
			b_games += 1
		if r.startswith('S'):
			s_losses += 1
			s_games += 1
		if r.startswith('G'):
			g_losses += 1
			g_games += 1
		if r.startswith('P'):
			p_losses += 1
			p_games += 1
		if r.startswith('D'):
			d_losses += 1
			d_games += 1

	rv = RANKS[r[0:2]]
	op_r = RANKS[match_data['Opponent Rank']]
	if r.startswith('B'):
		if rv > op_r:
			b_pd += 1
		if rv < op_r:
			b_pu += 1
		if rv == op_r:
			b_pe += 1
	if r.startswith('S'):
		if rv > op_r:
			s_pd += 1
		if rv < op_r:
			s_pu += 1
		if rv == op_r:
			s_pe += 1
	if r.startswith('G'):
		if rv > op_r:
			g_pd += 1
		if rv < op_r:
			g_pu += 1
		if rv == op_r:
			g_pe += 1
	if r.startswith('P'):
		if rv > op_r:
			p_pd += 1
		if rv < op_r:
			p_pu += 1
		if rv == op_r:
			p_pe += 1
	if r.startswith('D'):
		if rv > op_r:
			d_pd += 1
		if rv < op_r:
			d_pu += 1
		if rv == op_r:
			d_pe += 1

	# Get info on play/draw streaks
	if match_data['Play/Draw'] == 'Play':
		p_streak += 1
		d_streak = 0
		if p_streak > PLAY_STREAK:
			PLAY_STREAK = p_streak
	else:
		d_streak += 1
		p_streak = 0
		if d_streak > DRAW_STREAK:
			DRAW_STREAK = d_streak

	decklists.add(match_data['Deck'])
	matches[match] = match_data

# Alphabetize the decklists
dl = list(decklists)
dl.sort()

decks = {}
for i in matches:
	if not decks.get(matches[i]['Deck']):
		decks[matches[i]['Deck']] = {'wins': 0,
									 'losses': 0,
									 'matches': 1,
									 'play_wins': 0,
									 'play_losses': 0,
									 'pwin_pct': 0,
									 'draw_wins': 0,
									 'draw_losses': 0,
									 'dwin_pct': 0}
	else:
		decks[matches[i]['Deck']]['matches'] += 1
	if matches[i]['Result'] == 'W':
		decks[matches[i]['Deck']]['wins'] += 1
		if matches[i]['Play/Draw'] == 'Play':
			decks[matches[i]['Deck']]['play_wins'] += 1
		else:
			decks[matches[i]['Deck']]['draw_wins'] += 1
	else:
		decks[matches[i]['Deck']]['losses'] += 1
		if matches[i]['Play/Draw'] == 'Play':
			decks[matches[i]['Deck']]['play_losses'] += 1
		else:
			decks[matches[i]['Deck']]['draw_losses'] += 1

for i in decks:
	if decks[i]['play_wins'] + decks[i]['play_losses'] > 0:
		decks[i]['pwin_pct'] = round(100*decks[i]['play_wins']/
						 			 (decks[i]['play_wins']+
						 			 	decks[i]['play_losses']), 2)
	else:
		decks[i]['pwin_pct'] = '-'
	if decks[i]['draw_wins'] + decks[i]['draw_losses'] > 0:
		decks[i]['dwin_pct'] = round(100*decks[i]['draw_wins']/
						 			 (decks[i]['draw_wins']+
						 			 	decks[i]['draw_losses']), 2)
	else:
		decks[i]['dwin_pct'] = '-'
print('Games Played: %(g)s\t\tWins: %(w)s\t\tLosses: %(l)s\t\tWin %%: '
	  '%(p)s' % dict(g=TOTAL_GAMES, w=TOTAL_WINS, l=TOTAL_LOSSES, p=WIN_PCT))
print('Longest Win Streak: %(win)s\t\tLongest Losing Streak: %(lose)s'
	  % dict(win=WIN_STREAK, lose=LOSE_STREAK))
print('Longest Play Streak: %(play)s\t\tLongest Draw Streak: %(draw)s\n'
	  % dict(play=PLAY_STREAK, draw=DRAW_STREAK))

print('Rank Specific Data:')
rank_table.add_row(['Bronze', b_pe, b_pu, b_pd, b_wins, b_losses,
					round(100*b_wins/(b_wins+b_losses), 2), b_wins+b_losses])
rank_table.add_row(['Silver', s_pe, s_pu, s_pd, s_wins, s_losses,
					round(100*s_wins/(s_wins+s_losses), 2), s_wins+s_losses])
rank_table.add_row(['Gold', g_pe, g_pu, g_pd, g_wins, g_losses,
					round(100*g_wins/(g_wins+g_losses), 2), g_wins+g_losses])
rank_table.add_row(['Platinum', p_pe, p_pu, p_pd, p_wins, p_losses,
					round(100*p_wins/(p_wins+p_losses), 2), p_wins+p_losses])
rank_table.add_row(['Diamond', d_pe, d_pu, d_pd, d_wins, d_losses,
					round(100*d_wins/(d_wins+d_losses), 2), d_wins+d_losses])
print('%s\n' % rank_table)

print('Meta Breakdown:')
for d in dl:
	deck_table.add_row([d, decks[d]['matches'], decks[d]['wins'],
		  	       		decks[d]['losses'],
		  	       		round((100*decks[d]['wins']/decks[d]['matches']), 2),
		  	       		decks[d]['play_wins'], decks[d]['play_losses'],
		  	       		decks[d]['pwin_pct'], decks[d]['draw_wins'],
		  	       		decks[d]['draw_losses'], decks[d]['dwin_pct']])
print('%s\n' % deck_table)

print('Miscelaneous Data:')
misc_table.add_row(['Mana Flood', flood_w+flood_l, flood_w, flood_l,
				    round(100*flood_w/(flood_w+flood_l), 2),
				    round(100*(flood_w+flood_l)/TOTAL_GAMES, 2)])
misc_table.add_row(['Mana Screw', screw_w+screw_l, screw_w, screw_l,
				    round(100*screw_w/(screw_w+screw_l), 2),
				    round(100*(screw_w+screw_l)/TOTAL_GAMES, 2)])
misc_table.add_row(['Normal Lands', normal_w+normal_l, normal_w, normal_l,
				    round(100*normal_w/(normal_w+normal_l), 2),
				    round(100*(normal_w+normal_l)/TOTAL_GAMES, 2)])
misc_table.add_row(['Mulligan', mull_w+mull_l, mull_w, mull_l,
				    round(100*mull_w/(mull_w+mull_l), 2),
				    round(100*(mull_w+mull_l)/TOTAL_GAMES, 2)])
misc_table.add_row(['Opponent Mulligan', mull_opw+mull_opl,
					mull_opw, mull_opl,
				    round(100*mull_opw/(mull_opw+mull_opl), 2),
				    round(100*(mull_opw+mull_opl)/TOTAL_GAMES, 2)])
misc_table.add_row(['Experimental Frenzy', frenzy_w+frenzy_l,
					frenzy_w, frenzy_l,
				    round(100*frenzy_w/(frenzy_w+frenzy_l), 2),
				    round(100*(frenzy_w+frenzy_l)/TOTAL_GAMES, 2)])
print('%s\n' % misc_table)

# Additional requested table
additional_table = PrettyTable()
additional_table.field_names = ['Scenario', 'Games', 'Wins', 'Losses', 'Win %',
							    '% of Matches']
additional_table.add_row(['Mana Flood', flood_w6+flood_l6, flood_w6, flood_l6,
				    	  round(100*flood_w6/(flood_w6+flood_l6), 2),
				    	  round(100*(flood_w6+flood_l6)/TOTAL_GAMES, 2)])
additional_table.add_row(['Mana Screw', screw_w6+screw_l6, screw_w6, screw_l6,
					      round(100*screw_w6/(screw_w6+screw_l6), 2),
					      round(100*(screw_w6+screw_l6)/TOTAL_GAMES, 2)])
additional_table.add_row(['Normal Lands', normal_w6+normal_l6, normal_w6,
						  normal_l6,
						  round(100*normal_w6/(normal_w6+normal_l6), 2),
				    	  round(100*(normal_w6+normal_l6)/TOTAL_GAMES, 2)])
additional_table.add_row(['Experimental Frenzy', frenzy_w6+frenzy_l6,
						  frenzy_w6, frenzy_l6,
				    	  round(100*frenzy_w6/(frenzy_w6+frenzy_l6), 2),
				    	  round(100*(frenzy_w6+frenzy_l6)/TOTAL_GAMES, 2)])
print('%s\n' % additional_table)				    


