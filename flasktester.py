import sqlite3
from flask import g, Flask
import json

app = Flask(__name__)

html = """<!DOCTYPE html>
<html>
<meta charset="utf-8">
<head>
<title>
    MMR Vis
</title>
</head>
<style>

.chart rect {{
  fill: steelblue;
}}

.chart text {{
  fill: white;
  font: 10px sans-serif;
  text-anchor: middle;
}}

</style>
<div id="teamName"></div>
<svg class="chart"></svg>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.16/d3.min.js" charset="utf-8"></script>
<script>
var width = 960,
    height = 500;

var y = d3.scale.linear()
    .range([height / 2, 0]);

var chart = d3.select(".chart")
    .attr("width", width)
    .attr("height", height);

d3.json('/bball/{teamId}/{seasonLetter}', function(error, data) {{
  document.getElementById('teamName').innerHTML = data.teamName;
  data = data.data.map(function(d) {{
      return d[1] == {teamId} ? d[2] - d[4] : d[4] - d[2];
  }});

  y.domain([0, d3.max(data, function(d) {{ return d; }})]);

  var barWidth = width / data.length;

  var bar = chart.selectAll("g")
      .data(data)
    .enter().append("g")
      .attr("transform", function(d, i) {{ return "translate(" + i * barWidth + ",0)"; }});

  bar.append("rect")
      .attr("y", function(d) {{ return Math.min(height/2, y(d)); }})
      .attr("height", function(d) {{ return Math.abs(height / 2 - y(d)); }})
      .attr("width", barWidth - 1);

  bar.append("text")
      .attr("x", barWidth / 2)
      .attr("y", function(d) {{ return Math.min(height/2, y(d)) + 3; }})
      .attr("dy", ".75em")
      .text(function(d) {{ return d; }});
}});

</script>
</html>"""

@app.route("/hello")
def hello():
    return "Hello World!"

DATABASE = 'MMR'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/bball/<teamid>/<season>')
def bball(teamid, season):
    print "got to bball!"
    cur = get_db().cursor()
    cur.execute('SELECT season, wteam, wscore, lteam, lscore FROM regseasonresults WHERE (wteam = ' + teamid + ' or lteam = ' + teamid + ') and season ="' + season + '"')
    arr = cur.fetchall()
    cur.execute('SELECT name FROM teams WHERE id = ' + teamid)
    teamName = cur.fetchall()
    print arr
    print teamName
    return json.dumps({"data":arr, "teamName":teamName})

@app.route('/tourney/<teamid>/<season>')
def tourney(teamid, season):
    cur = get_db().cursor()
    cur.execute('SELECT seed FROM tourneyseeds WHERE (team = ' + teamid + ') and season ="' + season + '"')
    seeding = cur.fetchall()
    print seeding
    return json.dumps({"seeding":seeding, "season":season})

@app.route('/location/<region>/<season>')
def location(region, season):
    cur = get_db().cursor()
    cur.execute('SELECT ' + region + ' FROM seasons WHERE (season = "' + season + '")')
    location = cur.fetchall()
    print location
    return json.dumps({"location": location})

@app.route('/opponent/<teamid>/<season>')
def opponent(teamid, season):
    cur = get_db().cursor()
    cur.execute('SELECT wteam, wscore, lteam, lscore FROM tourneyresults WHERE (wteam = ' + teamid + ' or lteam = ' + teamid + ') and season ="' + season + '"')
    opponentStuff = cur.fetchall()
    print opponentStuff
    return json.dumps({"opponentStuff": opponentStuff})

@app.route('/teams')
def teams():
    cur = get_db().cursor()
    cur.execute('SELECT * from teams')
    teams = cur.fetchall()
    return json.dumps({"teams": teams})

@app.route('/seasons')
def season():
    cur = get_db().cursor()
    cur.execute('SELECT season, years FROM seasons')
    seasons = cur.fetchall()
    return json.dumps({"seasons": seasons})

@app.route('/graph/<teamid>/<season>')
def root(teamid, season):
    format = {
        "teamId": teamid,
        "seasonLetter": season
    }
    returnString = html.format(**format)
    return returnString

@app.route('/vis/<years>/<state>')
def vis(years, state):
    cur = get_db().cursor()
    #stateTeam = cur.execute('select * from teams where name =' + state + '')
    cur.execute('select regseasonresults.* from regseasonresults, teams, seasons where (regseasonresults.wteam = teams.id or regseasonresults.lteam = teams.id) and regseasonresults.season = seasons.season and teams.name = "' + state + '" and seasons.years ="' + years + '"')
    arr = cur.fetchall()
    return json.dumps({"data":arr})

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
#http://localhost:8080/graph/teamId/seasonLetter
