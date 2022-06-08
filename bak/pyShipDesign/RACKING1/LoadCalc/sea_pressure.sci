function Cw = wave_coefficient()
global Ls
    if Ls < 90 then
        Cw = 0.0856 * Ls;
    elseif Ls >= 90 & Ls <= 300 then
        Cw = 10.75 - ((300 - Ls) / 100)^1.5;
    elseif Ls > 300 & Ls <= 350 then
        Cw = 10.75;
    else        // 300 < Ls <= 500
        Cw = 10.75 - ((Ls - 350) / 150)^1.5;
    end
endfunction

// Ship motions
// Roll motion
function [Ttheta, theta] = roll_motion() 
global g kr GM fp fBK
    
    // Roll period - Ttheta
    Ttheta = 2.3 * %pi* kr / sqrt(g*GM);
    // Roll angle in deg. - theta
    theta = 9000 * (1.4 - 0.035 * Ttheta) * fp * fBK / ((1.15*B + 55)*%pi)
    
endfunction

// Pitch motion
function [Tpsi,psi]=pitch_motion(TLC)
global g Ls Ts fp
    
    fT = max(TLC/Ts, 0.5)
    lambda = 0.6*(1+fT)*Ls
    
    // pitch period, in sec
    Tpsi = sqrt(2*%pi*lambda/g)
    
    // pitch angle, in deg
    psi = 920*fp*Ls^-0.84*(1.0+(2.57/sqrt(g*Ls))^1.2)
        
endfunction

// Ship accelerations at the centre of gravity
// surge acceleration
function asurge = surge_acceleration()
global g Ls fp a0

    asurge = 0.2*(1.6+1.5/sqrt(g*Ls))*fp*a0*g

endfunction

function asway = sway_acceleration() 
global g Ls fp a0

    asway = 0.3*(2.25-20/sqrt(g*Ls))*fp*a0*g

endfunction

function aheave = heave_acceleration() 
global g Ls fp a0

if Ls<100 then
    nu = 0;
elseif Ls >= 100 & Ls < 150 then
    xy = [100, 150; 0, 5];
    nu = interpln(xy, Ls)
elseif Ls >= 150 then
    nu = 5.;
end

if Ls < 100 then
    aheave = 0.8*(1+0.03*nu)*(0.72+2*Ls/700)*(1.15-6.5/sqrt(g*Ls))*fp*a0*g;
elseif Ls > 100 & Ls < 150 then
    aheave = (0.4+Ls/250)*(1+0.03*nu*(3-Ls/50))*(1.15-6.5/sqrt(g*Ls))*fp*a0*g;           
elseif Ls >= 150 then
    aheave = (1.15-6.5/sqrt(g*Ls))*fp*a0*g;           
end

endfunction

function aroll = roll_acceleration()  // rad/sec^2
global fp

    [Ttheta, theta] = roll_motion()
    aroll = fp*theta*%pi/180*(2*%pi/Ttheta)^2
    
endfunction   

function apitch = pitch_acceleration(TLC) 
global fp Ls g

    [Tpsi, psi] = pitch_motion(TLC)
    if Ls < 100 then
        apitch = 0.8*(1+0.05*nu)*fp*(0.72+2*Ls/700)*(1.75-22/sqrt(g*Ls))*psi*%pi/180*(2*%pi/Tpsi)^2;
    elseif Ls <= 100 & Ls < 150 then
        apitch = (0.4+Ls/250)*(1+0.05*nu*(3-Ls/50))*fp*(1.75-22/sqrt(g*Ls))*psi*%pi/180*(2*%pi/Tpsi)^2;
    else        // Ls >= 150 
        apitch = fp*(1.75-22/sqrt(g*Ls))*psi*%pi/180*(2*%pi/Tpsi)^2;        
    end
    
endfunction

// Accelerations for dynamic load cases at any position
function ax = longitudinal_accelerations(Cx, TLC, z) 
global g a0 fb   

Cxs = Cx(1); Cxp = Cx(2); Cxg = Cx(3);

    R = min(D/4+TLC/2, D/2);
    asurge = surge_acceleration();
    apitch = pitch_acceleration(TLC);
    [Tpsi, psi] = pitch_motion(TLC)
    
    ax = fb*((-Cxg*g*sind(psi)) + Cxs*asurge + Cxp*apitch*(z-R));
    
endfunction

function ay = transverse_accelerations(Cy, TLC, z) 
global g a0 fb
Cys = Cy(1); Cyr = Cy(2); Cyg = Cy(3);

    R = min(D/4+TLC/2, D/2);
    [Ttheta, theta] = roll_motion()
    asway = sway_acceleration()
    aroll = roll_acceleration()
   
    ay = fb*((Cyg*g*sind(theta)) + Cys*asway + Cyr*aroll*(z-R));
    
endfunction

function az = vertical_accelerations(Cz, TLC, x, y) 
global Ls fb
Czh = Cz(1); Czr = Cz(2); Czp = Cz(3);

    aheave = heave_acceleration()
    apitch = pitch_acceleration(TLC)
    aroll = roll_acceleration()
    
    az = fb*(Czh*aheave + Czr*aroll*y - Czp*apitch*(x-0.45*Ls));
        
endfunction

// Envelope accelerations

function ax_env = envelope_longitudinal_accelerations(TLC, z) 
global g Ls Ts

if Ls < 90 then
    fL = 1.0
elseif Ls >= 90 & Ls < 150 then
    fL = 1.3-Ls/300
else    // Ls >= 150
    fL = 0.8    
end

L0 = max(Ls, 110);
    
    R = min(D/4+TLC/2, D/2);
    asurge = surge_acceleration();
    apitch = pitch_acceleration(TLC);
    [Tpsi, psi] = pitch_motion()
        
    apitch_x = apitch*(z-R);
    ax_env = 0.7*fL*(0.65+2*z/(7*Ts))*sqrt(asurge^2 + L0/320*(g*sind(psi)+apitch_x)^2)
    
endfunction

function ay_env = envelope_transverse_accelerations(z) 
global Ls GM g a0
    
    R = min(D/4+TLC/2, D/2);
    [Ttheta, theta] = roll_motion()
    asway = sway_acceleration()
    aroll = roll_acceleration()
    
    aroll_y = aroll*(z-R);
    ay_env = (1-%e^(-B*Ls/(215*GM)))*sqrt(asway^2 + (g*sind(theta)+aroll_y)^2)
        
endfunction

function [az_env, az_env_pitch, az_env_roll] = envelope_vertical_accelerations(x, y, z) 

    aheave = heave_acceleration()
    apitch = pitch_acceleration(TLC)
    aroll = roll_acceleration()

    apitch_z = apitch*(1.08*x-0.45*Ls)
    aroll_z = aroll*y
            
    az_env = sqrt(aheave^2+((0.95+%e^(-Ls/15))*apitch_z)^2 + (1.2*aroll_z)^2)
    az_env_pitch = sqrt(aheave^2+((0.95+%e^(-Ls/15))*apitch_z)^2)
    az_env_roll = sqrt(aheave^2+(1.2*aroll_z)^2)
    
endfunction

function Ps = hydrostatic_pressure(TLC, z)
global g sea;
    
    h = TLC - z;
    Ps = max(sea*g*h, 0);
   
endfunction

function P_BSR = hydrodynamic_pressure_BSR(LoadCase, y)

    Cw = Wave_Coefficient();
    [Ttheta, theta] = roll_motion();
    lambda = g/(2*%pi)*Ttheta^2;
    theta1 = 9000 * (1.4 - 0.035 * Ttheta)/((1.15*B + 55)*%pi);
    fnl = 1.0;
    fb = 1.0;
    L0 = max(Ls, 110);
    fyB1 = min(abs(2*y)/B, 1.0)
    
    if LoadCase == "BSR-1P" | LoadCase == "BSR-2P" then
        P_BSR = fb*fnl*(10*y*sin(theta1) + 0.88*fps*Cw*sqrt((L0+lambda-125)/L0)*(fyB1+1));
    elseif LoadCase == "BSR-1S" | LoadCase == "BSR-2S" then
        P_BSR = fb*fnl*(-10*y*sin(theta1) + 0.88*fps*Cw*sqrt((L0+lambda-125)/L0)*(fyB1+1));            
    else
        P_BSR = -1;    
    end
    
endfunction

function Pw_BSR = hydrodynamic_pressure_BSR_LC(LoadCase, TLC, y, z)

    Pbsr = hydrodynamic_pressure_BSR(LoadCase, y);
    disp(Pbsr)
if LoadCase == "BSR-1P" | LoadCase == "BSR-1S" then
    Pw_wl = Pbsr;
elseif LoadCase == "BSR-2P" | LoadCase == "BSR-2S" then     
    Pw_wl = -Pbsr;
end

hw = Pw_wl / (sea*g)

if z <= TLC then
    select LoadCase
        case "BSR-1P" then Pw_BSR = max(Pbsr, sea*g*(z-TLC))
        case "BSR-2P" then Pw_BSR = max(-Pbsr, sea*g*(z-TLC))
        case "BSR-1S" then Pw_BSR = max(Pbsr, sea*g*(z-TLC))
        case "BSR-2S" then Pw_BSR = max(-Pbsr, sea*g*(z-TLC))
    end    

elseif z > TLC & z <= hw+TLC then
    
    Pw_BSR = Pw_wl - sea*g*(z-TLC);
    
else
    Pw_BSR = 0;
end

endfunction

// Global Variable
global g;       // Graivty Acceleration, in m/s^2
    g = 9.81
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

global sea;      // sea water density = 1.025
    sea = 1.025;
global a0;       // basic acceleration parameter
global fps;      // fps = coefficient for strength assessments which is dependant on the applicable design load scenario specified in Sec.7, and shall be taken as:
                // fps = 1.0 for extreme sea loads design load scenario
global fp;       // fp = fps for strength assessment
global fBK;      // fBK = shall be taken as:
                // fBK = 1.2 for ships without bilge keel
                // fBK = 1.0 for ships with bilge keel
global fT;                
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

x = Ls*2/3, y=0, z= 0,


fid = mopen(TMPDIR+'/ressult.txt', 'wt');

mfprintf(fid, "==========================================================================\n");
mfprintf(fid, "               Principal Dimension\n");
mfprintf(fid, "==========================================================================\n");
mfprintf(fid, 'Rule Length                  Ls = %10.3f  m\n', Ls);
mfprintf(fid, 'Mouduled Breadth             B  = %10.3f  m\n', B);
mfprintf(fid, 'Mouduled Depth               D  = %10.3f  m\n', D);
mfprintf(fid, 'Scantling Draft              Ts = %10.3f  m\n', Ts);
mfprintf(fid, 'Block Coefficient            Cb = %10.3f  m\n', Cb);
mfprintf(fid, "--------------------------------------------------------------------------\n");
Cw = wave_coefficient();
mfprintf(fid, 'Wave Coefficient             Cw = %10.3f  m\n', Cw);
a0 = (1.58 - 0.47 * Cb) * (2.4 / sqrt(Ls) + 34 / Ls - 600 / Ls ^ 2);
mfprintf(fid, 'Basic Acceleration Parameter a0 = %10.3f  m\n\n', a0);

// Full load condition
TLC = Ts;
mfprintf(fid, "==========================================================================\n");
mfprintf(fid, "Full load condition TLC = %5.3f \n", TLC);
mfprintf(fid, "==========================================================================\n\n");
mfprintf(fid, "--------------------------------------------------------------------------\n");
mfprintf(fid, "Load factor\n");
mfprintf(fid, "--------------------------------------------------------------------------\n");
fT = TLC/Ts;
mfprintf(fid, 'fps = %5.1f   fp = %5.1f   fBK = %5.1f \n', fps, fp, fBK);
mfprintf(fid, 'fT = %5.1f    fb = %5.1f \n\n', fT, fb);
mfprintf(fid, "--------------------------------------------------------------------------\n");
mfprintf(fid, "Ship Motion\n");
mfprintf(fid, "--------------------------------------------------------------------------\n");
[Ttheta, theta] = roll_motion()
mfprintf(fid, "Roll Motion : \n");
mfprintf(fid, "Roll angle = %5.3f deg. Roll period = %5.3f m/s^2\n\n", theta, Ttheta);
[Tpsi, psi] = pitch_motion(TLC);
mfprintf(fid, "Pitch Motion : \n");
mfprintf(fid, "Pitch angle = %5.3f deg. Pitch period = %5.3f m/s^2\n\n", psi, Tpsi);
mfprintf(fid, "--------------------------------------------------------------------------\n");
mfprintf(fid, "Ship accelerations at the centre of gravity\n");
mfprintf(fid, "--------------------------------------------------------------------------\n");
asurge = surge_acceleration();
asway = sway_acceleration();
aheave = heave_acceleration();
aroll = roll_acceleration();
apitch = pitch_acceleration(TLC);

mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n", 'Surge acceleration','a_surge',asurge);
mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n", 'Sway acceleration', 'a_sway',asway);
mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n",'Heave acceleration', 'a_heave',aheave);
mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n", 'Roll acceleration', 'a_roll', aroll);
mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n\n", 'Pitch acceleration', 'a_pitch', apitch);
mfprintf(fid, "==========================================================================\n");    
// for BSR-1P, BSR-2P, BSR-1S, BSR-2S
// for BSR-1P
LC = ["BSR-1P", "BSR-2P", "BSR-1S", "BSR-2S"]
Cx = [0,0,0; 0,0,0; 0,0,0; 0,0,0]                                                       // Cxs, Cxp, Cxg : for Longitudinal acceleration 
Cy = [0.2-0.2*fT, 1, -1; 0.2*fT-0.2, -1, 1; 0.2*fT-0.2, -1, 1; 0.2-0.2*fT, 1, -1]       // Cys, Cyr, Cyg : for Transverse acceleration
Cz = [0.7-0.4*fT, 1, 0; 0.4*fT-0.7, -1, 0; 0.7-0.4*fT, -1, 0 ; 0.4*fT-0.7, 1, 0]        // Czh, Czr, Czp : for Vertical acceleration

for idx =1:4    
    mfprintf(fid, "%s\n", LC(idx));
    mfprintf(fid, "==========================================================================\n");    
    mfprintf(fid, "--------------------------------------------------------------------------\n");
    mfprintf(fid, "Ship accelerations at any position\n");
    mfprintf(fid, "--------------------------------------------------------------------------\n");
        
    ax = longitudinal_accelerations(Cx(idx,1:3), TLC, z) 
    ay = transverse_accelerations(Cy(idx,1:3), TLC, z) 
    az = vertical_accelerations(Cz(idx,1:3), TLC, x, y) 
    
    mfprintf(fid, "Load Combination Factor for %5s\n", LC(idx));
    mfprintf(fid, "CXS = %8.3f  CXP = %8.3f  CXG = %8.3f\n", Cx(idx,1:3));
    mfprintf(fid, "CYS = %8.3f  CYR = %8.3f  CYG = %8.3f\n", Cy(idx,1:3));
    mfprintf(fid, "CZH = %8.3f  CZR = %8.3f  CZP = %8.3f\n\n", Cz(idx,1:3));
    mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n", 'Longitudinal acceleration', 'ax',ax);
    mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n", 'Transverse acceleration', 'ay',ay);
    mfprintf(fid, "%-40s %-10s = %8.3f  m/s^2\n\n", 'Vertical acceleration', 'az',az);
    mfprintf(fid, "--------------------------------------------------------------------------\n");
    mfprintf(fid, "Envelope accelerations at any position \n");
    mfprintf(fid, "--------------------------------------------------------------------------\n");
    
    ax_env = envelope_longitudinal_accelerations(TLC, z)
    ay_env = envelope_transverse_accelerations(z) 
    [az_env, az_env_pitch, az_env_roll] = envelope_vertical_accelerations(x, y, z)
    mfprintf(fid, "%-40s %-12s = %8.3f  m/s^2\n", 'Envelope longitudinal acceleration', 'ax_env',ax_env);
    mfprintf(fid, "%-40s %-12s = %8.3f  m/s^2\n", 'Envelope transverse acceleration', 'ay_env',ay_env);
    mfprintf(fid, "%-40s %-12s = %8.3f  m/s^2\n", 'Envelope vertical acceleration', 'az_env',az_env);
    mfprintf(fid, "%-40s %-12s = %8.3f  m/s^2\n", 'Envelope vertical acceleration roll', 'az_env_roll',az_env_roll);
    mfprintf(fid, "%-40s %-12s = %8.3f  m/s^2\n", 'Envelope vertical acceleration pitch', 'az_env_pitch',az_env_pitch);
    mfprintf(fid, "==========================================================================\n");
end    
mclose(fid);
if (isdef('editor') | (funptr('editor')<>0)) then
  editor(TMPDIR+'/ressult.txt')
end

mfprintf(0,'stderr output.\n');
mfprintf(6,'stdout output.\n');

answer = hydrodynamic_pressure_BSR_LC("BSR-2S",TLC,0, 0)

disp(answer);















