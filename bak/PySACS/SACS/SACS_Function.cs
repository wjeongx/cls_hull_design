using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
 
namespace TESOL.SACS
{
    class SACS_Input
    {
        public SACS_Input()
        {

        }

        sealed public class Point
        {
            public Point(double x, double y, double z)
            {
                X = x;
                Y = y;
                Z = z;
            }

            public double X;
            public double Y;
            public double Z;
        }

        sealed public class SectionInfo
        {
            public SectionInfo(string SectionName, string SectionType, Double PLT1, Double Thk1, Double PLT2, Double Thk2)
            {
                SName = SectionName;
                SType = SectionType;
                PLT_1 = PLT1;
                Thk_1 = Thk1;
                PLT_2 = PLT2;
                Thk_2 = Thk2;
            }

            public string SName;
            public string SType;
            public double PLT_1;
            public double Thk_1;
            public double PLT_2;
            public double Thk_2;

        }

        sealed public class GRUPInfo
        {
            public GRUPInfo(string GrupName, string SectionName, String GrupColor)
            {
                GName = GrupName;
                SName = SectionName;
                GColor = GrupColor;
                //                PLT_1 = PLT1;
                //                Thk_1 = Thk1;
                //               PLT_2 = PLT2;
                //                Thk_2 = Thk2;
            }

            public string GName;
            public string SName;
            public string GColor;

        }

        sealed public class MemberInfo
        {
            public MemberInfo(String SJ, Point SJO, String EJ, Point EJO, GRUPInfo GRP)
            {
                StartJoint = SJ;
                StartJointOffset = SJO;
                EndJoint = EJ;
                EndJointOffset = EJO;
                GRUP = GRP;
            }
            
            public String StartJoint;
            public Point StartJointOffset;
            public String EndJoint;
            public Point EndJointOffset;
            public GRUPInfo GRUP;
        }

        sealed public class JointInfo
        {
            public JointInfo(string id, Point joint)
            {
                ID = id;
                Joint = joint;
            }

            public string ID;
            public Point Joint;
        }

        public string[] ReadSacsInput(String InputFile)
        {
            FileStream f = new FileStream(InputFile, FileMode.Open);
            StreamReader fr = new StreamReader(f);

            string StringLine;
            string[] StringLineArray = new string[1];

            int count = 0;

            while ((StringLine = fr.ReadLine()) != null)
            {
                if (StringLine.Trim().Length > 1 && StringLine.IndexOf("*") == -1)
                {
                    Array.Resize(ref StringLineArray, count + 1);
                    StringLineArray[count] = StringLine;
                    count += 1;
                }
            }

            f.Close();

            return StringLineArray;
        }

        public SectionInfo[] ReadSectData(string fname, ref int scnt)
        {
            FileStream fr = new FileStream(fname, FileMode.Open);
            StreamReader r = new StreamReader(fr);

            string str_line;
            scnt = 0;
            SectionInfo[] SECT = new SectionInfo[1];

            SECT = new SectionInfo[scnt + 1];

            while ((str_line = r.ReadLine()) != null)
            {
                if (str_line.IndexOf("*") == -1)
                {
                    if (str_line.Length > 5 && str_line.Substring(0, 4).Trim() == "SECT")
                    {
                        string s_tmp = string_fixed_colume(str_line, 100);

                        Array.Resize(ref SECT, scnt + 1);

                        String SNAME = s_tmp.Substring(5, 7).Trim();
                        String STYPE = s_tmp.Substring(15, 3).Trim();

                        SECT[scnt] = new SectionInfo(SNAME, STYPE, 0, 0, 0, 0);

                        scnt += 1;
                    }
                }
            }

            fr.Close();
            return SECT;
        }

        public GRUPInfo[] ReadGRUPData(string fname, ref int gcnt)
        {
            FileStream fr = new FileStream(fname, FileMode.Open);
            StreamReader r = new StreamReader(fr);

            string str_line;
            gcnt = 0;
            GRUPInfo[] GRUP = new GRUPInfo[1];

            GRUP = new GRUPInfo[gcnt + 1];

            while ((str_line = r.ReadLine()) != null)
            {
                if (str_line.IndexOf("*") == -1)
                {
                    if (str_line.Length > 6 && str_line.Substring(0, 5).Trim() == "GRUP")
                    {
                        string s_tmp = string_fixed_colume(str_line, 100);

                        Array.Resize(ref GRUP, gcnt + 1);

                        String GNAME = s_tmp.Substring(5, 3).Trim();
                        String GSECT = s_tmp.Substring(9, 7).Trim();
                        int iColor = (gcnt + 1) % 14;
                        GRUP[gcnt] = new GRUPInfo(GNAME, GSECT, iColor.ToString());

                        gcnt += 1;

                    }
                }
            }

            fr.Close();
            return GRUP;

        }

        public MemberInfo[] ReadMemberData(string fname, ref int mcnt)
        {
            FileStream fw = new FileStream("Member.dat", FileMode.Create);
            StreamWriter w = new StreamWriter(fw);

            FileStream fr = new FileStream(fname, FileMode.Open);
            StreamReader r = new StreamReader(fr);

            string str_line;
            mcnt = 0;
            MemberInfo[] MEMB = new MemberInfo[1];

            MEMB = new MemberInfo[mcnt + 1];
            Point SO, EO;

            while ((str_line = r.ReadLine()) != null)
            {
                if (str_line.IndexOf("*") == -1)
                {
                    if (str_line.Length > 6 && str_line.Substring(0, 6).Trim() == "MEMBER")
                    {
                        string s_tmp = string_fixed_colume(str_line, 100);

                        Array.Resize(ref MEMB, mcnt + 1);

                        String SJ = s_tmp.Substring(7, 4).Trim();
                        String EJ = s_tmp.Substring(11, 4).Trim();
                        String GNAME = s_tmp.Substring(16, 3).Trim();
                        String SNAME = null;
                        string GColor = null;

                        if (s_tmp.Substring(6, 1) == "1" || s_tmp.Substring(6, 1) == "2")
                        {
                            str_line = r.ReadLine();
                            s_tmp = string_fixed_colume(str_line, 100);

                            if (s_tmp.IndexOf("MEMB2") != -1)
                            {
                                str_line = r.ReadLine();
                                s_tmp = string_fixed_colume(str_line, 100);
                            }

                            Double SX = string_to_double(s_tmp.Substring(35, 6));
                            Double SY = string_to_double(s_tmp.Substring(41, 6));
                            Double SZ = string_to_double(s_tmp.Substring(47, 6));

                            Double EX = string_to_double(s_tmp.Substring(53, 6));
                            Double EY = string_to_double(s_tmp.Substring(59, 6));
                            Double EZ = string_to_double(s_tmp.Substring(65, 6));

                            SO = new Point(SX, SY, SZ);
                            EO = new Point(EX, EY, EZ);
                        }
                        else
                        {
                            SO = new Point(0.0, 0.0, 0.0);
                            EO = new Point(0.0, 0.0, 0.0);
                        }
                        
                        int gcnt = 0;
                        GRUPInfo[] GRUP = ReadGRUPData(fname, ref gcnt);

                        for (int cnt = 0; cnt < gcnt; cnt++)
                        {
                            if (GNAME == GRUP[cnt].GName)
                            {
                                SNAME = GRUP[cnt].SName;
                                GColor = GRUP[cnt].GColor;
                            }
                        }

                        GRUPInfo GRP = new GRUPInfo(GNAME, SNAME, GColor);

                        MEMB[mcnt] = new MemberInfo(SJ, SO, EJ, EO, GRP);

                        mcnt += 1;

                    }
                }
            }

            w.WriteLine(mcnt.ToString());
            for (int cnt = 0; cnt < mcnt; cnt++)
            {
                w.Write("{0},{1},{2},{3}\n", MEMB[cnt].StartJoint, MEMB[cnt].EndJoint, MEMB[cnt].GRUP.GName, MEMB[cnt].GRUP.SName);
            }

            fr.Close();
            return MEMB;

        }

        public JointInfo[] ReadJointData(string fname, ref int jcnt)
        {

            FileStream fr = new FileStream(fname, FileMode.Open);
            StreamReader r = new StreamReader(fr);

            string str_line;

            double XM, YM, ZM, XCM, YCM, ZCM;
            JointInfo[] JNT = new JointInfo[1];

            jcnt = 0;
            JNT = new JointInfo[jcnt + 1];

            while ((str_line = r.ReadLine()) != null)
            {
                if (str_line.IndexOf("*") == -1)
                {
                    if (str_line.Length > 5 && str_line.Substring(0, 5) == "JOINT")
                    {
                        if (str_line.IndexOf("PERSET") != -1) continue;

                        string s_tmp = string_fixed_colume(str_line, 100);

                        Array.Resize(ref JNT, jcnt + 1);

                        //=====================================================================================

                        XM = string_to_double(s_tmp.Substring(11, 7));
                        YM = string_to_double(s_tmp.Substring(18, 7));
                        ZM = string_to_double(s_tmp.Substring(25, 7));
                        XCM = string_to_double(s_tmp.Substring(32, 7));
                        YCM = string_to_double(s_tmp.Substring(39, 7));
                        ZCM = string_to_double(s_tmp.Substring(46, 7));

                        Point JointPoint = new Point(1000 * (XM + XCM / 100), 1000 * (YM + YCM / 100), 1000 * (ZM + ZCM / 100));
                        JNT[jcnt] = new JointInfo(s_tmp.Substring(6, 4).Trim(), JointPoint);
                        jcnt += 1;
                    }
                }
            }

            fr.Close();

            FileStream fw = new FileStream("Joint.dat", FileMode.Create);
            StreamWriter w = new StreamWriter(fw);

            w.WriteLine(jcnt.ToString());
            for (int cnt = 0; cnt < jcnt; cnt++)
            {
                w.Write("{0},{1},{2},{3:F0}\n", JNT[cnt].ID, JNT[cnt].Joint.X, JNT[cnt].Joint.Y, JNT[cnt].Joint.Z);
            }

            fw.Close();
            return JNT;

        }

        private double string_to_double(string s_x)
        {
            if (s_x.Trim() == "" || s_x.Trim() == null)
            {
                return 0.0;
            }
            else
            {
                return double.Parse(s_x.Trim());
            }
        }

        private string string_fixed_colume(string str_line, int col)
        {
            char[] c_tmp = new Char[col];
            for (int i = 0; i < col; i++)
            {
                c_tmp[i] = ' ';
            }

            StringReader sr = new StringReader(str_line);
            sr.ReadBlock(c_tmp, 0, col);

            string s_tmp = new string(c_tmp);

            return s_tmp;
        }

    }

    class SACS_Result
    {
        public SACS_Result()
        {

        }

        public string[] ReadSacsResult(ExtractiveList ExtList)
        {
            FileStream f = new FileStream(ExtList.ResultFile, FileMode.Open);
            StreamReader fr = new StreamReader(f);

            string _ReadLine;
            string[] StringLineArray = new string[1];

            int count = 0;

            while ((_ReadLine = fr.ReadLine()) != null)
            {
                if (_ReadLine.IndexOf(ExtList.SearchKey) != -1)
                {
                    for (int i = 0; i < Convert.ToInt32(ExtList.SkipLines); i++)
                    {
                        _ReadLine = fr.ReadLine();
                    }

                    while ((_ReadLine = fr.ReadLine()) != null)
                    {
                        if (_ReadLine.IndexOf(Convert.ToChar(12)) != -1) break;

                        if (_ReadLine.Trim().Length > 1)
                        {
                            Array.Resize(ref StringLineArray, count + 1);
                            StringLineArray[count] = _ReadLine;
                            count += 1;
                        }
                    }
                }
            }

            f.Close();

            return StringLineArray;
        }

        public string[] ReadSacsFatigue_Result(ExtractiveList ExtList)
        {

            string MemberType = string.Empty;

            switch (ExtList.ResultType)
            {
                case ("# Fatigue Result(WELD)"): 
                    MemberType = "WF";
                    break;
                case ("# Fatigue Result(TUB)"): 
                    MemberType = "TUB";
                    break;
            }

            FileStream fs = new FileStream(ExtList.ResultFile, FileMode.Open);
            StreamReader fr = new StreamReader(fs);

            string _ReadLine;
            string[] StringLineArray = new string[1];

            int count = 0;

            while ((_ReadLine = fr.ReadLine()) != null)
            {
                if (_ReadLine.IndexOf(ExtList.SearchKey) != -1)
                {
                    _ReadLine = fr.ReadLine();
                    if (_ReadLine.IndexOf("DAMAGE ORDER") != -1)
                    {

                        for (int j = 0; j < Convert.ToInt32(ExtList.SkipLines); j++)
                        {
                            _ReadLine = fr.ReadLine();
                        }

                        while ((_ReadLine = fr.ReadLine()) != null)
                        {
                            if (_ReadLine.IndexOf(Convert.ToChar(12)) != -1) break;

                            if (_ReadLine.Trim().Length > 1 && _ReadLine.IndexOf("-----") == -1)
                            {
                                if (_ReadLine.IndexOf(MemberType) != -1)
                                {
                                    Array.Resize(ref StringLineArray, count + 1);
                                    StringLineArray[count] = _ReadLine;
                                    count += 1;
                                }
                            }
                        }
                    }
                }
            }

            fr.Close();
            fs.Close();
            
            return StringLineArray;
        }

        public string[,] SacsResultArray(ExtractiveList ExtList)
        {
            string[] StringLineArray = null;

            if (ExtList.ResultType.IndexOf("Fatigue") != -1)
            {
                StringLineArray = ReadSacsFatigue_Result(ExtList);
            }
            else
            {
                StringLineArray = ReadSacsResult(ExtList);
            }

            int count = StringLineArray.GetUpperBound(0);

            char[] delimiterChars = { ',' };
            string[] sa_Col = ExtList.SplitColumn.Split(delimiterChars);
            int nCol = sa_Col.GetUpperBound(0);

            string[,] result = new string[count + 1, nCol];

            for (int icnt = 0; icnt <= count; icnt++)
            {
                for (int jcnt = 0; jcnt < nCol; jcnt++)
                {
                    int col1 = int.Parse(sa_Col[jcnt].Trim());
                    int col2 = int.Parse(sa_Col[jcnt + 1].Trim());

                    result[icnt, jcnt] = StringLineArray[icnt].Substring(col1, col2 - col1);
                }
            }

            return result;
        }



    }
}
