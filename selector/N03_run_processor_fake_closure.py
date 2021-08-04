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
import numba

# -- Coffea 0.8.0 --> Must fix!!
import warnings

warnings.filterwarnings("ignore")


# ---> Class JW Processor
class JW_Processor(processor.ProcessorABC):

	# -- Initializer
	def __init__(self, year, sample_name):

		# Parameter set
		self._year = year

		# Trigger set
		self._doubleelectron_triggers = {
			"2018": [
				"Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",  # Recomended
			],
			"2017": [
				"Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",  # Recomended
			],
		}

		self._singleelectron_triggers = (
			{  # 2017 and 2018 from monojet, applying dedicated trigger weights
				"2016": ["Ele27_WPTight_Gsf", "Ele105_CaloIdVT_GsfTrkIdT"],
				"2017": ["Ele35_WPTight_Gsf", "Ele115_CaloIdVT_GsfTrkIdT", "Photon200"],
				"2018": [
					"Ele32_WPTight_Gsf",  # Recomended
				],
			}
		)

		# hist set
		self._accumulator = processor.dict_accumulator(
			{
				"sumw": processor.defaultdict_accumulator(float),

				"phoIsoChg": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("phoIsoChg", "Photon IsoChg*$p_{T}$", 50, 3, 11),

				),
				"pho_EB_sieie": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("pho_EB_sieie", "Photon EB sieie", 200, 0, 0.1),
				),
				# -- Sieie bins -- #
				"PT_1_eta_1": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("PT_1_eta_1", "20 < pt <30 & |eta| < 1", 200, 0, 0.02),
				),
				"PT_1_eta_2": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_1_eta_2", "20 < pt <30 & 1 < |eta| < 1.5", 200, 0, 0.02
					),
				),
				"PT_1_eta_3": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_1_eta_3", "20 < pt <30 & 1.5 < |eta| < 2", 200, 0, 0.05
					),
				),
				"PT_1_eta_4": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_1_eta_4", "20 < pt <30 & 2 < |eta| < 2.5", 200, 0, 0.05
					),
				),
				"PT_2_eta_1": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("PT_2_eta_1", "30 < pt <40 & |eta| < 1", 200, 0, 0.02),
				),
				"PT_2_eta_2": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_2_eta_2", "30 < pt <40 & 1 < |eta| < 1.5", 200, 0, 0.02
					),
				),
				"PT_2_eta_3": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_2_eta_3", "30 < pt <40 & 1.5 < |eta| < 2", 200, 0, 0.05
					),
				),
				"PT_2_eta_4": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_2_eta_4", "30 < pt <40 & 2 < |eta| < 2.5", 200, 0, 0.05
					),
				),
				"PT_3_eta_1": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("PT_3_eta_1", "40 < pt <50 & |eta| < 1", 200, 0, 0.02),
				),
				"PT_3_eta_2": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_3_eta_2", "40 < pt <50 & 1 < |eta| < 1.5", 200, 0, 0.02
					),
				),
				"PT_3_eta_3": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_3_eta_3", "40 < pt <50 & 1.5 < |eta| < 2", 200, 0, 0.05
					),
				),
				"PT_3_eta_4": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin(
						"PT_3_eta_4", "40 < pt <50 & 2 < |eta| < 2.5", 200, 0, 0.05
					),
				),
				"PT_4_eta_1": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("PT_4_eta_1", "50 < pt & |eta| < 1", 200, 0, 0.02),
				),
				"PT_4_eta_2": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("PT_4_eta_2", "50 <pt  & 1 < |eta| < 1.5", 200, 0, 0.02),
				),
				"PT_4_eta_3": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("PT_4_eta_3", "50 < pt  & 1.5 < |eta| < 2", 200, 0, 0.05),
				),
				"PT_4_eta_4": hist.Hist(
					"Events",
					hist.Cat("dataset", "Dataset"),
					hist.Cat("Closure_bin", "Closure_bin"),
					hist.Bin("PT_4_eta_4", "50 < pt  & 2 < |eta| < 2.5", 200, 0, 0.05),
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

		# Stop processing if there is no event remain
		if len(events) == 0:
			return out

		# Cut flow
		cut0 = np.zeros(len(events))

		# <----- Helper functions ------>#

		# Sort by PT helper function
		def sort_by_pt(ele, pho, jet):
			ele = ele[ak.argsort(ele.pt, ascending=False, axis=1)]
			pho = pho[ak.argsort(pho.pt, ascending=False, axis=1)]
			jet = jet[ak.argsort(jet.pt, ascending=False, axis=1)]

			return ele, pho, jet

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

		# Cut-based ID modification
		@numba.njit
		def PhotonVID(vid, idBit):
			rBit = 0
			for x in range(0, 7):
				rBit |= (1 << x) if ((vid >> (x * 2)) & 0b11 >= idBit) else 0
			return rBit

		# Inverse Sieie and upper limit
		@numba.njit
		def make_fake_obj_mask(Pho, builder):

			# for eventIdx,pho in enumerate(tqdm(Pho)):   # --Event Loop
			for eventIdx, pho in enumerate(Pho):
				builder.begin_list()
				if len(pho) < 1:
					continue

				for phoIdx, _ in enumerate(pho):  # --Photon Loop

					vid = Pho[eventIdx][phoIdx].vidNestedWPBitmap
					vid_cuts1 = PhotonVID(vid, 1)  # Loose photon
					vid_cuts2 = PhotonVID(vid, 2)  # Medium photon
					vid_cuts3 = PhotonVID(vid, 3)  # Tight photon

					# Field name
					# |0|0|0|0|0|0|0|
					# |IsoPho|IsoNeu|IsoChg|Sieie|hoe|scEta|PT|

					# 1. Turn off cut (ex turn off Sieie
					# |1|1|1|0|1|1|1| = |1|1|1|0|1|1|1|

					# 2. Inverse cut (ex inverse Sieie)
					# |1|1|1|1|1|1|1| = |1|1|1|0|1|1|1|

					# if (vid_cuts2 & 0b1111111 == 0b1111111): # Cut applied
					#if vid_cuts2 & 0b1111111 == 0b1110111:  # Inverse Sieie
					if (vid_cuts2 & 0b1100111 == 0b1100111): # Without Sieie and IsoChg
						builder.boolean(True)
					else:
						builder.boolean(False)

				builder.end_list()

			return builder


		# Golden Json file
		if self._year == "2018":
			injson = "/x5/cms/jwkim/gitdir/JWCorp/JW_analysis/Coffea_WZG/Corrections/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt.RunABD"

		if self._year == "2017":
			injson = "/x5/cms/jwkim/gitdir/JWCorp/JW_analysis/Coffea_WZG/Corrections/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"

		# --- Selection
		Initial_events = events
		isData =  "genWeight" not in events.fields



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

		##----------- Cut flow1: Passing Triggers

		# double lepton trigger
		is_double_ele_trigger = True
		if not is_double_ele_trigger:
			double_ele_triggers_arr = np.ones(len(events), dtype=np.bool)
		else:
			double_ele_triggers_arr = np.zeros(len(events), dtype=np.bool)
			for path in self._doubleelectron_triggers[self._year]:
				if path not in events.HLT.fields:
					continue
				double_ele_triggers_arr = double_ele_triggers_arr | events.HLT[path]

		# single lepton trigger
		is_single_ele_trigger = True
		if not is_single_ele_trigger:
			single_ele_triggers_arr = np.ones(len(events), dtype=np.bool)
		else:
			single_ele_triggers_arr = np.zeros(len(events), dtype=np.bool)
			for path in self._singleelectron_triggers[self._year]:
				if path not in events.HLT.fields:
					continue
				single_ele_triggers_arr = single_ele_triggers_arr | events.HLT[path]

		events.Electron, events.Photon, events.Jet = sort_by_pt(
			events.Electron, events.Photon, events.Jet
		)

		# Apply cut1
		Initial_events = events
		# events = events[single_ele_triggers_arr | double_ele_triggers_arr]
		events = events[double_ele_triggers_arr]

		cut1 = np.ones(len(events))

		# Set Particles
		Electron = events.Electron
		Muon = events.Muon
		Photon = events.Photon
		MET = events.MET
		Jet = events.Jet

		# Stop processing if there is no event remain
		if len(Electron) == 0:
			return out

		#  --Muon ( only used to calculate dR )
		MuSelmask = (
			(Muon.pt >= 10)
			& (abs(Muon.eta) <= 2.5)
			& (Muon.tightId)
			& (Muon.pfRelIso04_all < 0.15)
		)
		# Muon = ak.mask(Muon,MuSelmask)
		Muon = Muon[MuSelmask]


		##----------- Cut flow2: Electron Selection

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

		# apply cut 2
		Tri_electron_mask = ak.num(Electron) >= 2
		Electron = Electron[Tri_electron_mask]
		Photon = Photon[Tri_electron_mask]
		Jet = Jet[Tri_electron_mask]
		MET = MET[Tri_electron_mask]
		Muon = Muon[Tri_electron_mask]
		events = events[Tri_electron_mask]

		# Stop processing if there is no event remain
		if len(Electron) == 0:
			return out

		cut2 = np.ones(len(Photon)) * 2


		##----------- Cut flow3: Photon Selection

		# Basic photon selection
		isgap_mask = (abs(Photon.eta) < 1.442) | (
			(abs(Photon.eta) > 1.566) & (abs(Photon.eta) < 2.5)
		)
		Pixel_seed_mask = ~Photon.pixelSeed
		PT_mask = Photon.pt >= 20

		# dR cut with selected Muon and Electrons
		dr_pho_ele_mask = ak.all(
			Photon.metric_table(Electron) >= 0.5, axis=-1
		)  # default metric table: delta_r
		dr_pho_mu_mask = ak.all(Photon.metric_table(Muon) >= 0.5, axis=-1)


		# Apply cut -Prompt photon-
		if not isData:

			# X+A MCs : prompt only
			if 'G' in dataset:
				genPartFlav_mask =  (Photon.genPartFlav == 1)
				PhoSelmask = (genPartFlav_mask & PT_mask & isgap_mask & Pixel_seed_mask & dr_pho_ele_mask & dr_pho_mu_mask)
			# others : non-prompt only
			else:
				genPartFlav_mask =  (Photon.genPartFlav == 1)
				PhoSelmask = (~genPartFlav_mask & PT_mask & isgap_mask & Pixel_seed_mask & dr_pho_ele_mask & dr_pho_mu_mask)
				
		else:
			PhoSelmask = (PT_mask & isgap_mask & Pixel_seed_mask & dr_pho_ele_mask & dr_pho_mu_mask)

		Photon = Photon[PhoSelmask]
		
		# Apply cut 3
		A_photon_mask = ak.num(Photon) > 0
		Electron = Electron[A_photon_mask]
		Photon = Photon[A_photon_mask]
		Jet = Jet[A_photon_mask]
		Muon = Muon[A_photon_mask]
		MET = MET[A_photon_mask]
		events = events[A_photon_mask]



		# ID for fake photon
		Photon_template_mask = make_fake_obj_mask(Photon, ak.ArrayBuilder()).snapshot()

		Photon = Photon[Photon_template_mask]
		# Apply cut -Fake Photon -
		A_photon_mask = ak.num(Photon) > 0
		Electron = Electron[A_photon_mask]
		Photon = Photon[A_photon_mask]
		Jet = Jet[A_photon_mask]
		Muon = Muon[A_photon_mask]
		MET = MET[A_photon_mask]
		events = events[A_photon_mask]


		# Stop processing if there is no event remain
		if len(Electron) == 0:
			return out

		cut3 = np.ones(len(Photon)) *  3

		##-----------  Cut flow4:  Select 2 OSSF electrons from Z
		@numba.njit
		def find_2lep(events_leptons, builder):
			for leptons in events_leptons:

				builder.begin_list()
				nlep = len(leptons)
				for i0 in range(nlep):
					for i1 in range(i0 + 1, nlep):
						if leptons[i0].charge + leptons[i1].charge != 0:
							continue

						if nlep == 2:
							builder.begin_tuple(2)
							builder.index(0).integer(i0)
							builder.index(1).integer(i1)
							builder.end_tuple()

						else:
							for i2 in range(nlep):
								if len({i0, i1, i2}) < 3:
									continue
								builder.begin_tuple(3)
								builder.index(0).integer(i0)
								builder.index(1).integer(i1)
								builder.index(2).integer(i2)
								builder.end_tuple()
				builder.end_list()
			return builder

		ossf_idx = find_2lep(Electron, ak.ArrayBuilder()).snapshot()

		# OSSF cut
		ossf_mask = ak.num(ossf_idx) >= 1
		ossf_idx = ossf_idx[ossf_mask]
		Electron = Electron[ossf_mask]
		Photon = Photon[ossf_mask]
		Jet = Jet[ossf_mask]
		MET = MET[ossf_mask]

		Double_electron = [Electron[ossf_idx[idx]] for idx in "01"]
		from coffea.nanoevents.methods import vector

		ak.behavior.update(vector.behavior)

		Diele = ak.zip(
			{
				"lep1": Double_electron[0],
				"lep2": Double_electron[1],
				"p4": TLorentz_vector(Double_electron[0] + Double_electron[1]),
			}
		)

		bestZ_idx = ak.singletons(ak.argmin(abs(Diele.p4.mass - 91.1876), axis=1))
		Diele = Diele[bestZ_idx]

		cut4 = np.ones(len(Electron)) * 4



		# --- Charged isolation * PT range for closure test
		
		low_isochg  = list(range(3,9,1))
		high_isochg = list(range(8,14,1))
		for low in low_isochg:
			for high in high_isochg:
				isoChg	  = Photon.pfRelIso03_chg* Photon.pt
				isoChg_mask =  (isoChg >= low) & (isoChg <= high)


				Sel_Photon      = Photon[isoChg_mask]
				Photon_evt_mask = (ak.num(Sel_Photon) >= 1)
				
				Electron_sel = Electron[Photon_evt_mask]
				Photon_sel   = Sel_Photon[Photon_evt_mask]
				Jet_sel      = Jet[Photon_evt_mask]
				MET_sel      = MET[Photon_evt_mask]
				Diele_sel    = Diele[Photon_evt_mask]
				

				Closure_bin = 'from_' + str(low) + '_to_' +str(high)
				

				##-----------  Cut flow 5: Event Selection
				
				def make_leading_pair(target, base):
					return target[ak.argmax(base.pt, axis=1, keepdims=True)]
				leading_pho_sel = make_leading_pair(Photon_sel, Photon_sel)
		
				# Mee cut
				Mee_cut_mask = ak.firsts(Diele_sel.p4.mass) > 4
		
				# Electron PT cuts
				Elept_mask = ak.firsts((Diele_sel.lep1.pt >= 25) & (Diele_sel.lep2.pt >= 20))
		
				# MET cuts
				MET_mask = MET_sel.pt > 20
				
				# --------Mask -------#
				Event_sel_mask   = Mee_cut_mask & Elept_mask & MET_mask
				Diele_base       = Diele_sel[Event_sel_mask]
				leading_pho_base = leading_pho_sel[Event_sel_mask]
				Jet_base		 = Jet_sel[Event_sel_mask]
				MET_base		 = MET_sel[Event_sel_mask]
		
				cut5 = np.ones(len(MET_base)) * 5
		
				#print('cutflow: ',len(cut1),len(cut2),len(cut3),len(cut4),len(cut5))

				# -------------------- Flatten variables ---------------------------#
		
		
				# -- Pho -- #
				Pho_PT	   = ak.flatten(leading_pho_base.pt)
				Pho_IsoChg = ak.flatten(leading_pho_base.pt * leading_pho_base.pfRelIso03_chg)
		
				
		
				# -------------------- Sieie bins---------------------------#
				def make_bins(pt, eta, sieie, bin_range_str):
		
					bin_dict = {
						"PT_1_eta_1": (pt > 20) & (pt < 30) & (eta < 1),
						"PT_1_eta_2": (pt > 20) & (pt < 30) & (eta > 1) & (eta < 1.5),
						"PT_1_eta_3": (pt > 20) & (pt < 30) & (eta > 1.5) & (eta < 2),
						"PT_1_eta_4": (pt > 20) & (pt < 30) & (eta > 2) & (eta < 2.5),
						"PT_2_eta_1": (pt > 30) & (pt < 40) & (eta < 1),
						"PT_2_eta_2": (pt > 30) & (pt < 40) & (eta > 1) & (eta < 1.5),
						"PT_2_eta_3": (pt > 30) & (pt < 40) & (eta > 1.5) & (eta < 2),
						"PT_2_eta_4": (pt > 30) & (pt < 40) & (eta > 2) & (eta < 2.5),
						"PT_3_eta_1": (pt > 40) & (pt < 50) & (eta < 1),
						"PT_3_eta_2": (pt > 40) & (pt < 50) & (eta > 1) & (eta < 1.5),
						"PT_3_eta_3": (pt > 40) & (pt < 50) & (eta > 1.5) & (eta < 2),
						"PT_3_eta_4": (pt > 40) & (pt < 50) & (eta > 2) & (eta < 2.5),
						"PT_4_eta_1": (pt > 50) & (eta < 1),
						"PT_4_eta_2": (pt > 50) & (eta > 1) & (eta < 1.5),
						"PT_4_eta_3": (pt > 50) & (eta > 1.5) & (eta < 2),
						"PT_4_eta_4": (pt > 50) & (eta > 2) & (eta < 2.5),
					}
		
					binmask = bin_dict[bin_range_str]
		
					return ak.to_numpy(sieie[binmask])
		
				bin_name_list = [
					"PT_1_eta_1",
					"PT_1_eta_2",
					"PT_1_eta_3",
					"PT_1_eta_4",
					"PT_2_eta_1",
					"PT_2_eta_2",
					"PT_2_eta_3",
					"PT_2_eta_4",
					"PT_3_eta_1",
					"PT_3_eta_2",
					"PT_3_eta_3",
					"PT_3_eta_4",
					"PT_4_eta_1",
					"PT_4_eta_2",
					"PT_4_eta_3",
					"PT_4_eta_4",
				]
		
				binned_sieie_hist = {}
				for name in bin_name_list:
					binned_sieie_hist[name] = make_bins(
						ak.flatten(leading_pho_base.pt),
						ak.flatten(abs(leading_pho_base.eta)),
						ak.flatten(leading_pho_base.sieie),
						name,
					)
		
				# -------------------- Fill hist ---------------------------#
		
				# Initial events
				out["sumw"][dataset] += len(Initial_events)
		
				out["phoIsoChg"].fill(dataset=dataset,phoIsoChg=Pho_IsoChg,
				Closure_bin=Closure_bin)
		
				# -- Binned sieie hist -- #
		
				if len(binned_sieie_hist["PT_1_eta_1"] > 0):
					out["PT_1_eta_1"].fill(
						dataset=dataset, PT_1_eta_1=binned_sieie_hist["PT_1_eta_1"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_1_eta_2"] > 0):
					out["PT_1_eta_2"].fill(
						dataset=dataset, PT_1_eta_2=binned_sieie_hist["PT_1_eta_2"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_1_eta_3"] > 0):
					out["PT_1_eta_3"].fill(
						dataset=dataset, PT_1_eta_3=binned_sieie_hist["PT_1_eta_3"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_1_eta_4"] > 0):
					out["PT_1_eta_4"].fill(
						dataset=dataset, PT_1_eta_4=binned_sieie_hist["PT_1_eta_4"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_2_eta_1"] > 0):
					out["PT_2_eta_1"].fill(
						dataset=dataset, PT_2_eta_1=binned_sieie_hist["PT_2_eta_1"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_2_eta_2"] > 0):
					out["PT_2_eta_2"].fill(
						dataset=dataset, PT_2_eta_2=binned_sieie_hist["PT_2_eta_2"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_2_eta_3"] > 0):
					out["PT_2_eta_3"].fill(
						dataset=dataset, PT_2_eta_3=binned_sieie_hist["PT_2_eta_3"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_2_eta_4"] > 0):
					out["PT_2_eta_4"].fill(
						dataset=dataset, PT_2_eta_4=binned_sieie_hist["PT_2_eta_4"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_3_eta_1"] > 0):
					out["PT_3_eta_1"].fill(
						dataset=dataset, PT_3_eta_1=binned_sieie_hist["PT_3_eta_1"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_3_eta_2"] > 0):
					out["PT_3_eta_2"].fill(
						dataset=dataset, PT_3_eta_2=binned_sieie_hist["PT_3_eta_2"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_3_eta_3"] > 0):
					out["PT_3_eta_3"].fill(
						dataset=dataset, PT_3_eta_3=binned_sieie_hist["PT_3_eta_3"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_3_eta_4"] > 0):
					out["PT_3_eta_4"].fill(
						dataset=dataset, PT_3_eta_4=binned_sieie_hist["PT_3_eta_4"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_4_eta_1"] > 0):
					out["PT_4_eta_1"].fill(
						dataset=dataset, PT_4_eta_1=binned_sieie_hist["PT_4_eta_1"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_4_eta_2"] > 0):
					out["PT_4_eta_2"].fill(
						dataset=dataset, PT_4_eta_2=binned_sieie_hist["PT_4_eta_2"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_4_eta_3"] > 0):
					out["PT_4_eta_3"].fill(
						dataset=dataset, PT_4_eta_3=binned_sieie_hist["PT_4_eta_3"]
						,Closure_bin=Closure_bin
					)
				if len(binned_sieie_hist["PT_4_eta_4"] > 0):
					out["PT_4_eta_4"].fill(
						dataset=dataset, PT_4_eta_4=binned_sieie_hist["PT_4_eta_4"]
						,Closure_bin=Closure_bin
					)
		
		return out

	# -- Finally! return accumulator
	def postprocess(self, accumulator):
		return accumulator


# <---- Class JW_Processor
if __name__ == "__main__":

	start = time.time()
	parser = argparse.ArgumentParser()

	parser.add_argument("--nWorker", type=int, help=" --nWorker 2", default=56)
	parser.add_argument("--metadata", type=str, help="--metadata xxx.json")
	parser.add_argument(
		"--dataset", type=str, help="--dataset ex) Egamma_Run2018A_280000"
	)
	parser.add_argument("--year", type=str, help="--year 2018", default="2017")
	parser.add_argument("--isdata", type=bool, help="--isdata False", default=False)
	args = parser.parse_args()

	## Prepare files
	N_node = args.nWorker
	metadata = args.metadata
	data_sample = args.dataset
	year = args.year

	## Json file reader
	with open(metadata) as fin:
		datadict = json.load(fin)

	filelist = glob.glob(datadict[data_sample])
	sample_name = data_sample.split('_')[0]

	print(sample_name)
	samples = {sample_name: filelist}

	# Class -> Object
	JW_Processor_instance = JW_Processor(year, sample_name)

	## -->Multi-node Executor
	result = processor.run_uproot_job(
		samples,  # dataset
		"Events",  # Tree name
		JW_Processor_instance,  # Class
		executor=processor.futures_executor,
		executor_args={"schema": NanoAODSchema, "workers": 48},
		# maxchunks=4,
	)

	# outname = data_sample + '.futures'
	outname = "Fake_template_" + data_sample + ".futures"
	save(result, outname)

	elapsed_time = time.time() - start
