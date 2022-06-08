# 1 VBM Vertical Bending Moment
# 2 HBM Horizontal Bending Moment
# 3 EPP External Pressure Port
# 4 EPS External Pressure Starboard
# 5 VAC Vertical Acceleration
# 6 TAC Transverse Acceleration
# 7 LAC Longitudinal Acceleration
# 8 PMO Pitch Motion
# 9 RMO Roll Motion
# 10 RVM Relative Vertical Motion at Forepeak
# 11 WHT Wave Height
# 12 VSF Vertical Shear Force
# 13 HSF Horizontal Shear Force

BETA1={'VBM':0.689,'HBM':0.566,'EPP':0.554,'EPS':0.569,'VAC':0.797,'TAC':0.533,
       'LAC':0.664,'PMO':0.716,'RMO':0.584,'RVM':0.715,'WHT':0.692,'VSF':0.722,
       'HSF':0.546};

BETA2={'VBM':0.859,'HBM':0.877,'EPP':0.797,'EPS':0.797,'VAC'0.795,'TAC':0.744,
       'LAC':0.899,'PMO':0.867,'RMO':0.723,'RVM':0.815,'WHT':0.859,'VSF':0.872,
       'HSF':0.860}


Wv =[0.0, 0.75,-0.75,0.75,-0.75,0.25,-0.25,0.4,-0.4,0.0,0.0]
Wl_FBHD =[0.0, 0.25,-0.25,0.25,-0.25,0.0,0.0,0.2,-0.2,0.0,0.0]
Wl_ABHD =[0.0, -0.25,0.25,-0.25,0.25,0.0,0.0,-0.2,0.2,0.0,0.0]
Wt_PBHD = [0.0, 0.0, 0.0 ,0.0 ,0.0,-0.75, 0.75,-0.4, 0.4,0.0,0.0]
Wt_SBHD = [0.0, 0.0, 0.0, 0.0 ,0.0, 0.75,-0.75, 0.4,-0.4,0.0,0.0]
