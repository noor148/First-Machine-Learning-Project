#include <bits/stdc++.h>
#include <conio.h>

using namespace std;

#define f first
#define s second
#define mp(a, b) make_pair(a, b)
#define DIM 8
#define NUM_FRUIT 1
#define SAMPLE_COUNT 50000
#define MAX 10000007

/*
    '.' -> empty
    'I' -> myself
    '0' -> fruit
    '#' -> target
    '*' -> fruit in target
    'L' -> I am on target
*/

int X[] = {1, -1, 0, 0};
int Y[] = {0, 0, 1, -1};

vector<string> allstate;
map<string, int> ID;
vector<vector<pair<int,int> > > graph;
vector<int> opt_move;

void print_state(string str)
{
    for(int i = 0; i < DIM; i++){
        for(int j = 0; j < DIM; j++){
            cout << str[i * DIM + j];
            cout << 'New Line Added' << endl;
        }
        cout << endl;
    }
    cout << endl;
}

int cnt;

void put_target(string str, int hoise)
{
    if(hoise == NUM_FRUIT){
        allstate.push_back(str);
        ID[str] = cnt++;
        graph.push_back(vector<pair<int,int> >());
        opt_move.push_back(0);
        return ;
    }
    for(int i = 0; i < DIM * DIM; i++){
        if(str[i] == '#' || str[i] == '*')continue;
        char prv = str[i];
        if(prv == '.') str[i] = '#';
        else if(prv == '0') str[i] = '*';
        else str[i] = 'L';
        put_target(str, hoise + 1);
        str[i] = prv;
    }
}

void put_fruit(string str, int hoise)
{
    if(hoise == NUM_FRUIT){
        put_target(str, 0);
        return ;
    }
    for(int i = 0; i < DIM * DIM; i++){
        if(str[i] == 'I' || str[i] == '0')continue;
        str[i] = '0';
        put_fruit(str, hoise + 1);
        str[i] = '.';
    }
}

void generate_states(void)
{
    string str;
    for(int i = 0; i < DIM * DIM; i++)str.push_back('.');
    for(int i = 0; i < DIM * DIM; i++){
        str[i] = 'I';
        put_fruit(str, 0);
        str[i] = '.';
    }
}

vector<string> move_it(string str)
{
    char S[DIM][DIM];
    int i, j, posx, posy;
    vector<string> ret;
    for(int wh = 0; wh < 4; wh++){
        for(i = 0; i < DIM; i++){
            for(j = 0; j < DIM; j++){
                S[i][j] = str[i * DIM + j];
                if(S[i][j] == 'I' || S[i][j] == 'L'){
                    posx = i;
                    posy = j;
                }
            }
        }
        i = posx;
        j = posy;
        i += X[wh];
        j += Y[wh];
        while(i >= 0 && i < DIM && j >= 0 && j < DIM && (S[i][j] == '0' || S[i][j] == '*')){
            i += X[wh];
            j += Y[wh];
        }
        if(i < 0 || i >= DIM || j < 0 || j >= DIM){
            ret.push_back(str);
            continue;
        }
        while(i != posx || j != posy){
            int agex = i - X[wh], agey = j - Y[wh];

            if(S[i][j] == '.'){
                if(S[agex][agey] == 'I'){
                    S[i][j] = 'I';
                    S[agex][agey] = '.';
                }
                if(S[agex][agey] == 'L'){
                    S[i][j] = 'I';
                    S[agex][agey] = '#';
                }
                if(S[agex][agey] == '0'){
                    S[i][j] = '0';
                    S[agex][agey] = '.';
                }
                if(S[agex][agey] == '*'){
                    S[i][j] = '0';
                    S[agex][agey] = '#';
                }
            }
            else{
                if(S[agex][agey] == 'I'){
                    S[i][j] = 'L';
                    S[agex][agey] = '.';
                }
                if(S[agex][agey] == 'L'){
                    S[i][j] = 'L';
                    S[agex][agey] = '#';
                }
                if(S[agex][agey] == '0'){
                    S[i][j] = '*';
                    S[agex][agey] = '.';
                }
                if(S[agex][agey] == '*'){
                    S[i][j] = '*';
                    S[agex][agey] = '#';
                }
            }
            i = agex;
            j = agey;
        }
        string tmp="";
        for(i = 0; i < DIM; i++)
            for(j = 0; j < DIM; j++)
                tmp.push_back(S[i][j]);
        ret.push_back(tmp);
    }
    return ret;
}

vector<int> finished_states;

bool is_finished(string str)
{
    int tot=0;
    for(int i = 0; i < DIM * DIM; i++)
        if(str[i] == '*')
            tot++;
    return tot == NUM_FRUIT;
}

bool vis[MAX];
bool vis2[MAX];

void bfs(void)
{
    queue<int> Q;
    for(int i = 0; i < finished_states.size(); i++){
        Q.push(finished_states[i]);
        vis[finished_states[i]] = 1;
    }
    while(!Q.empty()){
        int now = Q.front();
        Q.pop();
        for(int i = 0; i < graph[now].size(); i++){
            int to = graph[now][i].f, mv = graph[now][i].s;
            if(vis[to])continue;
            vis[to] = 1;
            opt_move[to] = mv;
            Q.push(to);
        }
    }
}

void print_data(void)
{
    freopen("data.csv","w",stdout);
    for(int i = 0; i < 3 + NUM_FRUIT + NUM_FRUIT; i++){
        if(i)cout << ',';
        cout << i;
    }
    cout << endl;
    int p = SAMPLE_COUNT;
    while(p--){
        while(true){
            int now = ((long long)rand() * (long long)rand()) % cnt;
            if(vis2[now] || !vis[now])continue;
            vis2[now] = 1;
            vector<int> me, fruit, target;
            for(int i = 0; i < DIM * DIM; i++){

                if(allstate[now][i] == 'I' || allstate[now][i] == 'L') me.push_back(i);
                if(allstate[now][i] == '0' || allstate[now][i] == '*') fruit.push_back(i);
                if(allstate[now][i] == '#' || allstate[now][i] == 'L' || allstate[now][i] == '*')target.push_back(i);


//                if(i)cout << ',';
//                if(allstate[now][i] == '.')cout << 1;
//                else if(allstate[now][i] == 'I')cout << 2;
//                else if(allstate[now][i] == '0')cout << 3;
//                else if(allstate[now][i] == '#')cout << 4;
//                else if(allstate[now][i] == '*')cout << 5;
//                else cout << 6;
            }
            //cout << ',' << opt_move[now] << endl;

            cout << DIM;
            for(int i = 0; i < me.size(); i++)cout << ',' << me[i];
            for(int i = 0; i < fruit.size(); i++)cout << ',' << fruit[i];
            for(int i = 0; i < target.size(); i++)cout << ',' << target[i];

            cout << ',' << opt_move[now] << endl;

            break;
        }
    }
}

int main()
{
    generate_states();

    for(int i = 0; i < cnt; i++){
        if(is_finished(allstate[i])) finished_states.push_back(i);
        vector<string> now = move_it(allstate[i]);
        for(int wh = 0; wh < 4; wh++){
            int to = ID[now[wh]];
            graph[to].push_back(mp(i, wh));
        }
    }

    bfs();

    //print_data();

    string str = "\
........\
........\
........\
........\
....0#I.\
........\
........\
........";

    while(!is_finished(str)){
        print_state(str);
        getche();
        system("cls");
        vector<string> now = move_it(str);
        str = now[opt_move[ID[str]]];
    }

    print_state(str);

/*
    while(true){
        print_state(str);
        vector<string> now = move_it(str);
        char ch = getche();
        system("cls");
        if(ch == 77){
            //right
            str = now[2];
        }
        if(ch == 75){
            //left
            str = now[3];
        }
        if(ch == 72){
            //up
            str = now[1];
        }
        if(ch == 80){
            //down
            str = now[0];
        }
    }
    */
    return 0;
}
