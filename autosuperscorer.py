from operator import itemgetter
import sys
import getopt
def main(argv):
    try:
        o, a = getopt.getopt(argv,"i:d:")
    except getopt.GetoptError:
        print ('Usage: test.py -i <inputfile> -d <drops>')
        sys.exit(0)
    if len(o)!=2:
        print ('Usage: test.py -i <inputfile> -d <drops>')
        sys.exit(0)
    for o1, a1 in o:
        if o1 in ("-i"):
            inp = a1
        elif o1 in ("-d"):
            drops = int(a1)
    file = open(inp,"r")
    events = file.readline().strip().split("\t")
    results = file.read().strip().split("\n")
    for i in range(0,len(results)):
        results[i]=results[i].strip().split("\t")
    print("If there are any trials, write the names of them separated by a comma. Else, just write 'No'.")
    trials = input(": ").replace(", ",",").split(",")
    if trials[0]!="No":
        for e in trials:
            temp = False
            if e not in events:
                print(e+" was not found in the list of events.")
                temp = True
            if temp:
                sys.exit(0)
    else:
        trials=[]
    teams = {}
    for team in results:
        if team[0].split(",")[0] not in teams:
            teams[team[0].split(",")[0]]=[team]
        else:
            teams[team[0].split(",")[0]].append(team)
    trialIndex = []
    for e in trials:
        trialIndex.append(events.index(e))
    for school in teams:
        super = [school,0,0]
        for event in range(3,len(events)):
            if event not in trialIndex:
                temp = []
                for team in teams[school]:
                    temp.append(int(team[event]))
                super.append(min(temp))
        super[2]=sum(super[3:])
        teams[school]=super
    scores = []
    for school in teams:
        scores.append(teams[school][2])
    scores.sort()
    results = []
    for school in teams:
        teams[school][1]=scores.index(teams[school][2])+1
        results.append(teams[school])
    for j in range(len(results)):
        for i in range(drops):
            results[j][2]-=sorted(results[j][3:])[len(results[j])-i-4]
    results = sorted(results,key=itemgetter(1))
    out = ""
    for team in results:
        out+="\t".join(str(e) for e in team)+"\n"
    file2 = open(inp.split(".")[0]+"OUT"+"."+inp.split(".")[1],"w")
    file2.write(out)
    file2.close()
if __name__ == "__main__":
    main(sys.argv[1:])