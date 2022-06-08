// Global Variable
global g;       // Graivty Acceleration, in m/s^2
    g = 9.81
global sea;      // sea water density = 1.025
    sea = 1.025;
    
global Ls;      // Rule length, in m
global B;       // Moulded breadth, in m
global D;       // Moulded Depth, in m
global Ts;      // Scantling Draught, in m
global Cb;      // Block coefficient
global kr;      // roll radius of gyration, in m, in the considered loading condition. 
                // In case kr has not been calculated, the following values may be used
                //      kr = 0.39*B in general
                //      kr = 0.35*B for tankers in ballast
global GM;      // Metacentric height, in m, in the considered loading condition, minimum 0.05 B. 
                //      In case GMhas not been calculated, the following values may be adopted:
                // GM= 0.07*B in general
global a0;       // basic acceleration parameter
global fps;      // fps = coefficient for strength assessments which is dependant on the applicable design load scenario specified in Sec.7, and shall be taken as:
                // fps = 1.0 for extreme sea loads design load scenario
global fp;       // fp = fps for strength assessment
global fBK;      // fBK shall be taken as:
                // fBK = 1.2 for ships without bilge keel
                // fBK = 1.0 for ships with bilge keel
global fb;      // fβ = heading correction factor , shall be taken as:
                // for strength assessment:
                // fβ = 1.0 in general
                // fβ = 0.8 for BSR and BSP load cases for the extreme sea loads design load scenario for fatigue assessment:
                // fβ = 1.0

Ls = 170.4;    
B = 30.2;      
D = 28.8;      
Ts = 8.7;      
Cb = 0.83;
kr = 0.35*B;
GM = 0.07*B;
fps = 1.0; fp = fps; fBK = 1.0; fb = 1.0;















