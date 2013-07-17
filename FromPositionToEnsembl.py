#! /usr/bin/env python
# -*- coding:Utf-8 -*-



"""
This script convert genomic positions in a tsv file to Ensembl gene id
using a .gtf or .gff file
usage:
From....py File1.tsv columnNumber File2.gtf
Need to be tested for column number other than 1....
"""
import sys;

class Gene(object):	
	def __init__(self, chromosome, ID , start, end, name):
		self.ID=ID;
		self.Name=name;
		self.Chr=chromosome;
		self.Start=[];
		self.Start.append(start);
		self.End=[];
		self.End.append(end);
	
def readGTF(gtfFile):
	genes={};
	for lines in open(gtfFile):
		chromosome=lines.split()[0];
		start=lines.split()[3];
		end=lines.split()[4];
		info=lines.split('\t')[8];
		name="";
		if("gene_name" in info):
		#	print(info);
			index=(info.split(' ')).index("gene_name");
			index+=1;
			name=(info.split(' ')[index]).split('"')[1];
		#	print(name);
		geneID=info.split(";")[0].split('"')[1];
		if geneID not in genes:
			#print(geneID);
			genes[geneID]=Gene(chromosome, geneID, start, end, name);
		else:
			genes[geneID].Start.append(start);
			genes[geneID].End.append(end);
			if genes[geneID].Name=="":
				genes[geneID].Name=name;
	return genes;

def getGene(chrom, start, end, genes):
	a=""
	
	#print(start+end);
	for i in genes:
		if (genes[i].Chr==chrom):
			#print("trouve")
			#print (genes[i].End);
			if end in genes[i].End:
				#print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
				if str(int(start)+1) in genes[i].Start:
					a=genes[i].ID;
					if(genes[i].Name!=""):
						a=a+" "+genes[i].Name;
					break;
	if(a==""):
		a=chrom+":"+start+"-"+end;
	return a;

def changeColumn(tsvFile, columnNumber, genes):
	columnNumber-=1;
	for lines in open(tsvFile):
		splited=lines.split('\t');
		newLine="";
                chromPos=splited[columnNumber];
                chrom=chromPos.split(':')[0];
                chromStart=chromPos.split(':')[1].split('-')[0];
                chromEnd=chromPos.split()[0].split(':')[1].split('-')[1];
                correspondant_gene=getGene(chrom, chromStart, chromEnd, genes);
		print(correspondant_gene);
		#3 cases: first, last and somewhere else on the list.
		"""if columnNumber==0:
			newLine=newLine+correspondant_gene;
			i=1;
			while i<len(splited):
				newLine=newLine+splited[i];
				i+=1;
		elif (columnNumber==(len(splited)-1)):
			i=0;
			while i<(len(splited)-1):
				newLine=newLine+splited[i];
				i+=1;
			newLine=newLine+correspondant_gene;
		else:
			i=0;
			while(i<columnNumber):
				newLine=newLine+splited[i];
				i+=1;
			newLine=newLine+correspondant_gene;
			i+=1;
			while(i<len(splited)):
				newLine=newLine+splited[i];
				i+=1;
		print(newLine);"""
			
			
			


if __name__=="__main__":
	genes=readGTF(sys.argv[3]);
	changeColumn(sys.argv[1], int(sys.argv[2]), genes);

