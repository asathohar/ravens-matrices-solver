class Agent:
    def __init__(self):
        pass

    def Solve(self,problem):
        #remove second condition before uploading to let test cases run here
        #if problem.hasVerbal and problem.problemSetName == "Basic Problems B":
        if problem.hasVerbal:
        
            print("**************************************************************")
            print(problem.name)

            atts = {
                'A': {
                    'huge': None,
                    'very large': None,
                    'large': None,
                    'medium': None,
                    'small': None,
                    'very small': None
                },
                'B': {
                    'huge': None,
                    'very large': None,
                    'large': None,
                    'medium': None,
                    'small': None,
                    'very small': None
                }
            }

            figureAObjects = problem.figures["A"].objects
            figureBObjects = problem.figures["B"].objects       
            
            # organize objects by size
            for obj in figureAObjects:
                size = figureAObjects[obj].attributes["size"]
                atts['A'][size] = figureAObjects[obj].attributes

            # organize objects by size
            for obj in figureBObjects:
                size = figureBObjects[obj].attributes["size"]
                atts['B'][size] = figureBObjects[obj].attributes

            transformations = {
                "huge": self.getTransformations(atts['A']['huge'], atts['B']['huge']),
                "very large": self.getTransformations(atts['A']['very large'], atts['B']['very large']),
                "large": self.getTransformations(atts['A']['large'], atts['B']['large']),
                "medium": self.getTransformations(atts['A']['medium'], atts['B']['medium']),
                "small": self.getTransformations(atts['A']['small'], atts['B']['small']),
                "very small": self.getTransformations(atts['A']['very small'], atts['B']['very small'])
            }

            expectedAtts = self.applyChanges(transformations, problem.figures["C"], atts)

            return self.findAnswer(expectedAtts, problem)
        else:
            return 4

    def getTransformations(self, A, B):
        
        if (A == None and B == None):
            return 'disregard'
        elif (A == None):
            angle = 'disregard'
            alignment = 'disregard'
            if 'angle' in B:
                angle = B['angle']
            if 'alignment' in B:
                alignment = B['alignment']
            return 'add ' + B['fill'] + ' ' + angle + ' ' + alignment + ' ' + B['shape']
        elif (B == None):
            return 'remove '
        else:
            A['inside'] = None
            A['above'] = None
            A['overlaps'] = None
            B['inside'] = None
            B['above'] = None
            B['overlaps'] = None
            if (A == B):
                return 'constant'
            else:
                return 'modify ' + self.compareFill(A, B) + ' ' + self.compareAngle(A, B) + ' ' + self.compareAlignment(A, B) + ' ' + self.compareShape(A, B)
        

    def compareFill(self, A, B):
        if (A["fill"] == B["fill"]):
            return 'constant'
        elif (A["fill"] == "yes" and B["fill"] == "no"):
            return 'unfill'
        elif (A["fill"] == "no" and B["fill"] == "yes"):
            return 'fill'
        else:
            return 'disregard'

    def compareAngle(self, A, B):
        if (not "angle" in A) or (not "angle" in B):
            return 'disregard'
        elif (A["angle"] == B["angle"]):
            return 'constant'
        else:
            return str(int(A["angle"]) - int(B["angle"]))

    def compareAlignment(self, A, B):
        if (not "alignment" in A) or (not "alignment" in B):
            return 'disregard'
        elif (A["alignment"] == B["alignment"]):
            return 'constant'
        else:
            alignA = A['alignment'].split('-')
            alignB = B['alignment'].split('-')
            operation = ''
            if (alignA[0] != alignB[0]):
                operation = operation + 'reflectY' + '-'
            else:
                operation = operation + 'keepY' + '-'
            if (alignA[1] != alignB[1]):
                operation = operation + 'reflectX'
            else:
                operation = operation + 'keepX'
            
            return operation
    
    def compareShape(self, A, B):
        if (not "shape" in A) or (not "shape" in B):
            return 'disregard'
        elif (A["shape"] == B["shape"]):
            print('A SHAPE B SHAPE CONSTANT?: ', A["shape"], B["shape"], 'YES')
            return 'constant'
        else:
            print('A SHAPE B SHAPE CONSTANT?: ', A["shape"], B["shape"], 'NO')
            return 'modify'
    
    #returns the correct answer's objects and attributes
    def applyChanges(self, transformations, figureC, atts):

        figureCObjects = figureC.objects
        cAtts = {
            'huge': None,
            'very large': None,
            'large': None,
            'medium': None,
            'small': None,
            'very small': None
        }
        for obj in figureCObjects:
            size = figureCObjects[obj].attributes["size"]
            cAtts[size] = figureCObjects[obj].attributes

        expectedAtts = {
            'huge': {},
            'very large': {},
            'large': {},
            'medium': {},
            'small': {},
            'very small': {}
        }
        
        for obj in transformations:
            tfs = transformations[obj].split()
            if (tfs[0] == "disregard"):
                expectedAtts[obj] = cAtts[obj]
            elif (tfs[0] == "add"):
                print('000000000000000000000000000000000000000000', tfs, obj)
                expectedAtts[obj]["fill"] = tfs[1]
                expectedAtts[obj]["shape"] = tfs[4]
                if 'angle' in expectedAtts[obj]:
                    expectedAtts[obj]['angle'] = tfs[2]
                if 'alignment' in expectedAtts[obj]:
                    expectedAtts[obj]['alignment'] = tfs[3]

                if (obj == 'medium'):
                    print(expectedAtts[obj])

            elif (tfs[0] == "remove"):
                expectedAtts[obj] = None
            elif (tfs[0] == "constant"):
                expectedAtts[obj] = cAtts[obj]
            else:
                if (tfs[1] == "fill"):
                    expectedAtts[obj]["fill"] = "yes"
                elif (tfs[1] == "unfill"):
                    expectedAtts[obj]["fill"] = "no"
                elif(tfs[1] == "constant"):
                    if ("fill" in cAtts[obj]):
                        expectedAtts[obj]["fill"] = cAtts[obj]["fill"]
                
                if (tfs[2] == "constant"):
                    expectedAtts[obj]["angle"] = cAtts[obj]["angle"]
                elif (tfs[2] != "disregard"):
                    angle = int(cAtts[obj]["angle"]) - int(tfs[2])
                    if (angle < 360):
                        expectedAtts[obj]["angle"] = str(angle)
                    else:
                        expectedAtts[obj]["angle"] = str(int(cAtts[obj]["angle"]) + int(tfs[2]))

                if (tfs[3] == "constant"):
                    if ('alignment' in cAtts[obj]):
                        expectedAtts[obj]["alignment"] = cAtts[obj]["alignment"]
                elif (tfs[3] == "disregard"):
                    pass
                else:
                    operations = tfs[3].split('-')
                    priorAlign = cAtts[obj]["alignment"].split('-')
                    if (operations[0] == 'keepY' and operations[1] == 'keepX'):
                        expectedAtts[obj]["alignment"] = cAtts[obj]["alignment"]
                    elif (operations[0] == 'keepY' and operations[1] != 'keepX'):
                        expectedAtts[obj]["alignment"] = priorAlign[0] + '-' + ('left' if priorAlign[1] == 'right' else 'right')
                    elif (operations[0] != 'keepY' and operations[1] == 'keepX'):
                        expectedAtts[obj]["alignment"] = ('top' if priorAlign[0] == 'bottom' else 'top') + '-' + priorAlign[1]
                    elif (operations[0] != 'keepY' and operations[1] != 'keepX'):
                        expectedAtts[obj]["alignment"] = ('top' if priorAlign[0] == 'bottom' else 'top') + '-' + ('left' if priorAlign[1] == 'right' else 'right')
                
                if (tfs[4] == "constant" or (tfs[4] == "disregard")):
                    expectedAtts[obj]["shape"] = cAtts[obj]["shape"]
                elif (tfs[4] == "modify"):
                    expectedAtts[obj]["shape"] = "square"

        return expectedAtts

    #returns the number of the correct answer
    def findAnswer(self, dAttributes, problem):
        answers = {
            "1": problem.figures['1'].objects,
            "2": problem.figures['2'].objects,
            "3": problem.figures['3'].objects,
            "4": problem.figures['4'].objects,
            "5": problem.figures['5'].objects,
            "6": problem.figures['6'].objects
        }

        answersAtts = {
            "1": {
                'huge': None,
                'very large': None,
                'large': None,
                'medium': None,
                'small': None,
                'very small': None
            },
            "2": {
                'huge': None,
                'very large': None,
                'large': None,
                'medium': None,
                'small': None,
                'very small': None
            },
            "3": {
                'huge': None,
                'very large': None,
                'large': None,
                'medium': None,
                'small': None,
                'very small': None
            },
            "4": {
                'huge': None,
                'very large': None,
                'large': None,
                'medium': None,
                'small': None,
                'very small': None
            },
            "5": {
                'huge': None,
                'very large': None,
                'large': None,
                'medium': None,
                'small': None,
                'very small': None
            },
            "6": {
                'huge': None,
                'very large': None,
                'large': None,
                'medium': None,
                'small': None,
                'very small': None
            }
        }
        
        isAnswer = False
        for answer in answers:
            objs = answers[answer]
            for obj in objs:
                size = objs[obj].attributes["size"]
                answersAtts[answer][size] = objs[obj].attributes

        isAnswer = False
        for answer in answers:
            #print(answersAtts[answer])
            for size in dAttributes:
                if (answersAtts[answer][size] != None):
                    answersAtts[answer][size].pop('inside', None)
                    answersAtts[answer][size].pop('above', None)
                    answersAtts[answer][size].pop('overlaps', None)
                    #answersAtts[answer][size].pop('alignment', None)
                if (dAttributes[size] != None):
                    dAttributes[size].pop('inside', None)
                    if (not 'size' in dAttributes[size]):
                        dAttributes[size]['size'] = size
                print('###Size: ', size)
                print('expected attributes: ', dAttributes[size])
                print('answer attributes: ', answersAtts[answer][size])
                if (dAttributes[size] == answersAtts[answer][size]):
                    isAnswer = True
                else:
                    isAnswer = False
                    break
            
            if (isAnswer):
                print('match found')
                return int(answer)
            else:
                print('not a match')
            print('\n')

        return -1