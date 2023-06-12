
## How to analyze aQGC

### Updated
- FakeLepton unc calculation is added all these processes 
- AK array is used (from pandas to AK)
- mplhep will be updated:  [MPLHEP based](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/Prepare_hist_turbo.py). Current I did not use this method yet.

### 1. First, you need to make ratios, test, npys directories (empty directory for output)
1. [AddHist_help_aQGC.py](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/AddHist_help_aQGC.py) : Main source code applying cut
2. [N01_Prepare_hist.py](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/N01_Prepare_hist.py) : Prepare histogram using 1.
3. [N02_Plot.py](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/N02_Plot.py): Plot histogram
4. [N03_make_ratio.py](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/N03_make_ratio.py) : Prepare ratio plot
5. [N04_plot_ratio.py](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/N04_plot_ratio.py) : Quadratic fit
6. [N05_Prepare_hist_forCombine.py](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/N05_Prepare_hist_forCombine.py) : Prepare HC tool 
 
### 2. Please check different CMSSW version 

Need CMSSW==python3.X+
- export SCRAM_ARCH=slc7_amd64_gcc900  
- CMSSW_11_3_0_pre2_PY3
- N01_Prepare_hist.py
- N02_Plot.py

Need CMSSW==corresponding thos of HiggsCombined tool setting
- N03_make_ratio.py
- N04_plot_ratio.py
- N05_Prepare_hist_forCombine.py


### 3. Please read this before running
- AddHist_help_aQGC.py: You need to change this block [359](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/AddHist_help_aQGC.py#L360) [360](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/AddHist_help_aQGC.py#L360) to process all re-weight. Currently only the first reweight (all parameter zero, so equal to SM) is default one. Beware the running time if you process the all re-weight. It is time-consumming job. 

- N01_Prepare_hist.py: Also you need to change this block [132](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/N01_Prepare_hist.py#L132) to [131](https://github.com/JW-corp/WZG/blob/main/AQGC/Plot/2018/N01_Prepare_hist.py#L131). For same reason.

- N05_Prepare_hist_forCombine.py: When you running N05_Prepare_hist_forCombine.py you need argument like
```bash
python N05_Prepare_hist_forCombine.py 0
```
0 means the 0th parameter: Standard model. You need to use 0 if there is no special reason. The starting point of HC should be the SM. We will fit this using pre-calculated quadratic function: ratios/XXX.npys
