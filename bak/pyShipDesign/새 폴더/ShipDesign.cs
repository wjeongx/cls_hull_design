using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ExcelDna.Integration;

namespace XEF.ShipDesign
{
    public class ShipDesign
    {
        public const double g0 = 9.81;
        [ExcelFunction(Description = "Wave Coefficient (Cw)", Category = "Longitudinal Strength")]
        public static double WaveCoefficient([ExcelArgument(Description = @"Rule Length")] double Ls)
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

        [ExcelFunction(Description = "Distribution Factor for still water bending Moment", Category = "Longitudinal Strength")]
        public static double DISTFAC_SWBM(double Ls, double X)
        {
            double ReturnValue = 0.0;
            double Xs = 0;

            Xs = X / Ls;

            if (Xs >= 0 & Xs < 0.1)
            {
                ReturnValue = 1.5 * Xs;
            }
            else if (Xs >= 0.1 & Xs < 0.3)
            {
                ReturnValue = 4.25 * Xs - 0.275;
            }
            else if (Xs >= 0.3 & Xs <= 0.7)
            {
                ReturnValue = 1.0;
            }
            else if (Xs > 0.7 & Xs <= 0.9)
            {
                ReturnValue = -4.25 * Xs + 3.975;
            }
            else if (Xs > 0.9 & Xs <= 1.0)
            {
                ReturnValue = -1.5 * Xs + 1.5;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution factor for vertical wave bending moment", Category = "Longitudinal Strength")]
        public static double DISTFAC_VWBM(double Ls, double X)
        {

            double ReturnValue = 0;
            double Lx = X / Ls;

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
                ReturnValue = -2.85714 * Lx + 2.85714;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Vertical Wave Bending Moment(kN-m)", Category = "Longitudinal Strength")]
        public static double VerWaveBM(  [ExcelArgument(Description = @"Hull girder motion(HOGGING,HOG, H for Hogging Motion, SAGGING, SAG, S for Sagging Motion")] string HullGirderMotion,
                                    [ExcelArgument(Description = @"Rule Length")] double Ls, double B, double Cb, double X)
        {
            double ReturnValue = 0.0;
            double Cw = WaveCoefficient(Ls);

            if (HullGirderMotion.ToUpper() == "HOGGING" | HullGirderMotion.ToUpper() == "HOG" | HullGirderMotion.ToUpper() == "H")
            {
                ReturnValue = 0.190 * DISTFAC_VWBM(Ls, X) * Cw * Math.Pow(Ls, 2) * B * Cb;
            }
            else if (HullGirderMotion.ToUpper() == "SAGGING" | HullGirderMotion.ToUpper() == "SAG" | HullGirderMotion.ToUpper() == "S")
            {
                ReturnValue = -0.110 * DISTFAC_VWBM(Ls, X) * Cw * Math.Pow(Ls, 2) * B * (Cb + 0.7);
            }
            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution factor for positive vertical wave shear force", Category = "Longitudinal Strength")]
        public static double DISTFAC_VWSFP([ExcelArgument(Description = @"Rule Length")] double Ls,
                                            [ExcelArgument(Description = @"Block Coefficient")] double Cb,
                                            [ExcelArgument(Description = @"Considered Loacation from A.P")] double X)
        {
            double ReturnValue = 0.0;
            double fpl = 0;
            double Xs = X / Ls;

            fpl = 190 * Cb / (110 * (Cb + 0.7));

            if (0 <= Xs & Xs < 0.2)
            {
                ReturnValue = 4.6 * fpl * (X / Ls);
            }
            else if (0.2 <= Xs & Xs <= 0.3)
            {
                ReturnValue =  0.92* fpl;
            }
            else if (0.3 < Xs & Xs < 0.4)
            {
                ReturnValue = -(9.2 * fpl - 7) * Xs + 3.68*fpl-2.1;
            }
            else if (0.4 <= Xs & Xs <= 0.6)
            {
                ReturnValue = 0.7;
            }
            else if (0.6 < Xs & Xs < 0.7)
            {
                ReturnValue = 3 * Xs - 1.1;
            }
            else if (0.7 <= Xs & Xs <= 0.85)
            {
                ReturnValue = 1;
            }
            else if (0.85 < Xs & Xs < 1)
            {
                ReturnValue = -6.6666667 * Xs+ 6.6666667;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution factor for negative vertical wave shear force", Category = "Longitudinal Strength")]
        public static double DISTFAC_VWSFN([ExcelArgument(Description = @"Rule Length")] double Ls,
                                            [ExcelArgument(Description = @"Block Coefficient")] double Cb,
                                            [ExcelArgument(Description = @"Considered Loacation from A.P")] double X)
        {
            double ReturnValue = 0.0;
            double fpl = 0;
            double Xs = X / Ls;

            fpl = 190 * Cb / (110 * (Cb + 0.7));

            if (0 <= Xs & Xs < 0.2)
            {
                ReturnValue = 4.6 * Xs;
            }
            else if (0.2 <= Xs & Xs <= 0.3)
            {
                ReturnValue = 0.92;
            }
            else if (0.3 < Xs & Xs < 0.4)
            {
                ReturnValue = -2.2 * Xs + 1.58;
            }
            else if (0.4 <= Xs & Xs <= 0.6)
            {
                ReturnValue = 0.7;
            }
            else if (0.6 < Xs & Xs < 0.7)
            {
                ReturnValue = (10 * fpl - 7) * Xs - 6*fpl + 4.9;
            }
            else if (0.7 <= Xs & Xs <= 0.85)
            {
                ReturnValue = fpl;
            }
            else if (0.85 * Ls < X & X < Ls)
            {
                ReturnValue = -6.6666667 * fpl * Xs + 6.6666667*fpl;
            }

            return -ReturnValue;
        }

        [ExcelFunction(Description = "Vertical wave shear force (Qwv, kN)", Category = "Longitudinal Strength")]
        public static double VerWaveSF(string Sign, double Ls, double b, double Cb, double X)
        {
            double Cw = WaveCoefficient(Ls);
            double fqwv = 0.0;

            if (Sign == "+")
            {
                fqwv = DISTFAC_VWSFP(Ls, Cb, X);
            }
            else if (Sign == "-")
            {
                fqwv = DISTFAC_VWSFN(Ls, Cb, X);
            }

            return 0.30 * fqwv * Cw * Ls * b * (Cb + 0.7);
        }

        [ExcelFunction(Description = "Distribution Factor for Horizontal wave bending moment", Category = "Longitudinal Strength")]
        public static double DISTFAC_HWBM([ExcelArgument(Description = @"Rule Length")] double Ls,
                                            [ExcelArgument(Description = @"Considered Loacation from A.P")] double Xs)
        {
            double ReturnValue = 0.0;
            double Lx = 0;

            Lx = Xs / Ls;

            if (Lx >= 0 & Lx < 0.4)
            {
                ReturnValue = 2.5 * Lx;
            }
            else if (Lx >= 0.4 & Lx < 0.6)
            {
                ReturnValue = 1.0;
            }
            else if (Lx >= 0.6 & Lx <= 1.0)
            {
                ReturnValue = -2.5 * Lx + 2.5;
            }

            return ReturnValue;
        }

        [ExcelFunction(Description = "Distribution Factor for Horizontal wave shear force", Category = "Longitudinal Strength")]
        public static double DISTFAC_HWSF(double Ls, double Xs)
        {
            double ReturnValue = 0.0;
            double Lx = 0;

            Lx = Xs / Ls;

            if (Lx >= 0 & Lx < 0.2)
            {
                ReturnValue = 5.0 * Lx;
            }
            else if (Lx >= 0.2 & Lx < 0.3)
            {
                ReturnValue = 1.0;
            }
            else if (Lx >= 0.3 & Lx <= 0.4)
            {
                ReturnValue = -3.0 * Lx + 1.9;
            }
            else if (Lx > 0.4 & Lx <= 0.6)
            {
                ReturnValue = 0.7;
            }
            else if (Lx > 0.6 & Lx <= 0.7)
            {
                ReturnValue = 3.0 * Lx - 1.1;
            }
            else if (Lx > 0.7 & Lx <= 0.8)
            {
                ReturnValue = 1.0;
            }
            else if (Lx > 0.8 & Lx <= 1.0)
            {
                ReturnValue = -5.0 * Lx + 5.0;
            }
            return ReturnValue;
        }

        [ExcelFunction(Description = "Horizontal wave bending moment(kN-m)", Category = "Longitudinal Strength")]
        public static double HWBM(double Ls, double D, double Cb, double X)
        {
            double Cw = WaveCoefficient(Ls);

            return DISTFAC_HWBM(Ls, X) * 180 * Cw * Math.Pow(Ls, 2) * D * Cb * Math.Pow(10, -3);
        }

        [ExcelFunction(Description = "Horizontal wave shear force(kN-m)", Category = "Longitudinal Strength")]
        public static double HWSF(double Ls, double D, double Cb, double X)
        {
            double Cw = WaveCoefficient(Ls);

            return DISTFAC_HWSF(Ls, X) * 36 * Cw * Ls * D * (Cb + 0.7) * Math.Pow(10, -2);

        }

        [ExcelFunction(Description = "Rule Minimum Hull Girder Section Modulus(cm^3)", Category = "Longitudinal Strength")]
        public static double MINHGSM(double Ls, double B, double Cb) 
        {
            double ReturnValue = 0.0;
            double Cw = WaveCoefficient(Ls);

            ReturnValue = Cw * Math.Pow(Ls, 2) * B * (Cb + 0.7);

            return ReturnValue;
        }

        [ExcelFunction(Description = "Pitch Amplitude, ABS", Category = "Design Load(ABS)")]
        public static double ABS_PitchAmplitude([ExcelArgument(Description = "Rule Length")] double Ls,
                                                 [ExcelArgument(Description = "Block Coefficient")] double Cb,
                                                 [ExcelArgument(Description = "Service Speed")] double V)
        {

            double phi = 0;
            double k1 = 1030;

            phi = k1 * Math.Pow(0.75 * V / Cb, 0.25) / Ls;

            return phi;

        }

        [ExcelFunction(Description = "Pitch Period, ABS", Category = "Design Load(ABS)")]
        public static double ABS_PitchPeriod([ExcelArgument(Description = "Block Coefficient")] double Cb,
                                              [ExcelArgument(Description = "draft amidships for the relevant loading conditions")] double Ti)
        {

            double k2 = 3.5;
            double Tp = 0;


            Tp = k2 * Math.Sqrt(Cb * Ti);

            return Tp;

        }

        [ExcelFunction(Description = "Roll Period, ABS", Category = "Design Load(ABS)")]
        public static double ABS_RollPeriod([ExcelArgument(Description = "Ship Breadth")] double B,
                                             [ExcelArgument(Description = "metacentric height")] double GM,
                                             [ExcelArgument(Description = "roll radius of gyration, in m")] double KR)

        {

            double TR = 0;
            double k4 = 2;

            TR = k4 * KR / Math.Sqrt(GM);

            return TR;

        }

        [ExcelFunction(Description = "Roll Amplitude, ABS", Category = "Design Load(ABS)")]
        public static double ABS_RollAmplitude([ExcelArgument(Description = "Rule Length")] double Ls,
                                             [ExcelArgument(Description = "Ship Breadth")] double B,
                                             [ExcelArgument(Description = "draft, as defined in 3-1-1/9, m (ft)")]double Ts,
                                             [ExcelArgument(Description = "Block Coefficient")] double Cb,
                                             [ExcelArgument(Description = "Service Speed")] double V,
                                             [ExcelArgument(Description = "draft amidships for the relevant loading conditions")]  double Ti,
                                             [ExcelArgument(Description = "metacentric height")] double GM,
                                             [ExcelArgument(Description = "roll radius of gyration, in m")] double KR)
        {

            double TR = 0;

            TR = ABS_RollPeriod(B, GM, KR);

            double CR = 1.3 - 0.025 * V;
            double Cdi = 1.06 * (Ts / Ti) - 0.06;
            double Delta = 10.05 * Ls * B * Ts * Cb;
            double kth = 0.005;
            double RA = 0.0;

            if (TR > 20)
            {
                RA = CR * (35 - kth * Cdi * Delta / 1000);
            }
            else if (12.5 <= TR & TR <= 20)
            {
                RA = CR * (35 - kth * Cdi * Delta / 1000) * (1.5375 - 0.027 * TR);
            }
            else
            {
                RA = CR * (35 - kth * Cdi * Delta / 1000) * (0.8625 + 0.027 * TR);
            }

            return RA;
        }

        [ExcelFunction(Description = "Acceleration Parameter a0, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Acceleration_Parameter([ExcelArgument(Description = "Rule Length")] double Ls,
                                             [ExcelArgument(Description = "1.3 – 0.47Cb for strength formulation ")] double k0)
        {
            double a0 = k0 * (2.4 / Math.Sqrt(Ls) + 34 / Ls - 600 / Math.Pow(Ls, 2));

            return a0;

        }

        [ExcelFunction(Description = "Vertical Acceleration, Positive downward, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Vertical_Acceleration([ExcelArgument(Description = "Rule Length")] double Ls,
                                             [ExcelArgument(Description = "Ship Breadth")] double B,
                                             [ExcelArgument(Description = "µ wave heading angle in degrees, 0° for head sea, and 90° for beam sea for wave coming from starboard")] double mu,
                                             [ExcelArgument(Description = "1.3 – 0.47Cb for strength formulation ")] double k0,
                                             [ExcelArgument(Description = "Longitudinal location considered from AE in m")] double XLOC, 
                                             double ZLOC)
        {

            // µ(mu) : wave heading angle in degrees, 0° for head sea, and 90° for beam sea for wave coming from starboard 
            double rad_mu = (double)XlCall.Excel(XlCall.xlfRadians, mu);

            double kv = ABS_Acc_kv(Ls, XLOC);
            double Cv = ABS_Acc_Cv(B, rad_mu, kv, ZLOC);
            double a0 = ABS_Acceleration_Parameter(Ls, k0);

            double av = Cv * kv * a0 * g0;


            return av;

        }


        [ExcelFunction(Description = "Longitudinal Acceleration, Positive forward, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Longitudinal_Acceleration([ExcelArgument(Description = "Rule Length")] double Ls,
                                       [ExcelArgument(Description = "1.3 – 0.47Cb for strength formulation ")] double k0, double YLOC)
        {

            double kl = ABS_Acc_kl(Ls, YLOC);
            double Cl = ABS_Acc_Cl(Ls);
            double a0 = ABS_Acceleration_Parameter(Ls, k0);

            double al = Cl * kl * a0 * g0;

            return al;

        }

        [ExcelFunction(Description = "Transverse Acceleration, Stardboard forward, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Trasverse_Acceleration([ExcelArgument(Description = "Rule Length")] double Ls,
                                       [ExcelArgument(Description = "Ship Breadth")]double B,
                                       [ExcelArgument(Description = "1.3 – 0.47Cb for strength formulation ")] double k0, double XLOC, double YLOC)
        {

            double kt = ABS_Acc_kt(B, YLOC);
            double Ct = ABS_Acc_Ct(Ls, XLOC);
            double a0 = ABS_Acceleration_Parameter(Ls, k0);

            double at = Ct * kt * a0 * g0;

            return at;

        }

        [ExcelFunction(Description = "Cv for Vertical Acceleration, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Acc_Cv([ExcelArgument(Description = "Ship Breadth")]double B,
                                             [ExcelArgument(Description = "wave heading angle in degrees, 0° for head sea, and 90° for beam sea for wave coming from starboard")] double mu,
                                             [ExcelArgument(Description = "[1 + 0.65(5.3 − 45/L)2 (x/L − 0.45)2]1/2")] double kv,
                                             double ZLOC)
        {

            double Cv = Math.Cos(mu) + (1 + 2.4 * ZLOC / B) * Math.Sin(mu) / kv;

            return Cv;
        }


        [ExcelFunction(Description = "kv for Vertical Acceleration, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Acc_kv([ExcelArgument(Description = "Rule Length")] double Ls, double XLOC)
        {

            double kv = Math.Sqrt(1 + 0.65 * Math.Pow(5.3 - 45 / Ls, 2) * Math.Pow(XLOC / Ls - 0.45, 2));

            return kv;
        }

        [ExcelFunction(Description = "Cl for Longitudinal Acceleration, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Acc_Cl([ExcelArgument(Description = "Rule Length")] double Ls)
        {

            double Cl = 0.35 - 0.0005 * (Ls - 200);

            return Cl;
        }

        [ExcelFunction(Description = "kl for Longitudinal Acceleration", Category = "Design Load(ABS)")]
        public static double ABS_Acc_kl([ExcelArgument(Description = "Rule Length")] double Ls, double YLOC)
        {

            double kl = 0.5 + 8 * YLOC / Ls;

            return kl;
        }

        [ExcelFunction(Description = "Ct for Transverse Acceleration, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Acc_Ct([ExcelArgument(Description = "Rule Length")] double Ls, double XLOC)
        {
            double Ct = 1.27 * Math.Sqrt(1 + 1.52 * Math.Pow(XLOC / Ls - 0.45, 2));

            return Ct;
        }

        [ExcelFunction(Description = "kt for Transverse Acceleration, ABS", Category = "Design Load(ABS)")]
        public static double ABS_Acc_kt([ExcelArgument(Description = "Ship Breadth")]double B, double YLOC)
        {
            double kt = 0.35 + YLOC / B;

            return kt;
        }
        /* 
         * ========================================================================================================
            BUREAU VERIAS (BV) - Marine & Offshore
            REF.1) NR645 DT R01 E - Rules for the Classification of Floating Storage Regasification Units and Floating Storage Units
            REF.2) NR445.D1 DT R07 E - Rules for the Classification of Offshore Units, PART D - Service Notations
           ========================================================================================================
        */

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,Symbols Wave parameter , hw ", Category = "Design Load(BV)")]
        public static double BV_hw( [ExcelArgument(Description = "Rule Length, Ls")]double Ls)
        {
            double hw = 0;

            if(Ls < 350)
            {
                hw = 11.44 - Math.Pow(Math.Abs((Ls - 250) / 110), 3);
            }
            else if(Ls >= 350 && Ls <= 500)
            {
                hw = 200 / Math.Sqrt(Ls); 
            }

            return hw;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.1 Acceleration parameter , aB ", Category = "Design Load(BV)")]
        public static double BV_aB( [ExcelArgument(Description = "Design Condition(S for onsite condition, T for Transit condition")]string design_condition,
                                    [ExcelArgument(Description = "Pt-D,CH-1,Sec-5,3.2.5 Table-1 Navigation coefficient")]double n,
                                    [ExcelArgument(Description = "Rule Length")]double Ls,
                                    [ExcelArgument(Description = "Maximu ahead speed in transit, 0 in onsite condition" )]double Vs,
                                    [ExcelArgument(Description = "Wave parameter")]double hw)
        {
            double aB = 0;

            if (design_condition == "S" || design_condition == "OnSite")
            {
                aB = n * (2.4 / Math.Sqrt(Ls)+ 3*hw/Ls);
            }
            else if (design_condition == "T" || design_condition == "Transit")
            {
                aB = n * (0.2*Vs/ Math.Sqrt(Ls) + 3 * hw / Ls);
            }

            return aB;
        }

        [ExcelFunction(Description = "NR445.D1 DT R07 E Pt-D,CH-1,Sec-5,3.4.2 Rule surge acceleration , aSU (m/sec^2) ", Category = "Design Load(BV)")]
        public static double BV_aSurge([ExcelArgument(Description = "Pt-D,CH-1,Sec-5,3.2.5 Table-1 Navigation coefficient")]double n)
        {
            double aSU = 0.8 * n;

            return aSU;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.3 Rule sway acceleration , aSW (m/sec^2)", Category = "Design Load(BV)")]
        public static double BV_aSway([ExcelArgument(Description = "Acceleration parameter, aB")]double aB)
        {
            double aSW = 0.775 * aB * g0;

            return aSW;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.4 Rule heave acceleration , aH (m/sec^2)", Category = "Design Load(BV)")]
        public static double BV_aHeave([ExcelArgument(Description = "Acceleration parameter, aB")]double aB)
        {
            double aH = aB * g0;

            return aH;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.5 Rule Roll acceleration , aR (rad/sec^2)", Category = "Design Load(BV)")]
        public static double BV_aRoll([ExcelArgument(Description = "Moulded Breadth, B")]double B,
                                    [ExcelArgument(Description = "GM")]double GM,
                                    [ExcelArgument(Description = "Acceleration parameter, aB")]double aB,
                                    [ExcelArgument(Description = "Roll radius of gyration, in m")]double delta)
        {
            double RA = BV_RollAmplitude(B, GM, aB, delta);
            double TR = BV_RollPeriod(B, GM, delta);

            double aR = RA * Math.Pow(2 * Math.PI / TR, 2);

            return aR;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.7 Rule Yaw acceleration , aY (rad/sec^2)", Category = "Design Load(BV)")]
        public static double BV_aYaw( [ExcelArgument(Description = "Rule Length")]double Ls,
                                    [ExcelArgument(Description = "Acceleration parameter, aB")]double aB)
        {
            double aY = 1.581* aB * g0/Ls;

            return aY;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.5 Roll amplitude, AR (rad)", Category = "Design Load(BV)")]
        public static double BV_RollAmplitude([ExcelArgument(Description = "Moulded Breadth, B")]double B,
                                    [ExcelArgument(Description = "GM")]double GM,
                                    [ExcelArgument(Description = "Acceleration parameter, aB")]double aB,
                                    [ExcelArgument(Description = "Roll radius of gyration, in m")]double delta)

        {
            if(delta == 0)
            {
                delta = 0.35 * B;
            }
            double E = Math.Max(1.39*GM*B/ Math.Pow(delta,2), 1.0);

            double AR = Math.Min(aB * Math.Sqrt(E), 0.35);

            return AR;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.5 Roll period, TR (s)", Category = "Design Load(BV)")]
        public static double BV_RollPeriod( [ExcelArgument(Description = "Moulded Breadth, B")]double B,
                                            [ExcelArgument(Description = "GM")]double GM,
                                            [ExcelArgument(Description = "Roll radius of gyration, in m")]double delta)

        {
            if (delta == 0)
            {
                delta = 0.35 * B;
            }
            
            double TR = 2.2*delta/Math.Sqrt(GM);

            return TR;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.5 Pitch amplitude, Ap (rad)", Category = "Design Load(BV)")]
        public static double BV_PitchAmplitude( [ExcelArgument(Description = "Rule Length")]double Ls,
                                                [ExcelArgument(Description = "Block coefficient")]double Cb,
                                                [ExcelArgument(Description = "Acceleration parameter, aB")]double aB)

        {
            double hw = BV_hw(Ls);

            double Ap = 0.328 * aB * (1.32 - hw / Ls) * Math.Pow(0.6 / Cb, 0.75);

            return Ap;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.5 Pitch period, TP (s)", Category = "Design Load(BV)")]
        public static double BV_PitchPeriod([ExcelArgument(Description = "Rule Length")]double Ls)
        {
            double TP = 0.575 * Math.Sqrt(Ls);

            return TP;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.4.5 Pitch Acceleration, aP (rad/s^2)", Category = "Design Load(BV)")]
        public static double BV_aPitch([ExcelArgument(Description = "Rule Length")]double Ls,
                                   [ExcelArgument(Description = "Block coefficient")]double Cb,
                                   [ExcelArgument(Description = "Acceleration parameter, aB")]double aB)

        {
            double PA = BV_PitchAmplitude(Ls, Cb, aB);
            double TP = BV_PitchPeriod(Ls);

            double aP = PA * Math.Pow(2 * Math.PI / TP, 2);

            return aP;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.5.2 Rule relative wave elevation in upright ship conditions, h1", Category = "Design Load(BV)")]
        public static double BV_h1RWE(  [ExcelArgument(Description = "Pt-D,CH-1,Sec-5,3.2.5 Table-1 Navigation coefficient")]double n,
                                        [ExcelArgument(Description = "Rule Length")]double Ls,
                                        [ExcelArgument(Description = "Block coefficient")]double Cb,
                                        [ExcelArgument(Description = "Longitudinal location considered from AE in m")]double X)
        {

            double Cw = WaveCoefficient(Ls);
            double h1M = 0.67*n*Cw*(Cb+0.7);
            double h1AE = 0;
            if (Cb < 0.875)
            {
                h1AE = 0.7 * (4.35 / Math.Sqrt(Cb) - 3.25) * h1M;
            }
            else
            {
                h1AE = h1M;
            }

            double h1FE = (4.35 / Math.Sqrt(Cb) - 3.25) * h1M;

            double h1X = 0;
            if( X == 0)
            {
                h1X = h1AE;
            }
            else if(X >0 && X < 0.3*Ls)
            {
                h1X = h1AE - ((h1AE - h1M) / 0.3) * (X / Ls);
            }
            else if (X >= 0.3*Ls && X <= 0.7 * Ls)
            {
                h1X = h1M;
            }
            else if(X > 0.7*Ls && X < Ls)
            {
                h1X = h1M + ((h1FE - h1M) / 0.3) * (X / Ls - 0.7);
            }
            else if(X == Ls)
            {
                h1X = h1FE;
            }
                return h1X;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.5.2 Rule relative wave elevation in inclined ship conditions, h2", Category = "Design Load(BV)")]
        public static double BV_h2RWE ([ExcelArgument(Description = "Pt-D,CH-1,Sec-5,3.2.5 Table-1 Navigation coefficient")]double n,
                                       [ExcelArgument(Description = "Rule Length")]double Ls,
                                       [ExcelArgument(Description = "Block coefficient")]double Cb,
                                       [ExcelArgument(Description = "Moulded breadth , in m, measured at the waterline at draught T1 at the hull transverse section considered")]double Bw,
                                       [ExcelArgument(Description = "Roll Amplitude, in rad")] double AR,
                                       [ExcelArgument(Description = "Longitudinal location considred from AE in m")]double X)
        {


            double h1X = BV_h1RWE(n, Ls, Cb, X);

            double h2X = 0.5 * h1X + AR * Bw / 2;
            

            return h2X;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.5.2 Rule longitudinal acceleration, ax m/sec^2", Category = "Design Load(BV)")]
        public static double BV_aX([ExcelArgument(Description = "Pt-D,CH-1,Sec-5,3.2.5 Table-1 Navigation coefficient")]double n, 
                                    [ExcelArgument(Description = @"Upright(U) or Inclined(I) Condition")] string Direction,
                                    [ExcelArgument(Description = "Rule Length")]double Ls,
                                    [ExcelArgument(Description = "Block coefficient")]double Cb,
                                    [ExcelArgument(Description = "Acceleration parameter, aB")]double aB,
                                    [ExcelArgument(Description = "Draught associated to the loading condition considered")] double T1,
                                    [ExcelArgument(Description = "Vertical location considered from A/B, in m")]double Z)
        {

            double aSU = BV_aSurge(n);
            double PA = BV_PitchAmplitude(Ls, Cb, aB);
            double aP = BV_aPitch(Ls, Cb, aB);

            double a1X = Math.Sqrt(Math.Pow(aSU, 2) + Math.Pow(PA * g0 + aP * (Z - T1), 2));

            double a2X = 0.0;

            double aX = 0.0;
            if(Direction == "U" || Direction == "Upright")
            {
                aX = a1X;
            }
            else if(Direction == "I" || Direction == "Inclined")
            {
                aX = a2X;
            }

            return aX;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.5.2 Rule transverse acceleration, aY m/sec^2", Category = "Design Load(BV)")]
        public static double BV_aY([ExcelArgument(Description = "Pt-D,CH-1,Sec-5,3.2.5 Table-1 Navigation coefficient")]double n,
                                    [ExcelArgument(Description = @"Upright(U) or Inclined(I) Condition")] string Direction,
                                    [ExcelArgument(Description = "Rule Length")]double Ls,
                                    [ExcelArgument(Description = "Moulded Breadth, B")]double B,
                                    [ExcelArgument(Description = "Block coefficient")]double Cb,
                                    [ExcelArgument(Description = "Acceleration parameter, aB")]double aB,
                                    [ExcelArgument(Description = "Roll Amplitude, RA")]double RA,
                                    [ExcelArgument(Description = "Roll Acceleration, aR")]double aR,
                                    [ExcelArgument(Description = "Draught associated to the loading condition considered")] double T1,
                                    [ExcelArgument(Description = "Longitudinal location considred from AE in m")]double X,
                                    [ExcelArgument(Description = "Vertical location considered from A/B, in m")]double Z)
        {
            
            double aSW = BV_aSway(aB);
            double aYaw = BV_aYaw(Ls, aB);
            double X0 = X / Ls;
            double kX = Math.Max(1.2 * X0 * X0 - 1.1 * X0 + 0.2, 0.018);
            double a1Y = 0.0;

            double a2Y = Math.Sqrt(Math.Pow(aSW, 2) + Math.Pow(RA * g0 + aR * (Z - T1), 2)) + aYaw * aYaw * kX * Ls * Ls;

            double aY = 0.0;
            if (Direction == "U" || Direction == "Upright")
            {
                aY = a1Y;
            }
            else if (Direction == "I" || Direction == "Inclined")
            {
                aY = a2Y;
            }

            return aY;
        }

        [ExcelFunction(Description = "NR645 DT R01 E, Pt-D,CH-1,Sec-5,3.5.2 Rule transverse acceleration, aY m/sec^2", Category = "Design Load(BV)")]
        public static double BV_aZ([ExcelArgument(Description = "Pt-D,CH-1,Sec-5,3.2.5 Table-1 Navigation coefficient")]double n,
                                    [ExcelArgument(Description = @"Upright(U) or Inclined(I) Condition")] string Direction,
                                    [ExcelArgument(Description = "Rule Length")]double Ls,
                                    [ExcelArgument(Description = "Moulded Breadth, B")]double B,
                                    [ExcelArgument(Description = "Block coefficient")]double Cb,
                                    [ExcelArgument(Description = "Acceleration parameter, aB")]double aB,
                                    [ExcelArgument(Description = "Roll Acceleration, aR")]double aR,
                                    [ExcelArgument(Description = "Longitudinal location considred from AE in m")]double X,
                                    [ExcelArgument(Description = "Transverse location considred from C.L in m")]double Y)
        {

            double aH = BV_aHeave(aB);
            double aP = BV_aPitch(Ls, Cb, aB);
            double X0 = X / Ls;
            double kX = Math.Max(1.2 * X0 * X0 - 1.1 * X0 + 0.2, 0.018);

            double a1Z = Math.Sqrt(aH*aH+aP*aP*kX*Ls*Ls);
            double a2Z = Math.Sqrt(0.25*aH * aH + aR * aR * Y * Y);

            double aZ = 0.0;
            if (Direction == "U" || Direction == "Upright")
            {
                aZ = a1Z;
            }
            else if (Direction == "I" || Direction == "Inclined")
            {
                aZ = a2Z;
            }

            return aZ;
        }

    }
}



