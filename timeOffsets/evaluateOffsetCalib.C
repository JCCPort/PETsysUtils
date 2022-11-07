#include <vector>
#include <string>

// macro to evaluate the accuracy of time offset calibrations by finding the
// average spread of hit times within LED pulses for non-calibrated and 
// calibrated data
void evaluateOffsetCalib()
{
  std::vector<TFile*> files;
  files.push_back(TFile::Open("/data/NewCube2_23-26C/20221026/run7_LED_10s_th20_single.root"));
  files.push_back(TFile::Open("/data/NewCube2_23-26C/20221026/run7_LED_10s_th20_single_tCalib.root"));
  std::vector<std::string> text = {"Av range pre-calib: ", "Av range post-calib: "};
  for (int f=0; f<2; f++)
  {
    TTree *tree = (TTree*)files[f]->Get("data");
    Int_t n = tree->GetEntries();

    Float_t energy;
    Long64_t t;
    UInt_t channelID;
    tree->SetBranchAddress("time",&t);
    tree->SetBranchAddress("energy",&energy);
    tree->SetBranchAddress("channelID",&channelID);

    Long64_t meanRange = 0;
    int pulseNum = 0;
    int pulseHits = 0;
    int margin = 10;
    tree->GetEntry(margin);
    Long64_t t_old = t;
    Long64_t t_max = 0;
    Long64_t t_min = 1e15;
    // iterate through events and get average pulse hit times
    for (Long64_t i=margin;i<n-margin;i++){
      tree->GetEntry(i);
      //if (energy < 0.5) continue; // PE cutoff
      if (t-t_old > 1e6) { // condition for new pulse
        if (pulseHits < 32) 
        {
          pulseHits = 0;
          t_max = 0;
          t_min = 1e15;
        }
        else
        {
          meanRange += t_max - t_min; 
          pulseNum++;
          t_max = 0;
          t_min = 1e15;
          pulseHits = 0;
        }
      }
      //if (channelID < 500) timeH4->Fill(t-mean2,channelID);
      //else timeH8->Fill(t-mean3,channelID);
      pulseHits++;
      if (t > t_max) t_max = t;
      if (t < t_min) t_min = t;
      t_old = t;
    }
    meanRange /= pulseNum;
 
    // print average time range
    printf("%s",text[f].c_str());
    printf("%.2f ns\n", (float)(meanRange/1e3));
  } //file loop
}
