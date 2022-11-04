
void extractTimeOffsets()
{
  TFile *_file0 = TFile::Open("/data/NewCube2_23-26C/20221026/run7_LED_10s_th20_single.root");
  TTree *tree = (TTree*)_file0->Get("data");
  Int_t n = tree->GetEntries();

  // means for run5 11/07
  //Double_t mean2 = 5000024958033.312500000;
  //Double_t mean3 = 5000024956028.312500000;
  // means and mins for run7 26/10
  long long mean2 = 3546066328407;
  //Double_t mean3 = 5000024956028.312500000;
  long long min1 = 3546.066324e9;

  int nbins = 10000;

  TH1D* timeH4 = new TH1D("timeH4",";time [ps];entries",nbins,min1-mean2,min1-mean2+nbins);
  TH1D* timeH8 = new TH1D("timeH8",";time [ps];entries",nbins,min1-mean2,min1-mean2+nbins);

  Float_t energy;
  Long64_t t;
  UInt_t channelID;
  tree->SetBranchAddress("time",&t);
  tree->SetBranchAddress("energy",&energy);
  tree->SetBranchAddress("channelID",&channelID);

  for (Long64_t i=0;i<n;i++){
    tree->GetEntry(i);
    //if (energy > 10){
      if (channelID < 500) timeH4->Fill(t-mean2,channelID);
      else timeH8->Fill(t-mean2,channelID);
    //}
  }

  for (int i = 1; i<nbins; i++){
    UInt_t val = timeH4->GetBinContent(i);
    UInt_t chip = (UInt_t)(val/64);
    UInt_t channel = val%64;
    if (val>0){
      Long64_t cent = timeH4->GetBinCenter(i);
      printf("%d\t%d\t%.lld\n",chip,channel,cent);
    }
    val = timeH8->GetBinContent(i);
    chip = (UInt_t)(val/64);
    channel = val%64;
    if (val>0){
      Long64_t cent = timeH8->GetBinCenter(i);
      printf("%d\t%d\t%.lld\n",chip,channel,cent);
    }
  }
}
