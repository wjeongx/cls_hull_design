/*
 * Created by SharpDevelop.
 * User: WJEONG
 * Date: 2010-05-08
 * Time: 오후 11:17
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */

using System;
using System.Collections.Generic;
using System.Text;
using System.Xml;
using ExcelDna.Integration;

namespace XEF.CSRBC
{
    /// #############################################################################
    ///         Section 2 - Ship Motion and Acceleration
    /// #############################################################################
    public class DesignBasic
    {
        [ExcelFunction(Description = "", Category = "Design Basic(CSRBC)")]
        public static double csrbc_fp(int Prob)
        {
            double fp = 0.0;

            if (Prob == -4)
            {
                fp = 0.5;
            }
            else if (Prob == -8)
            {
                fp = 1.0;
            }

            return fp;
        }

        public static double csrbc_Ca(double space, double span)
        {
            double Ca = 1.21 * Math.Sqrt(1 + 0.33 * Math.Pow(space / span, 2)) - 0.69 * space / span;

            Ca = (double)XlCall.Excel(XlCall.xlfMin, Ca, 1.0);

            return Ca;
        }

        public static double csrbc_Cr(double space, double curv)
        {
            double Cr = 1 - 0.5 * space / curv;

            Cr = (double)XlCall.Excel(XlCall.xlfMax, Cr, 0.4);
            
            return Cr;
        }
    }

    public class ShipMotion
    {
        public const double g0 = 9.81;

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Parameter_a0(int Prob, double Ls, double Cb)
        {
            double fp = 0.0;

            fp = DesignBasic.csrbc_fp(Prob);

            return fp * (1.58 - 0.47 * Cb) * (2.4 / Math.Sqrt(Ls) + 34 / Ls - 600 / Math.Pow(Ls, 2));

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Heave(double a0)
        {

            return a0 * 9.81;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_GM(string Loading, double B)
        {
            double GM = 0.0;

            switch (Loading.ToUpper())
            {
                case "HOMO":
                    GM = 0.12 * B;
                    break;
                case "ALT":
                    GM = 0.12 * B;
                    break;
                case "NORMAL":
                    GM = 0.33 * B;
                    break;
                case "HEAVY":
                    GM = 0.25 * B;
                    break;
            }

            return GM;
        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_kr(string Loading, double B)
        {
            double kr = 0.0;


            switch (Loading.ToUpper())
            {
                case "HOMO":
                    kr = 0.35 * B;
                    break;
                case "ALT":
                    kr = 0.35 * B;
                    break;
                case "NORMAL":
                    kr = 0.45 * B;
                    break;
                case "HEAVY":
                    kr = 0.4 * B;
                    break;
            }
            return kr;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Sway(double a0)
        {

            return 0.3 * a0 * 9.81;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Surge(double a0)
        {

            return 0.2 * a0 * g0;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Period_Roll_TR(double b, double GM, double KR)
        {

            return 2.3 * KR / Math.Sqrt(GM);

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Amplitude_Roll(int Prob, double B, double GM, double KR, Boolean BilgeKeel)
        {

            double TR = 0;
            double phi = 0;
            double fp = 0;

            fp = DesignBasic.csrbc_fp(Prob);

            TR = csrbc_Period_Roll_TR(B, GM, KR);

            double kb = 0.0;

            switch (BilgeKeel)
            {
                case true: kb = 1.0;
                    break;
                case false: kb = 1.2;
                    break;
            }

            phi = 9000 * (1.25 - 0.025 * TR) * fp * kb / ((B + 75) * Math.PI);

            return phi;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Roll_Y(int Prob, double B, double D, double TLC, double GM, double KR, double Z)
        {

            double TR = 0;
            double theta = 0;
            double R = 0;
            double fp = 0;

            fp = DesignBasic.csrbc_fp(Prob);

            TR = csrbc_Period_Roll_TR(B, GM, KR);

            theta = (double)XlCall.Excel(XlCall.xlfRadians, csrbc_Amplitude_Roll(Prob, B, GM, KR, true));

            R = Z - (double)XlCall.Excel(XlCall.xlfMin, D / 4 + TLC / 2, D / 2);

            return theta * Math.Pow((2 * Math.PI / TR), 2) * R;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Roll_Z(int Prob, double B, double GM, double KR, double YG)
        {

            double TR = 0;
            double theta = 0;

            TR = csrbc_Period_Roll_TR(B, GM, KR);

            theta = (double)XlCall.Excel(XlCall.xlfRadians, csrbc_Amplitude_Roll(Prob, B, GM, KR, true));
            return theta * Math.Pow((2 * Math.PI / TR), 2) * YG;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Period_Pitch_TP(double Ls, double Ts, double TLC)
        {

            double Lambda = 0;

            Lambda = 0.6 * (1 + (TLC / Ts)) * Ls;
            return Math.Sqrt(2 * Math.PI * Lambda / g0);

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Amplitude_Pitch(int Prob, double Ls, double Cb, double V)
        {

            double phi = 0;
            double fp = 0;

            fp = DesignBasic.csrbc_fp(Prob);

            phi = fp * 960 / Ls * Math.Pow((V / Cb), (1 / 4));

            return phi;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Pitch_X(int Prob, double Ls, double D, double Ts, double Cb, double V, double TLC, double ZG)
        {

            double phi = 0;
            double TP = 0;
            double R = 0;

            phi = (double)XlCall.Excel(XlCall.xlfRadians, csrbc_Amplitude_Pitch(Prob, Ls, Cb, V));


            TP = csrbc_Period_Pitch_TP(Ls, Ts, TLC);

            R = ZG - (double)XlCall.Excel(XlCall.xlfMin, (D / 4) + (TLC / 2), D / 2);

            return phi * (Math.Pow(((2 * Math.PI) / TP), 2)) * R;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Acceleration_Pitch_Z(int Prob, double Ls, double Ts, double Cb, double V, double TLC, double XG)
        {

            double phi = 0;
            double xL = 0;
            double TP = 0;

            phi = (double)XlCall.Excel(XlCall.xlfRadians, csrbc_Amplitude_Pitch(Prob, Ls, Cb, V));

            TP = csrbc_Period_Pitch_TP(Ls, Ts, TLC);

            xL = Math.Abs(XG - 0.45 * Ls);
            xL = (double)XlCall.Excel(XlCall.xlfMax, xL, 0.2 * Ls);

            return phi * Math.Pow((2 * Math.PI / TP), 2) * xL;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Accelerations_X(int Prob, double Ls, double D, double Ts, double Cb, double V, string LC, double TLC, double ZG)
        {

            double CXG = 0;
            double CXS = 0;
            double CXP = 0;
            double a0 = 0;
            double phi = 0;
            double a_surge = 0;
            double a_pitch_x = 0;

            CXG = LoadCases.csrbc_LCF_CXG(LC);
            CXS = LoadCases.csrbc_LCF_CXS(LC);
            CXP = LoadCases.csrbc_LCF_CXP(LC);

            phi = (double)XlCall.Excel(XlCall.xlfRadians, csrbc_Amplitude_Pitch(Prob, Ls, Cb, V));

            a0 = csrbc_Acceleration_Parameter_a0(Prob, Ls, Cb);
            a_surge = csrbc_Acceleration_Surge(a0);
            a_pitch_x = csrbc_Acceleration_Pitch_X(Prob, Ls, D, Ts, Cb, V, TLC, ZG);

            return CXG * g0 * Math.Sin(phi) + CXS * a_surge + CXP * a_pitch_x;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Accelerations_Y(int Prob, double Ls, double b, double D, double Cb, string LC, double TLC, double GM, double KR, double Z)
        {

            double CYG = 0;
            double CYS = 0;
            double CYR = 0;
            double theta = 0;
            double a0 = 0;
            double a_sway = 0;
            double a_roll_y = 0;
            double fp = 0;

            fp = DesignBasic.csrbc_fp(Prob);

            CYG = LoadCases.csrbc_LCF_CYG(LC);
            CYS = LoadCases.csrbc_LCF_CYS(LC);
            CYR = LoadCases.csrbc_LCF_CYR(LC);

            a0 = csrbc_Acceleration_Parameter_a0(Prob, Ls, Cb);

            a_sway = csrbc_Acceleration_Sway(a0);

            theta = (double)XlCall.Excel(XlCall.xlfRadians, csrbc_Amplitude_Roll(Prob, b, GM, KR, true));
            a_roll_y = csrbc_Acceleration_Roll_Y(Prob, b, D, TLC, GM, KR, Z);

            return CYG * g0 * Math.Sin(theta) + CYS * a_sway + CYR * a_roll_y;

        }

        [ExcelFunction(Description = "", Category = "Ship Motion(CSRBC)")]
        public static double csrbc_Accelerations_Z(int Prob, double Ls, double b, double D, double Ts, double Cb, double V, string LC, double TLC, double GM,
        double KR, double X, double Y)
        {

            double CZH = 0;
            double CZR = 0;
            double CZP = 0;
            double a0 = 0;
            double a_heave = 0;
            double a_roll_z = 0;
            double a_pitch_z = 0;
            double fp = 0;

            fp = DesignBasic.csrbc_fp(Prob);

            CZH = LoadCases.csrbc_LCF_CZH(LC, Ls, Ts, TLC);
            CZR = LoadCases.csrbc_LCF_CZR(LC);
            CZP = LoadCases.csrbc_LCF_CZP(LC);

            a0 = csrbc_Acceleration_Parameter_a0(Prob, Ls, Cb);

            a_heave = csrbc_Acceleration_Heave(a0);

            a_roll_z = csrbc_Acceleration_Roll_Z(Prob, b, GM, KR, Y);

            a_pitch_z = csrbc_Acceleration_Pitch_Z(Prob, Ls, Ts, Cb, V, TLC, X);

            return CZH * a_heave + CZR * a_roll_z + CZP * a_pitch_z;

        }
    }


    public class ExternalPressure
    {

        public const double g0 = 9.81;

        [ExcelFunction(Description = "Hydrostatic Pressure", Category = "External Pressure")]
        public static double Hydrostatic_Ps(double rho, double TLCi, double Z)
        {
            double Ps = 0;

            if (Z <= TLCi) Ps = rho * g0 * (TLCi - Z); else Ps = 0;

            return Ps;
        }

        [ExcelFunction(Description = "Lambda for H Case", Category = "External Pressure")]
        public static double Lambda_for_H(double Ls, double Ts, double TLC)
        {
            double ReturnValue = 0.6 * (1 + TLC / Ts) * Ls;
            return ReturnValue;
        }
        
        [ExcelFunction(Description = "Lambda for F Case", Category = "External Pressure")]
        public static double Lambda_for_F(double Ls, double Ts, double TLC)
        {
            double ReturnValue = 0.6 * (1 + 2 / 3 * TLC / Ts) * Ls;
            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Lambda_for_R(string Loading, double Ls, double B)
        {

            double GM = 0;
            double KR = 0;
            double TR = 0;

            GM = ShipMotion.csrbc_GM(Loading, B);
            KR = ShipMotion.csrbc_kr(Loading, B);
            TR = ShipMotion.csrbc_Period_Roll_TR(B, GM, KR);


            return g0 * Math.Pow(TR, 2) / (2 * Math.PI);
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Lambda_for_P(double Ls, double Ts, double TLC)
        {
            return (0.2 + 0.4 * TLC / Ts) * Ls;
        }

        [ExcelFunction(Description = "Hydrodynamic Pressure PHF", Category = "External Pressure")]
        public static double Hydrodynamic_PHF(int Prob, string LC, double Ls, double Ts, double TLC, double Bi, double TLCi, double Y, double Z)
        {
            double fnl = 0;
            double fp = 0;
            double Lambda = 0;

            if (Prob == -4)
            {
                fnl = 1.0;
                fp = 0.5;
            }
            else if (Prob == -8)
            {
                fnl = 0.9;
                fp = 1.0;
            }

            switch (LC.ToUpper())
            {
                case "H":
                    Lambda = Lambda_for_H(Ls, Ts, TLC);
                    break;
                case "F":
                    Lambda = Lambda_for_F(Ls, Ts, TLC);
                    break;
            }
            
            double F1 = (double)XlCall.Excel(XlCall.xlfMin, Math.Abs(2 * Y) / Bi, 1.0);

            Z = (double)XlCall.Excel(XlCall.xlfMin, Z, TLCi);

            double ReturnValue = 3 * fp * fnl * Hull_Girder_Loads.Cw(Ls) * Math.Sqrt((Ls + Lambda - 125) / Ls) * (Z / TLCi + F1 + 1);

            return ReturnValue;
        }

        [ExcelFunction(Description = "Amplitude_kl", Category = "External Pressure")]
        public static double Amplitude_kl(double Ls, double b, double Cb, double X, double Y)
        {
            double kl = 0;

            if (X / Ls >= 0 & X / Ls <= 0.5)
            {
                kl = 1 + 12 / Cb * (1 - Math.Sqrt(Math.Abs(2 * Y) / b)) * Math.Pow(Math.Abs(X / Ls - 0.5), 3);
            }
            else
            {
                kl = 1 + (6 / Cb) * (3 - Math.Abs(4 * Y) / b) * Math.Pow(Math.Abs(X / Ls - 0.5), 3);
            }

            return kl;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Coeff_Phase_kp(double Ls, double Ts, double TLC, double X, string LoadCondition)
        {
            double kp = 0;
			
            switch (LoadCondition.ToUpper())
            {
                case "HOMO":
                    kp = -1;
                    break;
                case "ALT":
                    kp = -1;
                    break;
                default:
                    kp = (1.25 - TLC / Ts) * Math.Cos(2 * Math.PI * Math.Abs(X - 0.5 * Ls) / Ls) - TLC / Ts + 0.25;
                    break;
            }

            return kp;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Hydrodynamic_PH1(int Prob, string Loading, string LoadCase, double Ls, double B, double Bi, double Cb, 
                                              double Ts, double TLC, double TLCi, double X,	double Y, double Z)
        {
            double kl = Amplitude_kl(Ls, B, Cb, X, Y);
            double kp = Coeff_Phase_kp(Ls, Ts, TLC, X, Loading);

            double PHF = Hydrodynamic_PHF(Prob, LoadCase.Substring(0, 1), Ls, Ts, TLC, Bi, TLCi, Y, Z);

            return -kl * kp * PHF;
        }

        public static double Hydrodynamic_PH2(int Prob, string Loading, string LoadCase, double Ls, double B, double Bi, double Cb, 
                                              double Ts, double TLC, double TLCi, double X,	double Y, double Z)
        {
            double kl = Amplitude_kl(Ls, B, Cb, X, Y);
            double kp = Coeff_Phase_kp(Ls, Ts, TLC, X, Loading);

            double PHF = Hydrodynamic_PHF(Prob, LoadCase.Substring(0, 1), Ls, Ts,  TLC, Bi, TLCi, Y, Z);

            return kl * kp * PHF;
        }
        
        public static double Hydrodynamic_PF1(int Prob, string LoadCase, double Ls, double Bi, double Ts, double TLC, double TLCi, 
                                              double X,	double Y, double Z)
        {
            double PHF = Hydrodynamic_PHF(Prob, LoadCase.Substring(0, 1), Ls, Ts, TLC, Bi, TLCi, Y, Z);

            return -PHF;
        }
        
        public static double Hydrodynamic_PF2(int Prob, string LoadCase, double Ls, double Bi, double Ts, double TLC, double TLCi, 
                                              double X,	double Y, double Z)
        {
            double PHF = Hydrodynamic_PHF(Prob, LoadCase.Substring(0, 1), Ls, Ts, TLC, Bi, TLCi, Y, Z);

            return PHF;
        }
        
        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double HydroDynamic_PR1(int Prob, string Loading, double Ls, double B, double c, double theta, double TR, double Y)
        {
            double fnl = 0, fp = 0;

            if (Prob == -4)
            {
                fnl = 1.0;
                fp = 0.5;
            }
            else if (Prob == -8)
            {
                fnl = 0.8;
                fp = 1.0;
            }

            double Lambda = Lambda_for_R(Loading, Ls, B);

            double PR1 = fnl * (10 * Y * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, theta)) + 0.88 * fp * c * Math.Sqrt((Ls + Lambda - 125) / Ls) * (Math.Abs(2 * Y) / B + 1));

            return PR1;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double HydroDynamic_PR2(int Prob, string Loading, double Ls, double B, double c, double theta, double TR, double Y)
        {
            double fnl = 0, fp = 0;

            if (Prob == -4)
            {
                fnl = 1.0;
                fp = 0.5;
            }
            else if (Prob == -8)
            {
                fnl = 0.8;
                fp = 1.0;
            }

            double Lambda = Lambda_for_R(Loading, Ls, B);

            double PR1 = fnl * (10 * Y * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, theta)) + 0.88 * fp * c * Math.Sqrt((Ls + Lambda - 125) / Ls) * (Math.Abs(2 * Y) / B + 1));
			double PR2 = -PR1;
			
            return PR2;
        }
        
        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Hydrodynamic_PP(int Prob, double Ls, double B, double c, double Ts, double TLC, double TLCi, double Y, double Z)
        {

            double fnl = 0, fp = 0;
            
            if (Prob == -4)
            {
                fnl = 1.0;
                fp = 0.5;
            }
            else if (Prob == -8)
            {
                fnl = 0.65;
                fp = 1.0;
            }

            double Lambda = Lambda_for_P(Ls, Ts, TLC);;

            double PP = 4.5 * fp * fnl * c * Math.Sqrt((Ls + Lambda - 125) / Ls) * (2 * Math.Abs(Z) / TLCi + 3 * Math.Abs(2 * Y) / B);

            return PP;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Hydrodynamic_PP1(int Prob, double Ls, double B, double c, double Ts, double TLC, double TLCi, double Y, double Z)
        {
        	double PP = Hydrodynamic_PP(Prob, Ls, B, c, Ts, TLC, TLCi, Y, Z);

            double PPW = PP;
            double PPL = PP / 3;

            int Sign = Convert.ToInt32(Y / Math.Abs(Y));
			
            double PP1 = 0;
            switch (Sign)
            {
                case 1:
                    PP1 = PPW;
                    break;
                case -1:
                    PP1 = PPL;
                    break;
            }

            return PP1;
        }

        public static double Hydrodynamic_PP2(int Prob, double Ls, double B, double c, double Ts, double TLC, double TLCi, double Y, double Z)
        {
        	double PP = Hydrodynamic_PP(Prob, Ls, B, c, Ts, TLC, TLCi, Y, Z);

            double PPW = -PP;
            double PPL = -PP / 3;

            int Sign = Convert.ToInt32(Y / Math.Abs(Y));
			
            double PP2 = 0;
            
            switch (Sign)
            {
                case 1:
                    PP2 = PPW;
                    break;
                case -1:
                    PP2 = PPL;
                    break;
            }

            return PP2;
        }
        
        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Hydrodynamic_Correction(string LoadCase, double Pw, double PwWL, double Z, double TLCi)
        {
            double rho = 1.025;
        	double hw = 0;
            double PwC = 0;

            hw = PwWL / (rho * g0);

            if (PwWL >= 0)
            {
                //Debug.Print 1
                if (LoadCase != "F1" & LoadCase != "P2")
                {
                    // Debug.Print 2
                    if (Z >= TLCi & Z <= (hw + TLCi))
                    {
                        // Debug.Print 3, TLCi, Z
                        PwC = PwWL + rho * g0 * (TLCi - Z);
                    }
                    else if (Z > hw + TLCi)
                    {
                        //Debug.Print 4
                        PwC = 0;
                    }
                    else
                    {
                        //Debug.Print 5
                        PwC = Pw;
                    }
                }
            }
            else if (PwWL < 0)
            {
                if (LoadCase != "F2" & LoadCase != "P1")
                {
                    if (Z < TLCi)
                    {
                        PwC = (double)XlCall.Excel(XlCall.xlfMax, Pw, rho * g0 * (Z - TLCi));
                    }
                    else if (Z > TLCi + hw)
                    {
                        PwC = 0;
                    }
                    else
                    {
                        PwC = Pw;
                    }
                }
            }


            return PwC;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Hydrodynamic_PwC(double Ls, double b, double Ts, double Cb, string LC, string LCase, double TLC, double Bi, double TLCi, double X,
        double Y, double Z, int Prob, double theta, double TR)
        {

            double c = 0;
            c = Hull_Girder_Loads.Cw(Ls);

            double PwC = 0;
            double Pw = 0;
            double PwWL = 0;
            double Pp = 0;
            double PpWL = 0;

            switch (LCase)
            {
            	case "H1":
            		break;
            	case "H2":
            		break;
            	case "F1":
            		break;
            	case "F2":
//                    Pw = Hydrodynamic_PHF(Prob, Ls, b, Ts, Cb, LCase, TLC, Bi, TLCi, X, Y, Z, LC);
//                    PwWL = Hydrodynamic_PHF(Prob, Ls, b, Ts, Cb, LCase, TLC, Bi, TLCi, X, Y, TLC, LC);
//                    PwC = Hydrodynamic_Correction(LCase, 1.025, Pw, PwWL, Z, TLCi);
                    break;
                case "R1":
                    break;
                case "R2":
//                    Pw = HydroDynamic_PR(Prob, LC, LCase, Ls, c, b, theta, TR, Y);
//                    PwWL = HydroDynamic_PR(Prob, LC, LCase, Ls, c, b, theta, TR, Y);
//                    PwC = Hydrodynamic_Correction(LCase, 1.025, Pw, PwWL, Z, TLCi);
                    break;
                   case "P1":
                    break;
               	case "P2":
//                    Pp = Pressure_Hydrodynamic_PP(Prob, Ls, b, c, Ts, TLC, TLCi, Y, Z, LCase);
//                    Pw = Pressure_Hydrodynamic_PPw(LCase, Y, Pp);

//                    PpWL = Pressure_Hydrodynamic_PP(Prob, Ls, b, c, Ts, TLC, TLCi, Y, TLC, LCase);
//                    PwWL = Pressure_Hydrodynamic_PPw(LCase, Y, PpWL);
//                    PwC = Hydrodynamic_Correction(LCase, 1.025, Pw, PwWL, Z, TLCi);
                    break;
            }
            return PwC;
        }
/*
        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Hydrodynamic_Pw(double Ls, double b, double Ts, double Cb, string LC, string LCase, double TLC, double Bi, double TLCi, double X,
        double Y, double Z, int Prob, double theta, double TR)
        {

            double c = 0;
            c = Hull_Girder_Loads.Cw(Ls);

            // double PwC = 0;
            double Pw = 0;
            // double PwWL = 0;
            double Pp = 0;
            // double PpWL = 0;

            switch (LCase)
            {
                case "H1": 
            		Pw = Hydrodynamic_PH1(Prob, Loading, LCase, Ls, B, Bi, Cb, Ts, TLC, TLCi, X, Y, Z);
            		break;
                case "H2": 
            		Pw = Hydrodynamic_PH2(Prob, Loading, LCase, Ls, B, Bi, Cb, Ts, TLC, TLCi, X, Y, Z);
            		break;
                case "F1": 
            		Pw = Hydrodynamic_PF1(Prob, LCase, Ls, Bi, Ts, TLC, TLCi, X, Y, Z);
            		break;
                case "F2": 
            		Pw = Hydrodynamic_PF2(Prob, LCase, Ls, Bi, Ts, TLC, TLCi, X, Y, Z);
                    break;
                case "R1":
                    Pw = HydroDynamic_PR1(Prob, Loading, Ls, B, c, theta, TR, Y);
                case "R2":
                    Pw = HydroDynamic_PR2(Prob, Loading, Ls, B, c, theta, TR, Y);
                    break;
                case "P1":
                    Pw = Hydrodynamic_PP1(Prob, Ls, B, c, Ts, TLC, TLCi, Y, Z);
                    break;
                case "P2":
                    Pw = Hydrodynamic_PP2(Prob, Ls, B, c, Ts, TLC, TLCi, Y, Z);
                    break;
            }

            return Pw;
        }
*/
        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Pressure_BottomSlamming(double Ls, double Cb, double TBFP, double X)
        {
            double ReturnValue = 0.0;
            double CSL = 0;

            double c1 = 3.6 - 6.5 * Math.Pow((TBFP / Ls), 0.2);
            double c2 = 0.33 * Cb + Ls / 2500;

            c1 = (double)XlCall.Excel(XlCall.xlfMin, c1, 1.0);
            c2 = (double)XlCall.Excel(XlCall.xlfMin, c2, 0.35);

            if (X / Ls <= 0.5)
            {
                CSL = 0;
            }
            else if (X / Ls > 0.5 & X / Ls < 0.5 + c2)
            {
                CSL = (X / Ls - 0.5) / c2;
            }
            else if (X / Ls > 0.5 + c2 & X / Ls <= 0.65 + c2)
            {
                CSL = 1.0;
            }
            else if (X / Ls > 0.65 + c2)
            {
                CSL = 0.5 * (1 + (1 - X / Ls) / (0.35 - c2));
            }

            if (Ls <= 150)
            {
                ReturnValue = 162 * c1 * CSL * Math.Sqrt(Ls);
            }
            else
            {
                ReturnValue = 1984 * c1 * CSL * (1.3 - 0.002 * Ls);
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double Pressure_BowFlareImpact(double Ls, double Cb, double V, double c, double TB, double X, double Z, double CFL, double Ps, double Pw)
        {
            double K = 0;
            double PFB = 0;

            K = CFL * Math.Pow((0.2 * V + 0.6 * Math.Sqrt(Ls)), 2) * (10 + Z - TB) / (42 * c * (Cb + 0.7) * (1 + 20 / Cb * Math.Pow((X / Ls - 0.7), 2)));

            if (K < 1) K = 1.0;

            PFB = K * (Ps + Pw);


            return PFB;
        }

        [ExcelFunction(Description = "", Category = "External Pressure")]
        public static double BowFlareImpact_K(double CFL, double V, double Ls, double c, double Cb, double X, double Z, double TLC)
        {
            double K = 0;

            K = CFL * Math.Pow((2 * V + 0.6 * Math.Sqrt(Ls)), 2) / ((42 * c * (Cb + 0.7) * (1 + 20 / Cb * Math.Pow((X / Ls - 0.7), 2)))) * (10 + Z - TLC);


            return K;
        }

    }

    //
    // Created by SharpDevelop.
    // User: WJEONG
    // Date: 2010-05-09
    // Time: 오전 2:34
    // 
    // To change this template use Tools | Options | Coding | Edit Standard Headers.
    //
    // #############################################################################
    // Section 3 - Hull Girder Loads
    // #############################################################################

    public class Hull_Girder_Loads
    {

        [ExcelFunction(Description = "", Category = "Hull Girder Loads")]
        public static double Cw(double Ls)
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

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.3 Hull Girder Loads")]
        public static double get_fm(double Ls, double X)
        {

            double ReturnValue = 0;

            if (X / Ls >= 0 & X / Ls < 0.4)
            {
                ReturnValue = 2.5 * X / Ls;
            }
            else if (X / Ls >= 0.4 & X / Ls < 0.65)
            {
                ReturnValue = 1.0;
            }
            else if (X / Ls >= 0.65 & X / Ls < 1.0)
            {
                ReturnValue = 2.86 * (1 - X / Ls);
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.3 Hull Girder Loads")]
        public static double Fsw(double Ls, double Xs)
        {
            double ReturnValue = 0.0;
            double Lx = 0;

            Lx = Xs / Ls;

            if (Lx >= 0 & Lx < 0.3)
            {
                ReturnValue = ((0.8 * Xs) / (0.3 * Ls)) + 0.2;
            }
            else if (Lx >= 0.3 & Lx <= 0.7)
            {
                ReturnValue = 1;
            }
            else if (Lx > 0.7 & Lx <= 1)
            {
                ReturnValue = (-0.8 * (Lx - 0.7)) / 0.3 + 1;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.3 Hull Girder Loads")]
        public static double VerWaveBM(string HullGirderMotion, int Prob, double Ls, double b, double Cb, double X)
        {
            double ReturnValue = 0.0;
            double fp = 0;

            if (Prob == -8)
            {
                fp = 1;
            }
            else if (Prob == -4)
            {
                fp = 0.5;
            }

            if (HullGirderMotion.ToUpper() == "HOGGING" | HullGirderMotion.ToUpper() == "HOG" | HullGirderMotion.ToUpper() == "H")
            {
                ReturnValue = 190.0 * get_fm(Ls, X) * fp * Cw(Ls) * Math.Pow(Ls, 2) * b * Cb * Math.Pow(10, -3);
            }
            else if (HullGirderMotion.ToUpper() == "SAGGING" | HullGirderMotion.ToUpper() == "SAG" | HullGirderMotion.ToUpper() == "S")
            {
                ReturnValue = -110.0 * get_fm(Ls, X) * fp * Cw(Ls) * Math.Pow(Ls, 2) * b * (Cb + 0.7) * Math.Pow(10, -3);
            }
            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.3 Hull Girder Loads")]
        public static double FQP(double Ls, double Cb, double X)
        {
            double ReturnValue = 0.0;
            double a = 0;

            a = 190 * Cb / (110 * (Cb + 0.7));

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

        [ExcelFunction(Description = "", Category = "SEC.3 Hull Girder Loads")]
        public static double FQN(double Ls, double Cb, double X)
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

        [ExcelFunction(Description = "", Category = "SEC.3 Hull Girder Loads")]
        public static double QWV(double fp, string Sign, double Ls, double b, double Cb, double X)
        {
            double FQ = 0;

            if (Sign == "+")
            {
                FQ = FQP(Ls, Cb, X);
            }
            else if (Sign == "-")
            {
                FQ = FQN(Ls, Cb, X);
            }


            return 30 * FQ * fp * Cw(Ls) * Ls * b * (Cb + 0.7) * Math.Pow(10, -2);
        }

        [ExcelFunction(Description = "", Category = "SEC.3 Hull Girder Loads")]
        public static double HorWaveBM(int Prob, double Ls, double Cb, double TLC, double X)
        {
            double fp = 0;

            if (Prob == -8)
            {
                fp = 1;
            }
            else if (Prob == -4)
            {
                fp = 0.5;
            }


            return (0.3 + Ls / 2000) * get_fm(Ls, X) * fp * Cw(Ls) * Math.Pow(Ls, 2) * TLC * Cb;
        }

    }

    /// #############################################################################
    /// Section 4 Load Cases
    /// #############################################################################

    public class LoadCases
    {
        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CWV(string LC, double Ts, double TLC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = -1;
                    break;
                case "H2":
                    ReturnValue = 1;
                    break;
                case "F1":
                    ReturnValue = -1;
                    break;
                case "F2":
                    ReturnValue = 1;
                    break;
                case "R1":
                    ReturnValue = 0;
                    break;
                case "R2":
                    ReturnValue = 0;
                    break;
                case "P1":
                    ReturnValue = 0.4 - TLC / Ts;
                    break;
                case "P2":
                    ReturnValue = TLC / Ts - 0.4;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CQW(string LC, double Ts, double TLC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = -1;
                    break;
                case "H2":
                    ReturnValue = 1;
                    break;
                case "F1":
                    ReturnValue = -1;
                    break;
                case "F2":
                    ReturnValue = 1;
                    break;
                case "R1":
                    ReturnValue = 0;
                    break;
                case "R2":
                    ReturnValue = 0;
                    break;
                case "P1":
                    ReturnValue = 0.4 - TLC / Ts;
                    break;
                case "P2":
                    ReturnValue = TLC / Ts - 0.4;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CWH(string LC, double Ts, double TLC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 0;
                    break;
                case "H2":
                    ReturnValue = 0;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 1.2 - TLC / Ts;
                    break;
                case "R2":
                    ReturnValue = TLC / Ts - 1.2;
                    break;
                case "P1":
                    ReturnValue = 0;
                    break;
                case "P2":
                    ReturnValue = 0;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CXS(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = -0.8;
                    break;
                case "H2":
                    ReturnValue = 0.8;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 0;
                    break;
                case "R2":
                    ReturnValue = 0;
                    break;
                case "P1":
                    ReturnValue = 0;
                    break;
                case "P2":
                    ReturnValue = 0;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CXP(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 1;
                    break;
                case "H2":
                    ReturnValue = -1;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 0;
                    break;
                case "R2":
                    ReturnValue = 0;
                    break;
                case "P1":
                    ReturnValue = 0;
                    break;
                case "P2":
                    ReturnValue = 0;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CXG(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 1;
                    break;
                case "H2":
                    ReturnValue = -1;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 0;
                    break;
                case "R2":
                    ReturnValue = 0;
                    break;
                case "P1":
                    ReturnValue = 0;
                    break;
                case "P2":
                    ReturnValue = 0;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CYS(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 0;
                    break;
                case "H2":
                    ReturnValue = 0;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 0;
                    break;
                case "R2":
                    ReturnValue = 0;
                    break;
                case "P1":
                    ReturnValue = 1;
                    break;
                case "P2":
                    ReturnValue = -1;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CYR(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 0;
                    break;
                case "H2":
                    ReturnValue = 0;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 1;
                    break;
                case "R2":
                    ReturnValue = -1;
                    break;
                case "P1":
                    ReturnValue = 0.3;
                    break;
                case "P2":
                    ReturnValue = -0.3;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CYG(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 0;
                    break;
                case "H2":
                    ReturnValue = 0;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 1;
                    break;
                case "R2":
                    ReturnValue = -1;
                    break;
                case "P1":
                    ReturnValue = 0.3;
                    break;
                case "P2":
                    ReturnValue = -0.3;
                    break;
            }


            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CZH(string LC, double Ls, double Ts, double TLC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 0.6 * TLC / Ts;
                    break;
                case "H2":
                    ReturnValue = -0.6 * TLC / Ts;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = Math.Sqrt(Ls) / 40;
                    break;
                case "R2":
                    ReturnValue = -Math.Sqrt(Ls) / 40;
                    break;
                case "P1":
                    ReturnValue = 1;
                    break;
                case "P2":
                    ReturnValue = -1;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CZR(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 0;
                    break;
                case "H2":
                    ReturnValue = 0;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 1;
                    break;
                case "R2":
                    ReturnValue = -1;
                    break;
                case "P1":
                    ReturnValue = 0.3;
                    break;
                case "P2":
                    ReturnValue = -0.3;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double csrbc_LCF_CZP(string LC)
        {

            double ReturnValue = 0;
            switch (LC.ToUpper())
            {
                case "H1":
                    ReturnValue = 1;
                    break;
                case "H2":
                    ReturnValue = -1;
                    break;
                case "F1":
                    ReturnValue = 0;
                    break;
                case "F2":
                    ReturnValue = 0;
                    break;
                case "R1":
                    ReturnValue = 0;
                    break;
                case "R2":
                    ReturnValue = 0;
                    break;
                case "P1":
                    ReturnValue = 0;
                    break;
                case "P2":
                    ReturnValue = 0;
                    break;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double HGF_CSW(string HullGirderMotion, string LoadCase)
        {
            double CSW = 0;

            if (HullGirderMotion.ToUpper() == "HOGGING" | HullGirderMotion.ToUpper() == "HOG" | HullGirderMotion.ToUpper() == "H")
            {
                switch (LoadCase)
                {
                    case "H1":
                        CSW = 0;
                        break;
                    case "F1":
                        CSW = 0;
                        break;
                    default:
                        CSW = 1;
                        break;
                }
            }

            else if (HullGirderMotion.ToUpper() == "SAGGING" | HullGirderMotion.ToUpper() == "SAG" | HullGirderMotion.ToUpper() == "S")
            {
                switch (LoadCase)
                {
                    case "H2":
                        CSW = 0;
                        break;
                    case "F2":
                        CSW = 0;
                        break;
                    default:
                        CSW = -1;
                        break;
                }
            }

            return CSW;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double HGF_CWV(string HullGirderMotion, string LoadCase, double Ts, double TLC)
        {
            double ReturnValue = 0.0;
            // int Sign = 0;

            if (HullGirderMotion.ToUpper() == "HOGGING" | HullGirderMotion.ToUpper() == "HOG" | HullGirderMotion.ToUpper() == "H")
            {
                switch (LoadCase.ToUpper())
                {
                    case "H2":
                        ReturnValue = 1;
                        break;
                    case "F2":
                        ReturnValue = 1;
                        break;
                    case "R1":
                        ReturnValue = 0;
                        break;
                    case "R2":
                        ReturnValue = 0;
                        break;
                    case "P1":
                        ReturnValue = 0.4 - TLC / Ts;
                        break;
                    case "P2":
                        ReturnValue = TLC / Ts - 0.4;
                        break;
                }
            }
            else if (HullGirderMotion.ToUpper() == "SAGGING" | HullGirderMotion.ToUpper() == "SAG" | HullGirderMotion.ToUpper() == "S")
            {
                switch (LoadCase.ToUpper())
                {
                    case "H1":
                        ReturnValue = -1;
                        break;
                    case "F1":
                        ReturnValue = -1;
                        break;
                    case "R1":
                        ReturnValue = 0;
                        break;
                    case "R2":
                        ReturnValue = 0;
                        break;
                    case "P1":
                        ReturnValue = 0.4 - TLC / Ts;
                        break;
                    case "P2":
                        ReturnValue = TLC / Ts - 0.4;
                        break;
                }
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double HGF_CWH(string HullGirderMotion, string LoadCase, double Ts, double TLC)
        {

            double ReturnValue = 0.0;
            if (HullGirderMotion.ToUpper() == "HOGGING" | HullGirderMotion.ToUpper() == "HOG" | HullGirderMotion.ToUpper() == "H")
            {
                switch (LoadCase.ToUpper())
                {
                    case "H2":
                        ReturnValue = 0;
                        break;
                    case "F2":
                        ReturnValue = 0;
                        break;
                    case "R1":
                        ReturnValue = 1.2 - TLC / Ts;
                        break;
                    case "R2":
                        ReturnValue = TLC / Ts - 1.2;
                        break;
                    case "P1":
                        ReturnValue = 0;
                        break;
                    case "P2":
                        ReturnValue = 0;
                        break;

                }
            }
            else if (HullGirderMotion.ToUpper() == "SAGGING" | HullGirderMotion.ToUpper() == "SAG" | HullGirderMotion.ToUpper() == "S")
            {
                switch (LoadCase.ToUpper())
                {
                    case "H1":
                        ReturnValue = 0;
                        break;
                    case "F1":
                        ReturnValue = 0;
                        break;
                    case "R1":
                        ReturnValue = 1.2 - TLC / Ts;
                        break;
                    case "R2":
                        ReturnValue = TLC / Ts - 1.2;
                        break;
                    case "P1":
                        ReturnValue = 0;
                        break;
                    case "P2":
                        ReturnValue = 0;
                        break;

                }
            }


            return ReturnValue;
        }

        [ExcelFunction(Description = "", Category = "SEC.4 Load Cases")]
        public static double normal_stress(int Prob, double Ls, double b, double Cb, double Ts, double NA, double Iy, double Iz, string HullGirderMotion, double Ms,
        string LoadCase, double TLC, double X, double Y, double Z)
        {

            double CSW = 0;
            double CWV = 0;
            double CWH = 0;
            double Mwv = 0;
            double Mwh = 0;


            CSW = HGF_CSW(HullGirderMotion, LoadCase);
            CWV = HGF_CWV(HullGirderMotion, LoadCase, Ts, TLC);
            CWH = HGF_CWH(HullGirderMotion, LoadCase, Ts, TLC);

            Mwv = Math.Round(Hull_Girder_Loads.VerWaveBM(HullGirderMotion, Prob, Ls, b, Cb, X), 0);
            Mwh = Math.Round(Hull_Girder_Loads.HorWaveBM(Prob, Ls, Cb, TLC, X), 0);

            //Debug.Print Mwv, Mwh, CSW, CWV, CWH

            return (CSW * Math.Abs(Ms / Iy) * (Z - NA) + CWV * Math.Abs(Mwv / Iy) * (Z - NA) - CWH * Math.Abs(Mwh / Iz) * Y) * Math.Pow(10, -3);
        }
    }

    public class ForeEndStructure
    {
        // #############################################################################
        //         Chapter 9 Section 1.5
        // #############################################################################

        public static double csrbc_Plating_BottomSlamming(double ReH, double space, double span, double Cs, double PSL)
        {

            double ca = DesignBasic.csrbc_Ca(space, span);

            double cr = 1.0;
            return 15.8 * ca * cr * space * Math.Sqrt(Cs * PSL / ReH);

        }

        public static double csrbc_Stiffener_SM_BottomSlamming(double ReH, double space, double span, double Cs, double PSL)
        {

            return Cs * PSL * space * Math.Pow(span, 2) * Math.Pow(10, 3) / (16 * ReH);

        }
        public static double csrbc_Stiffener_Ash_BottomSlamming(double ReH, double space, double span, double phi, double PSL)
        {

            return 5 * Math.Sqrt(3) * PSL * space * (span - 0.5 * space) / (Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, phi)) * ReH);

        }

        public static double csrbc_Plating_BowFlareImpact(double ReH, double space, double span, double Cs, double PFB)
        {

            double ca = DesignBasic.csrbc_Ca(space, span);
            double cr = 1.0;
            space = 0.83;

            return 15.8 * ca * cr * space * Math.Sqrt(PFB / ReH);

        }

    }

    public class InternalPressure
    {
        public const double g0 = 9.81;
        public static double csrbc_get_h1_dry_cargo(double M, double rC, double BH, double bIB, double LH, double hHPL, double psi, double VTS)
        {
            double h1 = 0.0;

            if (M == 0)
            {
                h1 = 0.0;
            }
            else
            {
                h1 = M / (rC * BH * LH) - (BH + bIB) * hHPL / (2 * BH) - 3 * BH * Math.Tan((double)XlCall.Excel(XlCall.xlfRadians, psi / 2)) / 16 + VTS / (BH * LH);
            }
            return h1;

        }

        public static double csrbc_h2_dry_cargo(double BH, double psi, double Y)
        {
            double h2 = 0.0;

            if (Math.Abs(Y) >= 0 & Math.Abs(Y) <= BH / 4)
            {
                h2 = BH / 4 * Math.Tan((double)XlCall.Excel(XlCall.xlfRadians, psi / 2));
            }
            else if (Math.Abs(Y) > BH / 4 & Math.Abs(Y) <= BH / 2)
            {
                h2 = (BH / 2 - Math.Abs(Y)) * Math.Tan((double)XlCall.Excel(XlCall.xlfRadians, psi / 2));
            }
            return h2;

        }

        // #############################################################################
        //         Section 6 INTERNAL PRESSURE & FORCE
        // #############################################################################

        public static double csrbc_Pressure_Liquid_In_StillWater(double ZTOP, double Z, double PPV, double ZdAP, bool FlowThrough)
        {
            double PL = 0;

            double rhoL = 0;
            double P1 = 0;
            double P2 = 0;
            // bool Bal = false;
            double PBS1 = 0;
            double PBS2 = 0;

            rhoL = 1.025;

            P1 = rhoL * g0 * (ZTOP + (ZdAP - ZTOP) / 2 - Z);
            P2 = rhoL * g0 * (ZTOP - Z) + 100 * PPV;
            //Debug.Print P1, P2
            PBS1 = (double)XlCall.Excel(XlCall.xlfMax, P1, P2, 25);

            PBS2 = rhoL * g0 * (ZdAP - Z) + 25;

            if (FlowThrough == true)
            {
                PL = (double)XlCall.Excel(XlCall.xlfMax, PBS1, PBS2);
            }
            else
            {
                PL = PBS1;
            }
            return PL;

            //Debug.Print PBS2
        }


        public static double csrbc_Pressure_Liquid_Inertial(double ax, double ay, double az, double phi, double theta, double ZTOP, double X, double Y, double Z, double YB1,
        double ZB1, string LoadCase, double LH)
        {

            double rhoL = 0;
            // bool Bal = false;
            double PBW = 0;
            double phi1 = 0;
            // double XB = 0;
            double YB = 0;
            double ZB = 0;

            YB = YB1;
            ZB = ZB1;

            if (LoadCase == "H1" | LoadCase == "H2")
            {
                phi1 = Math.Atan(Math.Abs(ax) / (g0 * Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, phi)) + az));
            }
            else if (LoadCase == "R1" | LoadCase == "R2" | LoadCase == "P1" | LoadCase == "P2")
            {
                phi1 = Math.Atan(Math.Abs(ay) / (g0 * Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, theta)) + az));
            }

            rhoL = 1.025;
            if (LoadCase == "H1")
            {
                PBW = rhoL * (az * (ZTOP - Z) + ax * 0.75 * LH);
            }
            else if (LoadCase == "H2")
            {
                PBW = rhoL * (az * (ZTOP - Z) + ax * -0.75 * LH);
            }
            else if (LoadCase == "F1" | LoadCase == "F2")
            {
                PBW = 0.0;
            }
            else if (LoadCase == "R1" | LoadCase == "R2" | LoadCase == "P1" | LoadCase == "P2")
            {
                PBW = rhoL * (az * (ZB - Z) + ay * (Y - YB));
                //Debug.Print LoadCase, az, ay, Y, Z, YB, ZB
            }

            return PBW;
        }

        public static double ph(int Prob, double Ls, double B, double D, double Ts, double Cb, double V, string LoadCase, double TLC, double GM,
        double KR, double X, double Y, double Z)
        {
            double ReturnValue = 0.0;

            double phi = ShipMotion.csrbc_Amplitude_Pitch(Prob, Ls, Cb, V);
            double theta = ShipMotion.csrbc_Amplitude_Roll(Prob, B, GM, KR, true);

            double ax = ShipMotion.csrbc_Accelerations_X(Prob, Ls, D, Ts, Cb, V, LoadCase, TLC, Z);
            double ay = ShipMotion.csrbc_Accelerations_Y(Prob, Ls, B, D, Cb, LoadCase, TLC, GM, KR, Z);
            double az = ShipMotion.csrbc_Accelerations_Z(Prob, Ls, B, D, Ts, Cb, V, LoadCase, TLC, GM, KR, X, Y);

            if (LoadCase == "H1" | LoadCase == "H2")
                ReturnValue = Math.Atan(Math.Abs(ax) / (g0 * Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, phi)) + az));

            if (LoadCase == "R1" | LoadCase == "R2" | LoadCase == "P1" | LoadCase == "P2")
                ReturnValue = Math.Atan(Math.Abs(ay) / (g0 * Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, theta)) + az));

            return ReturnValue;

        }

        public static double csrbc_Pressure_DryBulkCargo_In_StillWater(double rhoC, double alpha, double psi, double hDB, double hc, double Z)
        {
            double PCS = 0;
            double KC = 0;

            if (alpha <= 90)
            {
                KC = Math.Pow(Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, alpha)), 2) + (1 - Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, psi))) * Math.Pow(Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, alpha)), 2);
            }
            else if (alpha > 90)
            {
                KC = 0.0;
            }

            PCS = rhoC * g0 * KC * (hc + hDB - Z);

            if (hc + hDB - Z < 0)
            {
                PCS = 0;
            }

            return PCS;

        }

        public static double csrbc_Pressure_DryBulkCargo_Inertial(string LoadCase, double rhoC, double alpha, double psi, double ax, double ay, double az, double XG, double YG, double LH,
        double hDB, double hc, double X, double Y, double Z)
        {
            double PCW = 0;
            double KC = 0;

            if (alpha <= 90)
            {
                KC = Math.Pow(Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, alpha)), 2) + (1 - Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, psi))) * Math.Pow(Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, alpha)), 2);
            }
            else if (alpha > 90)
            {
                KC = 0.0;
            }

            switch (LoadCase.ToUpper())
            {
                case "H1":
                    PCW = rhoC * (0.25 * ax * 0.25 * LH + KC * az * (hc + hDB - Z));
                    break;
                case "H2":
                    PCW = rhoC * (0.25 * ax * -0.25 * LH + KC * az * (hc + hDB - Z));
                    break;
                case "F1":
                    PCW = 0;
                    break;
                case "F2":
                    PCW = 0;
                    break;
                case "R1":
                    PCW = rhoC * (0.25 * ay * (Y - YG) + KC * az * (hc + hDB - Z));
                    break;
                case "R2":
                    PCW = rhoC * (0.25 * ay * (Y - YG) + KC * az * (hc + hDB - Z));
                    break;
                case "P1":
                    PCW = rhoC * (0.25 * ay * (Y - YG) + KC * az * (hc + hDB - Z));
                    break;
                case "P2":
                    PCW = rhoC * (0.25 * ay * (Y - YG) + KC * az * (hc + hDB - Z));
                    break;
            }

            if (hc + hDB - Z < 0)
            {
                PCW = 0;
            }
            return PCW;

        }

        public static double csrbc_get_Kc(double alpha, double psi)
        {
            double KC = 0;

            if (alpha <= 90)
            {
                KC = Math.Pow(Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, alpha)), 2) + (1 - Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, psi))) * Math.Pow(Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, alpha)), 2);
            }
            else if (alpha > 90)
            {
                KC = 0.0;
            }

            return KC;
        }

        public static double csrbc_Flooded_Pressure_for_Trans_vertically_corrugated_bulkhead(string LoadCond, double rC, double hc, double hDB, double psi, double Perm, double ZF, double Z)
        {
            double rL = 0;
            double PB = 0;
            double PBF = 0;
            double PF = 0;
            rL = 1.025;

            if (ZF >= hc + hDB)
            {
                if (Z <= ZF & Z > hc + hDB)
                {
                    PBF = rL * g0 * (ZF - Z);
                }
                else if (Z <= hc + hDB)
                {
                    PBF = rL * g0 * (ZF - Z) + (rC - rL * (1 - Perm)) * g0 * (hc + hDB - Z) * Math.Pow(Math.Tan((double)XlCall.Excel(XlCall.xlfRadians, 45 - psi / 2)), 2);
                }
            }
            else
            {
                if (Z <= ZF & Z > hc + hDB)
                {
                    PBF = rC * g0 * (hc + hDB - Z) * Math.Pow(Math.Tan((double)XlCall.Excel(XlCall.xlfRadians, 45 - psi / 2)), 2);
                }
                else if (Z <= hc + hDB)
                {
                    PBF = rL * g0 * (ZF - Z) + (rC * (hc + hDB - Z) - rL * (1 - Perm) * (ZF - Z)) * g0 * Math.Pow(Math.Tan((double)XlCall.Excel(XlCall.xlfRadians, 45 - psi / 2)), 2);
                }
            }

            if (LoadCond.ToUpper() == "HOMO")
            {
                PB = rC * g0 * (hc + hDB - Z) * Math.Pow(Math.Tan((double)XlCall.Excel(XlCall.xlfRadians, 45 - psi / 2)), 2);
                PF = PBF - 0.8 * PB;
            }
            else if (LoadCond.ToUpper() == "ALT")
            {
                PF = PBF;
            }
            else
            {
                PF = rL * g0 * (ZF - Z);
            }

            return PF;
        }

    }

    public class HullScantling
    {

        // #############################################################################
        //         Section 1.3.2 - Plate thickness
        // #############################################################################

        public static double SideFrame_W(string ShipType, double Ry, double span, double space, double Ps, double Pw)
        {
            double am = 0;

            if (ShipType == "BC-A")
            {
                am = 0.42;
            }
            else
            {
                am = 0.36;
            }

            return 1.125 * am * (Ps + Pw) * space * Math.Pow(span, 2) / (10 * 0.9 * Ry) * Math.Pow(10, 3);

        }
        public static double csrbc_Lambda_for_plating(string StiffSystem, double Ry, double NormalStress)
        {
            double Lambda = 0;

            switch (StiffSystem.ToUpper())
            {
                case "L":
                    Lambda = 0.95 - 0.45 * Math.Abs(NormalStress / Ry);
                    break;
                case "T":
                    Lambda = 0.95 - 0.9 * Math.Abs(NormalStress / Ry);
                    break;
                case "O":
                    Lambda = 0.9;
                    break;
            }

            return (double)XlCall.Excel(XlCall.xlfMin, Lambda, 0.9);

        }

        public static double csrbc_Plating_tnet(double Ry, double space, double span, double P, double Lambda)
        {
            double ca = 0;

            ca = DesignBasic.csrbc_Ca(space, span);

            return 15.8 * ca * space * Math.Sqrt(Math.Abs(P) / (Lambda * Ry));

        }

        public static double csrbc_stiffiner_W(double Ry, double space, double span, double P, double Lambda, double M)
        {

            return P * space * Math.Pow(span, 2) * 1000 / (M * Lambda * Ry);

        }

        public static double csrbc_stiffener_Ash(double Ry, double space, double span, double Ps, double Pw, double phi)
        {
            double tauA = 0;

            tauA = Ry / Math.Sqrt(3);

            return 5 * (Ps + Pw) * space * span / (tauA * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, phi)));

        }

        public static double csrbc_get_Lambda_for_stiffener(string StiffSystem, double Ry, double NormalStress)
        {
            double Lambda = 0;

            switch (StiffSystem.ToUpper())
            {
                case "L":
                    Lambda = 1.2 * (1 - 0.85 * Math.Abs(NormalStress / Ry));
                    break;
                case "O":
                    Lambda = 0.9;
                    break;
            }

            return (double)XlCall.Excel(XlCall.xlfMin, Lambda, 0.9);

        }

    }

    public class SteelCoil
    {
        public const double g0 = 9.81;

        public static double csrbc_n2(int n3, double span, double LengthOfCoil)
        {

            double n2 = 0.0;

            if (n3 == 2)
            {
                if (span / LengthOfCoil > 0.0 & span / LengthOfCoil <= 0.5) n2 = 1;
                if (span / LengthOfCoil > 0.5 & span / LengthOfCoil <= 1.2) n2 = 2;
                if (span / LengthOfCoil > 1.2 & span / LengthOfCoil <= 1.7) n2 = 3;
                if (span / LengthOfCoil > 1.7 & span / LengthOfCoil <= 2.4) n2 = 4;
                if (span / LengthOfCoil > 2.4 & span / LengthOfCoil <= 2.9) n2 = 5;
                if (span / LengthOfCoil > 2.9 & span / LengthOfCoil <= 3.6) n2 = 6;
                if (span / LengthOfCoil > 3.6 & span / LengthOfCoil <= 4.1) n2 = 7;
                if (span / LengthOfCoil > 4.1 & span / LengthOfCoil <= 4.8) n2 = 8;
                if (span / LengthOfCoil > 4.8 & span / LengthOfCoil <= 5.3) n2 = 9;
                if (span / LengthOfCoil > 5.3 & span / LengthOfCoil <= 6.0) n2 = 10;
            }
            else if (n3 == 3)
            {
                if (span / LengthOfCoil > 0.0 & span / LengthOfCoil <= 0.33) n2 = 1;
                if (span / LengthOfCoil > 0.33 & span / LengthOfCoil <= 0.67) n2 = 2;
                if (span / LengthOfCoil > 0.67 & span / LengthOfCoil <= 1.2) n2 = 3;
                if (span / LengthOfCoil > 1.2 & span / LengthOfCoil <= 1.53) n2 = 4;
                if (span / LengthOfCoil > 1.53 & span / LengthOfCoil <= 1.87) n2 = 5;
                if (span / LengthOfCoil > 1.87 & span / LengthOfCoil <= 2.4) n2 = 6;
                if (span / LengthOfCoil > 2.4 & span / LengthOfCoil <= 2.73) n2 = 7;
                if (span / LengthOfCoil > 2.73 & span / LengthOfCoil <= 3.07) n2 = 8;
                if (span / LengthOfCoil > 3.07 & span / LengthOfCoil <= 3.6) n2 = 9;
                if (span / LengthOfCoil > 3.6 & span / LengthOfCoil <= 3.93) n2 = 10;
            }
            else if (n3 == 4)
            {
                if (span / LengthOfCoil > 0.0 & span / LengthOfCoil <= 0.25) n2 = 1;
                if (span / LengthOfCoil > 0.25 & span / LengthOfCoil <= 0.5) n2 = 2;
                if (span / LengthOfCoil > 0.5 & span / LengthOfCoil <= 0.75) n2 = 3;
                if (span / LengthOfCoil > 0.75 & span / LengthOfCoil <= 1.2) n2 = 4;
                if (span / LengthOfCoil > 1.2 & span / LengthOfCoil <= 1.45) n2 = 5;
                if (span / LengthOfCoil > 1.45 & span / LengthOfCoil <= 1.7) n2 = 6;
                if (span / LengthOfCoil > 1.7 & span / LengthOfCoil <= 1.95) n2 = 7;
                if (span / LengthOfCoil > 1.95 & span / LengthOfCoil <= 2.4) n2 = 8;
                if (span / LengthOfCoil > 2.4 & span / LengthOfCoil <= 2.65) n2 = 9;
                if (span / LengthOfCoil > 2.65 & span / LengthOfCoil <= 2.9) n2 = 10;
            }
            else if (n3 == 5)
            {
                if (span / LengthOfCoil > 0.0 & span / LengthOfCoil <= 0.2) n2 = 1;
                if (span / LengthOfCoil > 0.2 & span / LengthOfCoil <= 0.4) n2 = 2;
                if (span / LengthOfCoil > 0.4 & span / LengthOfCoil <= 0.6) n2 = 3;
                if (span / LengthOfCoil > 0.6 & span / LengthOfCoil <= 0.8) n2 = 4;
                if (span / LengthOfCoil > 0.8 & span / LengthOfCoil <= 1.2) n2 = 5;
                if (span / LengthOfCoil > 1.2 & span / LengthOfCoil <= 1.4) n2 = 6;
                if (span / LengthOfCoil > 1.4 & span / LengthOfCoil <= 1.6) n2 = 7;
                if (span / LengthOfCoil > 1.6 & span / LengthOfCoil <= 1.8) n2 = 8;
                if (span / LengthOfCoil > 1.8 & span / LengthOfCoil <= 2.0) n2 = 9;
                if (span / LengthOfCoil > 2.0 & span / LengthOfCoil <= 2.4) n2 = 10;
            }

            return n2;
        }

        public static double csrbc_get_l1(int n2, int n3, double LengthOfCoil)
        {

            double l1 = 0.0;
            if (n3 == 2)
            {
                switch (n2)
                {
                    case 1:
                        l1 = 0;
                        break;
                    case 2:
                        l1 = 0.5 * LengthOfCoil;
                        break;
                    case 3:
                        l1 = 1.2 * LengthOfCoil;
                        break;
                    case 4:
                        l1 = 1.7 * LengthOfCoil;
                        break;
                    case 5:
                        l1 = 2.4 * LengthOfCoil;
                        break;
                    case 6:
                        l1 = 2.9 * LengthOfCoil;
                        break;
                    case 7:
                        l1 = 3.6 * LengthOfCoil;
                        break;
                    case 8:
                        l1 = 4.1 * LengthOfCoil;
                        break;
                    case 9:
                        l1 = 4.8 * LengthOfCoil;
                        break;
                    case 10:
                        l1 = 5.3 * LengthOfCoil;
                        break;
                }
            }

            if (n3 == 3)
            {
                switch (n2)
                {
                    case 1:
                        l1 = 0;
                        break;
                    case 2:
                        l1 = 0.33 * LengthOfCoil;
                        break;
                    case 3:
                        l1 = 0.67 * LengthOfCoil;
                        break;
                    case 4:
                        l1 = 1.2 * LengthOfCoil;
                        break;
                    case 5:
                        l1 = 1.53 * LengthOfCoil;
                        break;
                    case 6:
                        l1 = 1.87 * LengthOfCoil;
                        break;
                    case 7:
                        l1 = 2.4 * LengthOfCoil;
                        break;
                    case 8:
                        l1 = 2.73 * LengthOfCoil;
                        break;
                    case 9:
                        l1 = 3.07 * LengthOfCoil;
                        break;
                    case 10:
                        l1 = 3.6 * LengthOfCoil;
                        break;
                }
            }

            if (n3 == 4)
            {
                switch (n2)
                {
                    case 1:
                        l1 = 0;
                        break;
                    case 2:
                        l1 = 0.25 * LengthOfCoil;
                        break;
                    case 3:
                        l1 = 0.5 * LengthOfCoil;
                        break;
                    case 4:
                        l1 = 0.75 * LengthOfCoil;
                        break;
                    case 5:
                        l1 = 1.2 * LengthOfCoil;
                        break;
                    case 6:
                        l1 = 1.45 * LengthOfCoil;
                        break;
                    case 7:
                        l1 = 1.7 * LengthOfCoil;
                        break;
                    case 8:
                        l1 = 1.95 * LengthOfCoil;
                        break;
                    case 9:
                        l1 = 2.4 * LengthOfCoil;
                        break;
                    case 10:
                        l1 = 2.65 * LengthOfCoil;
                        break;
                }
            }

            if (n3 == 5)
            {
                switch (n2)
                {
                    case 1:
                        l1 = 0;
                        break;
                    case 2:
                        l1 = 0.2 * LengthOfCoil;
                        break;
                    case 3:
                        l1 = 0.4 * LengthOfCoil;
                        break;
                    case 4:
                        l1 = 0.6 * LengthOfCoil;
                        break;
                    case 5:
                        l1 = 0.8 * LengthOfCoil;
                        break;
                    case 6:
                        l1 = 1.2 * LengthOfCoil;
                        break;
                    case 7:
                        l1 = 1.4 * LengthOfCoil;
                        break;
                    case 8:
                        l1 = 1.6 * LengthOfCoil;
                        break;
                    case 9:
                        l1 = 1.8 * LengthOfCoil;
                        break;
                    case 10:
                        l1 = 2.0 * LengthOfCoil;
                        break;
                }
            }



            return l1;
        }

        public static double csrbc_K1(double span, double space, double l1)
        {
            double K2 = 0;

            K2 = csrbc_K2(span, space, l1);


            return Math.Sqrt((1.7 * space * span * K2 - 0.73 * Math.Pow(space, 2) * Math.Pow(K2, 2) - Math.Pow((span - l1), 2)) / (2 * l1 * (2 * space + 2 * span * K2)));
        }

        public static double csrbc_K2(double span, double space, double l1)
        {
            return -space / span + Math.Sqrt(Math.Pow((space / span), 2) + 1.37 * Math.Pow((span / space), 2) * Math.Pow((1 - l1 / span), 2) + 2.33);
        }

        public static double csrbc_get_K3(int n2, double span, double l1)
        {

            double K3 = 0;
            switch (n2)
            {
                case 1:
                    K3 = span;
                    break;
                case 2:
                    K3 = span - Math.Pow(l1, 2) / span;
                    break;
                case 3:
                    K3 = span - 2 * Math.Pow(l1, 2) / (3 * span);
                    break;
                case 4:
                    K3 = span - 5 * Math.Pow(l1, 2) / (9 * span);
                    break;
                case 5:
                    K3 = span - Math.Pow(l1, 2) / (2 * span);
                    break;
                case 6:
                    K3 = span - 7 * Math.Pow(l1, 2) / (15 * span);
                    break;
                case 7:
                    K3 = span - 4 * Math.Pow(l1, 2) / (9 * span);
                    break;
                case 8:
                    K3 = span - 3 * Math.Pow(l1, 2) / (7 * span);
                    break;
                case 9:
                    K3 = span - 5 * Math.Pow(l1, 2) / (12 * span);
                    break;
                case 10:
                    K3 = span - 11 * Math.Pow(l1, 2) / (27 * span);
                    break;
            }

            return K3;
        }

        public static double csrbc_SteelCoil_tnet(double K1, double ay, double az, double F, double F1, double Lambda, double Ry, double theta1, double theta2)
        {

            double tnet = 0;
            if (theta1 == 0)
            {
                tnet = K1 * Math.Sqrt((g0 + az) * F / (Lambda * Ry));
            }
            else
            {
                tnet = K1 * Math.Sqrt((g0 * Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, theta1 - theta2)) + ay * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, theta1))) * F1 / (Lambda * Ry));
            }


            return tnet;
        }
        public static double csrbc_SteelCoil_w(double K3, double ay, double az, double F, double F1, double LamdaS, double Ry, double theta1, double theta2)
        {

            double ReturnValue = 0.0;
            if (theta1 == 0)
            {
                ReturnValue = K3 * (g0 + az) * F / (8 * LamdaS * Ry);
            }
            else
            {
                ReturnValue = K3 * (g0 * Math.Cos((double)XlCall.Excel(XlCall.xlfRadians, theta1 - theta2)) + ay * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, theta1))) * F1 / (8 * LamdaS * Ry);
            }

            return ReturnValue;
        }

        public static double csrbc_SteelCoil_Ash(double ay, double az, double F, double F1, double phi, double phi2, double Ry)
        {
            double ReturnValue = 0.0;
            double tauA = 0;

            tauA = Ry / Math.Sqrt(3);
            if (phi == 0)
            {
                ReturnValue = 5 * (g0 + az) * F / (tauA * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, phi2))) * Math.Pow(10, -3);
            }
            else
            {
                ReturnValue = 5 * ay * F1 / (tauA * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, phi)) * Math.Sin((double)XlCall.Excel(XlCall.xlfRadians, phi2))) * Math.Pow(10, -3);
            }

            return ReturnValue;
        }
    }
}
		

