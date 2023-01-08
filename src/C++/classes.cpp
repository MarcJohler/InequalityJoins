#include <iostream>
#include "classes.hpp"
#include <utility>
#include <algorithm>
#include <functional>
#include <map>
#include <string>
#include <vector>
#include <numeric>
#include <set>

int main()
{
    DataFrame<int> R = {{"A", {1, 2, 3}}, {"B", {4, 5, 6}}, {"C", {7, 8, 9}}};
    DataFrame<int> S = {{"D", {10, 11, 12}}, {"E", {3, 30, 1}}, {"F", {16, 17, 18}}};

    std::vector<std::string> r = {"A", "B"};
    std::vector<std::string> s = {"D", "E"};
    
    std::vector<std::pair<int, int>> result = naive_ineqjoin(R, S, "B", "E", true, true);


    for (const auto& [r, s] : result) {
        std::cout << "(" << r << ", " << s << ")" << std::endl;
    }
    
    return 0;
}
