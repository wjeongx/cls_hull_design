
        def SectionInfo[] ReadSectData(string fname, ref int scnt)
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