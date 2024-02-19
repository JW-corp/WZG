### WZG analysis aQGC page

### 🚀 Contents 

* [N01_MakeHist](https://github.com/JW-corp/WZG/tree/main/AQGC_FINAL/N01_MakeHist) : Make histogram used as input of counting based method in HiggsCombined tool. 

* [N02_HCTOOL](https://github.com/JW-corp/WZG/tree/main/AQGC_FINAL/N02_HCTOOL) : Calculate limit using higgscombined tool

* [Quadratic_Fit](https://github.com/JW-corp/WZG/tree/main/AQGC_FINAL/Quadratic_Fit) : Only used for input files except for special case like changing aQGC bin or aQGC input file. Pre-calculated function from qudratic fits are stored.


### 🚀 General step..  
1. Do N01  : Make hist 
2. Do N02  : Read number of expected events from output of N01 (histogram) and read function in Quadratic Fit. Calculate Limit.

    
