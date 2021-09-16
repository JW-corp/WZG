import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import time
from coffea import processor, hist
from coffea.util import load, save
import json
import glob
import os
import argparse
import numpy as np
from coffea import lumi_tools
import numba
import pandas as pd


# -- Coffea 0.8.0 --> Must fix!!
import warnings

warnings.filterwarnings("ignore")


# ---> Class JW Processor
class JW_Processor(processor.ProcessorABC):

	# -- Initializer
	def __init__(self, year, sample_name, puweight_arr, corrections, isFake):

		# Parameter set
		self._year = year
		self._isFake = isFake

		# Trigger set
		self._triggers = {
			'Egamma':{
			"2018":["Ele23_Ele12_CaloIdL_TrackIdL_IsoVL","Ele32_WPTight_Gsf"]
			},
			'SingleMuon':{
			"2018":["IsoMu24"]
			},
			'DoubleMuon':{
			"2018":["Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]
			},
			'MuonEG':{
			"2018":["Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ","Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]
			},
		}

		# Corrrection set
		self._corrections = corrections
		self._puweight_arr = puweight_arr

		# hist set
		self._accumulator = processor.dict_accumulator(
			{
				"sumw": processor.defaultdict_accumulator(float),

				"cutflow": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Bin("cutflow", "Cut index", [0, 1, 2, 3, 4, 5, 6, 7]),
				),

				# -- Kinematics -- #
				"mass": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("mass", "$m_{e+e-}$ [GeV]", 100, 0, 200),
				),
				"mass_lll": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("mass_lll", "$m_{lll}$ [GeV]", 1000, 0, 1000),
				),
				"MT": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("MT", "W MT [GeV]", 100, 0, 200),
				),
				"met": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("met", "met [GeV]", 300, 0, 600),
				),
				# -- Electron -- #
				"ele1pt": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("ele1pt", "Leading Electron $P_{T}$ [GeV]", 300, 25, 600),
				),
				"ele2pt": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin(
						"ele2pt", "Subleading $Electron P_{T}$ [GeV]", 300, 10, 600
					),
				),
				"ele3pt": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("ele3pt", "Third $Electron P_{T}$ [GeV]", 300, 25, 600),
				),
				"ele1eta": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("ele1eta", "Leading Electron $\eta$ [GeV]", 20, -5, 5),
				),
				"ele2eta": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("ele2eta", "Subleading Electron $\eta$ [GeV]", 20, -5, 5),
				),
				"ele1phi": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin(
						"ele1phi", "Leading Electron $\phi$ [GeV]", 20, -3.15, 3.15
					),
				),
				"ele2phi": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin(
						"ele2phi", "Subleading Electron $\phi$ [GeV]", 20, -3.15, 3.15
					),
				),
				# -- Photon -- #
				"phopt": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("phopt", "Leading Photon $P_{T}$ [GeV]", 300, 20, 600),
				),
				"phoeta": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("phoeta", "Photon  $\eta$ ", 50, -5, 5),
				),
				"phophi": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("phophi", "Photon $\phi$ ", 50, -3.15, 3.15),
				),
				# -- Photon Endcap -- #
				"pho_EE_pt": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EE_pt", "Photon EE $P_{T}$ [GeV]", 300, 20, 600),
				),
				"pho_EE_eta": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EE_eta", "Photon EE $\eta$ ", 50, -5, 5),
				),
				"pho_EE_phi": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EE_phi", "Photon EE $\phi$ ", 50, -3.15, 3.15),
				),
				"pho_EE_sieie": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EE_sieie", "Photon EE sieie", 100, 0, 0.03),
				),
				"pho_EE_Iso_chg": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin(
						"pho_EE_Iso_chg", "Photon EE pfReoIso03_charge", 200, 0, 1
					),
				),
				# -- Photon Barrel -- #
				"pho_EB_pt": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EB_pt", "Photon EB $P_{T}$ [GeV]", 300, 20, 600),
				),
				"pho_EB_eta": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EB_eta", "Photon EB $\eta$ ", 50, -5, 5),
				),
				"pho_EB_phi": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EB_phi", "Photon EB $\phi$ ", 50, -3.15, 3.15),
				),
				"pho_EB_sieie": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin("pho_EB_sieie", "Photon EB sieie", 100, 0, 0.012),
				),
				"pho_EB_Iso_chg": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("region", "region"),
					hist.Bin(
						"pho_EB_Iso_chg", "Photon EB pfReoIso03_charge", 100, 0, 0.03
					),
				),
			}
		)

	# -- Accumulator: accumulate histograms
	@property
	def accumulator(self):
		return self._accumulator

	# -- Main function : Process events
	def process(self, events):

		# Initialize accumulator
		out = self.accumulator.identity()
		dataset = sample_name
		# events.metadata['dataset']

		# Data or MC
		isData = "genWeight" not in events.fields
		isFake = self._isFake

		# Stop processing if there is no event remain
		if len(events) == 0:
			return out

		# Golden Json file
		if (self._year == "2018") and isData:
			injson = "/x5/cms/jwkim/gitdir/JWCorp/JW_analysis/Coffea_WZG/Corrections/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt.RunABCD"

		if (self._year == "2017") and isData:
			injson = "/x5/cms/jwkim/gitdir/JWCorp/JW_analysis/Coffea_WZG/Corrections/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"

		# <----- Get Scale factors ------>#

		if not isData:

			# Egamma reco ID
			get_ele_reco_above20_sf = self._corrections["get_ele_reco_above20_sf"][
				self._year
			]
			get_ele_medium_id_sf = self._corrections["get_ele_medium_id_sf"][self._year]
			get_pho_medium_id_sf = self._corrections["get_pho_medium_id_sf"][self._year]

			get_ele_trig_leg1_SF = self._corrections["get_ele_trig_leg1_SF"][
				self._year
			]
			get_ele_trig_leg1_data_Eff = self._corrections[
				"get_ele_trig_leg1_data_Eff"
			][self._year]
			get_ele_trig_leg1_mc_Eff = self._corrections[
				"get_ele_trig_leg1_mc_Eff"
			][self._year]
			get_ele_trig_leg2_SF = self._corrections["get_ele_trig_leg2_SF"][
				self._year
			]
			get_ele_trig_leg2_data_Eff = self._corrections[
				"get_ele_trig_leg2_data_Eff"
			][self._year]
			get_ele_trig_leg2_mc_Eff = self._corrections[
				"get_ele_trig_leg2_mc_Eff"
			][self._year]

			# PU weight with custom made npy and multi-indexing
			pu_weight_idx = ak.values_astype(events.Pileup.nTrueInt, "int64")
			pu = self._puweight_arr[pu_weight_idx]


		# <----- Helper functions ------>#

		#  Sort by PT  helper function
		def sort_by_pt(ele, pho, jet,muon):
			ele  = ele[ak.argsort(ele.pt, ascending=False, axis=1)]
			pho  = pho[ak.argsort(pho.pt, ascending=False, axis=1)]
			jet  = jet[ak.argsort(jet.pt, ascending=False, axis=1)]
			muon = muon[ak.argsort(muon.pt, ascending=False, axis=1)] 
			return ele, pho, jet, muon

		# Lorentz vectors
		from coffea.nanoevents.methods import vector

		ak.behavior.update(vector.behavior)

		def TLorentz_vector(vec):
			vec = ak.zip(
				{"x": vec.x, "y": vec.y, "z": vec.z, "t": vec.t},
				with_name="LorentzVector",
			)
			return vec

		def TLorentz_vector_cylinder(vec):

			vec = ak.zip(
				{
					"pt": vec.pt,
					"eta": vec.eta,
					"phi": vec.phi,
					"mass": vec.mass,
				},
				with_name="PtEtaPhiMLorentzVector",
			)

			return vec

		# <----- Selection ------>#
		Initial_events = events
		# Good Run ( Golden Json files )
		from coffea import lumi_tools

		if isData:
			lumi_mask_builder = lumi_tools.LumiMask(injson)
			lumimask = ak.Array(
				lumi_mask_builder.__call__(events.run, events.luminosityBlock)
			)
			events = events[lumimask]
			# print("{0}%  of files pass good-run conditions".format(len(events)/ len(Initial_events)))

		# Stop processing if there is no event remain
		if len(events) == 0:
			return out

		# Cut flow
		cut0 = np.zeros(len(events))
		
		if not isFake:
			out["cutflow"].fill(dataset=dataset, cutflow=cut0)


		##----------- Cut flow1: Passing Triggers
		
		triggers_mask = np.zeros(len(events),dtype=np.bool)
		if isData:
			# --Trigger-mask for SingleMuon
			if dataset == 'SingleMuon':
				print('SingleMuon trigger')
				triggers_mask = events.HLT[self._triggers['SingleMuon'][year][0]]
		
			# --Trigger-mask for DoubleMuon
			elif dataset == 'DoubleMuon':
				print('DoubleMuon trigger')
				triggers_mask = (~events.HLT[self._triggers['SingleMuon'][year][0]])\
								& events.HLT[self._triggers['DoubleMuon'][year][0]]
		
			# --Trigger-maks for Egamma
			elif dataset == 'Egamma':
				print('Egamma trigger')
				triggers_mask = (~events.HLT[self._triggers['SingleMuon'][year][0]])\
								& (~events.HLT[self._triggers['DoubleMuon'][year][0]])\
								& (events.HLT[self._triggers['Egamma'][year][0]] | events.HLT[self._triggers['Egamma'][year][1]])
					
			# --Trigger-maks for MuonEG
			elif dataset == 'MuonEG':
				print('MuonEG trigger')
				triggers_mask =  (~events.HLT[self._triggers['SingleMuon'][year][0]])\
								& (~events.HLT[self._triggers['Egamma'][year][0]]) &  (~events.HLT[self._triggers['Egamma'][year][1]])\
								& (~events.HLT[self._triggers['DoubleMuon'][year][0]])\
								& (events.HLT[self._triggers['MuonEG'][year][0]] | events.HLT[self._triggers['MuonEG'][year][1]])
	
			elif dataset == 'FakeLepton':
				print('Fake lepton --> pass')
				triggers_mask = np.ones(len(events),dtype=np.bool)

		else:
			for key in self._triggers.keys():
				for t in self._triggers[key][year]:
					triggers_mask = triggers_mask | events.HLT[t]
	



		events.Electron, events.Photon, events.Jet, events.Muon = sort_by_pt(
			events.Electron, events.Photon, events.Jet, events.Muon
		)
		
		
		# Good Primary vertex
		nPV = events.PV.npvsGood
		nPV_nw = events.PV.npvsGood
		if not isData:
			nPV = nPV * pu

			#print(pu)

		# Apply cut1
		events = events[triggers_mask]
		if not isData:
			pu = pu[triggers_mask]

		# Stop processing if there is no event remain
		if len(events) == 0:
			return out

		cut1 = np.ones(len(events))
		if not isFake:
			out["cutflow"].fill(dataset=dataset, cutflow=cut1)

		# Set Particles
		Electron = events.Electron
		Muon = events.Muon
		vetoMuon = events.Muon
		Photon = events.Photon
		MET = events.MET
		Jet = events.Jet


		#  --Muon

		if dataset == "FakeLepton":
			MuSelmask = (
				(Muon.pt >= 10)
				& (abs(Muon.eta) <= 2.5)
				& (Muon.tightId)
			)

		if (dataset !="FakeLepton") & (not isData):
			MuSelmask = (
				(Muon.pt >= 10)
				& (abs(Muon.eta) <= 2.5)
				& (Muon.tightId)
				& (Muon.pfRelIso04_all < 0.15)
				& (Muon.genPartFlav == 1)
			)
		if (dataset !="FakeLepton") & (isData):
			MuSelmask = (
				(Muon.pt >= 10)
				& (abs(Muon.eta) <= 2.5)
				& (Muon.tightId)
				& (Muon.pfRelIso04_all < 0.15)
			)
		Muon = Muon[MuSelmask]

		#  --vetoMuon

		if dataset == "FakeLepton":

			MuSelmask = (
				(vetoMuon.pt >= 10)
				& (abs(vetoMuon.eta) <= 2.5)
				& (vetoMuon.looseId)
			)

		else:
			MuSelmask = (
				(vetoMuon.pt >= 10)
				& (abs(vetoMuon.eta) <= 2.5)
				& (vetoMuon.looseId)
				& (vetoMuon.pfRelIso04_all < 0.4)
			)
		vetoMuon = vetoMuon[MuSelmask]





		##----------- Cut flow2: Electron Selection
		if dataset == "FakeLepton":
			
			EleSelmask = (
				(Electron.pt >= 10)
				& (np.abs(Electron.eta + Electron.deltaEtaSC) < 1.479)
				& (abs(Electron.dxy) < 0.05)
				& (abs(Electron.dz) < 0.1)
			) | (
				(Electron.pt >= 10)
				& (np.abs(Electron.eta + Electron.deltaEtaSC) > 1.479)
				& (np.abs(Electron.eta + Electron.deltaEtaSC) <= 2.5)
				& (abs(Electron.dxy) < 0.1)
				& (abs(Electron.dz) < 0.2)
			)

		else:
			if not isData:
				EleSelmask = (
					(Electron.pt >= 10)
					& (np.abs(Electron.eta + Electron.deltaEtaSC) < 1.479)
					& (Electron.cutBased > 2)
					& (abs(Electron.dxy) < 0.05)
					& (abs(Electron.dz) < 0.1)
					& (Electron.genPartFlav == 1)
				) | (
					(Electron.pt >= 10)
					& (np.abs(Electron.eta + Electron.deltaEtaSC) > 1.479)
					& (np.abs(Electron.eta + Electron.deltaEtaSC) <= 2.5)
					& (Electron.cutBased > 2)
					& (abs(Electron.dxy) < 0.1)
					& (abs(Electron.dz) < 0.2)
					& (Electron.genPartFlav == 1)
				)
			else:
				EleSelmask = (
					(Electron.pt >= 10)
					& (np.abs(Electron.eta + Electron.deltaEtaSC) < 1.479)
					& (Electron.cutBased > 2)
					& (abs(Electron.dxy) < 0.05)
					& (abs(Electron.dz) < 0.1)
				) | (
					(Electron.pt >= 10)
					& (np.abs(Electron.eta + Electron.deltaEtaSC) > 1.479)
					& (np.abs(Electron.eta + Electron.deltaEtaSC) <= 2.5)
					& (Electron.cutBased > 2)
					& (abs(Electron.dxy) < 0.1)
					& (abs(Electron.dz) < 0.2)
				)
				

		Electron = Electron[EleSelmask]

		# Apply flow2
		Tri_electron_mask = ak.num(Electron) == 3

		Electron = Electron[Tri_electron_mask]
		Photon = Photon[Tri_electron_mask]
		if (not isData) and (not isFake):
		#	gen_photons = gen_photons[Tri_electron_mask]
			pu = pu[Tri_electron_mask]
		Jet = Jet[Tri_electron_mask]
		MET = MET[Tri_electron_mask]
		Muon = Muon[Tri_electron_mask]
		vetoMuon = vetoMuon[Tri_electron_mask]
		events = events[Tri_electron_mask]

		#print("N veto muon: ",ak.sum(ak.num(vetoMuon)))
		# Stop processing if there is no event remain
		if len(Electron) == 0:
			return out

		cut2 = np.ones(len(events)) * 2
		if not isFake:
			out["cutflow"].fill(dataset=dataset, cutflow=cut2)


		print("passing eee: ",len(events))
		##----------- Cut flow3: Photon Selection

		# Basic photon selection
		isgap_mask = (abs(Photon.eta) < 1.442) | (
			(abs(Photon.eta) > 1.566) & (abs(Photon.eta) < 2.5)
		)
		Pixel_seed_mask = ~Photon.pixelSeed

		if (dataset == "ZZ") and (self._year == "2017"):
			PT_ID_mask = (Photon.pt >= 20) & (
				Photon.cutBasedBitmap >= 3
			)  # 2^0(Loose) + 2^1(Medium) + 2^2(Tights)
		else:
			PT_ID_mask = (Photon.pt >= 20) & (Photon.cutBased > 1)


		# Photon cleaning
		if ak.sum(ak.num(Muon)) > 0:
			dr_mask = (ak.all(Photon.metric_table(Muon) >= 0.5, axis=-1) &
			ak.all(Photon.metric_table(Electron) >= 0.5, axis=-1))

		else:
			dr_mask = ak.all(Photon.metric_table(Electron) >= 0.5, axis=-1)


		# Add genPartFlav to remove Fake Photon in MC samples ( They are already considered by data driven method )
		if not isData:
			genPartFlav_mask =  (Photon.genPartFlav == 1)
			PhoSelmask = (genPartFlav_mask & PT_ID_mask & isgap_mask & Pixel_seed_mask & dr_mask)
		else:
			PhoSelmask = (PT_ID_mask & isgap_mask & Pixel_seed_mask & dr_mask)
			
		
		Photon = Photon[PhoSelmask]

		# Apply cut 3
		A_photon_mask = ak.num(Photon) > 0
		Electron = Electron[A_photon_mask]
		Photon = Photon[A_photon_mask]
		Jet = Jet[A_photon_mask]
		if ak.sum(ak.num(Muon)) != 0:
			Muon = Muon[A_photon_mask]

		if ak.sum(ak.num(vetoMuon)) != 0:
			vetoMuon = vetoMuon[A_photon_mask]


		MET = MET[A_photon_mask]
		if (not isData) and (not isFake):
		#	gen_photons = gen_photons[A_photon_mask]
			pu = pu[A_photon_mask]
		events = events[A_photon_mask]
		
		# Stop processing if there is no event remain
		if len(Photon) == 0:
			return out

		def make_leading_pair(target, base):
			return target[ak.argmax(base.pt, axis=1, keepdims=True)]

		leading_pho = make_leading_pair(Photon, Photon)



		# --veto Bjet
		dr_jet_ele_mask = ak.all(
			Jet.metric_table(Electron) >= 0.5, axis=-1
		)  # default metric table: delta_r

		if ak.sum(ak.num(Muon)) != 0:
			dr_jet_mu_mask = ak.all(Jet.metric_table(Muon) >= 0.5, axis=-1)
			bJet_mask =  (Jet.pt > 10) & (abs(Jet.eta) <2.4) & (dr_jet_ele_mask) & (dr_jet_mu_mask) & (Jet.btagDeepB > 0.7665)

		else:
			bJet_mask =  (Jet.pt > 10) & (abs(Jet.eta) <2.4) & (dr_jet_ele_mask) & (Jet.btagDeepB > 0.7665)

		Jet = Jet[bJet_mask]



		# -------------------- Make Fake Photon BKGs---------------------------#
		def make_bins(pt, isEB,isEE, bin_range_str):

			bin_dict = {
				"PT_1_eta_1": (pt > 20) & (pt < 30) & isEB,
				"PT_1_eta_2": (pt > 20) & (pt < 30) & isEE,
				"PT_2_eta_1": (pt > 30) & (pt < 40) & isEB,
				"PT_2_eta_2": (pt > 30) & (pt < 40) & isEE,
				"PT_3_eta_1": (pt > 40) &  isEB,
				"PT_3_eta_2": (pt > 40) &  isEE
			}

			binmask = bin_dict[bin_range_str]

			return binmask

		bin_name_list = [
			"PT_1_eta_1",
			"PT_1_eta_2",
			"PT_2_eta_1",
			"PT_2_eta_2",
			"PT_3_eta_1",
			"PT_3_eta_2"
		]

		## -- Fake-fraction Lookup table --##
		if isFake:
			# Make Bin-range mask
			binned_pteta_mask = {}
			for name in bin_name_list:
				binned_pteta_mask[name] = make_bins(
					ak.flatten(leading_pho.pt),
					ak.flatten(leading_pho.isScEtaEB),
					ak.flatten(leading_pho.isScEtaEE),
					name,
				)
			# Read Fake fraction --> Mapping bin name to int()

			if self._year == "2018":
				in_dict = np.load("Fitting_210914_FakeTemplate/Fit_results.npy", allow_pickle="True")[
					()
				]

			if self._year == "2017":
				in_dict = np.load("Fitting_2017/Fit_results.npy", allow_pickle="True")[
					()
				]

			idx = 0
			fake_dict = {}
			for i, j in in_dict.items():
				fake_dict[idx] = j
				idx += 1

			# Reconstruct Fake_weight
			fw = 0
			for i, j in binned_pteta_mask.items():
				fw = fw + j * fake_dict[bin_name_list.index(i)]

			# Process 0 weight to 1
			@numba.njit
			def zero_one(x):
				if x == 0:
					x = 1
				return x

			vec_zero_one = np.vectorize(zero_one)
			fw = vec_zero_one(fw)
		else:
			fw = np.ones(len(events))

		cut3 = np.ones(len(events)) * 3
		out["cutflow"].fill(dataset=dataset, cutflow=cut3,weight=fw)

		##----------- Cut flow4: OSSF
		# OSSF index maker
		@numba.njit
		def find_3lep(events_leptons, builder):
			for leptons in events_leptons:

				builder.begin_list()
				nlep = len(leptons)
				for i0 in range(nlep):
					for i1 in range(i0 + 1, nlep):
						if leptons[i0].charge + leptons[i1].charge != 0:
							continue

						for i2 in range(nlep):
							if len({i0, i1, i2}) < 3:
								continue

							if nlep <= 3:
								builder.begin_tuple(3)
								builder.index(0).integer(i0)
								builder.index(1).integer(i1)
								builder.index(2).integer(i2)
							else:
								builder.begin_tuple(4)
								builder.index(0).integer(i0)
								builder.index(1).integer(i1)
								builder.index(2).integer(i2)
								builder.index(3).integer(
									list({0, 1, 2, 3} - {i0, i1, i2})[0]
								)

							builder.end_tuple()
				builder.end_list()
			return builder

		eee_triplet_idx = find_3lep(Electron, ak.ArrayBuilder()).snapshot()

		ossf_mask = (
			(ak.num(eee_triplet_idx) == 2)
			| (ak.num(eee_triplet_idx) == 6)
			| (ak.num(eee_triplet_idx) == 8)
		)
		# 2 for e+ e+ e- ,  e+ e- e-
		# 6 for e+ e+ e+ e- or e- e- e- e+
		# 8 for e+ e+ e- e-

		# Apply cut 4
		eee_triplet_idx = eee_triplet_idx[ossf_mask]
		Electron = Electron[ossf_mask]
		Photon = Photon[ossf_mask]
		leading_pho = leading_pho[ossf_mask]
		fw = fw[ossf_mask]
		if ak.sum(ak.num(Jet)) != 0:
			Jet = Jet[ossf_mask]
		if ak.sum(ak.num(Muon)) != 0:
			Muon = Muon[ossf_mask]

		if ak.sum(ak.num(vetoMuon)) != 0:
			vetoMuon = vetoMuon[ossf_mask]

		MET = MET[ossf_mask]
		if not isData:
			pu = pu[ossf_mask]
		events = events[ossf_mask]

		# Stop processing if there is no event remain
		if len(Electron) == 0:
			return out

		cut4 = np.ones(len(events)) * 4
		out["cutflow"].fill(dataset=dataset, cutflow=cut4,weight=fw)


		# Fake Lepton weight
		if dataset == "FakeLepton":
			fake_lep_w = events.fake.lepton_weight



		# Define Electron Triplet

		Triple_electron = [Electron[eee_triplet_idx[idx]] for idx in "012"]
		Triple_eee = ak.zip(
			{
				"lep1": Triple_electron[0],
				"lep2": Triple_electron[1],
				"lep3": Triple_electron[2],
				"p4": TLorentz_vector(Triple_electron[0] + Triple_electron[1]),
			}
		)

		# Ele pair selector --> Close to Z mass
		bestZ_idx = ak.singletons(ak.argmin(abs(Triple_eee.p4.mass - 91.1876), axis=1))
		Triple_eee = Triple_eee[bestZ_idx]

		leading_ele = Triple_eee.lep1
		subleading_ele = Triple_eee.lep2
		third_ele = Triple_eee.lep3

		# -- Scale Factor for each electron

		# Trigger weight helper function

		if not isData:

			## -------------< Egamma ID and Reco Scale factor > -----------------##
			pho_medium_id_sf = get_pho_medium_id_sf(
				ak.flatten(leading_pho.eta), ak.flatten(leading_pho.pt)
			)

			ele_reco_sf = (
				get_ele_reco_above20_sf(
					ak.flatten(leading_ele.deltaEtaSC + leading_ele.eta),
					ak.flatten(leading_ele.pt),
				)
				* get_ele_reco_above20_sf(
					ak.flatten(subleading_ele.deltaEtaSC + subleading_ele.eta),
					ak.flatten(subleading_ele.pt),
				)
				* get_ele_reco_above20_sf(
					ak.flatten(third_ele.deltaEtaSC + third_ele.eta),
					ak.flatten(third_ele.pt),
				)
			)

			ele_medium_id_sf = (
				get_ele_medium_id_sf(
					ak.flatten(leading_ele.deltaEtaSC + leading_ele.eta),
					ak.flatten(leading_ele.pt),
				)
				* get_ele_medium_id_sf(
					ak.flatten(subleading_ele.deltaEtaSC + subleading_ele.eta),
					ak.flatten(subleading_ele.pt),
				)
				* get_ele_medium_id_sf(
					ak.flatten(third_ele.deltaEtaSC + third_ele.eta),
					ak.flatten(third_ele.pt),
				)
			)

			## -------------< Double Electron Trigger Scale factor > -----------------##

			ele_trig_weight = np.ones(len(pho_medium_id_sf)) * 0.987/0.988 # year 2018

		##----------- Cut flow5: Basline selection

		# Mee cut
		diele = Triple_eee.p4
		Mee_cut_mask = ak.firsts(diele.mass) > 4

		# Electron PT cuts
		Elept_mask = ak.firsts(
			(leading_ele.pt >= 25) & (subleading_ele.pt >= 10) & (third_ele.pt >= 25)
		)

		Baseline_mask = Elept_mask & Mee_cut_mask  # SR,CR

		# Apply cut5
		Triple_eee_base = Triple_eee[Baseline_mask]
		leading_pho_base = leading_pho[Baseline_mask]
		Electron_base = Electron[Baseline_mask]
		MET_base = MET[Baseline_mask] 
		events_base = events[Baseline_mask]

		if ak.sum(ak.num(Muon)) != 0:
			Muon_base = Muon[Baseline_mask]

		# Photon  EE and EB
		isEE_mask = leading_pho.isScEtaEE
		isEB_mask = leading_pho.isScEtaEB
		Pho_EE_base = leading_pho[isEE_mask & Baseline_mask]
		Pho_EB_base = leading_pho[isEB_mask & Baseline_mask]

		# Stop processing if there is no event remain
		if len(leading_pho_base) == 0:
			return out

		fw_cut5 = fw[Baseline_mask]
		cut5 = np.ones(len(events_base)) * 5
		out["cutflow"].fill(dataset=dataset, cutflow=cut5,weight=fw_cut5)


		base_arr_dict ={
			"Triple_eee_sel" :   Triple_eee_base
			,"leading_pho_sel":  leading_pho_base 
			,"Electron_sel"	 :	Electron_base
			,"MET_sel"		 :	MET_base
			,"Pho_EE_sel"	 :	Pho_EE_base
			,"Pho_EB_sel"	 :	Pho_EB_base
		}

		
		##-----------  << SR >>
		Zmass_window_mask = ak.firsts(abs(Triple_eee.p4.mass - 91.1876)) <= 15

		if dataset == "FakeLepton":
			MET_mask = MET > 20
		else:
			MET_mask = MET.pt > 20

		bjet_veto = ak.num(Jet) == 0
		#Mlll_mask = ak.firsts((Triple_eee.p4 + Triple_eee.lep3).mass) > 100
		
		


		print("######: show show show",sum(ak.num(vetoMuon)))
		if ak.sum(ak.num(vetoMuon)) != 0:
			Muon_veto = ak.num(vetoMuon) == 0
			#SR_mask = (Muon_veto & Zmass_window_mask & MET_mask & bjet_veto & Mlll_mask)
			SR_mask = (Muon_veto & Zmass_window_mask & MET_mask & bjet_veto)
		
		else:
			#SR_mask = (Zmass_window_mask & MET_mask & bjet_veto & Mlll_mask)
			SR_mask = (Zmass_window_mask & MET_mask & bjet_veto)
		


		SR_mask				= Baseline_mask & SR_mask
		Triple_eee_SR		= Triple_eee[SR_mask]
		leading_pho_SR		= leading_pho[SR_mask]
		MET_SR				= MET[SR_mask]
		Jet_SR				= Jet[SR_mask]
		events_SR			= events[SR_mask]
		Pho_EE_SR			= leading_pho[isEE_mask & SR_mask]
		Pho_EB_SR			= leading_pho[isEB_mask & SR_mask]

		fw_cut6 = fw[SR_mask]
		cut6 = np.ones(len(events_SR)) * 6
		out["cutflow"].fill(dataset=dataset, cutflow=cut6,weight=fw_cut6)

		SR_arr_dict ={
			"Triple_eee_sel" :   Triple_eee_SR
			,"leading_pho_sel":  leading_pho_SR 
			,"MET_sel"		 :	 MET_SR
			,"Pho_EE_sel"	 :	 Pho_EE_SR
			,"Pho_EB_sel"	 :	 Pho_EB_SR
		}

		
		##-----------  << CR-ZZA >>
		N_muon=0
		if ak.sum(ak.num(Muon)) != 0:
			N_muon = ak.num(Muon)
		
		is4lep = (N_muon +ak.num(Electron)) == 4
		Zmass_window_mask = ak.firsts(abs(Triple_eee.p4.mass - 91.1876)) < 15


		if dataset == "FakeLepton":
			MET_mask = MET > 30
		else:
			MET_mask = MET.pt > 30

		bjet_veto = ak.num(Jet) == 0
		CR_ZZA_mask = (is4lep & Zmass_window_mask & MET_mask & bjet_veto)
		
		CR_ZZA_mask					= Baseline_mask & CR_ZZA_mask
		Triple_eee_CR_ZZA			= Triple_eee[CR_ZZA_mask]
		leading_pho_CR_ZZA			= leading_pho[CR_ZZA_mask]
		MET_CR_ZZA					= MET[CR_ZZA_mask]
		Jet_CR_ZZA					= Jet[CR_ZZA_mask]
		events_CR_ZZA				= events[CR_ZZA_mask]
		Pho_EE_CR_ZZA				= leading_pho[isEE_mask & CR_ZZA_mask]
		Pho_EB_CR_ZZA				= leading_pho[isEB_mask & CR_ZZA_mask]

		CR_ZZA_arr_dict ={
			"Triple_eee_sel" :   Triple_eee_CR_ZZA
			,"leading_pho_sel":  leading_pho_CR_ZZA
			,"MET_sel"		 :	 MET_CR_ZZA
			,"Pho_EE_sel"	 :	 Pho_EE_CR_ZZA
			,"Pho_EB_sel"	 :	 Pho_EB_CR_ZZA
		}


 		##-----------  << LowMET >>
		Zmass_window_mask = ak.firsts(abs(Triple_eee.p4.mass - 91.1876)) <= 15

		if dataset == "FakeLepton":
			MET_mask = MET <= 20
		else:
			MET_mask = MET.pt <= 20

		bjet_veto = ak.num(Jet) == 0
		#Mlll_mask = ak.firsts((Triple_eee.p4 + Triple_eee.lep3).mass) > 100
		
		if ak.sum(ak.num(vetoMuon)) != 0:
			print("What?!!!!!! another lepton! Muon!")
			Muon_veto = ak.num(vetoMuon) == 0
			#CR_ZJets_mask = (Muon_veto & Zmass_window_mask & MET_mask & bjet_veto & Mlll_mask)
			CR_ZJets_mask = (Muon_veto & Zmass_window_mask & MET_mask & bjet_veto)
		else:
			#CR_ZJets_mask = (Zmass_window_mask & MET_mask & bjet_veto & Mlll_mask)
			CR_ZJets_mask = (Zmass_window_mask & MET_mask & bjet_veto)

		CR_ZJets_mask					= Baseline_mask & CR_ZJets_mask
		Triple_eee_CR_ZJets				= Triple_eee[CR_ZJets_mask]
		leading_pho_CR_ZJets			= leading_pho[CR_ZJets_mask]
		MET_CR_ZJets					= MET[CR_ZJets_mask]
		Jet_CR_ZJets					= Jet[CR_ZJets_mask]
		events_CR_ZJets					= events[CR_ZJets_mask]
		Pho_EE_CR_ZJets					= leading_pho[isEE_mask & CR_ZJets_mask]
		Pho_EB_CR_ZJets					= leading_pho[isEB_mask & CR_ZJets_mask]


		CR_ZJets_arr_dict ={
			"Triple_eee_sel" :   Triple_eee_CR_ZJets
			,"leading_pho_sel":  leading_pho_CR_ZJets
			,"MET_sel"		 :	 MET_CR_ZJets
			,"Pho_EE_sel"	 :	 Pho_EE_CR_ZJets
			,"Pho_EB_sel"	 :	 Pho_EB_CR_ZJets
		}
		
		
		##-----------  << CR-T-enriched >>
		Zmass_window_mask = ak.firsts(abs(Triple_eee.p4.mass - 91.1876)) > 5

		if dataset == "FakeLepton":
			MET_mask = MET > 30
		else:
			MET_mask = MET.pt > 30

		bjet_veto = ak.num(Jet) == 0
		#Mlll_mask = ak.firsts((Triple_eee.p4 + Triple_eee.lep3).mass) > 100
		
		if ak.sum(ak.num(vetoMuon)) != 0:
			Muon_veto = ak.num(vetoMuon) == 0
			CR_Tenri_mask = (Muon_veto & Zmass_window_mask & MET_mask & bjet_veto)
			
		else:
			CR_Tenri_mask = (Zmass_window_mask & MET_mask & bjet_veto)
		
		CR_Tenri_mask			= Baseline_mask & CR_Tenri_mask
		Triple_eee_CR_t			= Triple_eee[CR_Tenri_mask]
		leading_pho_CR_t		= leading_pho[CR_Tenri_mask]
		MET_CR_t				= MET[CR_Tenri_mask]
		Jet_CR_t				= Jet[CR_Tenri_mask]
		events_CR_t 			= events[CR_Tenri_mask]
		Pho_EE_CR_t				= leading_pho[isEE_mask & CR_Tenri_mask]
		Pho_EB_CR_t				= leading_pho[isEB_mask & CR_Tenri_mask]
		
		CR_tEnriched_arr_dict ={
			"Triple_eee_sel" :   Triple_eee_CR_t
			,"leading_pho_sel":  leading_pho_CR_t
			,"MET_sel"		 :	 MET_CR_t
			,"Pho_EE_sel"	 :	 Pho_EE_CR_t
			,"Pho_EB_sel"	 :	 Pho_EB_CR_t
		}



		##-----------  << CR-Conversion >>
		Zmass_window_mask = ak.firsts(abs(Triple_eee.p4.mass - 91.1876)) > 15


		if dataset == "FakeLepton":
			MET_mask = MET <= 30
		else:
			MET_mask = MET.pt <= 30


		bjet_veto = ak.num(Jet) == 0
		#Mlll_mask = ak.firsts((Triple_eee.p4 + Triple_eee.lep3).mass) <= 100

		if ak.sum(ak.num(vetoMuon)) != 0:
			Muon_veto = ak.num(vetoMuon) == 0
			CR_conv_mask = (Muon_veto & Zmass_window_mask & MET_mask & bjet_veto)

		else:
			CR_conv_mask = (Zmass_window_mask & MET_mask & bjet_veto)


		CR_conv_mask		= Baseline_mask & CR_conv_mask
		Triple_eee_CR_conv	= Triple_eee[CR_conv_mask]
		leading_pho_CR_conv = leading_pho[CR_conv_mask]
		MET_CR_conv			= MET[CR_conv_mask]
		Jet_CR_conv			= Jet[CR_conv_mask]
		events_CR_conv		= events[CR_conv_mask]
		Pho_EE_CR_conv		= leading_pho[isEE_mask & CR_conv_mask]
		Pho_EB_CR_conv		= leading_pho[isEB_mask & CR_conv_mask]
	

		CR_Conversion_dict ={
			"Triple_eee_sel" :   Triple_eee_CR_conv
			,"leading_pho_sel":  leading_pho_CR_conv
			,"MET_sel"		 :	 MET_CR_conv
			,"Pho_EE_sel"	 :	 Pho_EE_CR_conv
			,"Pho_EB_sel"	 :	 Pho_EB_CR_conv
		}
		
		## -------------------- Prepare making hist --------------#

		regions = {
			"Baseline"		 :	base_arr_dict
			,"Signal"		 :	SR_arr_dict
			,"CR_ZZA"		 :	CR_ZZA_arr_dict
			,"CR_ZJets"		 :	CR_ZJets_arr_dict
			,"CR_tEnriched"	 :	CR_tEnriched_arr_dict
			,"CR_conversion" :	CR_Conversion_dict
		}
	
		mask_dict = {
			"Baseline"		 : Baseline_mask  
			,"Signal"		 : SR_mask
			,"CR_ZZA"		 : CR_ZZA_mask
			,"CR_ZJets"		 : CR_ZJets_mask
			,"CR_tEnriched"	 : CR_Tenri_mask
			,"CR_conversion" : CR_conv_mask
		}


		for region,arr_dict in regions.items():
		

			# Do not consider no-evt 
			# Stop processing if there is no event remain
			#if len(arr_dict['MET_sel']) == 0:
			#	continue
			
			# Photon
			phoPT = ak.flatten(arr_dict["leading_pho_sel"].pt)
			phoEta = ak.flatten(arr_dict["leading_pho_sel"].eta)
			phoPhi = ak.flatten(arr_dict["leading_pho_sel"].phi)

			# Photon EE
			if len(arr_dict["Pho_EE_sel"].pt) != 0:
				Pho_EE_PT = ak.flatten(arr_dict["Pho_EE_sel"].pt)
				Pho_EE_Eta = ak.flatten(arr_dict["Pho_EE_sel"].eta)
				Pho_EE_Phi = ak.flatten(arr_dict["Pho_EE_sel"].phi)
				Pho_EE_sieie = ak.flatten(arr_dict["Pho_EE_sel"].sieie)
				Pho_EE_Iso_charge = ak.flatten(arr_dict["Pho_EE_sel"].pfRelIso03_chg)

			# Photon EB
			if len(arr_dict["Pho_EB_sel"].pt) != 0:
				Pho_EB_PT  = ak.flatten(arr_dict["Pho_EB_sel"].pt)
				Pho_EB_Eta = ak.flatten(arr_dict["Pho_EB_sel"].eta)
				Pho_EB_Phi = ak.flatten(arr_dict["Pho_EB_sel"].phi)
				Pho_EB_sieie = ak.flatten(arr_dict["Pho_EB_sel"].sieie)
				Pho_EB_Iso_charge = ak.flatten(arr_dict["Pho_EB_sel"].pfRelIso03_chg)

			# Electrons
			ele1PT  = ak.flatten(arr_dict["Triple_eee_sel"].lep1.pt)
			ele1Eta = ak.flatten(arr_dict["Triple_eee_sel"].lep1.eta)
			ele1Phi = ak.flatten(arr_dict["Triple_eee_sel"].lep1.phi)
			ele2PT  = ak.flatten(arr_dict["Triple_eee_sel"].lep2.pt)
			ele2Eta = ak.flatten(arr_dict["Triple_eee_sel"].lep2.eta)
			ele2Phi = ak.flatten(arr_dict["Triple_eee_sel"].lep2.phi)
			ele3PT  = ak.flatten(arr_dict["Triple_eee_sel"].lep3.pt)
			ele3Eta = ak.flatten(arr_dict["Triple_eee_sel"].lep3.eta)
			ele3Phi = ak.flatten(arr_dict["Triple_eee_sel"].lep3.phi)

			# MET
			if dataset == "FakeLepton":
				met = arr_dict["MET_sel"]
			else:
				met = arr_dict["MET_sel"].pt

			# M(eea) M(ee)
			diele = arr_dict["Triple_eee_sel"].p4
			lll_vec = diele + arr_dict["Triple_eee_sel"].lep3
			Mlll = ak.flatten(lll_vec.mass)
			Mee = ak.flatten(arr_dict["Triple_eee_sel"].p4.mass)

			## W MT (--> beta )
			#Ele3 = ak.flatten(arr_dict["Triple_eee_sel"].lep3)
			#MT = np.sqrt(
			#	2 * Ele3.pt * arr_dict["MET_sel"].pt * (1 - np.cos(abs(arr_dict["MET_sel"].delta_phi(Ele3))))
			#)
			#MT = np.array(MT)

			# --- Apply weight and hist
			weights = processor.Weights(len(cut4))

			def skim_weight(arr):
				mask1 = ~ak.is_none(arr)
				subarr = arr[mask1]
				mask2 = subarr != 0
				return ak.to_numpy(subarr[mask2])

			cuts = mask_dict[region]
			cuts_pho_EE = ak.flatten(isEE_mask)
			cuts_pho_EB = ak.flatten(isEB_mask)

			if isFake:
				weights.add("fake_fraction", fw)


			if dataset == "FakeLepton":
				weights.add("fake_lepton_weight",fake_lep_w)

			else:
				# Weight and SF here
				if not (isData | isFake):
					weights.add("pileup", pu)
					weights.add("ele_id", ele_medium_id_sf)
					weights.add("pho_id", pho_medium_id_sf)
					weights.add("ele_reco", ele_reco_sf)
					weights.add("ele_trigger", ele_trig_weight)

			# ---------------------------- Fill hist --------------------------------------#

			
			# Merger dataset
			
			if isFake:
				dataset = "FakePhoton"
 
			else:
				if ((dataset == "SingleMuon") or (dataset =="DoubleMuon") or (dataset =="Egamma") or (dataset =="MuonEG")):
					dataset = "Data"
				
			
			out["sumw"][dataset] += len(Initial_events)

			print(
				"region: {0} ###  cut0: {1},cut1: {2},cut2: {3},cut3: {4},cut4: {5},cut5: {6}, cut6: {7}".format(
					region,
					len(cut0),
					len(cut1),
					len(cut2),
					len(cut3),
					len(cut4),
					len(cut5),
					len(met),
				)
			)

			# Fill hist

			# -- met -- #
			out["met"].fill(
				dataset=dataset, region = region, met=met,weight=skim_weight(weights.weight() * cuts)
			)

			# --mass -- #
			#out["MT"].fill(
			#	dataset=dataset, region = region,MT=MT, weight=skim_weight(weights.weight() * cuts)
			#)
			out["mass"].fill(
				dataset=dataset, region = region,mass=Mee, weight=skim_weight(weights.weight() * cuts)
			)
			out["mass_lll"].fill(
				dataset=dataset, region = region,mass_lll=Mlll, weight=skim_weight(weights.weight() * cuts)
			)

			# -- Electron -- #
			out["ele1pt"].fill(
				dataset=dataset, region = region,ele1pt=ele1PT, weight=skim_weight(weights.weight() * cuts)
			)
			out["ele1eta"].fill(
				dataset=dataset,
				region=region,
				ele1eta=ele1Eta,
				weight=skim_weight(weights.weight() * cuts),
			)
			out["ele1phi"].fill(
				dataset=dataset,
				region=region,
				ele1phi=ele1Phi,
				weight=skim_weight(weights.weight() * cuts),
			)
			out["ele2pt"].fill(
				dataset=dataset, region=region, ele2pt=ele2PT, weight=skim_weight(weights.weight() * cuts)
			)
			out["ele2eta"].fill(
				dataset=dataset,
				region=region,
				ele2eta=ele2Eta,
				weight=skim_weight(weights.weight() * cuts),
			)
			out["ele2phi"].fill(
				dataset=dataset,
				region=region,
				ele2phi=ele2Phi,
				weight=skim_weight(weights.weight() * cuts),
			)
			out["ele3pt"].fill(
				dataset=dataset, region=region, ele3pt=ele3PT, weight=skim_weight(weights.weight() * cuts)
			)

			# -- Photon -- #

			out["phopt"].fill(
				dataset=dataset,region=region,  phopt=phoPT, weight=skim_weight(weights.weight() * cuts)
			)
			out["phoeta"].fill(
				dataset=dataset,region=region,  phoeta=phoEta, weight=skim_weight(weights.weight() * cuts)
			)
			out["phophi"].fill(
				dataset=dataset,region=region,  phophi=phoPhi, weight=skim_weight(weights.weight() * cuts)
			)

			if len(arr_dict["Pho_EE_sel"].pt) != 0:

				out["pho_EE_pt"].fill(
					dataset=dataset,
					region=region,
					pho_EE_pt=Pho_EE_PT,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EE),
				)
				out["pho_EE_eta"].fill(
					dataset=dataset,
					region=region,
					pho_EE_eta=Pho_EE_Eta,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EE),
				)
				out["pho_EE_phi"].fill(
					dataset=dataset,
					region=region,
					pho_EE_phi=Pho_EE_Phi,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EE),
				)
				out["pho_EE_sieie"].fill(
					dataset=dataset,
					region=region,
					pho_EE_sieie=Pho_EE_sieie,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EE),
				)
				out["pho_EE_Iso_chg"].fill(
					dataset=dataset,
					region=region,
					pho_EE_Iso_chg=Pho_EE_Iso_charge,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EE),
				)

			if len(arr_dict["Pho_EB_sel"].pt) != 0:
				out["pho_EB_pt"].fill(
					dataset=dataset,
					region=region,
					pho_EB_pt=Pho_EB_PT,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EB),
				)
				out["pho_EB_eta"].fill(
					dataset=dataset,
					region=region,
					pho_EB_eta=Pho_EB_Eta,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EB),
				)
				out["pho_EB_phi"].fill(
					dataset=dataset,
					region=region,
					pho_EB_phi=Pho_EB_Phi,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EB),
				)
				out["pho_EB_sieie"].fill(
					dataset=dataset,
					region=region,
					pho_EB_sieie=Pho_EB_sieie,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EB),
				)
				out["pho_EB_Iso_chg"].fill(
					dataset=dataset,
					region=region,
					pho_EB_Iso_chg=Pho_EB_Iso_charge,
					weight=skim_weight(weights.weight() * cuts * cuts_pho_EB),
				)

		return out

	# -- Finally! return accumulator
	def postprocess(self, accumulator):

		return accumulator


# <---- Class JW_Processor


if __name__ == "__main__":

	start = time.time()
	parser = argparse.ArgumentParser()

	parser.add_argument("--nWorker", type=int, help=" --nWorker 2", default=8)
	parser.add_argument("--metadata", type=str, help="--metadata xxx.json")
	parser.add_argument(
		"--dataset", type=str, help="--dataset ex) Egamma_Run2018A_280000"
	)
	parser.add_argument("--year", type=str, help="--year 2018", default="2017")
	parser.add_argument("--isdata", type=bool, help="--isdata True", default=False)
	parser.add_argument("--isFake", type=bool, help="--isFake True", default=False)
	args = parser.parse_args()

	## Prepare files
	N_node = args.nWorker
	metadata = args.metadata
	data_sample = args.dataset
	year = args.year
	isdata = args.isdata
	isFake = args.isFake

	## Json file reader
	with open(metadata) as fin:
		datadict = json.load(fin)

	filelist = glob.glob(datadict[data_sample])

	sample_name = data_sample.split("_")[0]



	corr_file = "../Corrections/corrections.coffea"
	# corr_file = "corrections.coffea" # Condor-batch

	corrections = load(corr_file)

	## Read PU weight file

	if not isdata:
		pu_path_dict = {
			"DY": "mcPileupDist_DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8.npy",
			"TTWJets": "mcPileupDist_TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8.npy",
			"TTZtoLL": "mcPileupDist_TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8.npy",
			"WW": "mcPileupDist_WW_TuneCP5_DoubleScattering_13TeV-pythia8.npy",
			"WZ": "mcPileupDist_WZ_TuneCP5_13TeV-pythia8.npy",
			"ZZ": "mcPileupDist_ZZ_TuneCP5_13TeV-pythia8.npy",
			"tZq": "mcPileupDist_tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8.npy",
			"WZG": "mcPileupDist_wza_UL18_sum.npy",
			"ZGToLLG": "mcPileupDist_ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8.npy",
			"TTGJets": "mcPileupDist_TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8.npy",
			"WGToLNuG": "mcPileupDist_WGToLNuG_01J_5f_PtG_120_TuneCP5_13TeV-amcatnloFXFX-pythia8.npy",
		}

		if year == "2018":
			pu_path = "../Corrections/Pileup/puWeight/npy_UL_Run2018/"+ pu_path_dict[sample_name]
			


		if year == "2017":
			pu_path = (
				"../Corrections/Pileup/puWeight/npy_Run2017/"
				+ pu_path_dict[sample_name]
			)  # 2017

		print("Use the PU file: ", pu_path)
		with open(pu_path, "rb") as f:
			pu = np.load(f)

	else:
		pu = -1

	print("Processing the sample: ", sample_name)
	samples = {sample_name: filelist}

	# Class -> Object
	JW_Processor_instance = JW_Processor(year, sample_name, pu, corrections, isFake)

	## -->Multi-node Executor
	result = processor.run_uproot_job(
		samples,  # dataset
		"Events",  # Tree name
		JW_Processor_instance,  # Class
		executor=processor.futures_executor,
		executor_args={"schema": NanoAODSchema, "workers": 56},
		# maxchunks=4,
	)

	if isFake:
		outname =  "FaktePhoton_" + data_sample + ".futures"
	elif ((sample_name == "SingleMuon") or (sample_name == "DoubleMuon") or (sample_name =="Egamma") or (sample_name =="MuonEG")):
		outname = "Data_" + data_sample + ".futures"
	else:
		outname = data_sample + ".futures"
	# outname = 'DY_test.futures'
	save(result, outname)

	elapsed_time = time.time() - start
	print("Time: ", elapsed_time)
