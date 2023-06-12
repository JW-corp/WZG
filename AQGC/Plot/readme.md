
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
