using System;
using System.Collections.Generic;
using System.Text;
using System.Xml;
using ExcelDna.Integration;
using XEF; 

namespace XEF.Fatigue
{
    public class Fatigue
    {
		[ExcelFunction(Description = "Strain_Life Curve", Category = "Fatigue")]
        public static double Strain_Life(double eta, double E, double sf, double b, double ef, double c)
        {
            double K1 = (sf / E);
            double K2 = ef;

            double N22 = 1;
            double N21 = 0.0;
            double fN21 = 0.0, fN22 = 0.0;

            while (Math.Abs(N22 - N21) > 1E-06)
            {
                N21 = N22;
                fN21 = K1 * Math.Pow(N21, b) + K2 * Math.Pow(N21, c) - eta;
                fN22 = b * K1 * Math.Pow(N21, (b - 1)) + c * K2 * Math.Pow(N21, (c - 1));
                N22 = N21 - fN21 / fN22;
            }
     
       		return N22;
       	
		}
        
        [ExcelFunction(Description = "Stress_Life Curve(Stress)", Category = "Fatigue")]
        public static double Stress_Life_Stress(double Life, double A, double m)
        {
        	double LogSR = (Math.Log(A) - Math.Log(Life))/m;
     
        	return Math.Pow(10, LogSR);
       	
		}
 
        [ExcelFunction(Description = "Stress_Life Curve(Life)", Category = "Fatigue")]
        public static double Stress_Life_Life(double SR, double A, double m)
        {
        	double LogN = Math.Log(A) - m*Math.Log(SR);
     
        	return Math.Pow(10, LogN);
       	
		}
        
        [ExcelFunction(Description = "Cumulative Damage", Category = "Fatigue")]
        public static double CumulativeDamage(double FL, double a, double m, double v0, double[] SR, double[] p, double[] n0, double[] GAMMAF)
        {
            // double hn	weibull shape parameter
            // double pn    fraction of desing life in load condition n
            // double qn    weibull scale parameter
            // double v0    long-term average reponse zero-crossing frequency
            
            double Td = FL*365*24*3600;
            double[] q = new double[10];
           	double D1 = 0;
            int n = 0;
            foreach(double StressRange in SR)
            {
            	q[n] = StressRange/(Math.Log(n0[n]));
            	D1 = D1 + p[n]*Math.Pow(q[n], m)*GAMMAF[n];
            	n += 1;
            }

			return v0*Td/a*D1;
		}
    }
}
