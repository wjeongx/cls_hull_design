using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ExcelDna.Integration;

namespace XEF.Buckling
{
    public class Buckling
    {
        [ExcelFunction(Description = "Buckling Factor K1", Category = "Buckling")]
        public static Double Buckling_Factor_K1(double psi)
        {
            double K = 0;

            if (psi <= 1 & psi >= 0)
            {
                K = 8.4 / (psi + 1.1);
            }
            else if (psi < 0 & psi > -1)
            {
                K = 7.63 - psi * (6.26 - 10 * psi);
            }
            else if (psi <= -1)
            {
                K = Math.Pow((1 - psi), 2) * 5.973;
            }

            return K;
        }

        [ExcelFunction(Description = "Buckling Factor K2", Category = "Buckling")]
        public static Double Buckling_Factor_K2(double Panel_a, double Panel_b, double psi, double F1)
        {

            double K = 0;
            double alpha = 0;

            alpha = Panel_a / Panel_b;
            if (psi >= 0 & psi <= 1)
            {
                K = F1 * Math.Pow((1 + 1 / Math.Pow(alpha, 2)), 2) * 2.1 / (psi + 1.1);
            }
            else if (psi < 0 & psi > -1)
            {
                if (alpha >= 1 & alpha < 1.5)
                {
                    K = F1 * (Math.Pow((1 + 1 / Math.Pow(alpha, 2)), 2) * 2.1 * (1 + psi) / 1.1 - psi / Math.Pow(alpha, 2) * (13.9 - 10 * psi));
                }
                else if (alpha > 1.5)
                {
                    K = Math.Pow((1 + 1 / Math.Pow(alpha, 2)), 2) * 2.1 * (1 + psi) / 1.1 - psi / Math.Pow(alpha, 2) * (5.87 + 1.87 * Math.Pow(alpha, 2) + 8.6 / Math.Pow(alpha, 2) - 10 * psi);
                    K = F1 * K;
                }
            }

            else if (psi <= -1)
            {
                if (alpha >= 1 & alpha <= 3 * (1 - psi) / 4)
                {
                    K = F1 * Math.Pow(((1 - psi) / alpha), 2) * 5.975;
                }
                else if (alpha > 3 * (1 - psi) / 4)
                {
                    K = F1 * (Math.Pow(((1 - psi) / alpha), 2) * 3.9675 + 0.5375 * Math.Pow(((1 - psi) / alpha), 4) + 1.87);
                }
            }


            return K;
        }

        [ExcelFunction(Description = "Buckling Factor K5", Category = "Buckling")]
        public static Double Buckling_Factor_K5(Double alpha)
        {
            double kt = 0;

            if (alpha >= 1)
            {
                kt = (5.34 + 4 / Math.Pow(alpha, 2));
            }
            else if (alpha > 0 & alpha < 1)
            {
                kt = (4 + 5.34 / Math.Pow(alpha, 2));
            }

            double K5 = kt * Math.Sqrt(3);

            return K5;
        }

        [ExcelFunction(Description = "Buckling Factor K6", Category = "Buckling")]
        public static Double Buckling_Factor_K6(Double a, Double b, Double Da, Double Db)
        {
            double alpha = 0;
            double R = 0;
            double K6 = 0;

            alpha = a / b;

            double K5 = 0;

            K5 = Buckling_Factor_K5(alpha);

            if (Da / a <= 0.7 & Db / b <= 0.7)
            {
                R = (1 - Da / a) * (1 - Db / b);
            }
            else
            {
                R = 0.022;
            }

            K6 = R * K5;

            return K6;
        }


        private static Double Buckling_B(Double kx, Double ky, Double sigx, Double sigy)
        {

            if (sigx > 0 & sigy > 0)
            {
                return Math.Pow((kx * ky), 5);
            }
            else
            {
                return 1.0;
            }

        }

        private static Double Buckling_F(double f1, double alpha, double Lamda, double K)
        {
            double c1 = 0;
            double Lamdap2;

            c1 = (1 - f1 / alpha);

            Lamdap2 = Math.Pow(Lamda, 2) - 0.5;

            if (Lamdap2 <= 1)
            {
                Lamdap2 = 1;
            }
            else if (Lamdap2 >= 3)
            {
                Lamdap2 = 3;
            }

            //            Excel.Application xApp = new Excel.Application();
            //            Excel.WorksheetFunction WorksheetFunction = xApp.WorksheetFunction;

            double F = (1 - ((K / 0.91) - 1) / Lamdap2) * c1;

            double ReturnValue = (double)XlCall.Excel(XlCall.xlfMax, F, 0);

            return ReturnValue;
        }

        private static Double Buckling_H(double Lamda, double c, double R)
        {
            double T = Lamda + 14 / (15 * Lamda) + 1 / 3;

            double H = Lamda - 2 * Lamda / (c * (T + Math.Sqrt(Math.Pow(T, 2) - 4)));

            double ReturnValue = (double)XlCall.Excel(XlCall.xlfMax, H, R);

            return ReturnValue;
        }

        [ExcelFunction(Description = "Buckling Reduction Factor ky", Category = "Buckling")]
        public static double Buckling_Reduction_Factor_ky(double F1, double Panel_a, double Panel_b, double psi, double K, double Lamda, double Sigma_Y)
        {

            Double alpha = Panel_a / Panel_b;

            double c = Bucling_Factor_c(psi);

            Double LamdaC = c / 2 * (1 + Math.Sqrt(1 - 0.88 / c));

            double R = 0;
            if (Lamda < LamdaC)
            {
                R = Lamda * (1 - Lamda / c);
            }
            else if (Lamda >= LamdaC)
            {
                R = 0.22;
            }

            double F = Buckling_F(F1, alpha, Lamda, K);

            double H = Buckling_H(Lamda, c, R);

            double ky = c * (1 / Lamda - (R + Math.Pow(F, 2) * (H - R)) / Math.Pow(Lamda, 2));

            if (Sigma_Y <= 0)
            {
                return 1.0;
            }
            else
            {
                return ky;
            }

        }

        [ExcelFunction(Description = "Buckling Reduction Factor kx", Category = "Buckling")]
        public static double Buckling_Reduction_Factor_kx(double Panel_a, double Panel_b, double psi, double Lamda, double Sigma_X)
        {

            Double alpha = Panel_a / Panel_b;

            double c = Bucling_Factor_c(psi);

            Double LamdaC = c / 2 * (1 + Math.Sqrt(1 - 0.88 / c));

            double kx = c * (1 / Lamda - 0.22 / Math.Pow(Lamda, 2));

            if (Sigma_X <= 0 || Lamda < LamdaC)
            {
                return 1.0;
            }
            else
            {
                return kx;
            }
        }

        private static double Bucling_Factor_c(double psi)
        {

            double c = 1.25 - 0.12 * psi;

            double ReturnValue = (double)XlCall.Excel(XlCall.xlfMin, c, 1.25);

            return ReturnValue;
        }
    }
}
