/*
 * SharpDevelop으로 작성되었습니다.
 * 사용자: wjeong
 * 날짜: 2011-07-09
 * 시간: 오후 5:57
 * 
 * 이 템플리트를 변경하려면 [도구->옵션->코드 작성->표준 헤더 편집]을 이용하십시오.
 */
using System;
using System.Text;
using System.Collections.Generic;
using System.Xml;
using System.ComponentModel;
using System.Windows.Forms;
using ExcelDna.Integration;

namespace XEF.ABSFPSO
{
	/// <summary>
	/// Description of FloatingProductionInstallation.
	/// </summary>
	public class FPI
	{
		[ExcelFunction(Description = "kf for load(5A-3-2, 5.5.3)", Category = "ABS FPSO - Loads")]
		public static double ext_kf(double Ls, double kf0, double mu, double x0, double lx)
		{
			
			double kf = kf0*(1-(1-Math.Cos(2*Math.PI*(lx-x0)/Ls))*Math.Cos(mu*Math.PI/180));
			
			return kf;
		}
		
		[ExcelFunction(Description = "Distribution Factor(kl) for External Pressure", Category = "ABS FPSO - Loads")]
		public static double ext_kl(double Ls, double XLOC, double mu)
		{
			
			double Lx = XLOC / Ls;
			
			double kl0 = 0.0;
			
			if(Lx >= 0 & Lx < 0.2)
			{
				kl0 = -2.5 * Lx + 1.5;
			}
			else if(Lx >= 0.2 & Lx <= 0.7)
			{
				kl0 = 1.0;				
			}
			else if(Lx > 0.7 & Lx < 1.0)
			{
				kl0 = 5 * Lx - 2.5;
			}
			
			double rad_mu = (double)XlCall.Excel(XlCall.xlfRadians, mu);
			double kl = 1 + (kl0 - 1) * Math.Cos(rad_mu);
			
			return kl;
		}
		
		[ExcelFunction(Description = "Pitch Amplitude - phi", Category = "ABS FPSO - Loads")]
		public static double Pitch_Amplitude(double Ls, double Cb)
		{
			double k1 = 1030.0;
			double phi = k1*Math.Pow(10/Cb,0.25)/Ls;
			
			return phi;
		}
		
		[ExcelFunction(Description = "Roll Amplitude - theta", Category = "ABS FPSO - Loads")]
		public static double Roll_Amplitude(double Tr, double delta, double df, double di)
		{
			double CR = 1.05;
			double kq = 0.005;
			
			double Cdi = 1.06*(di/df)-0.06;
			double theta = 0;
			
			if(Tr > 20)
			{
				theta = CR*(35-kq*Cdi*delta/1000);
			}
			else if(Tr>=12.5 && Tr<=20.0)
			{
				theta = CR*(35-kq*Cdi*delta/1000)*(1.5375-0.027*Tr);
			}
			else if(Tr<12.5)
			{
				theta = CR*(35-kq*Cdi*delta/1000)*(0.8625+0.027*Tr);
			}
			
			return theta;
		}
		
		[ExcelFunction(Description = "Pitch Natural Period - Tp", Category = "ABS FPSO - Loads")]
		public static double Pitch_Period(double Cb, double di)
		{
			double k2 = 3.5;
			double Tp = k2*Math.Sqrt(Cb*di);
			
			return Tp;
		}
		
		[ExcelFunction(Description = "Roll Natural Period - Tr", Category = "ABS FPSO - Loads")]
		public static double Roll_Period(double kr, double GM)
		{
			double k4 = 2.0;
			double Tr = k4*kr/Math.Sqrt(GM);
			
			return Tr;
		}
		
		[ExcelFunction(Description = "Cv for Vertical Acceleration", Category = "ABS FPSO - Loads")]
		public static double Acc_Cv(double B, double mu, double kv, double ZLOC)
		{
						
			double Cv = Math.Cos(mu)+(1+2.4*ZLOC/B)*Math.Sin(mu)/kv;
			
			return Cv;
		}
		
		[ExcelFunction(Description = "Cl for Longitudinal Acceleration", Category = "ABS FPSO - Loads")]
		public static double Acc_Cl(double Ls)
		{
			
			double Cl = 0.35-0.0005*(Ls-200);

			return Cl;
		}
		
		[ExcelFunction(Description = "Ct for Transverse Acceleration", Category = "ABS FPSO - Loads")]
		public static double Acc_Ct(double Ls, double XLOC)
		{
			double Ct = 1.27*Math.Sqrt(1+1.52*Math.Pow(XLOC/Ls-0.45,2));
			
			return Ct;
		}
		
		[ExcelFunction(Description = "kv for Vertical Acceleration", Category = "ABS FPSO - Loads")]
		public static double Acc_kv(double Ls, double B, double mu, double XLOC)
		{
			
			double kv = Math.Sqrt(1+0.65*Math.Pow(5.3-45/Ls,2)*Math.Pow(XLOC/Ls-0.45, 2)) ;
			
			return kv;
		}
		
		[ExcelFunction(Description = "kl for Longitudinal Acceleration", Category = "ABS FPSO - Loads")]
		public static double Acc_kl(double Ls, double YLOC)
		{
			
			double kl = 0.5+8*YLOC/Ls;

			return kl;
		}
		
		[ExcelFunction(Description = "kt for Transverse Acceleration", Category = "ABS FPSO - Loads")]
		public static double Acc_kt(double B, double YLOC)
		{
			double kt = 0.35 + YLOC/B;
			
			return kt;
		}
		
		[ExcelFunction(Description = "Added Pressure Head (Delta hi-1)", Category = "ABS FPSO - Loads")]
		public static double Int_Delta_hi_i(double Cru, double b, double phi, double theta, double Cphi, double Ctheta, double xi, double zeta, double eta)
		{
			
				double theta_e = 0.71*Ctheta*theta;
				double phi_e = 0.71*Cphi*phi;
				double zeta_e = b - zeta;
				double eta_e = eta;
				
				double r_thetae = (double)XlCall.Excel(XlCall.xlfRadians, theta_e);
				double r_phie = (double)XlCall.Excel(XlCall.xlfRadians, phi_e);
				double r_zetae = (double)XlCall.Excel(XlCall.xlfRadians, zeta_e);
				double r_etae = (double)XlCall.Excel(XlCall.xlfRadians, eta_e);
				
				double dh = 0;
				
				dh = xi*Math.Sin(-r_phie)+Cru*(zeta_e*Math.Sin(r_thetae)*Math.Cos(r_phie)+eta_e*Math.Cos(r_thetae)*Math.Cos(r_phie)-zeta);

				return dh;
		}

		[ExcelFunction(Description = "Added Pressure Head (Delta hi-2)", Category = "ABS FPSO - Loads")]
		public static double Int_Delta_hi_ii(double Cru, double l, double delta_b, double delta_h, double phi, double theta, double Cphi, double Ctheta, double xi, double zeta, double eta)
		{
			
				double theta_e = 0.71*Ctheta*theta;
				double phi_e = 0.71*Cphi*phi;
				double zeta_e = zeta-delta_b;
				double eta_e = eta-delta_h;
				
				double r_thetae = (double)XlCall.Excel(XlCall.xlfRadians, theta_e);
				double r_phie = (double)XlCall.Excel(XlCall.xlfRadians, phi_e);
				double r_zetae = (double)XlCall.Excel(XlCall.xlfRadians, zeta_e);
				double r_etae = (double)XlCall.Excel(XlCall.xlfRadians, eta_e);
				
				double dh = 0;
				
				dh = (l-xi)*Math.Sin(r_phie)+Cru*(zeta_e*Math.Sin(-r_thetae)*Math.Cos(r_phie)+eta_e*Math.Cos(r_thetae)*Math.Cos(r_phie)-zeta);
	
				return dh;
		}		

		/*
		[ExcelFunction(Description = "Plating(mm)", Category = "ABS FPSO")]
		public static double plating(
			[ExcelArgument(Description="Frame System (L or T)")]string FrameSystem, 
			double Yield,
			[ExcelArgument(Description="Frame space(s)")]double space, 
			[ExcelArgument(Description="Unspported Span(l)")]double span,
			[ExcelArgument(Description="Design Pressure")]double pressure)
		{

			double Sm = 0.0;
			
			if(Yield == 2400)
			{
				Sm = 1.0;
			}
			else if(Yield == 3200)
			{
				Sm = 0.95;
			}
			else if(Yield == 3600)
			{
				Sm = 0.908;
			}
			else if(Yield == 4000)
			{
				Sm = 0.875;
			}
			
			double k1 = 0.0;
			double k2 = 0.0;

			switch(FrameSystem)
			{
				case "L":
					k1 = 0.342;
					k2 = 0.5;
					break;
				case "T":
					k1 = 0.5;
					k2 = 0.342;
					break;
			}

			double k3 = 0.5;
			double k4 = 0.74;

			double f1 = 0.65*Sm*Yield;			
			double f2 = 0.85*Sm*Yield;
			double f3 = 0.85*Sm*Yield;
			
			double t1 = 0.73*space*Math.Pow(k1*pressure/f1,0.5);
			double t2 = 0.73*space*Math.Pow(k2*pressure/f2,0.5);
//			double t3 = 0.73*space*Math.Pow(k3*k4*pressure/f2,0.5);
			return t1;
		}
		
		[ExcelFunction(Description = "Frame and Longitudianls(cm^3)", Category = "ABS FPSO")]
		public static double stiffeners(double Ls, double Lfx, double Yield, double space, double span, double pressure)
		{
			double k = 12;
			double M = 1000*pressure*space*Math.Pow(span,2)/k;
			
			double Sm = 0.0;
			
			if(Yield == 2400)
			{
				Sm = 1.0;
			}
			else if(Yield == 3200)
			{
				Sm = 0.95;
			}
			else if(Yield == 3600)
			{
				Sm = 0.908;
			}
			else if(Yield == 4000)
			{
				Sm = 0.875;
			}
			
			double fi = 0.0;
			
			if(Lfx>0.125*Ls & Lfx<=0.2*Ls)
			{
				fi = 0.80*Sm*Yield;
			}
			else
			{
				fi = 0.85*Sm*Yield;
			}
				
			double Result = M/fi;
			
			return Result;
		}
		
		[ExcelFunction(Description = "Alpha for External Pressure", Category = "ABS FPSO")]
		public static double FPI_Load_Alpha(double Breadth, double Draft, double mu, double bilgeR, double loady, double loadz)
		{
			double alpha = 0;
			double bilge_PY = Breadth/2 - Math.Sqrt(Math.Pow(bilgeR,2)/2);
			double bilge_PZ = Math.Sqrt(Math.Pow(bilgeR,2)/2);
			
			double alpha1 = 1.0-0.25*Math.Cos(mu);
			double alpha2 = 0.4-0.1*Math.Cos(mu);
			double alpha3 = 0.3-0.2*Math.Sin(mu);
			double alpha4 = 2*alpha3-alpha2;
			double alpha5 = 0.75 - 1.25*Math.Sin(m
				                                     
				                                     
			if(loady == -Breadth/2 & loadz == Draft)
			{
				alpha = alpha1;
			}
			else if(loady <= -bilge_PY & loadz >= bilge_PZ)
			{
				alpha = alph
					
					
					
					
					a2;
			}
			else if(loady == 0 & loadz == 0)
			{
				alpha = alpha3;
			}
			else if(loady == bilge_PY & loadyz == bilge_PZ)
			{
				alpha = 2*alpha3-alpha2;
			}
			else if(loady ==  Breadth/2 & loadz == Draft)
			{
				alpha = alpha5;
			}
			
			return alpha;
	
		}
*/		
		/*
		public static double ShellPlatingForebody(string FrameSystem, double space, double span, double pressure)
		{
			double k1 = 0.0;
			double k2 = 0.0;
			
			if(FrameSystem == "L")
			{
				k1 = 0.342;
				k2 = 0.5*Math.Pow(k,2);
			}
			else if(FrameSystem == "T")
			{
				k1 = 0.5*Math.Pow(k,2);
				k2 = 0.342;
			}
			
			double k3 = 0.5;
			double k4 = 0.74;
			double alpha = span/space;
			
			if(alpha >= 1 and alpha <= 2)
			{
				k = (3.075*Math.Pow(alpha, 0.5)-2.077)/(alpha + 0.272);
			}
			else
			{
				k = 1.0;
			}
			
			double t1 = 0.73*space*Math.Pow(k1*pressure/f1,0.5);
			double t2 = 0.73*space*Math.Pow(k2*pressure/f2,0.5);
			double t3 = 0.73*space*k*Math.Pow(k3*k4*pressure/f3,0.5);
		}
		*/
		/*
		[ExcelFunction(Description = "FPI_ExternalPressure(kN/m^2)", Category = "FPI Design Pressure")]
		public static double FPI_ExternalPressure(double loadx, double loady, double loadz)
		{
    		double sea_density = 1.025;
			double gravity = 9.81;
    		double Ts, zp, Ls, xp;			
    		
			/// hydrostatic pressure
				double hs = Ts - zp;
				double ps = sea_density * gravity * hs;
//				double beta = BETA1['EPS'];
				double beta = 0.0;	
				double ku = 1.0;					


    /// hydrodynamic pressure head induced by the wave
    			double k = 1.0;
    			double Cw = FloatingProductionInstallation.WaveCoefficient(Ls);
    			double hdo = 1.36*k*Cw;
    
    			double Lx = xp/Ls;

				double alpha = 0;
				double wave_angle = 0.0;
				
    			foreach(dobule wave_angle in heading_angle)
    			{
    				alpha = 0.3-0.20* sin(wave_angle*pi/180.)
			        if(xr < 0.2)
    				{
			            kl0 = LinearInterpolation(0.0,0.2,1.5,1.0,xr)
    				}
			        else if(xr >= 0.2 and xr <= 0.7)
			        {
			            kl0 = 1.0
			        }
			        else if(xr > 0.7)
			        {
						kl0 = LinearInterpolation(0.7,1.0,1.0,2.5,xr)
			        }
    			}
        
        		double kl = 1+(kl0-1)*cos(wave_angle*pi/180.)

        		double hdi = kl*alpha*hdo

        		double kc = 1.0
        		double hde = kc*hdi
*/        		
		}
	
}

