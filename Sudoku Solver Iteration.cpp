#include <iostream>
using namespace std;

void initsudoku(int (*s)[10]){
  for(int i=0;i<81;i++){
    for(int j=1;j<10;j++){
      s[i][j]=1;
    }
  }
}

char display(int x){
  if(x==0){return ' ';}
  return '0'+x;
}

void displaysudoku(int (*s)[10]){
  cout << s[0][0] << " " << s[1][0] << " " << s[2][0] << "|" << s[3][0] << " " << s[4][0] << " " << s[5][0] << "|"<< s[6][0] << " " << s[7][0] << " " << s[8][0] << endl;
  cout << s[9][0] << " " << s[10][0] << " " << s[11][0] << "|" << s[12][0] << " " << s[13][0] << " " << s[14][0] << "|"<< s[15][0] << " " << s[16][0] << " " << s[17][0] << endl;
  cout << s[18][0] << " " << s[19][0] << " " << s[20][0] << "|" << s[21][0] << " " << s[22][0] << " " << s[23][0] << "|"<< s[24][0] << " " << s[25][0] << " " << s[26][0] << endl;
  cout << "*****************" << endl;
  cout << s[27][0] << " " << s[28][0] << " " << s[29][0] << "|" << s[30][0] << " " << s[31][0] << " " << s[32][0] << "|"<< s[33][0] << " " << s[34][0] << " " << s[35][0] << endl;
  cout << s[36][0] << " " << s[37][0] << " " << s[38][0] << "|" << s[39][0] << " " << s[40][0] << " " << s[41][0] << "|"<< s[42][0] << " " << s[43][0] << " " << s[44][0] << endl;
  cout << s[45][0] << " " << s[46][0] << " " << s[47][0] << "|" << s[48][0] << " " << s[49][0] << " " << s[50][0] << "|"<< s[51][0] << " " << s[52][0] << " " << s[53][0] << endl;
  cout << "*****************" << endl;
  cout << s[54][0] << " " << s[55][0] << " " << s[56][0] << "|" << s[57][0] << " " << s[58][0] << " " << s[59][0] << "|"<< s[60][0] << " " << s[61][0] << " " << s[62][0] << endl;
  cout << s[63][0] << " " << s[64][0] << " " << s[65][0] << "|" << s[66][0] << " " << s[67][0] << " " << s[68][0] << "|"<< s[69][0] << " " << s[70][0] << " " << s[71][0] << endl;
  cout << s[72][0] << " " << s[73][0] << " " << s[74][0] << "|" << s[75][0] << " " << s[76][0] << " " << s[77][0] << "|"<< s[78][0] << " " << s[79][0] << " " << s[80][0] << endl;
}

void createsudoku(int (*s)[10]){
  string str;
  int ss;
  cout << "please inpute the 1st line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=0;i<9;i++){
    if(str[i]>='0'&&str[i]<='9'){ss=(str[i]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 2nd line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=9;i<18;i++){
    if(str[i-9]>='0'&&str[i-9]<='9'){ss=(str[i-9]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 3rd line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=18;i<27;i++){
    if(str[i-18]>='0'&&str[i-18]<='9'){ss=(str[i-18]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 4th line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=27;i<36;i++){
    if(str[i-27]>='0'&&str[i-27]<='9'){ss=(str[i-27]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 5th line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=36;i<45;i++){
    if(str[i-36]>='0'&&str[i-36]<='9'){ss=(str[i-36]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 6th line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=45;i<54;i++){
    if(str[i-45]>='0'&&str[i-45]<='9'){ss=(str[i-45]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 7th line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=54;i<63;i++){
    if(str[i-54]>='0'&&str[i-54]<='9'){ss=(str[i-54]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 8th line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=63;i<72;i++){
    if(str[i-63]>='0'&&str[i-63]<='9'){ss=(str[i-63]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
  cout << "please inpute the 9th line with 9 integers between 1 and 9, empty slot use 0:" << endl;
  cin >> str;
  for(int i=72;i<81;i++){
    if(str[i-72]>='0'&&str[i-72]<='9'){ss=(str[i-72]-'0');s[i][0]=ss;}
    else{s[i][0]=0;}
  }
}




void setslot(int (*s)[10],int n){
  int i=n/9,j=n%9;
  for(int k=0;k<9;k++){
    s[9*i+k][s[n][0]]=0;
  }
  for(int k=0;k<9;k++){
    s[9*k+j][s[n][0]]=0;
  }
  int l=3*(9*(i/3)+j/3),g;
  for(int k=0;k<9;k++){
    g=l+9*(k/3)+k%3;
    s[g][s[n][0]]=0;
  }
}

void copysudoku(int (*s)[10],int (*p)[10]){
  for(int i=0;i<81;i++){
    for(int j=0;j<10;j++){
      p[i][j]=s[i][j];
    }
  }
}

bool checkslot(int (*s)[10],int n){
  int i=n/9,j=n%9;
  if(s[n][0]==0){return 1;}
  for(int k=1;k<9;k++){
    if(s[9*i+(k+j)%9][0]==s[n][0]){return 0;}
  }
  for(int k=1;k<9;k++){
    if(s[9*((k+i)%9)+j][0]==s[n][0]){return 0;}
  }
  j=3*(9*(i/3)+j/3);
  for(int k=0;k<9;k++){
    i=j+9*(k/3)+k%3;
    if(i!=n){
      if(s[i][0]==s[n][0]){return 0;}
    }
  }
  return 1;
}

bool sudokusolver(int s[81][10]){
  bool flag=1;
  for(int i=0;i<81;i++){
    if(s[i][0]==0){
      flag=0;
      bool ks=s[i][1]||s[i][2]||s[i][3]||s[i][4]||s[i][5]||s[i][6]||s[i][7]||s[i][8]||s[i][9];
      if(ks==0){
        return 0;
      }
      for(int j=1;j<10;j++){
        if(s[i][j]!=0){
          s[i][j]=0;
          int p[81][10];
          copysudoku(s,p);
          p[i][0]=j;
          setslot(p,i);
          sudokusolver(p);
        }
      }
    }
  }
  if(flag==1){
    cout << "a solution is:" << endl;
    displaysudoku(s);
    cout << endl;
  }
  return 1;
}



int main() {
  int s[81][10];
  createsudoku(s);
  initsudoku(s);
  displaysudoku(s);

  for(int i=0;i<81;i++){
    if(s[i][0]!=0){
      if(checkslot(s,i)==0){cout << "invalid sudoku problem" << endl; return 0;}
      setslot(s,i);
    }
  }

  sudokusolver(s);


  return 0;
}