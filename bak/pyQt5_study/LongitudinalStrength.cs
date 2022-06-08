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

namespace XEF.LongitudinalStrength
{
	/// <summary>
	/// Description of LongitudinalStrength.
	/// </summary>
	public class LongitudinalStrength
	{
		[ExcelFunction(Description = "Wave Coefficient (Cwv)", Category = "Longitudinal Strength")]
        public static double WaveCoefficient(double Ls)
        {

            double ReturnValue = 0.0;
            
            if (90.0 <= Ls & Ls < 300)
            {
                ReturnValue = 10.75 - Math.Pow(((300 - Ls) / 100), 1.5);
            }
            else if (300 <= Ls & Ls < 350)
            {
                ReturnValue = 10.75;
            }
            else if (350 < Ls & Ls <= 500)
            {
                 ReturnValue = 10.75 - Math.Pow(((Ls - 350) / 150), 1.5);    	
            }
            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution factor for vertical wave bending moment", Category = "Longitudinal Strength")]
        public static double fwv_v(double Ls, double X)
        {

        	double ReturnValue = 0;
			double Lx = X/Ls;

			if (Lx >= 0 & Lx < 0.4)
            {
                ReturnValue = 2.5 * Lx;
            }
            else if (Lx >= 0.4 & Lx < 0.65)
            {
                ReturnValue = 1.0;
            }
            else if (Lx >= 0.65 & Lx < 1.0)
            {
                ReturnValue = -2.85714*Lx + 2.85714;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution Factor for still water bending Moment", Category = "Longitudinal Strength")]
        public static double fsw(double Ls, double Xs)
        {
            double ReturnValue = 0.0;
            double Lx = 0;

            Lx = Xs / Ls;

            if(Lx >= 0 & Lx < 0.1)
            {
            	ReturnValue = 1.5*Lx;
            }
            else if (Lx >= 0.1 & Lx < 0.3)
            {
                ReturnValue = 4.25*Lx - 0.275;
            }
            else if (Lx >= 0.3 & Lx <= 0.7)
            {
                ReturnValue = 1.0;
            }
            else if (Lx > 0.7 & Lx <= 0.9)
            {
                ReturnValue = -4.25*Lx + 3.975;
            }
            else if (Lx > 0.9 & Lx <= 1.0)
            {
            	ReturnValue = -1.5*Lx + 1.5;
            }

            return ReturnValue;
        }
        
        [ExcelFunction(Description = "Distribution Factor for Horizontal wave bending moment", Category = "Longitudinal Strength")]
        public static double fmh(double Ls, double Xs)
        {
            double ReturnValue = 0.0;
            double Lx = 0;

            Lx = Xs / Ls;

            if(Lx >= 0 & Lx < 0.4)
            {
            	ReturnValue = 2.5*Lx;
            }
            else if (Lx >= 0.4 & Lx < 0.6)
            {
                ReturnValue = 1.0;
            }
            else if (Lx >= 0.6 & Lx <= 1.0)
            {
                ReturnValue = -2.5*Lx + 2.5;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution Factor for Horizontal wave shear force", Category = "Longitudinal Strength")]
        public static double fsh(double Ls, double Xs)
        {
            double ReturnValue = 0.0;
            double Lx = 0;

            Lx = Xs / Ls;

            if(Lx >= 0 & Lx < 0.2)
            {
            	ReturnValue = 5.0*Lx;
            }
            else if (Lx >= 0.2 & Lx < 0.3)
            {
                ReturnValue = 1.0;
            }
            else if (Lx >= 0.3 & Lx <= 0.4)
            {
                ReturnValue = -3.0*Lx + 1.9 ;
            }
            else if (Lx > 0.4 & Lx <= 0.6)
            {
                ReturnValue = 0.7;
            }
            else if (Lx > 0.6 & Lx <= 0.7)
            {
            	ReturnValue = 3.0*Lx - 1.1;
            }
            else if (Lx > 0.7 & Lx <= 0.8)
            {
            	ReturnValue = 1.0;
            }
            else if (Lx > 0.8 & Lx <= 1.0)
            {
            	ReturnValue = -5.0*Lx + 5.0;
            }
            return ReturnValue;
        }
        
        [ExcelFunction(Description = "Vertical Wave Bending Moment(kN-m)", Category = "Longitudinal Strength")]
        public static double VerWaveBM(string HullGirderMotion, double Ls, double B, double Cb, double X)
        {
            double ReturnValue = 0.0;
			double Cw = WaveCoefficient(Ls);
			
            if (HullGirderMotion.ToUpper() == "HOGGING" | HullGirderMotion.ToUpper() == "HOG" | HullGirderMotion.ToUpper() == "H")
            {
                ReturnValue = 0.190 * fwv_v(Ls, X) * Cw * Math.Pow(Ls, 2) * B * Cb;
            }
            else if (HullGirderMotion.ToUpper() == "SAGGING" | HullGirderMotion.ToUpper() == "SAG" | HullGirderMotion.ToUpper() == "S")
            {
                ReturnValue = -0.110 * fwv_v(Ls, X) * Cw * Math.Pow(Ls, 2) * B * (Cb + 0.7);
            }
            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution factor for positive vertical wave shear force", Category = "Longitudinal Strength")]
        public static double fqwv_pos(double Ls, double Cb, double X)
        {
            double ReturnValue = 0.0;
            double a = 0;

            a = 0.92 * 190 * Cb / (110 * (Cb + 0.7));

            if (0 <= X & X < 0.2 * Ls)
            {
                ReturnValue = 4.6 * a * X / Ls;
            }
            else if (0.2 * Ls <= X & X <= 0.3 * Ls)
            {
                ReturnValue = 0.92 * a;
            }
            else if (0.3 * Ls < X & X < 0.4 * Ls)
            {
                ReturnValue = (9.2 * a - 7) * (0.4 - X / Ls) + 0.7;
            }
            else if (0.4 * Ls <= X & X <= 0.6 * Ls)
            {
                ReturnValue = 0.7;
            }
            else if (0.6 * Ls < X & X < 0.7 * Ls)
            {
                ReturnValue = 3 * (X / Ls - 0.6) + 0.7;
            }
            else if (0.7 * Ls <= X & X <= 0.85 * Ls)
            {
                ReturnValue = 1;
            }
            else if (0.85 * Ls < X & X < Ls)
            {
                ReturnValue = 6.67 * (1 - X / Ls);
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution factor for negative vertical wave shear force", Category = "Longitudinal Strength")]
        public static double fqwv_neg(double Ls, double Cb, double X)
        {
            double ReturnValue = 0.0;
            double a = 0;

            a = 190 * Cb / (110 * (Cb + 0.7));

            if (0 <= X & X < 0.2 * Ls)
            {
                ReturnValue = -4.6 * X / Ls;
            }
            else if (0.2 * Ls <= X & X <= 0.3 * Ls)
            {
                ReturnValue = -0.92;
            }
            else if (0.3 * Ls < X & X < 0.4 * Ls)
            {
                ReturnValue = -2.2 * (0.4 - X / Ls) + 0.7;
            }
            else if (0.4 * Ls <= X & X <= 0.6 * Ls)
            {
                ReturnValue = -0.7;
            }
            else if (0.6 * Ls < X & X < 0.7 * Ls)
            {
                ReturnValue = -(10 * a - 7) * (X / Ls - 0.6) - 0.7;
            }
            else if (0.7 * Ls <= X & X <= 0.85 * Ls)
            {
                ReturnValue = -a;
            }
            else if (0.85 * Ls < X & X < Ls)
            {
                ReturnValue = 6.67 * a * (1 - X / Ls);
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Vertical wave shear force (Qwv, kN)", Category = "Longitudinal Strength")]
        public static double VerWaveSF(string Sign, double Ls, double b, double Cb, double X)
        {
            double Cw = WaveCoefficient(Ls);
            double fqwv = 0.0;

            if (Sign == "+")
            {
                fqwv = fqwv_pos(Ls, Cb, X);
            }
            else if (Sign == "-")
            {
                fqwv = fqwv_neg(Ls, Cb, X);
            }

            return 0.30 * fqwv * Cw * Ls * b * (Cb + 0.7);
        }

        [ExcelFunction(Description = "Horizontal wave bending moment(kN-m)", Category = "Longitudinal Strength")]
        public static double HorWaveBM(double Ls, double D, double Cb, double X)
        {
        	double Cw = WaveCoefficient(Ls);
        	
            return fmh(Ls,X)*180*Cw*Math.Pow(Ls,2)*D*Cb*Math.Pow(10,-3);
        }
        
        [ExcelFunction(Description = "Horizontal wave shear force(kN-m)", Category = "Longitudinal Strength")]
        public static double HorWaveSF(double Ls, double D, double Cb, double X)
        {
        	double Cw = WaveCoefficient(Ls);
        	
        	return fsh(Ls, X)*36*Cw*Ls*D*(Cb + 0.7)*Math.Pow(10,-2);
        	
        }
        
        [ExcelFunction(Description = "Rule Minimum Hull Girder Section Modulus(cm^3)", Category = "Longitudinal Strength")]
        public static double MinHullGirderSM(double Ls, double B, double Cb)
        {
        	double ReturnValue = 0.0;
        	double Cw = WaveCoefficient(Ls);
        	
        	ReturnValue = Cw*Math.Pow(Ls,2)*B*(Cb+0.7);
        	
            return ReturnValue;
        }

	}
}

