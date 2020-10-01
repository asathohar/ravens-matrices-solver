import os
import sys
import csv

from Agent import Agent
from ProblemSet import ProblemSet
from RavensGrader import grade

def getNextLine(r):
    return r.readline().rstrip()


def solve():
    sets=[] # The variable 'sets' stores multiple problem sets.
            # Each problem set comes from a different folder in /Problems/.

    r = open(os.path.join("Problems","ProblemSetList.txt"))    # ProblemSetList.txt lists the sets to solve.
    line = getNextLine(r)                                   
    while not line=="":                                     
        sets.append(ProblemSet(line))                      
        line=getNextLine(r)                                 

    agent=Agent()

    # Running agent against each problem set
    with open("AgentAnswers.csv","w") as results:
        results.write("ProblemSet,RavensProblem,Agent's Answer\n")
        for set in sets:
            for problem in set.problems:
                answer = agent.Solve(problem)

                results.write("%s,%s,%d\n" % (set.name, problem.name, answer))
    r.close()

def main():
    solve()
    grade()

if __name__ == "__main__":
    main()
