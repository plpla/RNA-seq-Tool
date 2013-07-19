#!/usr/bin/python

"""
This script transform the output from cuffdiff to a table that can be imported
in tmev to create a heat-map.
To use:
HeatMapFromCuffdiff.py file referenceEntry
File is a cuffdiff file.
ReferenceEntry is one of the sampl. Ideally the "first" one.
"""

import sys

class Test(object):
	def __init__(self, id, locus, sample1, sample2, value1, value2):
		self.Id=id;
		self.Locus=locus;
		self.Sample1=sample1;
		self.Sample2=sample2;
		self.Value1=value1;
		self.Value2=value2;
	
	def getSample1(self):
		return self.Sample1;

	def getSample2(self):
		return self.Sample2;

	def getValue1(self):
		return self.Value1;

	def getValue2(self):
		return self.Value2;

class geneEntry(object):
	def __init__(self, locus, sample1, sample2, value1, value2):
		self.Gene=locus;
		self.entry={};
		self.entry[sample1]=value1;
		self.entry[sample2]=value2;

	def addEntry(self, sample, value):
		if sample not in self.entry:
			self.entry[sample]=value;

	def getOrder(self):
		order=[];
		for i in self.entry:
			order.append(i);
		order.sort();
		return order;

	def getGeneEntry(self, order):
		line=self.Gene;
		pos=0;
		while(pos<len(order) and pos<len(self.entry)):
			line=line+"\t"+self.entry[order[pos]];
			pos=pos+1;
		return line;


def readFile(file, refEntry):
	a=[];
	for lines in open(file):
		id=lines.split()[0];
		locus=lines.split()[3];
		sample1=lines.split()[4];
		sample2=lines.split()[5];
		value1=lines.split()[7];
		value2=lines.split()[8];
		if(sample1==refEntry):
			test=Test(id, locus, sample1, sample2, value1, value2);
			a.append(test);
	return a;

def generateTable(valid_entry):
	table={};
	for i in valid_entry:
		if i.Locus in table:
			table[i.Locus].addEntry(i.Sample2, i.Value2);
		else:
			table[i.Locus]=geneEntry(i.Locus, i.Sample1, i.Sample2, i.Value1, i.Value2);
	return table;







if __name__=="__main__":
	havePrintedFirstLine=0;
	order=[];
	valid_entry=readFile(sys.argv[1], sys.argv[2]);
	geneList=generateTable(valid_entry);
	for i in geneList:
		if havePrintedFirstLine==1:
			line=geneList[i].getGeneEntry(order);
		else:
			order=geneList[i].getOrder();
			header="Gene";
			for a in order:
				header=header+"\t"+a;
			print(header);
			line=geneList[i].getGeneEntry(order);
			havePrintedFirstLine=1;
		print(line);



























