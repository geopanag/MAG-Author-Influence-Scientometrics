/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.*;
import java.util.HashMap;
import java.util.Map;

/**
 * @author georg
 */
public class frontiers_2 {

    private static final int STEP = 100;
    private static final String zerosDirectory = "/storage2/mag10/cores_onlyNodes2";

    private static void iterate(String directory, int start, int end, PrintWriter core_sizes, PrintWriter author_frontiers) throws FileNotFoundException, IOException, Exception {
        BufferedReader fo = null;
        for (int incore = start; incore >= end; incore -= STEP) {
            //int[] id_outcore = new int[9007172];
            Map<Integer, Integer> id_outcore = new HashMap<>();
            //Arrays.fill(id_outcore, -1);
            ///////////////////////////////////////////////////////////////////
            ////////////////////      Outcore : 0         ////////////////////
            //////////////////////////////////////////////////////////////////
            int outcore = 0;
            try {
                fo = new BufferedReader(new FileReader(new File(zerosDirectory + "/core_" + incore + "_" + outcore + ".txt")));
                String ln = fo.readLine();
                int idx = 0;
                while (ln != null) {
                    idx++;
                    int id = Integer.parseInt(ln.replace("\n", ""));
                    id_outcore.put(id, outcore);
                    ln = fo.readLine();
                }
                core_sizes.println(incore + " " + outcore + " " + idx);
            } catch (Exception e) {
                System.out.println("not found");
            } finally {
                if (fo != null) {
                    fo.close();
                }
            }

            System.out.println("---------------------");
            System.out.println(incore);
            ///////////////////////////////////////////////////////////////////
            ////////////////////    Rest Outcores         ////////////////////
            //////////////////////////////////////////////////////////////////
            int outcoreStep = 100;
            for (outcore = outcoreStep; outcore <= 7900; outcore += outcoreStep) {
                if(outcore == 100){
                        outcoreStep = 100;
                }
//                System.out.println(outcore);
                fo = null;
                try {
                    fo = new BufferedReader(new FileReader(new File(directory + "/core_" + incore + "_" + outcore + ".txt")));
                    String ln = fo.readLine();
                    int idx = 0;
                    while (ln != null) {
                        idx++;
                        int id = Integer.parseInt(ln.replace("\n", ""));
                        id_outcore.put(id, outcore);
                        ln = fo.readLine();
                    }
                    core_sizes.println(incore + " " + outcore + " " + idx);
                } catch (Exception ign) {
//                    System.out.println("not found");
			System.out.println(incore + " @ " + outcore);
                } finally {
                    if (fo != null) {
                        fo.close();
                    }
                }
            }

            for (Map.Entry<Integer, Integer> entry : id_outcore.entrySet()) {
                author_frontiers.println(entry.getKey() + "\t" + incore + "#" + entry.getValue());
            }

            //for (int i = 0; incore <= 9007172; i += 1) {
            //    author_frontiers.println(i + " " + incore + "#" + id_outcore[i]);
            //}
        }
    }

    public static void main(String[] args) throws FileNotFoundException, IOException, Exception {
        // list of author - frontiers size = 9007172
        PrintWriter author_frontiers = new PrintWriter(new File("/storage3/dcore/author_frontiers_ids2.csv"));
        PrintWriter core_sizes = new PrintWriter(new File("/storage3/dcore/core_sizes_ids2.csv"));
        String directory;
        int start, end;
//        storage2:
//        cores_onlyNodes2:    0 -> 1905
//        storage3:
//        cores_ids       : 1904 -> 3770
//        cores_ids2      : 3770 -> 5609
//        cores_ids3      : 5609 -> 7598
//        cores_ids4      : 7598 -> 7859

/*
        // Directory /storage3/cores_ids4
        directory = "/storage3/dcore/cores_ids4";
        start = 7860;
        end = 7598;
        iterate(directory, start, end, core_sizes, author_frontiers);

        // Directory storage3/cores_ids3
        directory = "/storage3/dcore/cores_ids3";
        start = 7597;
        end = 5609;
        iterate(directory, start, end, core_sizes, author_frontiers);
*/
        // Directory storage3/cores_ids2
        directory = "/storage3/dcore/cores_ids2";
        //start = 5608;
	start = 5600;
       	//end = 3770;
	end = 3800;
        iterate(directory, start, end, core_sizes, author_frontiers);
/*
        // Directory storage3/cores_ids
        directory = "/storage3/dcore/cores_ids";
        start = 3769;
        end = 1904;
        iterate(directory, start, end, core_sizes, author_frontiers);

        // Directory storage2/cores_onlyNodes2

        directory = "/storage2/mag10/cores_onlyNodes2";
        start = 1903;
        end = 0;
        iterate(directory, start, end, core_sizes, author_frontiers);
*/
        author_frontiers.close();
        core_sizes.close();

        // BufferedReader in = new BufferedReader(new FileReader(folder));
        //core_sizes.close();
        //use_d.store_intermediate("/storage2/mag10/tmp_dict.txt");
    }
}
