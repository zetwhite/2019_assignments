#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
using namespace std;
typedef pair<int,int> co;

ofstream& operator<<(ofstream& os, const co& p) {
	//os << "(" << p.first << "," << p.second << ")";
	os << p.first << ", " << p.second << endl;
	return os;
}

ofstream& operator<<(ofstream& os, vector<co>& v){
  for(int i = 0; i < v.size(); i++)
    os << v[i];
  return os;
}

ostream& operator << (ostream& os, vector<co>& v){
  for(int i = 0; i < v.size(); i++)
      cout << v[i].first << ", "<<v[i].second << endl;
  return os;
}

vector<co> merge(vector<co>& left, vector<co>& right){
  int l_walk = 0;
  int r_walk = 0;
  int l_height = 0;
  int r_height = 0;
  vector<co> total;
  while(l_walk < left.size() && r_walk < right.size()){
    if(left[l_walk].first < right[r_walk].first){
      l_height = left[l_walk].second;
      int height = max(left[l_walk].second, r_height);
      if(total.empty() || total.back().second != height){
        total.push_back(make_pair(left[l_walk].first, height));
      }
      l_walk++;
    }
    else if(left[l_walk].first > right[r_walk].first){
      r_height = right[r_walk].second;
      int height = max(right[r_walk].second, l_height);
      if(total.empty() || total.back().second != height){
        total.push_back(make_pair(right[r_walk].first, height));
      }
      r_walk++;
    }
    else{
      l_height = left[l_walk].second;
      r_height = right[r_walk].second;
      int height = max(l_height, right[r_walk].second);
      total.push_back(make_pair(left[l_walk].first, height));
    }
  }

  if(l_walk < left.size()){
    for(int walk = l_walk; walk < left.size(); walk++)
      total.push_back(left[walk]);
  }
  if(r_walk < right.size()){
    for(int walk = r_walk; walk < right.size(); walk++)
      total.push_back(right[walk]);
  }
  return total;
}

vector<co> merge_s(vector<co>& skyLines, int start, int end){
  vector<pair<int, int>> res;
  if(start == end){
    res.push_back(skyLines[start*2]);
    res.push_back(skyLines[start*2+1]);
  }
  if(start < end){
    int mid = (start + end)/2;
    vector<pair<int, int>> first = merge_s(skyLines, start, mid);
    vector<pair<int, int>> second = merge_s(skyLines, mid+1, end);
    res = merge(first, second);
  }
  return res;
}

int main(int argv, char* argc[]){
  if(argv < 2){
    string progName = argc[0];
    cout << "too few argument " << endl << "$" <<progName << " [inputFileName]" << endl;
    return 0;
  }
  string inputfile = argc[1];
  ifstream in(inputfile);
  ofstream out("PA01-2.out");
  vector<co> skyLines;
  int n;
  in >> n;
  for(int i = 0; i < n; i++){
    int right;
    int height;
    int left;
    in >> right >> height >> left;
    skyLines.push_back(make_pair(right, height));
    skyLines.push_back(make_pair(left, 0));
  }

  vector<co> res = merge_s(skyLines, 0, n-1);
  out << res << endl;
  cout << res << endl;
	return 0;
}
