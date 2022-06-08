exec('global_var.sci')
exec('ship_motion.sci')
exec('loads.sci')

x = Ls*1/3, y=0, z= 0,


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
// for BSR-1P, BSR-2P, BSR-1S, BSR-2S
// for BSR-1P
LC = ["BSR-1P", "BSR-2P", "BSR-1S", "BSR-2S"]
Cx = [0,0,0; 0,0,0; 0,0,0; 0,0,0]                                                       // Cxs, Cxp, Cxg : for Longitudinal acceleration 
Cy = [0.2-0.2*fT, 1, -1; 0.2*fT-0.2, -1, 1; 0.2*fT-0.2, -1, 1; 0.2-0.2*fT, 1, -1]       // Cys, Cyr, Cyg : for Transverse acceleration
Cz = [0.7-0.4*fT, 1, 0; 0.4*fT-0.7, -1, 0; 0.7-0.4*fT, -1, 0 ; 0.4*fT-0.7, 1, 0]        // Czh, Czr, Czp : for Vertical acceleration

for idx =1:4    
    mfprintf(fid, "==========================================================================================\n");    
    mfprintf(fid, "  *** %s *** \n", LC(idx));
    mfprintf(fid, "==========================================================================================\n");
    mfprintf(fid, "------------------------------------------------------------------------------------------\n");
    mfprintf(fid, "Load Combination Factor for %5s\n", LC(idx));
    mfprintf(fid, "------------------------------------------------------------------------------------------\n");    
    mfprintf(fid, "CXS = %8.3f  CXP = %8.3f  CXG = %8.3f\n", Cx(idx,1:3));
    mfprintf(fid, "CYS = %8.3f  CYR = %8.3f  CYG = %8.3f\n", Cy(idx,1:3));
    mfprintf(fid, "CZH = %8.3f  CZR = %8.3f  CZP = %8.3f\n\n", Cz(idx,1:3));
    mfprintf(fid, "------------------------------------------------------------------------------------------\n");
    mfprintf(fid, "Ship accelerations at any position\n");
    ax = longitudinal_accelerations(Cx(idx,1:3), TLC, z) 
    ay = transverse_accelerations(Cy(idx,1:3), TLC, z) 
    az = vertical_accelerations(Cz(idx,1:3), TLC, x, y) 

    ax_env = envelope_longitudinal_accelerations(TLC, z)
    ay_env = envelope_transverse_accelerations(z) 
    [az_env, az_env_pitch, az_env_roll] = envelope_vertical_accelerations(x, y, z)

    mfprintf(fid, "------------------------------------------------------------------------------------------\n");
    mfprintf(fid, "%7s %7s %7s %7s %7s %7s %7s %7s %8s %8s %8s \n", ...
    "X","Y","Z","ax","ay","az","ax_env","ay_env","az_env","az_env","az_env");
    mfprintf(fid, "------------------------------------------------------------------------------------------\n");
    mfprintf(fid, "%7.3f %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f %8.3f %8.3f %8.3f\n", ...
    x, y, z, ax, ay, az, ax_env, ay_env, az_env, az_env_roll, az_env_pitch);
    mfprintf(fid, "==========================================================================================\n\n\n");
end    
mclose(fid);
if (isdef('editor') | (funptr('editor')<>0)) then
  editor(TMPDIR+'/ressult.txt')
end

mfprintf(0,'stderr output.\n');
mfprintf(6,'stdout output.\n');

answer = hydrodynamic_pressure_BSR_LC("BSR-2S",TLC,0, 0)

disp(answer);















