import os
import glob
import re
import tools
import subprocess
import find_clades2
import gc_stats
import tools
import sys
class Analyze(object): 
    def __init__(self,opt):
        self.opt = opt
    def gcStatAnalysis(self):
        opt = self.opt
        outFile = opt.label + "/gc-stat.csv"
        f = open(outFile, 'w')
        searchFile = " ".join(glob.glob(opt.search))
	if searchFile is "":
		print("no alignment file found! please provide your aligments with the structure specified in the examples")
		sys.exit(1)
	print("number of alignments found is " + str(len(searchFile.split(" "))))
        for align in searchFile.split(" "):
            gc_stats.main(align)	
        print "All GC stat files have been generated"

        search = opt.path + "/*/gc-stat.txt"

        print >>f, "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" %("GENE","SEQUENCE","TAXON","A_C","C_C","G_C","T_C","N_C","frag_C","A_R","C_R","G_R","T_R","c1_A_C","c1_C_C","c1_G_C","c1_T_C","c1_N_C","c1_frag_C","c1_A_R","c1_C_R","c1_G_R","c1_T_R","c2_A_C","c2_C_C","c2_G_C","c2_T_C","c2_N_C","c2_frag_C","c2_A_R","c2_C_R","c2_G_R","c2_T_R","c3_A_C","c3_C_C","c3_G_C","c3_T_C","c3_N_C","c3_frag_C","c3_A_R","c3_C_R","c3_G_R","c3_T_R")	
        f.close()
        tools.concatenateFiles(outFile, search)	
        print "Concatenated GC stats are written to %s" % (outFile)
        currPath = os.path.dirname(os.path.abspath(__file__))
        WS_HOME = os.environ['WS_HOME']
	if WS_HOME is None or WS_HOME == "":
		print("Please set up WS_HOME as specified in the installation guide!")
		sys.exit(1)

        command = 'Rscript'
        path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
        args = ["-p", WS_HOME, "-s", str(opt.mode),  "-i", opt.label]
        stderrFile = opt.label + "/error.log"
        cmd = [command, path2script] + args
        print "printing outputs and errors on " + stderrFile
        print cmd
        fi = open(stderrFile,'w')
        fi.close()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
    #       x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        err = open(stderrFile,'a')
        err.write(stdout)
        err.write(stderr)
        err.close()
    def occupancyAnalysis(self):
        opt = self.opt
        outFile = opt.label + "/occupancy.csv"
	print opt.search
        tools.occupancy(opt.search, outFile)
        print "All the occupancy stats have written on file %s" % (outFile)  
        currPath = os.path.dirname(os.path.abspath(__file__))
        WS_HOME = os.environ['WS_HOME']
	if WS_HOME is None or WS_HOME == "":
                print("Please set up WS_HOME as specified in the installation guide!")
                sys.exit(1)
        command = 'Rscript'
        path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
        if (opt.modelCond is None):
            args = ["-p", WS_HOME, "-s", str(opt.mode), "-i", opt.label, "-a", opt.annotation]
        else:
            args = ["-p",  WS_HOME, "-s", str(opt.mode), "-i", opt.label, "-a", opt.annotation, "-x", opt.modelCond]
        stderrFile = opt.label + "/error.log"
        cmd = [command, path2script] + args
        print "printing outputs and errors on " + stderrFile
        print cmd
        fi = open(stderrFile,'w')
        fi.close()

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
    #       x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        err = open(stderrFile,'a')
        err.write(stdout)
        err.write(stderr)
        err.close()

    def treesAnalyses(self):
        opt = self.opt
        outFile = opt.label + "/clades.txt"
	try:
	        f = open(outFile,'w')
        	f.close()
	except IOError:
		print("The result directory does not exist!")
		sys.exit(1)
		

        outFilethr = opt.label + "/clades.hs.txt"
	try:
	        f = open(outFilethr,'w')
        	f.close()
	except IOError:
		print("The result directory does not exist!")
		sys.exit(1)
        finegrained = opt.label + "/finegrained"	
        if not os.path.exists(finegrained):
	    try:
	    	os.makedirs(finegrained)
	    except IOError:
	    	print("The result directory does not exist!")
	    	sys.exit(1)
	searchFiles = " ".join(glob.glob(opt.search))
	if searchFiles == "" or searchFiles is None:
		print("No tree found! please follow the structure specified in the examples!")
		sys.exit(1)
	print("Number of trees found is: " + str(len(searchFiles.split(" ")))) 
	for tree in searchFiles.split(" "):
 #          tools.reroot(tree, opt.root, opt.annotation, 1)
	   try:
	   	tools.remove_edges_from_tree(tree, opt.threshold)
	   except ValueError:
	   	print("an error occurred in contracting low support branches")
		raise
	   	sys.exit(1)	

        searchFilesthr = " ".join(glob.glob(opt.searchthr))
	if searchFilesthr == "" or searchFilesthr is None:
		print("No contracted tree found!")
		sys.exit(1)
#        for tree in searchFilesthr.split(" "):
#            tools.reroot(tree, opt.root, opt.annotation, 1)

        searchFiles = " ".join(glob.glob(opt.searchrooted))
	print("number of contracted trees is :" + str(len(searchFilesthr.split(" "))))
        searchFilesthr = " ".join(glob.glob(opt.searchthrrooted))
        if float(opt.threshold)<= 1.0:
            multiplier = 100.
        else:
            multiplier = 1.0
	try:		
		find_clades2.main(opt.names, opt.clades, outFile, multiplier, searchFiles) 
	except ValueError:
		print("An error occured during tree analysis process!")
		raise
		sys.exit(1)
	try:
		find_clades2.main(opt.names, opt.clades, outFilethr, multiplier, searchFilesthr)
	except ValueError:
		print("An error occured during tree analysis process!")
		raise
		sys.exit(1)
	try:
	        f = open(outFile,'r')
	except IOError:
		print("could not open outfile: " + outFile)
		sys.exit(1)
        outRes = outFile + ".res"
	try:
	        oRes = open(outRes, 'w')
	except IOError:
		print("could not open result file: " + outRes)
		sys.exit(1)

        outResthr = outFilethr + ".res"
	try:
	        oResThr = open(outResthr, 'w')
	except IOError:
		print("could not open result file: " + oResThr )
		sys.exit(1)
        oRes.write("ID\tDS\tMONO\tBOOT\tCLADE\tBRANCHLEN\n")

        for line in f:
            linet = line.replace("\n","")
            listLine = linet.split("\t")
            b = os.path.basename(os.path.dirname(listLine[0]))

            #if opt.mode == 1:
            #	ID = os.path.basename(os.path.dirname(os.path.dirname(listLine[0])))
            #	method = re.sub("^-","",re.split(ID,b)[1])
            #else:
            ID = b
            tmp = re.split("-", b)
            method = tmp[len(tmp)-1]

            MONO = listLine[1]
            BOOT = listLine[2]
            CLADE = re.sub("\s+\(.*","", listLine[3])
	    BRANCHLEN = listLine[4]
            oRes.write( "%s\t%s\t%s\t%s\t%s\t%s\n" % (ID, method, MONO, BOOT, CLADE, BRANCHLEN))
        f.close()
        oRes.close()
        oResThr.write("ID\tDS\tMONO\tBOOT\tCLADE\tBRANCHLEN\n")
        f = open(outFilethr,'r')
        for line in f:
            linet = line.replace("\n","")
            listLine = linet.split("\t")

            b = os.path.basename(os.path.dirname(listLine[0]))
        #	if opt.mode == 1:
        #		ID = os.path.basename(os.path.dirname(os.path.dirname(listLine[0])))
        #		method = re.sub("^-","",re.split(ID,b)[1])
        #	else:
            ID = b
            tmp = re.split("-", b)
            method = tmp[len(tmp)-1]

            MONO = listLine[1]
            BOOT = listLine[2]
            CLADE = re.sub("\s+\(.*","",listLine[3])
	    BRANCHLEN = listLine[3]
            oResThr.write( "%s\t%s\t%s\t%s\t%s\t%s\n" % (ID, method, MONO, BOOT, CLADE, BRANCHLEN))
        oResThr.close()
        currPath = os.path.dirname(os.path.abspath(__file__))
        WS_HOME = os.environ['WS_HOME']
	if WS_HOME is None or WS_HOME == "":
                print("Please set up WS_HOME as specified in the installation guide!")
                sys.exit(1)
        command = 'Rscript'
        path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
	if opt.newModel is not None and opt.newOrder is not None:
	        args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.label, "-t", str(os.path.abspath(opt.newOrder)), "-y", str(os.path.abspath(opt.newModel)), 
			"-m", str(opt.missing)]
	elif opt.newModel is not None and opt.newOrder is None:
		args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.label, "-y", os.path.abspath(opt.newModel), "-m", str(opt.missing)]
	elif opt.newModel is None and opt.newOrder is not None:
		args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.label, "-t", os.path.abspath(opt.newOrder), "-m", str(opt.missing)]
	else:
		args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.label, "-m", str(opt.missing)]
        stderrFile = opt.label + "/error.log"
        cmd = [command, path2script] + args
        print "printing outputs and errors on " + stderrFile
        print cmd
        fi = open(stderrFile,'w')
        fi.close()
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
    #	x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        err = open(stderrFile,'a')
        err.write(stdout)
        err.write(stderr)
        err.close()
    def geneTreeBranchInfo(self):
        opt = self.opt
        searchFiles = " ".join(glob.glob(opt.search))
        for tree in searchFiles.split(" "):
            tools.reroot(tree, opt.root, opt.annotation, 1)
        treeName = glob.glob(opt.searchrooted)
        outFile = opt.label + "/branchStats.csv"
        outFile2 = opt.label + "/branchSupport.csv"
        tools.branchInfo(treeName, outFile, outFile2)	
        print "The branch Length and support values are written on file %s" % (outFile)
        currPath = os.path.dirname(os.path.abspath(__file__))
        WS_HOME = os.environ['WS_HOME']
	if WS_HOME is None or WS_HOME == "":
                print("Please set up WS_HOME as specified in the installation guide!")
                sys.exit(1)
        command = 'Rscript'
        path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
	if opt.newModel is not None and opt.newOrder is not None:
        	args = ["-p", WS_HOME, "-s", str(opt.mode), "-i", opt.label, "-t", str(os.path.abspath(opt.newOrder)), "-y", str(os.path.abspath(opt.newModel))]
        elif opt.newModel is not None and opt.newOrder is None:
        	args = ["-p", WS_HOME, "-s", str(opt.mode),  "-i", opt.label, "-y", os.path.abspath(opt.newModel)]
        elif opt.newModel is None and opt.newOrder is not None:
        	args = ["-p", WS_HOME, "-s", str(opt.mode), "-i", opt.label, "-t", os.path.abspath(opt.newOrder)]
        else:
        	args = ["-p", WS_HOME, "-s", str(opt.mode), "-i", opt.label]
        stderrFile = opt.label + "/error.log"
        cmd = [command, path2script] + args
        print "printing outputs and errors on " + stderrFile
        print cmd
        fi = open(stderrFile,'w')
        fi.close()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
    #       x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        err = open(stderrFile,'a')
        err.write(stdout)
        err.write(stderr)
        err.close()
    def relFreq(self):
	WS_HOME = os.environ['WS_HOME']
	if WS_HOME is None or WS_HOME == "":
                print("Please set up WS_HOME as specified in the installation guide!")
                sys.exit(1)
	opt = self.opt
	command = WS_HOME + "/" + "DiscoVista/src/utils/pos-for-hyp.sh"
	args = [opt.path, opt.annotation, opt.names, opt.label, opt.outg ]
	cmd = ["bash",command] + args
	stderrFile = opt.label + "/error.log"
	print "printing errors on " + stderrFile
	print cmd
	fi = open(stderrFile,'w')
	fi.close()
	print cmd
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	err = open(stderrFile,'a')
	err.write(stdout)
	err.write(stderr)
	err.close()
    def analyze(self):
        if self.opt.mode == 0 or self.opt.mode == 1:
            self.treesAnalyses()
        elif self.opt.mode == 2:
            self.gcStatAnalysis()
        elif self.opt.mode == 3:
            self.occupancyAnalysis()
        elif self.opt.mode == 4:
            self.geneTreeBranchInfo()
	elif self.opt.mode == 5:
	    self.relFreq()
