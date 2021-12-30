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


class WZG_Producer(Module):
	def __init__(self, year):
		self.year = year
		pass
	def ZZ_GetLepIndex(self, abs_mll_mz):
		lepton_index_mark = abs_mll_mz.index(min(abs_mll_mz))
		lepton_map = {0:[0,1], 1:[0,2], 2:[0,3], 3:[1,2], 4:[1,3], 5:[2,3]}
		l1_index = lepton_map[lepton_index_mark][0]
		l2_index = lepton_map[lepton_index_mark][1]
		l3_index = [x for x in range(0,4) if x not in lepton_map[lepton_index_mark]][0]
		l4_index = [x for x in range(0,4) if x not in lepton_map[lepton_index_mark]][1]
		return (l1_index, l2_index, l3_index, l4_index)
	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.out = wrappedOutputTree
		self.out.branch("MET",  "F")
		# self.out.branch("max_CMVA","F")
		# self.out.branch("max_CSVV2","F")
		# self.out.branch("max_DeepB","F")
		self.out.branch("channel_mark","i")
		self.out.branch("nJets","i")
		self.out.branch("nbJets","i")
		self.out.branch("nvetoMuon","i")
		self.out.branch("nvetoElectron","i")


		self.out.branch("ntight_photons","i")
		self.out.branch("ntight_electrons","i")
		self.out.branch("ntight_muons","i")



		self.out.branch("WZG_lepton1_pt",  "F")
		self.out.branch("WZG_lepton1_eta",  "F")
		self.out.branch("WZG_lepton1_phi",  "F")
		self.out.branch("WZG_lepton1_mass",  "F")
		self.out.branch("WZG_lepton1_genPartFlav",  "i")
		self.out.branch("WZG_lepton1_index",  "i")
		self.out.branch("WZG_lepton2_pt",  "F")
		self.out.branch("WZG_lepton2_eta",  "F")
		self.out.branch("WZG_lepton2_phi",  "F")
		self.out.branch("WZG_lepton2_mass",  "F")
		self.out.branch("WZG_lepton2_genPartFlav",  "i")
		self.out.branch("WZG_lepton2_index",  "i")
		self.out.branch("WZG_lepton3_pt",  "F")
		self.out.branch("WZG_lepton3_eta",  "F")
		self.out.branch("WZG_lepton3_phi",  "F")
		self.out.branch("WZG_lepton3_mass",  "F")
		self.out.branch("WZG_lepton3_genPartFlav",  "i")
		self.out.branch("WZG_lepton3_index",  "i")
		self.out.branch("WZG_photon_pt",  "F")
		self.out.branch("WZG_photon_eta",  "F")
		self.out.branch("WZG_photon_phi",  "F")
		self.out.branch("WZG_photon_mass",  "F")
		self.out.branch("WZG_photon_genPartFlav",  "i")
		self.out.branch("WZG_photon_index",  "i")
		self.out.branch("WZG_dileptonmass",  "F")
		self.out.branch("WZG_trileptonmass",  "F")
		self.out.branch("WZG_mlla",  "F")
		self.out.branch("WZG_MET",  "F")


		self.out.branch("Muon_ID_Weight", "F")
		self.out.branch("Muon_ID_Weight_UP", "F")
		self.out.branch("Muon_ID_Weight_DOWN", "F")
		self.out.branch("Electron_ID_Weight", "F")
		self.out.branch("Electron_ID_Weight_UP", "F")
		self.out.branch("Electron_ID_Weight_DOWN", "F")
		self.out.branch("Electron_RECO_Weight", "F")
		self.out.branch("Electron_RECO_Weight_UP", "F")
		self.out.branch("Electron_RECO_Weight_DOWN", "F")


	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass

	def analyze(self, event):
		"""process event, return True (go to next module) or False (fail, go to next event)"""
		electrons = Collection(event, "Electron")
		muons = Collection(event, "Muon")
		photons = Collection(event, "Photon")
		jets = Collection(event, "Jet")
		jet_select = [] 
		dileptonp4 = ROOT.TLorentzVector()
		tight_photons = []
		tight_electrons = [] 
		tight_muons = [] 
		tight_jets = [] 
		tight_bjets = []
		veto_muons = []
		veto_electrons = []

		# selection on MET. Pass to next event directly if fail.
		if hasattr(event, "MET_T1Smear_pt"):
			MET = event.MET_T1Smear_pt
			self.out.fillBranch("MET",event.MET_T1Smear_pt)
		else:
			MET = event.MET_pt
			self.out.fillBranch("MET",event.MET_pt)


		#selection on muons
		for i in range(0,len(muons)):
			if event.Muon_corrected_pt[i] < 10:
				continue
			if abs(muons[i].eta) > 2.4:
				continue
			if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
				tight_muons.append(i)
			elif muons[i].looseId and muons[i].pfRelIso04_all < 0.4:
				veto_muons.append(i)
			muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())

		Muon_ID_Weight = 1
		Muon_ID_Weight_UP = 1
		Muon_ID_Weight_DOWN = 1
		if hasattr(event, "Muon_CutBased_TightID_SF"):
			for i in tight_muons:
				Muon_ID_Weight = Muon_ID_Weight * event.Muon_CutBased_TightID_SF[i]
				Muon_ID_Weight_UP = max(Muon_ID_Weight_UP * (event.Muon_CutBased_TightID_SF[i] + event.Muon_CutBased_TightID_SFerr[i]), Muon_ID_Weight_UP * (event.Muon_CutBased_TightID_SF[i] - event.Muon_CutBased_TightID_SFerr[i]))
				Muon_ID_Weight_DOWN = min(Muon_ID_Weight_DOWN * (event.Muon_CutBased_TightID_SF[i] + event.Muon_CutBased_TightID_SFerr[i]), Muon_ID_Weight_DOWN * (event.Muon_CutBased_TightID_SF[i] - event.Muon_CutBased_TightID_SFerr[i]))
			for i in veto_muons:
				Muon_ID_Weight = Muon_ID_Weight * event.Muon_CutBased_LooseID_SF[i]
				Muon_ID_Weight_UP = max(Muon_ID_Weight_UP * (event.Muon_CutBased_LooseID_SF[i] + event.Muon_CutBased_LooseID_SFerr[i]), Muon_ID_Weight_UP * (event.Muon_CutBased_LooseID_SF[i] - event.Muon_CutBased_LooseID_SFerr[i]))
				Muon_ID_Weight_DOWN = min(Muon_ID_Weight_DOWN * (event.Muon_CutBased_LooseID_SF[i] + event.Muon_CutBased_LooseID_SFerr[i]), Muon_ID_Weight_DOWN * (event.Muon_CutBased_LooseID_SF[i] - event.Muon_CutBased_LooseID_SFerr[i]))


		# selection on electrons
		for i in range(0,len(electrons)):
			if electrons[i].pt < 10:
				continue
			if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
				continue
			if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
				if electrons[i].cutBased >= 3:
					tight_electrons.append(i)
				elif electrons[i].cutBased >= 1:
					veto_electrons.append(i)

		Electron_ID_Weight = 1
		Electron_ID_Weight_UP = 1
		Electron_ID_Weight_DOWN = 1
		Electron_RECO_Weight = 1
		Electron_RECO_Weight_UP = 1
		Electron_RECO_Weight_DOWN = 1
		if hasattr(event, "Electron_RECO_SF"):
			for i in tight_electrons:
				Electron_ID_Weight = Electron_ID_Weight * event.Electron_CutBased_MediumID_SF[i]
				Electron_ID_Weight_UP = max(Electron_ID_Weight_UP * (event.Electron_CutBased_MediumID_SF[i] + event.Electron_CutBased_MediumID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_MediumID_SF[i] - event.Electron_CutBased_MediumID_SFerr[i]))
				Electron_ID_Weight_DOWN = min(Electron_ID_Weight_DOWN * (event.Electron_CutBased_MediumID_SF[i] + event.Electron_CutBased_MediumID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_MediumID_SF[i] - event.Electron_CutBased_MediumID_SFerr[i]))
				Electron_RECO_Weight = Electron_RECO_Weight * event.Electron_RECO_SF[i]
				Electron_RECO_Weight_UP = max(Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))
				Electron_RECO_Weight_DOWN = min(Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))
			for i in veto_electrons:
				Electron_ID_Weight = Electron_ID_Weight * event.Electron_CutBased_VetoID_SF[i]
				Electron_ID_Weight_UP = max(Electron_ID_Weight_UP * (event.Electron_CutBased_VetoID_SF[i] + event.Electron_CutBased_VetoID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_VetoID_SF[i] - event.Electron_CutBased_VetoID_SFerr[i]))
				Electron_ID_Weight_DOWN = min(Electron_ID_Weight_DOWN * (event.Electron_CutBased_VetoID_SF[i] + event.Electron_CutBased_VetoID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_VetoID_SF[i] - event.Electron_CutBased_VetoID_SFerr[i]))
				Electron_RECO_Weight = Electron_RECO_Weight * event.Electron_RECO_SF[i]
				Electron_RECO_Weight_UP = max(Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))
				Electron_RECO_Weight_DOWN = min(Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))

		self.out.fillBranch("Muon_ID_Weight", Muon_ID_Weight)
		self.out.fillBranch("Muon_ID_Weight_UP", Muon_ID_Weight_UP)
		self.out.fillBranch("Muon_ID_Weight_DOWN", Muon_ID_Weight_DOWN)
		self.out.fillBranch("Electron_ID_Weight", Electron_ID_Weight)
		self.out.fillBranch("Electron_ID_Weight_UP", Electron_ID_Weight_UP)
		self.out.fillBranch("Electron_ID_Weight_DOWN", Electron_ID_Weight_DOWN)
		self.out.fillBranch("Electron_RECO_Weight", Electron_RECO_Weight)
		self.out.fillBranch("Electron_RECO_Weight_UP", Electron_RECO_Weight_UP)
		self.out.fillBranch("Electron_RECO_Weight_DOWN", Electron_RECO_Weight_DOWN)

		# selection on photons, but not requirement on photon number in this module
		for i in range(0,len(photons)):

			# This condition should be changed for different process
			#  photons[i].genPartFlav == 1:
				# continue

			if photons[i].pt < 20:
				continue

			if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
				continue

			if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
				continue

			if photons[i].pixelSeed:
				continue

			pass_lepton_dr_cut = True

			for j in range(0,len(tight_muons)):
				if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
					pass_lepton_dr_cut = False

			for j in range(0,len(tight_electrons)):
				if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
					pass_lepton_dr_cut = False

			if not pass_lepton_dr_cut:
				continue

			if photons[i].cutBased < 2:
				continue

			tight_photons.append(i)


		for i in range(0,len(jets)): 

			if event.Jet_pt_nom[i] < 10:
				continue

			if abs(jets[i].eta) > 2.4:
				continue
			
			if not jets[i].jetId == 6:
				continue

			pass_lepton_dr_cut = True

			for j in range(0,len(tight_photons)):
				if deltaR(jets[i].eta,jets[i].phi,photons[tight_photons[j]].eta,photons[tight_photons[j]].phi) < 0.5:
					pass_lepton_dr_cut = False

			for j in range(0,len(tight_electrons)):
				if deltaR(jets[i].eta,jets[i].phi,electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi) < 0.5:
					pass_lepton_dr_cut = False

			for j in range(0,len(tight_muons)):
				if deltaR(jets[i].eta,jets[i].phi,muons[tight_muons[j]].eta,muons[tight_muons[j]].phi) < 0.5:
					pass_lepton_dr_cut = False

			if not pass_lepton_dr_cut: 
				continue







			# https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
			# https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
			# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Jets
			# tightLepVeto PF jets (ak4), UL 2016/2017/2018 (jetId 110=6), medium B-tag WP
			# UL17 DeepCSV=(nanoaod btagDeepB) loose: 0.1355, medium: 0.4506, tight: 0.7738
			# UL18 DeepCSV=(nanoaod btagDeepB) loose: 0.1208, medium: 0.4168, tight: 0.7665
			# UL17 DeepFlavor=(nanoaod btagDeepFlavB) loose: 0.0532, medium: 0.3040, tight: 0.7476
			# UL18 DeepFlavor=(nanoaod btagDeepFlavB) loose: 0.0490, medium: 0.2783, tight: 0.7100

			# c-jet tag is based on two-D cuts, medium DeepJet WP:
			# UL17 CvsL=btagDeepFlavCvL: 0.085, CvsB=btagDeepFlavCvB: 0.34
			# UL18 CvsL=btagDeepFlavCvL: 0.099, CvsB=btagDeepFlavCvB: 0.325
			# c-tag not available in NANOAOD yet

			tight_jets.append(i)

			if event.Jet_pt_nom[i] >= 30:
				if self.year == '2016_preVFP':
					if jets[i].btagDeepB > 0.8819	:
							tight_bjets.append(i)


				if self.year == '2016':
					if jets[i].btagDeepB > 0.8767:
							tight_bjets.append(i)



				elif self.year == '2017':
					if jets[i].btagDeepB > 0.7738:
							tight_bjets.append(i)



				elif self.year == '2018':
					if jets[i].btagDeepB > 0.7665:
							tight_bjets.append(i)

		self.out.fillBranch("nJets", len(tight_jets))
		self.out.fillBranch("nbJets", len(tight_bjets))

		channel = -99 





		# WZG Signal Region
		# MET > 30
		# 3 leptons with an OSSF lepton pair, mll cloest to mz as z leptons
		# pt(lz1) > 25, pt(lz2) > 10, pt(lw) > 25
		# |m(lz1,lz2)-mz| <= 15
		# >=1 tight photon
		# |m(lz1,lz2,a)+m(lz1,lz2)| >= 182 !!abandoned!!
		# m(lz1,lz2) > 4
		# m(lll) > 100
		
		self.out.fillBranch('ntight_photons',len(tight_photons))
		self.out.fillBranch('ntight_electrons',len(tight_electrons))
		self.out.fillBranch('ntight_muons',len(tight_muons))

		if len(tight_electrons) >=2 or len(tight_muons) >= 2:

			dileptonmass = float('inf')
			m_lla = -float('inf')


			# ee
			if len(tight_electrons)>=2:
				# move the different charge lepton to the end for further analysis
				dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
				
				if electrons[tight_electrons[0]].pt < 25:
					return False

				if len(tight_photons) > 0:
					m_lla = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4() + photons[tight_photons[0]].p4()).M()

				temp_zl1_p4 = electrons[tight_electrons[0]].p4()
				temp_zl1_index = tight_electrons[0]
				temp_zl2_p4 = electrons[tight_electrons[1]].p4()
				temp_zl2_index = tight_electrons[1]
				if hasattr(electrons[tight_electrons[0]],"genPartFlav"):
					temp_zl1_genPartFlav = electrons[tight_electrons[0]].genPartFlav
					temp_zl2_genPartFlav = electrons[tight_electrons[1]].genPartFlav

				channel = 0


			# mu
			if len(tight_muons)>=2:
				dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
				
				if muons[tight_muons[0]].pt < 25:
					return False
				if len(tight_photons) > 0:
					m_lla = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4() + photons[tight_photons[0]].p4()).M()

				temp_zl1_p4 = muons[tight_muons[0]].p4()
				temp_zl1_index = tight_muons[0]
				temp_zl1_p4.SetPtEtaPhiM(event.Muon_corrected_pt[0], temp_zl1_p4.Eta(), temp_zl1_p4.Phi(), temp_zl1_p4.M())
				temp_zl2_p4 = muons[tight_muons[1]].p4()
				temp_zl2_index = tight_muons[1]
				temp_zl2_p4.SetPtEtaPhiM(event.Muon_corrected_pt[1], temp_zl2_p4.Eta(), temp_zl2_p4.Phi(), temp_zl2_p4.M())
				if hasattr(muons[tight_muons[0]],"genPartFlav"):
					temp_wl1_genPartFlav = muons[tight_muons[0]].genPartFlav
					temp_zl1_genPartFlav = muons[tight_muons[1]].genPartFlav

				channel = 1
			
			
			if True:


				self.out.fillBranch("channel_mark", channel)
				# l1: w, l2: zl1, l3: zl2
				if len(tight_muons)>=2 or len(tight_electrons)>=2:
					self.out.fillBranch("WZG_lepton1_pt", temp_zl1_p4.Pt())
					self.out.fillBranch("WZG_lepton1_eta", temp_zl1_p4.Eta())
					self.out.fillBranch("WZG_lepton1_phi", temp_zl1_p4.Phi())
					self.out.fillBranch("WZG_lepton1_mass", temp_zl1_p4.M())
					self.out.fillBranch("WZG_lepton1_index", temp_zl1_index)
					self.out.fillBranch("WZG_lepton2_pt", temp_zl2_p4.Pt())
					self.out.fillBranch("WZG_lepton2_eta", temp_zl2_p4.Eta())
					self.out.fillBranch("WZG_lepton2_phi", temp_zl2_p4.Phi())
					self.out.fillBranch("WZG_lepton2_mass", temp_zl2_p4.M())
					self.out.fillBranch("WZG_lepton2_index", temp_zl2_index)
					self.out.fillBranch("WZG_dileptonmass", dileptonmass)
				if len(tight_photons)>=1:
					self.out.fillBranch("WZG_photon_pt", photons[tight_photons[0]].pt)
					self.out.fillBranch("WZG_photon_eta", photons[tight_photons[0]].eta)
					self.out.fillBranch("WZG_photon_phi", photons[tight_photons[0]].phi)
					self.out.fillBranch("WZG_photon_mass", photons[tight_photons[0]].mass)
					self.out.fillBranch("WZG_photon_index", tight_photons[0])
					if hasattr(photons[tight_photons[0]], "genPartFlav"):
						self.out.fillBranch("WZG_photon_genPartFlav", photons[tight_photons[0]].genPartFlav)
					self.out.fillBranch("WZG_mlla", m_lla)
				#if 'temp_wl1_genPartFlav' in locals():
				#	self.out.fillBranch("WZG_lepton1_genPartFlav", temp_wl1_genPartFlav)
				#	self.out.fillBranch("WZG_lepton2_genPartFlav", temp_zl1_genPartFlav)
				self.out.fillBranch("WZG_MET", MET)
				return True

		return False
	

class first_Template_Producer(Module):
	def __init__(self):
		pass
	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.out = wrappedOutputTree
		self.out.branch("nLooseNotTightLep","I")
		self.out.branch("nTightLep","I")
		self.out.branch("nTightMuon","I")
		self.out.branch("nTightElectron","I")
		self.out.branch("nLooseNotTightMuon","I")
		self.out.branch("nLooseNotTightElectron","I")
		pass

	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass

	def analyze(self, event):
		"""process event, return True (go to next module) or False (fail, go to next event)"""
		electrons = Collection(event, "Electron")
		muons = Collection(event, "Muon")
		# photons = Collection(event, "Photon")
		tight_photons = []
		tight_electrons = [] 
		tight_muons = [] 
		loose_but_not_tight_muons = []
		loose_but_not_tight_electrons = []

		if (event.nElectron + event.nMuon) < 2:
			return False

		for i in range (0,len(muons)):
			if event.Muon_corrected_pt[i] < 10:
				continue
			if abs(muons[i].eta) > 2.4:
				continue
			if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
				tight_muons.append(i)
			elif muons[i].looseId and muons[i].pfRelIso04_all < 0.4:
				loose_but_not_tight_muons.append(i)

		for i in range(0,len(electrons)):
			if electrons[i].pt < 10:
				continue
			if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
				continue
			if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
				if electrons[i].cutBased >= 3:
					tight_electrons.append(i)
				elif electrons[i].cutBased >= 1:
					loose_but_not_tight_electrons.append(i)

		if (len(tight_electrons) + len(tight_muons) > 4) or (len(tight_electrons) + len(tight_muons) <= 2):
			return False

		self.out.fillBranch("nLooseNotTightLep", len(loose_but_not_tight_muons)+len(loose_but_not_tight_electrons))
		self.out.fillBranch("nTightLep", len(tight_muons)+len(tight_electrons))
		self.out.fillBranch("nTightMuon", len(tight_muons))
		self.out.fillBranch("nTightElectron", len(tight_electrons))
		self.out.fillBranch("nLooseNotTightMuon", len(loose_but_not_tight_muons))
		self.out.fillBranch("nLooseNotTightElectron", len(loose_but_not_tight_electrons))

		return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
WZG_select_Module_PKUKNU			= lambda : WZG_Producer()
WZG_select_Module_16preVFP_PKUKNU  = lambda : WZG_Producer("2016_preVFP")
WZG_select_Module_16_PKUKNU		= lambda : WZG_Producer("2016")
WZG_select_Module_17_PKUKNU		= lambda : WZG_Producer("2017")
WZG_select_Module_18_PKUKNU		= lambda : WZG_Producer("2018")
first_Template_Module_PKUKNU		= lambda : first_Template_Producer()
