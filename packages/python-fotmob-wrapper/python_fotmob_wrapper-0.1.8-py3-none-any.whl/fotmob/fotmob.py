import requests,re,json
from datetime import datetime

website = "https://www.fotmob.com/"
DEFAULT_MAX_RETURN=5

class Match(object):
    matchID = 0
    homeTeam = ""
    awayTeam = ""
    date = ""
    ko_time = ""
    result = ""
    content = {}

    def __init__(self,matchID,homeTeam,awayTeam,date,ko_time,result,content):
        self.matchID = matchID
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.date = date 
        self.ko_time = ko_time
        self.result = result
        self.content = content

    def getMatchID(self):
        return self.matchID

    def getDate(self):
        return self.date.strftime('%b %d, %Y')

    def getKickOff(self):
        return self.ko_time

    def getHomeTeam(self):
        return self.homeTeam

    def getAwayTeam(self):
        return self.awayTeam

    def getResult(self):
        return self.result
    
    def getContent(self):
        return self.content

def getLeague(comp: int, page: str="overview", league: str="league", timezone: str="America/New_York", matchDate: str=None) -> list:
    """
    Return the overview page for a league or cup competition

    :param comp:
    :param page:
    :param timezone:
    :return: A list of all the matches in the competition
    """
    url = website+"leagues?id="+str(comp)+"&tab="+page+"&type="+league+"&timeZone="+timezone
    matches_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    fixtures = json.loads(matches_html)['fixtures']
    matches = []
    #for match in matches_table:
    for match in fixtures:
        matchID = match['id']
        homeTeam,awayTeam = match['home']['name'],match['away']['name']
        if match['notStarted']:
            try:
                ko_time = match['status']['startTimeStr']
                result = ""
            except KeyError:
                ko_time = "In Progress"
                result = match['status']['scoreStr']
        else:
            result = match['status']['scoreStr']
            ko_time = ""
        try:
            date = datetime.strptime(match['status']['startDateStr'],"%d %B %Y")
        except ValueError:
            date = datetime.strptime(match['status']['startDateStrShort'],"%d. %b.")
            date = date.replace(year=int(datetime.today().strftime('%Y')))
        except KeyError:
            date = datetime.today()
        if matchDate is not None:
            if date.strftime('%Y%m%d') < matchDate:
                continue
            elif date.strftime('%Y%m%d') > matchDate:
                return matches
        match = Match(matchID,homeTeam,awayTeam,date,ko_time,result,"")
        matches.append(match)
    return matches

def getTeamID(teamName: str) -> str:
    url = website+"searchData?term="+teamName
    search_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    search_results = json.loads(search_html)['teams']['dataset']
    for team in search_results:
        if team['name'] == teamName:
            return team['id']
    return 0


def printMatch(m):
    output = m.matchID +" " + m.date.strftime('%b %d, %Y') + " "
    if m.ko_time:
        output += m.ko_time + " "
    output += m.homeTeam
    if m.result:
        output += " " + m.result + " "
    else:
        output += " v "
    output += m.awayTeam
    return output

def printAllMatches(day):
    for key,matches in day.items():
        print(key)
        for match in matches:
            print(printMatch(match))


def getMatch(matchID: str) -> Match:
    """
    Return the info for a specific match

    :param matchID: Fotmob Match ID
    return Match: a Match object with relevant info
    """
    url = website+"matchDetails?matchId="+matchID
    match_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    match = json.loads(match_html)['header']
    content = json.loads(match_html)['content']
    matchID = matchID
    homeTeam,awayTeam = match['teams'][0]['name'],match['teams'][1]['name']
    if not match['status']['started']:
        ko_time = match['status']['startTimeStr']
        result = ""
    else:
        result = match['status']['scoreStr']
        ko_time = ""
    date = datetime.strptime(match['status']['startDateStr'],'%b %d, %Y')
    match = Match(matchID,homeTeam,awayTeam,date,ko_time,result,content)
    return match

def getMatchesByDate(date: str) -> dict:
    """
    Return all the matches being played on a specific date
    
    :param date: A date string in format YYYYMMDD
    return matches: A list of match objects
    """
    url = website+"matches?date="+date
    match_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    matches_json = json.loads(match_html)
    fixtures = matches_json['leagues']
    leagues = {}
    for league in fixtures: 
        leagueName,leagueID = league['ccode'],league['id']
        #matches_table = re.split(r'"primaryId"',league)[1:]
        matches_table = league['matches']
        matches = []
        for match in matches_table:
            matchID = match['id']
            homeTeam,awayTeam = match['home']['name'],match['away']['name']
            if not match['status']['started']:
                ko_time = match['status']['startTimeStr']
                result = ""
            else:
                result = match['status']['scoreStr']
                ko_time = ""
            date = datetime.today().strftime("%b %d, %Y")
            match = Match(matchID,homeTeam,awayTeam,date,ko_time,result,"")
            matches.append(match)
        leagues[leagueName] = matches
    return leagues 

def getHeadToHead(team1: str, team2: str, numResults: str=str(DEFAULT_MAX_RETURN)):
    if numResults.lower() == 'any':
        numResults = '99'
    url = website+"searchData?term=" + team1 + "-" + team2
    search_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    search_results = json.loads(search_html)['matches']['dataset']
    search_results = list(search_results.values())[0][0]
    matchId = search_results['pageUrl'].split('/')[2]
    match = getMatch(matchId)
    h2h = match.getContent()['h2h']['matches']
    while h2h[0]['status']['started'] == False:
        match = getMatch(h2h[0]['matchUrl'].split('/')[2])
        h2h = match.getContent()['h2h']['matches']
    matches = []
    for match in h2h:
        matchID = match['matchUrl'].split('/')[2]
        homeTeam,awayTeam = match['home']['name'],match['away']['name']
        result = match['status']['scoreStr']
        ko_time = ""
        date = datetime.strptime(match['status']['startDateStr'],'%b %d, %Y')
        match = Match(matchID,homeTeam,awayTeam,date,ko_time,result,"")
        matches.append(match)
        if len(matches) >= int(numResults):
            return matches
    return matches




if __name__ == '__main__':
    quit()
