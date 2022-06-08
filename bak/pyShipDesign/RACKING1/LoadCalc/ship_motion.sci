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
global Ls

    aheave = heave_acceleration()
    apitch = pitch_acceleration(TLC)
    aroll = roll_acceleration()

    apitch_z = apitch*(1.08*x-0.45*Ls)
    aroll_z = aroll*y
            
    az_env = sqrt(aheave^2+((0.95+%e^(-Ls/15))*apitch_z)^2 + (1.2*aroll_z)^2)
    az_env_pitch = sqrt(aheave^2+((0.95+%e^(-Ls/15))*apitch_z)^2)
    az_env_roll = sqrt(aheave^2+(1.2*aroll_z)^2)
    
endfunction

