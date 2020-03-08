import pandas as pd
import matplotlib.pyplot as plt

def one_dict(list_dict):
    keys=list_dict[0].keys()
    out_dict={key:[] for key in keys}
    for dict_ in list_dict:
        for key, value in dict_.items():
            out_dict[key].append(value)
    return out_dict 

dict_={'a':[11,21,31],'b':[12,22,32]}
print(dict_)
df = pd.DataFrame(dict_)
print(df)

from nba_api.stats.static import teams
import matplotlib.pyplot as plt

#https://pypi.org/project/nba-api/

nba_teams = teams.get_teams()
print(nba_teams[0:3])

dict_nba_team = one_dict(nba_teams)
df_teams = pd.DataFrame(dict_nba_team)
#print(df_teams.head())
#print(df_teams['full_name'].unique())

df_warriors = df_teams[df_teams['nickname']=='Warriors']
print(df_warriors)

from nba_api.stats.endpoints import leaguegamefinder

# Since https://stats.nba.com does lot allow api calls from Cloud IPs and Skills Network Labs uses a Cloud IP.
# The following code is comment out, you can run it on jupyter labs on your own computer.
# gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=id_warriors)

# Since https://stats.nba.com does lot allow api calls from Cloud IPs and Skills Network Labs uses a Cloud IP.
# The following code is comment out, you can run it on jupyter labs on your own computer.
# gamefinder.get_json()

# Since https://stats.nba.com does lot allow api calls from Cloud IPs and Skills Network Labs uses a Cloud IP.
# The following code is comment out, you can run it on jupyter labs on your own computer.
# games = gamefinder.get_data_frames()[0]
# games.head()

file_name = "Golden_State.pkl"
games = pd.read_pickle(file_name)
print(games.head())

games_home=games [games ['MATCHUP']=='GSW vs. TOR']
games_away=games [games ['MATCHUP']=='GSW @ TOR']

x = games_home.mean()['PLUS_MINUS']
y = games_away.mean()['PLUS_MINUS']

print(x,y)

fig, ax = plt.subplots()

games_away.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
games_home.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
ax.legend(["away", "home"])
plt.show()



