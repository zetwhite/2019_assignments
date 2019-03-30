#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <limits>
#include <cmath>
using namespace std;
#define INT_MAX numeric_limits<int>::max()

int distance_line(pair<int, int> a, pair<int, int> b){
  int dx = a.first - b.first;
  int dy = a.second - b.second;
  return dx*dx + dy*dy;
}

class line{
public:
  pair<int, int> coo1;
  pair<int, int> coo2;
  int distance;
  line(pair<int, int> a, pair<int, int> b){
    this->coo1 = a;
    this->coo2 = b;
    this->distance = distance_line(a, b);
  }
  line(){
    this->coo1 = make_pair(-1, -1);
    this->coo2 = make_pair(-1, -1);
    distance = INT_MAX;
  }
  bool operator<(line& l){
    if(this->distance < l.distance)
      return true;
    return false;
  }
  line(const line& l){
    this->coo1 = l.coo1;
    this->coo2 = l.coo2;
    this->distance = l.distance;
  }
};

ofstream& operator<<(ofstream& os, vector<pair<int, int>>& a){
  for(int i = 0; i < a.size(); i++)
    os << "(" << a[i].first << ", " << a[i].second << ")" << " ";
  os << endl;
}

ofstream& operator<<(ofstream& os, const pair<int, int>& p) {
	os << "(" << p.first << "," << p.second << ")";
	return os;
}

ofstream& operator<<(ofstream& os, const line& l){
  os << "(" << l.coo1.first << "," << l.coo1.second << ")";
  os << "-" ;
  os << "(" << l.coo2.first << "," << l.coo2.second << ") = ";
  os << "sqrt(" << l.distance  << ")" << "= " << sqrt(l.distance) << endl;
  return os;
}

ostream& operator<<(ostream& os, const line& l){
  os << "(" << l.coo1.first << "," << l.coo1.second << ")";
  os << "-" ;
  os << "(" << l.coo2.first << "," << l.coo2.second << ") = ";
  os << "sqrt(" << l.distance  << ")" << "= " << sqrt(l.distance) << endl;
  return os;
}



line min(line a, line b){
  if(a < b)
    return a;
  return b;
}

line min(line a, line b,line c){
  if(a < b)
    if(a < c)
      return a;
    else
      return c;
  else
    if(b < c)
     return b;
    else
      return c;
}

bool compare(pair<int, int> a, pair<int, int> b){
  if(a.second == b.second)
    return a.first < b.first;
  return a.second < b.second;
}


line crossDistnace(line l, vector<pair<int, int>>& coordinates, double midLine){
  vector<pair<int, int>> candidates;
  for(int i = 0; i < coordinates.size(); i++){
    if(midLine - sqrt(l.distance) <= coordinates[i].first && coordinates[i].first <= sqrt(l.distance) + midLine){
      candidates.push_back(coordinates[i]);
    }
  }
  line result;
  if(candidates.size()==0) return result;
  sort(candidates.begin(), candidates.end(), compare);

  double limitDistance = sqrt(l.distance);
  for(int i = 0; i < candidates.size()-1; i++){
    for(int j = i+1; j < candidates.size(); j++){
      if(candidates[j].second > candidates[i].second + limitDistance)
        break;
      if(result.distance> distance_line(candidates[i], candidates[j]))
        result = line(candidates[i], candidates[j]);
    }
  }
  return result;
}

line findMinDistance(vector<pair<int, int>>& coordinates, int startIdx, int endIdx){
  line l;
  int midIdx = (startIdx + endIdx)/2;
  if(startIdx == endIdx){
    l.distance = INT_MAX;
    return l;
  }
  else if(startIdx + 1 == endIdx){
    l = line(coordinates[startIdx], coordinates[endIdx]);
    return l;
  }
  else{
    line tmp = min(findMinDistance(coordinates, startIdx, midIdx), findMinDistance(coordinates, midIdx+1, endIdx));
    double midLine_x = double(tmp.coo1.first + tmp.coo2.first)/2;
    line res = min(tmp, crossDistnace(tmp, coordinates, midLine_x));
    return res;
  }
}

int main(int argv, char* argc[]){
  string filename;
  /*if(argv < 2){
    string progName = argc[0];
    cout << "too few argument" << endl << "$" << progName << " [inputFileName] "<< endl;
    return 0;
  }
  else{
    filename = argc[1];
  }*/
  cin >> filename;
  ifstream in(filename);
  ofstream out("PA01-1.out");
  vector<pair<int, int>> coordinates;
  int n;
  in >> n;

  for(int i = 0; i < n; i++){
    int x, y;
    in >> x >> y;
    coordinates.push_back(make_pair(x, y));
  }
  sort(coordinates.begin(), coordinates.end());

  cout << findMinDistance(coordinates, 0, coordinates.size()-1) << endl;
  out << findMinDistance(coordinates, 0, coordinates.size()-1) << endl;
	return 0;
}
