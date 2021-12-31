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



class ApplyWeightFakePhotonProducer(Module):
	def __init__(self,year):
		self.year = str(year)

	def beginJob(self):
		pass
	def endJob(self):
		pass
	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.out = wrappedOutputTree
		self.out.branch("fake_photon_weight",  "F")

	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass
	def analyze(self, event):
		"""process event, return True (go to next module) or False (fail, go to next event)"""


		is_ElectronCh = (event.channel_mark == 2) | (event.channel_mark == 3) | (event.channel_mark == 12) | (event.channel_mark == 13) | (event.channel_mark == 22) | (event.channel_mark == 23)
		is_MuonCh = (event.channel_mark == 1) | (event.channel_mark == 4)|  (event.channel_mark == 11) | (event.channel_mark == 14) | (event.channel_mark == 21) | (event.channel_mark == 24) 
		

		weight = 1





		mu_barrel_pt_map = {

			'2018':	{
					"20-25": 0.36,
					"25-30": 0.30,
					"30-35": 0.23,
					"35-40": 0.21,
					"40-50": 0.17,
					"50-60": 0.14,
					"60-100": 0.14,
					"100-400": 0.10
					},

			'2017':	{
					"20-25": 0.41,
					"25-30": 0.40,
					"30-35": 0.36,
					"35-40": 0.32,
					"40-50": 0.26,
					"50-60": 0.20,
					"60-100": 0.16,
					"100-400": 0.12
					},
			'2016':	{
					"20-25": 0.39,
					"25-30": 0.35,
					"30-35": 0.30,
					"35-40": 0.27,
					"40-50": 0.22,
					"50-60": 0.17,
					"60-100": 0.15,
					"100-400": 0.11
					},

		}

		mu_endcap_pt_map = {

		   '2018':  {
					"20-25": 0.24,
					"25-30": 0.20,
					"30-40": 0.16,
					"40-50": 0.19,
					"50-60": 0.15,
					"60-400": 0.13
					},
		   '2017':  {
					"20-25": 0.30,
					"25-30": 0.33,
					"30-40": 0.37,
					"40-50": 0.23,
					"50-60": 0.25,
					"60-400": 0.25
					},
		   '2016':  {
					"20-25": 0.27,
					"25-30": 0.26,
					"30-40": 0.26,
					"40-50": 0.21,
					"50-60": 0.20,
					"60-400": 0.19
					},

		}

		ele_barrel_pt_map = {

			'2018': {
					"20-25": 0.42,
					"25-30": 0.30,
					"30-35": 0.26,
					"35-40": 0.23,
					"40-50": 0.17,
					"50-60": 0.12,
					"60-100": 0.12,
					"100-400": 0.05
					},

			'2017': {
					"20-25": 0.55,
					"25-30": 0.46,
					"30-35": 0.39,
					"35-40": 0.35,
					"40-50": 0.28,
					"50-60": 0.26,
					"60-100": 0.24,
					"100-400": 0.16
					},
			
			'2016': {
					"20-25": 0.48,
					"25-30": 0.38,
					"30-35": 0.32,
					"35-40": 0.29,
					"40-50": 0.22,
					"50-60": 0.19,
					"60-100": 0.18,
					"100-400": 0.11
					},
		}

		ele_endcap_pt_map = {

			'2018': {
					"20-25": 0.14,
					"25-30": 0.17,
					"30-40": 0.14,
					"40-50": 0.08,
					"50-60": 0.10,
					"60-400": 0.13
					},
			'2017': {
					"20-25": 0.38,
					"25-30": 0.33,
					"30-40": 0.25,
					"40-50": 0.13,
					"50-60": 0.30,
					"60-400": 0.26
					},
			'2016': {
					"20-25": 0.26,
					"25-30": 0.25,
					"30-40": 0.20,
					"40-50": 0.11,
					"50-60": 0.20,
					"60-400": 0.19
					}
		}

		
		if is_ElectronCh:

			# Barrel


			if abs(event.WZG_photon_eta) < 1.4442:
				if (event.WZG_photon_pt >= 20) and (event.WZG_photon_pt < 25):
					weight = ele_barrel_pt_map[self.year]["20-25"]
				elif (event.WZG_photon_pt >= 25) and (event.WZG_photon_pt < 30):
					weight = ele_barrel_pt_map[self.year]["25-30"]
				elif (event.WZG_photon_pt >= 30) and (event.WZG_photon_pt < 35):
					weight = ele_barrel_pt_map[self.year]["30-35"]
				elif (event.WZG_photon_pt >= 35) and (event.WZG_photon_pt < 40):
					weight = ele_barrel_pt_map[self.year]["35-40"]
				elif (event.WZG_photon_pt >= 40) and (event.WZG_photon_pt < 50):
					weight = ele_barrel_pt_map[self.year]["40-50"]
				elif (event.WZG_photon_pt >= 50) and (event.WZG_photon_pt < 60):
					weight = ele_barrel_pt_map[self.year]["50-60"]
				elif (event.WZG_photon_pt >= 60) and (event.WZG_photon_pt < 100):
					weight = ele_barrel_pt_map[self.year]["60-100"]
				elif (event.WZG_photon_pt >= 100) and (event.WZG_photon_pt < 400):
					weight = ele_barrel_pt_map[self.year]["100-400"]

			# Endcap
			elif (abs(event.WZG_photon_eta) > 1.566) and (abs(event.WZG_photon_eta) < 2.5):
				if (event.WZG_photon_pt >= 20) and (event.WZG_photon_pt < 25):
					weight = ele_endcap_pt_map[self.year]["20-25"]
				elif (event.WZG_photon_pt >= 25) and (event.WZG_photon_pt < 30):
					weight = ele_endcap_pt_map[self.year]["25-30"]
				elif (event.WZG_photon_pt >= 30) and (event.WZG_photon_pt < 40):
					weight = ele_endcap_pt_map[self.year]["30-40"]
				elif (event.WZG_photon_pt >= 40) and (event.WZG_photon_pt < 50):
					weight = ele_endcap_pt_map[self.year]["40-50"]
				elif (event.WZG_photon_pt >= 50) and (event.WZG_photon_pt < 60):
					weight = ele_endcap_pt_map[self.year]["50-60"]
				elif (event.WZG_photon_pt >= 60) and (event.WZG_photon_pt < 400):
					weight = ele_endcap_pt_map[self.year]["60-400"]

		elif is_MuonCh:
		
			# Barrel
			if abs(event.WZG_photon_eta) < 1.4442:
				if (event.WZG_photon_pt >= 20) and (event.WZG_photon_pt < 25):
					weight = mu_barrel_pt_map[self.year]["20-25"]
				elif (event.WZG_photon_pt >= 25) and (event.WZG_photon_pt < 30):
					weight = mu_barrel_pt_map[self.year]["25-30"]
				elif (event.WZG_photon_pt >= 30) and (event.WZG_photon_pt < 35):
					weight = mu_barrel_pt_map[self.year]["30-35"]
				elif (event.WZG_photon_pt >= 35) and (event.WZG_photon_pt < 40):
					weight = mu_barrel_pt_map[self.year]["35-40"]
				elif (event.WZG_photon_pt >= 40) and (event.WZG_photon_pt < 50):
					weight = mu_barrel_pt_map[self.year]["40-50"]
				elif (event.WZG_photon_pt >= 50) and (event.WZG_photon_pt < 60):
					weight = mu_barrel_pt_map[self.year]["50-60"]
				elif (event.WZG_photon_pt >= 60) and (event.WZG_photon_pt < 100):
					weight = mu_barrel_pt_map[self.year]["60-100"]
				elif (event.WZG_photon_pt >= 100) and (event.WZG_photon_pt < 400):
					weight = mu_barrel_pt_map[self.year]["100-400"]

			# Endcap
			elif (abs(event.WZG_photon_eta) > 1.566) and (abs(event.WZG_photon_eta) < 2.5):
				if (event.WZG_photon_pt >= 20) and (event.WZG_photon_pt < 25):
					weight = mu_endcap_pt_map[self.year]["20-25"]
				elif (event.WZG_photon_pt >= 25) and (event.WZG_photon_pt < 30):
					weight = mu_endcap_pt_map[self.year]["25-30"]
				elif (event.WZG_photon_pt >= 30) and (event.WZG_photon_pt < 40):
					weight = mu_endcap_pt_map[self.year]["30-40"]
				elif (event.WZG_photon_pt >= 40) and (event.WZG_photon_pt < 50):
					weight = mu_endcap_pt_map[self.year]["40-50"]
				elif (event.WZG_photon_pt >= 50) and (event.WZG_photon_pt < 60):
					weight = mu_endcap_pt_map[self.year]["50-60"]
				elif (event.WZG_photon_pt >= 60) and (event.WZG_photon_pt < 400):
					weight = mu_endcap_pt_map[self.year]["60-400"]

		
		self.out.fillBranch("fake_photon_weight", weight)

		return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakePhotonModule16 = lambda : ApplyWeightFakePhotonProducer('2016')
ApplyWeightFakePhotonModule17 = lambda : ApplyWeightFakePhotonProducer('2017')
ApplyWeightFakePhotonModule18 = lambda : ApplyWeightFakePhotonProducer('2018')
