# a new model definition where it is essentially a wrapper
# for a set of reactions

from .reactions.Reactions import Reactions

class Model: 

    def __init__(self, modelName = "None"):

        self.reactions = []
        self.modelName = modelName

        # structure: "specieName": "initial concentration"
        self.activators = []
        self.specieFamily = {}
        self.species = {}

    def setModelName(self, name):

        self.modelName = name

    def updateSpecies(self):

        # checks every reaction within the model
        # a O(N) update

        i = 0 
        while i < len(self.reactions):
            re = self.reactions[i]
            for fs in re.fs:
                if fs not in self.species and fs != 'None' and fs != None:
                    self.species[fs] = 100
            
            for bs in re.bs:
                if bs not in self.species and bs != 'None' and bs != None:
                    self.species[bs] = 100
            i += 1

    def specieConc(self, specieNames: list, conc: list):

        assert len(specieNames) == len(conc)

        i = 0 
        while i < len(specieNames):
            s = specieNames[i]
            self.species[s] = conc[i]
            i += 1

    def addReaction(self, reaction: Reactions):

        self.reactions.append(reaction)
        self.updateSpecies()

    def addActivation(self, activator: str, conc: float, activationTime: float):

        self.activators.append((activator, conc, activationTime))

    def generateTxtbc(self):
        
        txtbc = open("{filename}.txtbc".format(filename=self.modelName), "w")

        ### HEADER

        txtbc.write("********** MODEL NAME\n")
        txtbc.write(self.modelName + "\n")
        txtbc.write("\n")
        txtbc.write("********** MODEL NOTES\n")
        txtbc.write("\n")

        ### Model state information

        txtbc.write("********** MODEL STATE INFORMATION\n")
        txtbc.write("% Initial Conditions\n")
        txtbc.write("\n")

        species = self.species.keys()
        for s in species:
            txtbc.write("{specie}(0) = {conc}\n".format(specie = s, conc = self.species[s]))
        txtbc.write("\n")

        
        # NOTE: deprecated code below, have not deleted for possible later reference

        # families = self.specieFamily.keys()
        # families = list(families)

        # for fam in families:
        #     for member in self.specieFamily[fam]: 
        #         txtbc.write("{specie}(0) = {conc}\n".format(specie = member, conc = self.species[member]))
        #     txtbc.write("\n")


        ### Model parameters

        txtbc.write("********** MODEL PARAMETERS\n")

        i = 0 
        while i < len(self.reactions):
            re = self.reactions[i]
            id_ = i + 1
            re_params = re.getParams(id_)
            names = re_params.keys()
            for n in names:
                toStr = n + " = " + str(re_params[n]) + "\n"
                txtbc.write(toStr)
            
            txtbc.write("\n")
            i += 1

        txtbc.write("% Constants\n")
        txtbc.write("\n")

        txtbc.write("% Stimulation Concentration\n")
        for a in self.activators:
            txtbc.write("{s} = {v}\n".format(s=a[0], v=a[1]))
        txtbc.write("\n")

        txtbc.write("% Drug Concentration\n")
        txtbc.write("\n")

        txtbc.write("% Time Variables\n")
        for a in self.activators:
            txtbc.write("{s}_on = {time}\n".format(s=a[0], time=a[2]))
        txtbc.write("\n")

        ### Model variables

        txtbc.write("********** MODEL VARIABLES\n")
        txtbc.write("\n")

        # NOTE: deprecated code below, have not deleted for possible later reference

        # for fam in families:

        #     totalStr = "{familyName}_Total = ".format(familyName=fam)
        #     for member in self.specieFamily[fam]: 
        #         totalStr = totalStr + member + " + "

        #     totalStr = totalStr[:-3]
        #     txtbc.write(totalStr)
        #     txtbc.write("\n")

        txtbc.write("\n")
        for a in self.activators:
            txtbc.write("{s}0 = {s}*piecewiseIQM(1,ge(time,{s}_on),0)\n".format(s=a[0]))

        ### Model reactions

        txtbc.write("********** MODEL REACTIONS\n")

        i = 0 
        while i < len(self.reactions):
            re = self.reactions[i]
            id_ = i + 1

            txtbc.write(re.getEqHeaderStr(id_))
            txtbc.write("\n")
            if re.getForwardEqStr(id_) is not None:
                txtbc.write("\tvf = " + re.getForwardEqStr(id_))
                txtbc.write("\n")
            if re.getBackwardEqStr(id_) is not None:
                txtbc.write("\tvr = " + re.getBackwardEqStr(id_))
                txtbc.write("\n")
            
            txtbc.write("\n")
            i += 1

        txtbc.write("********** MODEL FUNCTIONS")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")

        txtbc.write("********** MODEL EVENTS")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")

        txtbc.write("********** MODEL MATLAB FUNCTIONS")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")

        ### END

        txtbc.close()

# if __name__ == "__main__":

#     from MassAction import MassAction
#     from MichaelisMentenGeneral import MichaelisMentenGeneral
#     from Synthesis import Synthesis
#     from Degradation import Degradation

#     peakModel = Model()
#     peakModel.addActivation("EGF", 100, 5000)
#     peakModel.specieConc(['SFKs'],[0])
#     r1 = MichaelisMentenGeneral("EGFR", "uEGFR")
#     r1.addStimulator("PEAK3duCbl")
#     r1.addStimulator("Grb2upPEAK3duCbl")
#     r1.addInhibitor("PEAK3duPYK2")
#     r1.addInhibitor("Grb2upPEAK3duPYK2")
#     r1.noBackward = True

#     r2 = MichaelisMentenGeneral("EGFR", "pEGFR")
#     r2.addStimulator("EGF0", kc=100) # if kc is too low model have no response

#     r3 = MichaelisMentenGeneral("iSFKs", "SFKs")
#     r3.addStimulator("pEGFR", kc=1)

#     r4 = MichaelisMentenGeneral("Shc", "pShc")
#     r4.addStimulator("pEGFR", kc=1)

#     r5 = MassAction("PEAK3", "PEAK3", "PEAK3d")

#     r6 = MassAction("Grb2", "PEAK3d", "Grb2uPEAK3d")

#     r7 = MassAction("PEAK3d", "Cbl", "PEAK3duCbl", Ka=0.01) # Cbl binding with PEAK3 stronger
#     r8 = MassAction("PEAK3d", "PYK2", "PEAK3duPYK2")
#     r9 = MassAction("PEAK3d", "CrkII", "PEAK3duCrkII")

#     r10 = MichaelisMentenGeneral("Grb2uPEAK3d", "Grb2upPEAK3d")
#     r10.addStimulator("SFKs")
#     r10.noBackward = True

#     r11 = MassAction("Grb2uPEAK3d", "pShc", "Grb2uPEAK3dupShc", Ka=0.1, Kd=10)

#     r12 = MassAction("Grb2upPEAK3d", "pShc", "Grb2upPEAK3dupShc", Ka=0.1, Kd=10)

#     r13 = MichaelisMentenGeneral("Grb2upPEAK3dupShc", "Grb2uPEAK3dupShc")
#     r13.addStimulator("PTPN12", kc=100)
#     r13.noBackward = True


#     r14 = MassAction("ASAP1", "Grb2upPEAK3d", "Grb2upPEAK3duASAP1")

#     r15 = MassAction("Grb2upPEAK3d", "Cbl", "Grb2upPEAK3duCbl")
#     r16 = MassAction("Grb2upPEAK3d", "PYK2", "Grb2upPEAK3duPYK2")
#     r17 = MassAction("Grb2upPEAK3d", "CrkII", "Grb2upPEAK3duCrkII", Ka=0.01) # CrkII binding with pPEAK3 stronger

#     r18 = Synthesis("PTPN12", KSyn=0) # PTPN12 stays constant 

#     r19 = Degradation("uEGFR")
#     r20 = Synthesis("EGFR")

#     reactions = [r1, r2, r3, r4, r5, r6, r7, r8,
#                 r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20]

#     for r in reactions:
#         peakModel.addReaction(r)

#     peakModel.setModelName("PEAK3-Model-4d")
#     peakModel.generateTxtbc()
#     print(peakModel.species)
#     peakModel.generateTxtbc()