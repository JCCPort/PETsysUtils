#include <TFile.h>                                                              
#include <TGraph.h>                                                              
#include <TH1D.h>                                                               
#include <TF1.h>                                                                
#include <TSpectrum.h>                                                          
#include <TCanvas.h>                                                            
#include <TStyle.h>                                                             
#include <stdio.h>                                                              
#include <stdint.h>                                                             
#include <TGraphErrors.h>

int PEfit(char const *filePrefix, Int_t channel=-1)
{
  char fn[1024];
  sprintf(fn, "%s.ldat", filePrefix);
        FILE * dataFile = fopen(fn, "rb");
  sprintf(fn, "%s.lidx", filePrefix);
        FILE * indexFile = fopen(fn, "rb");
  if (dataFile == NULL) { printf("Could not find datafile\n"); return 1;}

  int minToT = 0;
  int maxToT = 200;
  TH1D * hE1 = new TH1D("hE1", ";tot [ns]", (maxToT-minToT)*5, minToT, maxToT);

  struct CEvent {
    long long  time;
    float   tot;
    int   id;
  };

  const Int_t MAX_EVENTS = 1000000;
  const Int_t MAX_EVENTS_TOTAL = 250000000;

  long long stepBegin, stepEnd;
  float step1, step2;
  double offset = 0.01;

  TCanvas *c1 = new TCanvas();
  TCanvas *c2 = NULL;

  CEvent ei;
  while(fscanf(indexFile,"%lld\t%lld\t%f\%f\n", &stepBegin, &stepEnd, &step1, &step2) == 4) {
 
    fseek(dataFile, stepBegin, SEEK_SET);
    Int_t count = 0;
    int nRead = 0;
    if(step1 > 20-offset && step1 < 20+offset){
      while(ftell(dataFile) < stepEnd && fread(&ei, sizeof(ei), 1, dataFile) == 1 && count < MAX_EVENTS_TOTAL) {
        if(ei.tot < minToT || ei.tot > maxToT) continue;
        if (channel == ei.id){
          hE1->Fill(ei.tot);
          count++;
          if(count%1000000==0)cout << count <<endl;
        }
      }
    }
  }

  TSpectrum *spectrum = new TSpectrum(10,3);
  spectrum->Search(hE1, 3, " ", 0.1);
  Int_t nPeaks = spectrum->GetNPeaks();
  printf("nPeaks = %d\n",nPeaks);

  Double_t *xPositions = spectrum->GetPositionX();
  std::sort(xPositions, xPositions+nPeaks);
  Double_t tot[nPeaks-1];
  Double_t pn[nPeaks-1];
  for (int i=1; i<nPeaks; i++)
  {
    pn[i-1] = i+2;
    tot[i-1] = xPositions[i];
  }

  hE1->Draw();

  TGraph *g = new TGraph(nPeaks-1,tot,pn);
  g->GetXaxis()->SetTitle("TOT [ns]");
  g->GetYaxis()->SetTitle("Peak Number");
  TF1 *sfunc = new TF1("sfunc","sqrt([0]*x)+[1]",0,100);
  TF1 *pfunc = new TF1("pfunc","[0]*x^5+[1]*x^4+[2]*x^3+[3]*x^2+[4]*x+[5]",0,10000);
  sfunc->SetParameter(0,500);
  //g->Fit("sfunc","","",0,100);
  g->Fit("pfunc");
  g->Draw("A*");
  //pfunc->Draw();
  //pfunc->GetXaxis()->SetTitle("TOT [ns]");
  //pfunc->GetYaxis()->SetTitle("Peak Number");

  
  return 0;
} 
