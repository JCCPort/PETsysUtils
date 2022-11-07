
void plotTimeOffsets()
{
  TFile *_file0 = TFile::Open("/data/NewCube2_23-26C/20221026/\
run7_LED_10s_th20_single_tCalib1p.root");
  TTree *tree = (TTree*)_file0->Get("data");
  Int_t n = tree->GetEntries();

  //means and mins for run5 11/07 calib pulse
  //Double_t mean2 = 5000024958033.312500000;
  //Double_t mean3 = 5000024956028.312500000;
  //Double_t min1 = 4105.7003e9; // min for early pulse
  //Double_t min2 = 5000.024954e9; // min for calib pulse
  //Double_t min3 = 5000.010704e9; // min for pulse prior to calib pulse

  //means and mins for run7 26/10 calib pulse
  long long min = 7780.503225e9;

  TH1D* timeH4 = new TH1D("timeH1",";time [ns];entries",10000,0,20);
  TH1D* timeH8 = new TH1D("timeH4",";time [ns];entries",10000,0,20);

  Float_t energy;
  Long64_t t;
  UInt_t channelID;
  tree->SetBranchAddress("time",&t);
  tree->SetBranchAddress("energy",&energy);
  tree->SetBranchAddress("channelID",&channelID);

  for (Long64_t i=0;i<n;i++){
    tree->GetEntry(i);
    //if (energy > 10){
      Double_t t1 = (t-min)*1e-3;
      if (channelID < 500) timeH4->Fill(t1);
      else timeH8->Fill(t1);
    //}
  }
  timeH4->SetLineColor(kRed);
  timeH8->SetLineColor(kBlue);
  THStack* hs = new THStack("hs",";time [ns]; entries");
  hs->Add(timeH4);
  hs->Add(timeH8);
  hs->Draw();
  TLegend *leg = new TLegend(0.75,0.75,0.95,0.95);
  leg->AddEntry(timeH4,"chipID 4");
  leg->AddEntry(timeH8,"chipID 8");
  leg->Draw();

}
