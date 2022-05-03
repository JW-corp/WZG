#!/usr/bin/env python
# Analyzer for WZG Analysis based on nanoAOD tools

import os, sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module



class ApplyWeightFakeLeptonProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        self.file_ele = ROOT.TFile("/x5/cms/jwkim/gitdir/JWCorp/JW_analysis/for_graduation2022/CMSSW_10_6_19/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/local_condor_run/DB_v3/FakeLepton/fakerate_hist/Ele_Fake_Rate_2D_2016.root","READ")
        self.file_mu = ROOT.TFile("/x5/cms/jwkim/gitdir/JWCorp/JW_analysis/for_graduation2022/CMSSW_10_6_19/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/local_condor_run/DB_v3/FakeLepton/fakerate_hist/Mu_Fake_Rate_2D_2016.root","READ") 
        self.FR_E = self.file_ele.Get("fake_rate_e")
        self.FR_M = self.file_mu.Get("fake_rate_m")
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fake_lepton_weight",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # Open the root file with 2D pt-eta fake rate

        weight = 1
        number_of_loose = event.nLooseMuon + event.nLooseElectron

        for i in range(0, len(event.LooseNotTightMuon_pt)):
            BinX = self.FR_M.GetXaxis().FindBin(abs(event.LooseNotTightMuon_eta[i]))
            BinY = self.FR_M.GetYaxis().FindBin(abs(event.LooseNotTightMuon_pt[i]))
            if BinX > self.FR_M.GetNbinsX():
                BinX = self.FR_M.GetNbinsX()
            if BinY > self.FR_M.GetNbinsY():
                BinY = self.FR_M.GetNbinsY()
            weight = weight*self.FR_M.GetBinContent(BinX, BinY)/(1 - self.FR_M.GetBinContent(BinX, BinY))
            
        for i in range(0, len(event.LooseNotTightElectron_pt)):
            BinX = self.FR_E.GetXaxis().FindBin(abs(event.LooseNotTightElectron_eta[i]))
            BinY = self.FR_E.GetYaxis().FindBin(abs(event.LooseNotTightElectron_pt[i]))
            if BinX > self.FR_E.GetNbinsX():
                BinX = self.FR_E.GetNbinsX()
            if BinY > self.FR_E.GetNbinsY():
                BinY = self.FR_E.GetNbinsY()
            weight = weight*self.FR_E.GetBinContent(BinX, BinY)/(1 - self.FR_E.GetBinContent(BinX, BinY))

        if (number_of_loose % 2 > 0):
            weight = weight
        else:
            weight = -weight
        self.out.fillBranch("fake_lepton_weight", weight)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakeLeptonModule16 = lambda : ApplyWeightFakeLeptonProducer()
ApplyWeightFakeLeptonModule17 = lambda : ApplyWeightFakeLeptonProducer()
ApplyWeightFakeLeptonModule18 = lambda : ApplyWeightFakeLeptonProducer()

