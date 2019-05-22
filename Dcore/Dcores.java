import java.io.*;
import java.util.*;
import java.util.zip.*;
import java.util.concurrent.ExecutorService;  
import java.util.concurrent.Executors;  

public class cores2{
	public ArrayList<int []> web=new ArrayList<int []>();
	public ArrayList<Integer> outD=new ArrayList<Integer>();
	public ArrayList<int []> webr=new ArrayList<int []>();
	public ArrayList<Integer> inD=new ArrayList<Integer>();
	public ArrayList<Integer> ids=new ArrayList<Integer>();
 
	//assume ids are numeric 0 to N no missing values in between
	public cores2(String out,String in,String degrees) throws Exception{
		
		//another hack to preallocate
		int i=0;
		BufferedReader f=new BufferedReader(new FileReader(degrees));
		String ln=f.readLine();
		int t=0;
   
		while(ln!=null){
			String [] lna=ln.split("\t");
			t=Integer.parseInt(lna[0]);
			outD.add(t);
			web.add(new int[t]);
			t=Integer.parseInt(lna[1]);
			inD.add(t);
			webr.add(new int[t]);
			ids.add(i);
			ln=f.readLine();
			i++;
		}
   
		this.load(new BufferedReader(new FileReader(out)));
		this.loadr(new BufferedReader(new FileReader(in)));		
	}
 
	public void load(BufferedReader f) throws Exception{
		String ln=f.readLine();
		int pos=0;
		while(ln!=null){
			String[] lna=ln.split("\t");
			for(int i=1;i<lna.length;i++){
				web.get(pos)[i-1] = Integer.parseInt(lna[i]);
			}
			ln=f.readLine();
			pos++;
		}
	}
 
	public void loadr(BufferedReader f) throws Exception{
		String ln=f.readLine();
		int pos=0;
		while(ln!=null){
			String [] lna=ln.split("\t");
			for(int i=1;i<lna.length;i++){
				webr.get(pos)[i-1]=Integer.parseInt(lna[i]);
			}
			ln=f.readLine();
			pos++;
		}
	}
 
 
	public void compute(int k,int l){
		//System.err.println("Starting k:"+k+" l:"+l);
		boolean ff=true;
		int o=0;
		while(ff){
			ff=false;
			ArrayList<Integer> tokeep=new ArrayList<Integer>();
			int temp=0;
			for(int i=0;i<ids.size();i++){
				
				int id=ids.get(i);
				if(inD.get(id)>=k && outD.get(id)>=l){
					//ff=true;
					//ids.remove(i);
					//i--;
					tokeep.add(id);
				}
				else{
					for (int j=0;j<web.get(id).length;j++){
						temp=web.get(id)[j];
						inD.set(temp,inD.get(temp)-1);
					}
					for (int j=0;j<webr.get(id).length;j++){
						temp=webr.get(id)[j];
						outD.set(temp,outD.get(temp)-1);
					}
					ff=true;
				}
			}
			ids=tokeep;
			o++;
		}

	}
	public void loadCache(ObjectInputStream fids,ObjectInputStream fid,ObjectInputStream fod) throws Exception{
		ids=(ArrayList<Integer>) fids.readObject();
		inD=(ArrayList<Integer>) fid.readObject();
		outD=(ArrayList<Integer>) fod.readObject();
		fids.close();
		fid.close();
		fod.close();		
	}
	public int size(){
		return this.ids.size();
	}
	public void saveIDS(String path)throws Exception{
		File file = new File(path);
		PrintWriter printWriter = new PrintWriter(file);
		for(int i=0;i<ids.size();i++){
		printWriter.println(ids.get(i));
		}
		printWriter.flush();
		printWriter.flush();
	}
	public void Save_cache(ObjectOutputStream oi,ObjectOutputStream id,ObjectOutputStream od) throws Exception{
		oi.writeObject(ids);
		oi.flush();
		oi.close();
		id.writeObject(inD);
		id.flush();
		id.close();
		od.writeObject(outD);
		od.flush();
		od.close();	
	}
	
	public static void main(String [] args){//test(){//
		try{
			
			//first create the first lines ..we cant use cache for this
			int outT=1;
			int inT=1;
			
			cores2 c=new cores2("./mag_outgraph_sample.txt","./mag_ingraph_sample.txt","./auth_degree_sample.txt");
			while (c.size()>0){
				c.compute(0,outT);
				ObjectOutputStream oi=new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream("./cache2/core_"+0+"_"+outT+".ids")));
				ObjectOutputStream w=new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream("./cache2/core_"+0+"_"+outT+".w")));
				ObjectOutputStream wr=new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream("./cache2/core_"+0+"_"+outT+".wr")));
				c.Save_cache(oi,w,wr);
				c.saveIDS("./cores_onlyNodes2/core_"+0+"_"+outT+".txt");
				outT++;
			}
			//System.out.println("Done out");
			
			
			//c=new cores2("./smgraph_T.txt","./rsmgraph_T.txt","./smdegree_T.txt");
			c=new cores2("./mag_outgraph_sample.txt","./mag_ingraph_sample.txt","./auth_degree_sample.txt");
			while (c.size()>0){
				c.compute(inT,0);
				ObjectOutputStream oi=new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream("./cache2/core_"+inT+"_"+0+".ids")));
				ObjectOutputStream w=new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream("./cache2/core_"+inT+"_"+0+".w")));
				ObjectOutputStream wr=new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream("./cache2/core_"+inT+"_"+0+".wr")));
				c.Save_cache(oi,w,wr);
				c.saveIDS("./cores_onlyNodes2/core_"+inT+"_"+0+".txt");
				inT++;
			}
			//System.out.println("Done in");
			
			
			for (int i=1;i<inT;i++){
				ObjectInputStream fo=new ObjectInputStream(new BufferedInputStream(new FileInputStream("./cache2/core_"+i+"_0.ids")));
				ObjectInputStream fw=new ObjectInputStream(new BufferedInputStream(new FileInputStream("./cache2/core_"+i+"_0.w")));
				ObjectInputStream fwr=new ObjectInputStream(new BufferedInputStream(new FileInputStream("./cache2/core_"+i+"_0.wr")));
				c.loadCache(fo,fw,fwr);
				int out=1;
				while (c.size()>0){
					c.compute(i,out);
					c.saveIDS("./cores_onlyNodes2/core_"+i+"_"+out+".txt");
					out++;
				 }
				
			}
			
		}
		catch(Exception e){
			e.printStackTrace();
		}
		
		

	}
	
  
}

	