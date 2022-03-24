#include <algorithm>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <omp.h>
#define STAND 0
#define HIT 1
using namespace std;

// Return the high-possible points among cards.
int get_points(vector<int> &cards) {
    int result = 0;
    bool has_ace = false;
    for (int card : cards) {
        if (card == 1)
            has_ace = true;
        result += card;
    }
    if (result <= 11 && has_ace)
        result += 10;
    return result;
}

// Get hash from a cards.
long long cards_hash(vector<int> &cards) {
    static long long M = 1000000009;
    long long result = get_points(cards);
    for (auto x : cards)
        result = (result * 29 + x) % M;
    return result;
}

// Given the cards remaining, return the probabilities of 
// the points that dealer may holds.
vector<double> dealer_prob(
    vector<int> dealer_cards, 
    vector<int> &remain_cards,
    bool check_dealer_has_no_T=false) {

    sort(dealer_cards.begin(), dealer_cards.end());
    // If this cards has been calculate, return the results.
    bool dealer_has_no_T = check_dealer_has_no_T && dealer_cards.size() == 1 && dealer_cards[0] == 1;
    // The final results to return
    vector<double> probability(7, 0.0);
    // If the dealer_cards is larget than 17, we can just return the results.
    int dealer_points = get_points(dealer_cards);
    if (17 <= dealer_points) {
        probability[max(16, min(22, dealer_points)) - 16] = 1;
        return probability;
    }
    // Calculate current # of cards
    int remain_cards_num = 0;
    for (int i=0; i<10; i++)
        remain_cards_num += remain_cards[i];

    // Let's burst!
    for (int next_card=1; next_card<=10; next_card++) {
        if (remain_cards[next_card-1] == 0 || dealer_has_no_T && next_card==10)
            continue;
        // Calculate the base prob of next cards.
        double card_prob;
        if (dealer_has_no_T) 
            card_prob = 1.0 * remain_cards[next_card-1] / (remain_cards_num - remain_cards[9]);
        else
            card_prob = 1.0 * remain_cards[next_card-1] / remain_cards_num;
        // Generate next status
        dealer_cards.push_back(next_card);
        remain_cards[next_card-1] --;
        vector<double> next_probs = dealer_prob(dealer_cards, remain_cards, false);
        for (int next_points=0; next_points<7; next_points++)
            probability[next_points] += card_prob * next_probs[next_points];
        // Recover next status
        dealer_cards.pop_back();
        remain_cards[next_card-1] ++;
    }
    return probability;
}

class Policy{
public:
    unordered_map<long long, pair<vector <double>, vector <double>>> mem;
    Policy () {
        mem.clear();
    }
    pair<vector <double>, vector <double>> get_policy(    
        vector<int> player_cards, 
        vector<int> &dealer_cards, 
        vector<int> &remain_cards, 
        bool check_dealer_has_no_T = false, 
        bool only_one_hit = false) {
        
        sort(player_cards.begin(), player_cards.end());
        // Memoization
        long long hash_key = cards_hash(player_cards);
        if (mem.find(hash_key) != mem.end())
            return mem[hash_key];
        // format: [dealer win, even, player win]
        vector<double> stand_rate(3, 0.0), hit_rate(3, 0.0);
        // Calculate End Step
        int player_stand_points = get_points(player_cards);
        if (player_stand_points > 21) {
            // If player current points is larger than 21 then player lose.
            stand_rate[0] = hit_rate[0] = 1;
        } else if (player_cards.size() == 5) {
            // If player current cards has more than 5 cards then player win.
            stand_rate[2] = 1;
            // No more cards when hit 5 cards
            hit_rate[0] = 1;
        } else {
            // Calculate stand rate
            vector<double> dealer_result = dealer_prob(dealer_cards, remain_cards, check_dealer_has_no_T);
            int player_stand_points_index = max(16, min(22, player_stand_points)) - 16;
            for (int i=0; i<player_stand_points_index; i++)
                stand_rate[2] += dealer_result[i];
            stand_rate[1] = dealer_result[player_stand_points_index];
            for (int i=player_stand_points_index+1; i<6; i++)
                stand_rate[0] += dealer_result[i];
            stand_rate[2] += dealer_result[6];
            if (!only_one_hit || player_cards.size() == 2) {
                // if it's not double down or it's just first card to receive, 
                // We ad-hocly find the next card.

                // Calculate current # of cards
                int remain_cards_num = 0;
                for (int i=0; i<10; i++)
                    remain_cards_num += remain_cards[i];
                // Calculate hit rate
                for (int next_card=1; next_card<=10; next_card++) {
                    if (remain_cards[next_card-1] == 0)
                        continue;
                    // Calculate the base prob of next cards.
                    double card_prob = 1.0 * remain_cards[next_card-1] / remain_cards_num;
                    // Generate next status
                    player_cards.push_back(next_card);
                    remain_cards[next_card-1] --;
                    // Get policy of next step
                    auto next_policy = get_policy(player_cards, dealer_cards, remain_cards, check_dealer_has_no_T, only_one_hit);
                    double stand_ev = next_policy.first[2] - next_policy.first[0];
                    double hit_ev = next_policy.second[2] - next_policy.second[0];
                    auto result = next_policy;
                    for (int i=0; i<3; i++) {
                        if (stand_ev > hit_ev)
                            hit_rate[i] += card_prob * next_policy.first[i];
                        else
                            hit_rate[i] += card_prob * next_policy.second[i];
                    }
                    // Recover next status
                    player_cards.pop_back();
                    remain_cards[next_card-1] ++;
                }
            } else {
                // if only one hit (for double down), and now it's third cards, 
                // Then we'll forcely give "hit" 100% lose.
                hit_rate[0] = 1;
            }
        }
        return mem[hash_key] = {stand_rate, hit_rate};
    }
    pair<double, double> initial_EV(vector<int> &remain_cards) {
        // Calculate current # of cards
        int remain_cards_num = 0;
        for (int i=0; i<10; i++)
            remain_cards_num += remain_cards[i];

        double return_ev = 0, return_winrate = 0;
        for (int i=1; i<=10; i++) {
            for (int j=i; j<=10; j++) {
                if (i == j && remain_cards[i-1] <= 1)
                    continue;
                if (remain_cards[i-1] == 0 || remain_cards[j-1] == 0)
                    continue;
                double cards_prob;
                if (i == j)
                    cards_prob = remain_cards[i-1] * (remain_cards[i-1] - 1);
                else
                    cards_prob = 2 * remain_cards[i-1] * remain_cards[j-1];
                cards_prob /= remain_cards_num * (remain_cards_num - 1);
                // Effect in remain_cards
                remain_cards[i-1]--, remain_cards[j-1]--;

                vector<int> player_cards{i, j}, dealer_cards{};
                int player_points = get_points(player_cards);
                auto result = get_policy(player_cards, dealer_cards, remain_cards, true);
                double stand_ev = result.first[2] - result.first[0];
                double hit_ev = result.second[2] - result.second[0];
                double best_ev = max(stand_ev, hit_ev);
                double best_win = max(result.first[2], result.second[2]);
                if (player_points == 21) {
                    // Black jack will return 1.5
                    double dealer_black_jack_prob = 2 * remain_cards[0] * remain_cards[9];
                    dealer_black_jack_prob /= (remain_cards_num-2) * (remain_cards_num-3);
                    best_ev = (1 - dealer_black_jack_prob) * 1.5;
                    best_win = (1 - dealer_black_jack_prob);
                } else if (9 <= player_points && player_points <= 11) {
                    // Double Down
                    Policy tmp_policy;
                    auto dd_result = tmp_policy.get_policy(player_cards, dealer_cards, remain_cards, true, true).second;
                    best_ev = max(best_ev, (dd_result[2] - dd_result[0])*2);
                } else if (i == j){
                    // Split
                    vector<int> split_player_cards{i};
                    auto sp_result = get_policy(split_player_cards, dealer_cards, remain_cards, true).second;
                    best_ev = max(best_ev, (sp_result[2] - sp_result[0])*2);
                    double split_win = sp_result[2] * sp_result[2] + 2 * sp_result[2] * sp_result[1];
                    best_win = max(best_win, split_win);
                }
                // Add ev
                return_ev += cards_prob * best_ev;
                return_winrate += cards_prob * best_win;
                // Recover in remain_cards
                remain_cards[i-1]++, remain_cards[j-1]++;
            }
        }
        return {return_ev, return_winrate};
    }
};


int main(int argc, char **argv) {
    // FILE *fout = fopen("EV.log", "a");
    vector<int> card_nums{24, 20, 20, 20, 20, 24, 24, 24, 24, 96};
    Policy policy;
    auto result = policy.initial_EV(card_nums);
    printf("%.6f %.6f%%\n",result.first, result.second*100);

    // string to_c = "-A23456789T";
    // vector<int> dealer_cards{1};
    // vector<int> player_cards{2};
    exit(0);
    // vector<int> card_nums{4, 4, 4, 4, 4, 4, 4, 4, 4, 16};
    // vector<double> remain_cards();
    // for(auto x: dealer_cards){
    //     printf("%c", to_c[x]);
    // }puts("");

    // for(auto p: dealer_prob(dealer_cards, card_nums)){
    //     printf("%.6f ", p);
    // }puts("");
    // auto result = policy.get_policy(player_cards, dealer_cards, card_nums, true);
    // for(auto p : result.first)
    //     printf("%.6f |", p);
    // puts("");
    // double x = 0;
    // for(auto p : result.second)
    //     printf("%.6f |", p), x+=p;
    // puts("");
    // exit(0);
    // puts("===========");
    // // return 0;
    // // Policy policy;
    // char S[12][12];
    // for (int i=1; i<=10; i++) {
    //     for (int j=1; j<=10; j++) {
    //         vector<int> dealer_cards{};
    //         vector<int> player_cards{i, j};
    //         auto result = policy.get_policy(player_cards, dealer_cards, card_nums, true);
    //         double stand_ev = result.first[2] - result.first[0];
    //         double hit_ev = result.second[2] - result.second[0];
    //         printf("%3d %3d : ", i, j);
    //         if (stand_ev > hit_ev) {
    //             S[i-1][j-1] = 'S';
    //             printf("S\n");
    //         } else {
    //             S[i-1][j-1] = 'H';
    //             printf("H\n");
    //         }
    //     }
    // }
    // for (int i=0; i<10; i++) {
    //     for (int j=0; j<10; j++)
    //         printf("%c", S[i][j]);
    //     printf("\n");
    // }
    // return 0;
}
/*

0.0000 0.1458 0.1381 0.1348 0.1758 0.1219 0.2836
0.7164 |0.0000 |0.2836 |
0.4807 |0.0854 |0.4340 |
1.000000


0.718079 |0.000000 |0.281921 |
0.477694 |0.087607 |0.434699 |
*/
/*
HHHHHHSSSS
HHHHHHHHHH
HHHHHHHHHH
HHHHHHHHHH
HHHHHHHHHS
HHHHHHHHSS
SHHHHHHSSS
SHHHHHSSSS
SHHHHSSSSS
SHHHSSSSSS


HSSHSHHHHH
HHHHHHHHHS
HHHHHHHHSS
HHHHHHHSSS
SHHHHHSSSS
HHHHHSSSSS
HHHHSSSSSS
HHHSSSSSSS
HHSSSSSSSS
HSSSSSSSSS
*/