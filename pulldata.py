import sqlite3
sqlite_file = 'MMR'
conn = sqlite3.connect(sqlite_file)
conn.text_factory = str
c = conn.cursor()
#c.execute('SELECT * FROM teams')
#all_rows = c.fetchall()
#for e in all_rows:
#    print(e[1])
#    print "\n"
c.execute('SELECT season, wteam, wscore, lteam, lscore FROM regseasonresults WHERE (wteam = 606 or lteam = 606) and season = "A"')
arr = c.fetchall()
teamList = ["season","wteam","wscore","lteam","lscore", "wteamName", "lteamName"]
teamNames = []
for entry in arr:
    print("\n")
    for i in xrange(1,4,2):
        c.execute('SELECT name FROM teams WHERE id=?',(entry[i],))
        temp = str(c.fetchall()[0][0])
        entry = entry + (temp,)
    for index,e in enumerate(entry):
        print(teamList[index] + ": " + e)
#for e in order:
#    teamid = e[2]
#    c.execute('SELECT name FROM teams WHERE id=?', (teamid,))
#    teamName = c.fetchall()
#    print("Regular Season Results for ")
#    print(teamName)
#    print "\n"
#teamid = arr[0][2]
#c.execute('SELECT name FROM teams WHERE id=?', (teamid,))
#teamName = c.fetchall()
#teamName = str(teamName)
#teamName = teamName[3:15]
#print("Regular Season Results for ")
#print(teamName[0][0])
#print "\n"
c.close()
