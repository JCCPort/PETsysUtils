#include <vector>

// macro to find time offsets of each channel using pulsed LED data
// the average hit time of each LED pulse is found by averaging over both arrays
// the offset of each channel to the pulse average is then found
// the average offset is then calculated and printed for each channel
void extractTimeOffsets()
{
  TFile *_file0 = TFile::Open("/data/NewCube2_23-26C/20221026/run7_LED_10s_th20_single.root");
  TTree *tree = (TTree*)_file0->Get("data");
  Int_t n = tree->GetEntries();

  // means for run5 11/07
  //Double_t mean2 = 5000024958033.312500000;
  //Double_t mean3 = 5000024956028.312500000;

  //TH1D* timeH4 = new TH1D("timeH4",";time [ps];entries",7000,5000.024954e9,5000.024961e9);
  //TH1D* timeH8 = new TH1D("timeH8",";time [ps];entries",7000,5000.024954e9,5000.024961e9);
  //TH1D* timeH = new TH1D("timeH",";time [ps];entries",7000,5000.024954e9,5000.024961e9);
  TH1D* meanH = new TH1D("meanH",";time [ps];entries",350868,0,350868);
  TH1D* timeH = new TH1D("timeH",";time [ps];entries",700,0,700);

  Float_t energy;
  Long64_t t;
  UInt_t channelID;
  tree->SetBranchAddress("time",&t);
  tree->SetBranchAddress("energy",&energy);
  tree->SetBranchAddress("channelID",&channelID);

  Long64_t mean = 0;
  int pulse[700] = {0};
  int pulseNum = 1;
  int margin = 10;
  int pulseHits = 0;
  tree->GetEntry(margin);
  Long64_t t_old = t;
  // iterate through events and get average pulse hit times
  for (Long64_t i=margin;i<n-margin;i++){
    tree->GetEntry(i);
    //if (energy < 0.5) continue; // PE cutoff
    if (t-t_old > 1e6) { // condition for new pulse
      mean /= (double)pulseHits; 
      if (pulseHits < 32) 
      {
        mean = 0;
        pulseHits = 0;
      }
      else
      {
        meanH->Fill(pulseNum, mean);
        mean = 0; 
        pulse[channelID]++;
        pulseNum++;
        pulseHits = 0;
      }
    }
    //if (channelID < 500) timeH4->Fill(t-mean2,channelID);
    //else timeH8->Fill(t-mean3,channelID);
    pulseHits++;
    mean += t;
    t_old = t;
  }
  int pulseTotal[700] = {0};
  pulseNum = 2;
  tree->GetEntry(margin);
  t_old = t;
  pulseHits = 0;
  Long64_t meanArray[700] = {0};
  std::vector<UInt_t> chID_tmp;
  std::vector<Long64_t> t_tmp;
  // iterate through events and find hit offsets relative to pulse average
  for (Long64_t i=margin;i<n-margin;i++){
    tree->GetEntry(i);
    //if (energy < 0.5) continue;
    //if (i%10000==0) printf("%f\n",t-mean);
    if (t-t_old > 1e6){
      printf("%d\n",pulseHits);
      if (pulseHits < 32){
        pulseHits = 0;
        chID_tmp.clear();
        t_tmp.clear();
      }
      else
      {
        pulseHits = 0;
        for (int j=0; j<chID_tmp.size(); j++)
        {
          mean = meanH->GetBinContent(pulseNum);
          meanArray[chID_tmp[j]] += (t_tmp[j]-mean);
          pulseTotal[chID_tmp[j]]++;
        }
        pulseNum++;
        chID_tmp.clear();
        t_tmp.clear();
      }
    }
    chID_tmp.push_back(channelID);
    t_tmp.push_back(t);
    mean = meanH->GetBinContent(pulseNum);
    //if (abs(t-mean)>10e3) {t_old = t; continue;}
    pulseHits++;
    t_old = t;
  }

  // print average time offsets for each channel
  for (int i = 1; i<700; i++){
    Double_t val = meanArray[i]/(pulseTotal[i]+1);
    UInt_t chip = (UInt_t)(i/64);
    UInt_t channel = i%64;
    if (val!=0){
      printf("0\t0\t%d\t%d\t%f\n",chip,channel,val);
    }
  }
}
