#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

from PhysicsTools.NanoAODTools.postprocessing.modules.FakeLep_Apply_weight_Template_Module import *

import argparse
import re
import optparse


parser = argparse.ArgumentParser(description='create attachment NanoAOD-like fake lepton result')
parser.add_argument('-f', dest='file', default='', help='File input')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-dataset_name', dest='dataset_name',default="B", help="Run period, only work for data")


args = parser.parse_args()

if args.year == '2016':
        Modules = [ApplyWeightFakeLeptonModule16()]
if args.year == '2017':
        Modules = [ApplyWeightFakeLeptonModule17()]
if args.year == '2018':
        Modules = [ApplyWeightFakeLeptonModule18()]

infilelist = [args.file]
jsoninput = None
fwkjobreport = False

# Check weather the output directory exists
isExist = os.path.exists(args.dataset_name)
# If not.. mkdir
if not isExist:
        os.makedirs(args.dataset_name)


#p=PostProcessor(".",infilelist,
p=PostProcessor(args.dataset_name,infilelist,  # new: specify the directory following name of dataset 
                branchsel="Apply_weight_keep_and_drop.txt",
                modules=Modules,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                provenance=True,
                outputbranchsel="Apply_weight_output_branch_selection.txt",
                )
p.run()
