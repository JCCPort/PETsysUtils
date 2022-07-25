
void extractTimeOffsets()
{
  TFile *_file0 = TFile::Open("~/Documents/Work/sussex_petsys/data/cube_test_singleFan/2022_07_11/run5_LED_qdc_single.root");
  TTree *tree = (TTree*)_file0->Get("data");
  Int_t n = tree->GetEntries();

  // means for run5 11/07
  Double_t mean2 = 5000024958033.312500000;
  Double_t mean3 = 5000024956028.312500000;

  TH1D* timeH4 = new TH1D("timeH4",";time [ps];entries",7000,5000.024954e9-mean2,5000.024961e9-mean2);
  TH1D* timeH5 = new TH1D("timeH5",";time [ps];entries",7000,5000.024954e9-mean3,5000.024961e9-mean3);

  Float_t energy;
  Long64_t t;
  UInt_t channelID;
  tree->SetBranchAddress("time",&t);
  tree->SetBranchAddress("energy",&energy);
  tree->SetBranchAddress("channelID",&channelID);

  for (Long64_t i=0;i<n;i++){
    tree->GetEntry(i);
    if (energy > 10){
      if (channelID < 500) timeH4->Fill(t-mean2,channelID);
      else timeH5->Fill(t-mean3,channelID);
    }
  }

  for (int i = 1; i<7000; i++){
    UInt_t val = timeH4->GetBinContent(i);
    UInt_t chip = (UInt_t)(val/64);
    UInt_t channel = val%64;
    if (val>0){
      Long64_t cent = timeH4->GetBinCenter(i);
      printf("%d %d %.lld\n",chip,channel,cent);
    }
    val = timeH5->GetBinContent(i);
    chip = (UInt_t)(val/64);
    channel = val%64;
    if (val>0){
      Long64_t cent = timeH5->GetBinCenter(i);
      printf("%d %d %.lld\n",chip,channel,cent);
    }
  }
}
