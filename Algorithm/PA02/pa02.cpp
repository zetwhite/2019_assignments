//2018.00.00 roonm813 writes.
#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>

#define MATCH 3
#define MISMATCH (-2)
#define GAP_first (-2)
#define GAP (-5)

#define size 1000
#define resultNum 5
#define lineSet 70

using namespace std;
char* DNA1;
char* DNA2;

/* Element
  Element is unit to store(for dynamic programming)
*/
class Element{
public:
  short value; //save score
  short loseCount; //save continuity of not match, to find out continuity of gap or mismatch
  bool first_gap; //true => first gap, false => not first gap
                  //to find out this gap is first or not. first gap penalty is -5, whereas other gap penalty is -2.
  Element(){
    value = 0;
    loseCount = 0;
    first_gap = true;
  }
};

/* coo
  this class is to save information about maximum 5 score point.
*/
class coo{
public:
  int row;  //row index (row is associated with DNA2)
  int col;  //col index (col is associated with DNA1)
  int value; //save score
  string res;
  coo(){
    row = 0;
    col = 0;
    value = 0;
  }
  coo(const coo& a){
    row = a.row;
    col = a.col;
    value = a.value;
  }
  coo(int _row, int _col, int _value){
    row = _row;
    col = _col;
    value = _value;
  }
};

bool operator <= (coo& co1, coo& co2){
  if(co1.value <= co2.value)
    return true;
  return false;
}

bool operator < (coo& co1, coo& co2){
  if(co1.value < co2.value)
    return true;
  return false;
}

/* MaxCoo
  this class is for data structure to manage five maximum score point(=name class coo)
  this class is shell for coo array[resultNum].
  this class help insert to coo array, and get element from coo array.
*/
class MaxCoo{
public:
  coo cooArray[resultNum];
  void insert(coo newCo){//insert newCo if newCo's value(=score) is larger than cooArray
    if(newCo <= cooArray[resultNum-1]){
      return;
    }
    int i;
    for(i = 0; i < resultNum; i++){
      if(cooArray[i] < newCo)
        break;
    }
    for(int j = resultNum-1; j > i; j--){
      cooArray[j] = cooArray[j-1];
    }
    cooArray[i] = newCo;
  }
  void print(){//this is for debugging
    cout << "========= max coo ==========" <<endl;
    for(int i = 0; i < resultNum; i++){
      cout << "(" << cooArray[i].row << "," << cooArray[i].col << ") :: ";
      cout << cooArray[i].value;
      cout << endl;
    }
  }
  coo getCoo(int index){//get coo from cooArray by index
    return cooArray[index];
  }
};

/*printDNA || this is for debugging.
  usage : print out DNA char array
  arg : char* DNA (= dna array)
        : int DNA_size (= size of dna array)
*/
void printDNA(char* DNA, int DNA_size);

/*initDNA
  usage : get DNA sequence size and get DNA sequence. also print out input file info.
  arg : char** DNA (=get DNA sequence in this array)
          int* DNAsize (= get DNA sequence size int this variable)
*/
void initDNA(char** DNA, ifstream& in, int* DNAsize, ofstream& out);

/*maxInt
  usage : get maximun integer between val1, val2 and val3
*/
int maxInt(int val1, int val2, int val3);

/*fillLine
  usage : fill dp2 from dp1, and also fill maximum score information in maxC
*/
void fillLine(int DNA1_size, Element dp1[], Element dp2[], MaxCoo& maxC, int l);

/* findMaxPoint
  usage : maximum score index and score value , this information is stored in maxC and pass through maxC;
*/
void findMaxPoint(int DNA1_size, int DNA2_size, MaxCoo& maxC);

/*fillTarget
  usage : fill dp(=target) using information DNA1[row:row+row_size], DNA2[col:col+col_size]
*/
void fillTarget(Element target[][size+1],int row, int row_size, int col,  int col_size);

/* traceBack
  usage : find sequence alignment from Element target[][], and print out result in ofstream& out
*/
void traceBack(Element target[][size+1], int row_base, int col_base, int row_size, int col_size, ofstream& out);

/* getSequence
  usage : from co(which is storage for max score and and max score index), find out sequence alignment
        : this function call fillTarget(to fill dp) -> traceBack(to find and print alignment)
*/
void getSequence(coo co, int DNA1_size, int DNA2_size, ofstream& out);

int main(int argv, char* argc[]){
  string filename1, filename2, filename3;
  if(argv < 3){
    string progName = argc[0];
    cout << "too few argument" << endl << "$" << progName<< "[filename1] [filename2]" << endl;
  }
  else{
    filename1 = argc[1];
    filename2 = argc[2];
    filename3 = "output_" + filename1+ "_" + filename2 + ".algin";
  }
  ifstream in1(filename1);
  ifstream in2(filename2);
  ofstream out(filename3);

  int DNA1_size;
  int DNA2_size;
  initDNA(&DNA1, in1, &DNA1_size, out);
  initDNA(&DNA2, in2, &DNA2_size, out);

  MaxCoo maxC;
  findMaxPoint(DNA1_size, DNA2_size, maxC);
  for(int i = 0; i < resultNum; i++)
    getSequence(maxC.getCoo(i), DNA1_size, DNA2_size, out);
	return 0;
}

void printDNA(char* DNA, int DNA_size){
  for(int i = 1; i < DNA_size; i++){
    cout << DNA[i] <<" ";
  }
  cout <<endl;
}

void initDNA(char** DNA, ifstream& in, int* DNAsize, ofstream& out){
  int fileline = -1;
  string line;
  while(getline(in, line))
    fileline++;
  in.clear();
  in.seekg(in.beg);
  *DNA = new char[fileline * lineSet + 1];
  getline(in, line);
  cout << line << endl;
  out << line << endl;
//  out << ", "<< fileline * lineSet << endl; //print file info;
  for(int i = 1; i < fileline * lineSet + 1; i++)
    in >> (*DNA)[i];
  *DNAsize = fileline * lineSet + 1;
}

int maxInt(int val1, int val2, int val3){
  if(val1 < val2){
    if(val2 < val3)
      return val3;
    return val2;
  }
  if(val1 < val3)
    return val3;
  return val1;
}

void fillLine(int DNA1_size, Element dp1[], Element dp2[], MaxCoo& maxC, int l){
    for(int i = 1; i < DNA1_size; i++){
      int val1, val2, val3;
      bool match = false;
      //gap
      if(dp1[i].first_gap)
        val1 = dp1[i].value + GAP_first;
      else{
        val1 = dp1[i].value + GAP;
      }
      if(dp2[i-1].first_gap)
        val2 = dp2[i-1].value + GAP_first;
      else{
        val2 = dp2[i-1].value + GAP;
      }
      //match
      if(DNA1[i] == DNA2[l]){
        match = true;
        val3 = dp1[i-1].value + MATCH;
      }
      else//mismatch
        val3 = dp1[i-1].value + MISMATCH;
      int value = maxInt(val1, val2, val3);
      //set value
      if(value < 0)
        dp2[i].value = 0;
      else{
        maxC.insert(coo(l, i, value));
        dp2[i].value = value;
      }
      //set loseCount, gapContinuity;
      if(value == val1){
        dp2[i].loseCount = dp1[i].loseCount+1;
        dp2[i].first_gap = false;
      }
      else if(value == val2){
        dp2[i].loseCount = dp2[i-1].loseCount + 1;
        dp2[i].first_gap = false;
      }
      else if(match == false){
        dp2[i].loseCount = dp1[i-1].loseCount + 1;
      }
      //if gap continue with 5, reset value;
      if(dp2[i].loseCount == 4){
        dp2[i] = Element();
      }
    }
}

void findMaxPoint(int DNA1_size, int DNA2_size, MaxCoo& maxC){
  Element dp1[DNA1_size];
  Element dp2[DNA1_size];
  bool rotation = true;
  for(int i = 1; i < DNA2_size; i++){
    cout <<"running..." << i << "/" << DNA2_size << endl; //print to show that program is running...
    if(rotation)
      fillLine(DNA1_size, dp1, dp2, maxC, i);
    else
      fillLine(DNA1_size, dp2,dp1, maxC, i);
    rotation = !rotation;
  }
}

void fillTarget(Element target[][size+1],int row, int row_size, int col,  int col_size){
  for(int i = 1; i < row_size + 1; i++){
    for(int j = 1; j < col_size + 1; j++){
      int val1, val2, val3;
      bool match = false;
      //gap
      if(target[i-1][j].first_gap)
        val1 = target[i-1][j].value + GAP_first;
      else{
        val1 = target[i-1][j].value + GAP;
      }
      if(target[i][j-1].first_gap)
        val2 = target[i][j-1].value + GAP_first;
      else{
        val2 = target[i][j-1].value + GAP;
      }
      //match
      if(DNA1[j+col-1] == DNA2[i+row-1]){
        match = true;
        val3 = target[i-1][j-1].value + MATCH;
      }
      else//mismatch
        val3 = target[i-1][j-1].value + MISMATCH;
      int value = maxInt(val1, val2, val3);
      //set value
      if(value < 0)
        target[i][j]= Element();
      else
        target[i][j].value = value;
      //set loseCount, gapContinuity;
      if(value == val1){
        target[i][j].loseCount = target[i-1][j].loseCount+1;
        target[i][j].first_gap = false;
      }
      else if(value == val2){
        target[i][j].loseCount = target[i][j-1].loseCount + 1;
        target[i][j].first_gap = false;
      }
      else if(match == false){
        target[i][j].loseCount = target[i-1][j-1].loseCount + 1;
      }
      //if gap continue with 5, reset value;
      if(target[i][j].loseCount == 4){
        target[i][j] = Element();
      }
    }
  }
}

void traceBack(Element target[][size+1], int row_base, int col_base, int row_size, int col_size, ofstream& out){
  int row = row_size ;
  int col = col_size ;
  row_base--;
  col_base--;
  string str1, str2;
  short value = target[row][col].value;
  while(target[row][col].value != 0){
    if(target[row-1][col-1].value + MATCH == value){
      str1 = DNA1[col + col_base] + str1;
      str2 = DNA2[row + row_base] + str2;
      row--; col--;
    }
    else if(target[row-1][col-1].value + MISMATCH == value){
      str1 = DNA1[col + col_base] + str1;
      str2 = DNA2[row + row_base] + str2;
      row--; col--;
    }
    else if(target[row-1][col].first_gap && target[row-1][col].value + GAP_first == value){
      str1 = DNA1[col + col_base] + str1;
      str2 = "-" + str2;
      col--;
    }
    else if( !target[row-1][col].first_gap && target[row-1][col].value + GAP == value){
      str1 = DNA1[col + col_base] + str1;
      str2 = "-" + str2;
      col--;
    }
    else if(target[row][col-1].first_gap && target[row][col-1].value + GAP_first == value){
      str2 = "-" +str2;
      str1 = DNA2[row + row_base] + str1;
      row--;
    }
    else if(!target[row][col-1].first_gap && target[row][col-1].value + GAP == value){
      str2 = "-" +str2;
      str1 = DNA2[row + row_base] + str1;
      row--;
    }
    else{
      str1 = "<<error>>" + str1;
      str2 = "<<error>>" + str2;
      break;
    }
    value = target[row][col].value;
  }
  cout << "\t" << "seq1 : " << str1 << endl;
  cout << "\t" << "seq2 : " << str2 << endl;
  out <<"\t" << "seq1 : " << str1 << endl;
  out <<"\t" << "seq2 : " << str2 << endl;
}

void getSequence(coo co, int DNA1_size, int DNA2_size, ofstream& out){
  int row = co.row;
  int col = co.col;
  row = row - size + 1; //start point
  col = col - size + 1; //start point
  if(row < 1)
    row = 1;
  if(col < 1)
    col = 1;
  int row_size = co.row - row + 1; //size
  int col_size = co.col - col + 1;

  Element target[size+1][size+1];
  fillTarget(target, row, row_size, col, col_size);
  cout << "score : " << co.value << endl;
  out << "score : " << co.value <<endl;
  traceBack(target, row, col, row_size, col_size, out);
}
