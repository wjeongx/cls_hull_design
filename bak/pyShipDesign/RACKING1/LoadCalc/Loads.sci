function Ps = hydrostatic_pressure(TLC, z)
global g sea;
    
    h = TLC - z;
    Ps = max(sea*g*h, 0);
   
endfunction

function P_BSR = hydrodynamic_pressure_BSR(LoadCase, y)
global Ls
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















