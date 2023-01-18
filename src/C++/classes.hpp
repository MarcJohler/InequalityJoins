#include <utility>
#include <algorithm>
#include <functional>
#include <map>
#include <string>
#include <vector>
#include <numeric>
#include <set>
#include <cassert>

template <typename T>
class DataFrame {
public:
    DataFrame(std::initializer_list<std::pair<std::string, std::vector<T>>> columns) {
        for (const auto& column : columns) {
            columns_.emplace(column.first, column.second);
        }
    }

    const std::vector<T>& operator[](const std::string& column_name) const {
        return columns_.at(column_name);
    }

private:
    std::map<std::string, std::vector<T>> columns_;
};
    
std::vector<std::pair<int, int>> pairs(const std::vector<int>& arr1, const std::vector<int>& arr2) {
    std::vector<std::pair<int, int>> output;
    for (int i = 0; i < arr1.size(); i++) {
        for (int j = 0; j < arr2.size(); j++) {
            output.emplace_back(arr1[i], arr2[j]);
        }
    }
    return output;
}

std::function<bool(int, int)> lt = ([](int x, int y) { return x < y; });
std::function<bool(int, int)> leq = ([](int x, int y) { return x <= y; });
std::function<bool(int, int)> gt = ([](int x, int y) { return x > y; });
std::function<bool(int, int)> geq = ([](int x, int y) { return x >= y; });
bool compare(int x, int y, bool less_than, bool strict) {
    if (less_than && strict) {
        return x < y;
    };
    if (less_than && !strict) {
        return x <= y;
    };
    if (!less_than && strict) {
        return x > y;
    };
    if (!less_than && !strict){
        return x >= y;
    };
    return false;
}

template<typename T>
std::vector<std::pair<int, int>>  naive_ineqjoin(
    const DataFrame<T>& R, 
    const DataFrame<T>& S, 
    const std::string& r, 
    const std::string& s, 
    const bool less_than,
    const bool strict){
    // Initialize the arrays in the right order
    std::vector<T> r_sorted = R[r];
    std::vector<int> rid(r_sorted.size());
    std::iota(rid.begin(), rid.end(), 0);
    std::vector<T> s_sorted = S[s];
    std::vector<int> sid(s_sorted.size());
    std::iota(sid.begin(), sid.end(), 0);

    if (less_than == true) {
        std::sort(rid.begin(), rid.end(), [&](int i, int j) {return r_sorted[i] > r_sorted[j]; });
        std::reverse(r_sorted.begin(), r_sorted.end());
        std::sort(sid.begin(), sid.end(), [&](int i, int j) {return s_sorted[i] < s_sorted[j]; });
        std::sort(s_sorted.begin(), s_sorted.end());
    }
    else {
        std::sort(rid.begin(), rid.end(), [&](int i, int j) {return r_sorted[i] < r_sorted[j]; });
        std::sort(r_sorted.begin(), r_sorted.end());
        std::sort(sid.begin(), sid.end(), [&](int i, int j) {return s_sorted[i] > s_sorted[j]; });
        std::reverse(s_sorted.begin(), s_sorted.end());
    }

    std::vector<std::pair<int, int>> result;
    // Check for the inequality constraints
    for (int i = 0; i < r_sorted.size(); i++) {
        int j = 0;
        while (j < s_sorted.size()) { 
            if (compare(r_sorted[i], s_sorted[j], less_than, strict)) {
                // Append pairs of indices
                result.insert(result.end(), 
                    // you probably gonna need an iterator to solve this, C++ is such an underdeveloped language...
                    std::make_pair(rid[i], sid[j]));
                // Remember the indices from the second relation
                s_sorted = std::vector<T>(s_sorted.begin(), s_sorted.begin() + j);
                sid = std::vector<int>(sid.begin(), sid.begin() + j);
                break;
            }
            j++;
        }
    }
    return result;
}

std::vector<std::pair<int, int>> intersect_pairs(const std::vector<std::vector<std::pair<int, int>>>& pair_lists, const std::vector<size_t>& pair_list_lengths) {
    // start with the shortes pair lists
    std::vector<size_t> length_order(pair_list_lengths.size());
    std::iota(length_order.begin(), length_order.end(), 0);
    std::sort(length_order.begin(), length_order.end(), [&pair_list_lengths](size_t i, size_t j) { return pair_list_lengths[i] < pair_list_lengths[j]; });

    // start the intersection
    std::set<std::pair<int, int>> result(pair_lists[length_order[0]].begin(), pair_lists[length_order[0]].end());
    for (size_t i = 1; i < length_order.size(); ++i) {
        std::set<std::pair<int, int>> next(pair_lists[length_order[i]].begin(), pair_lists[length_order[i]].end());
        std::vector<std::pair<int, int>> intersection;
        std::set_intersection(result.begin(), result.end(), next.begin(), next.end(), std::back_inserter(intersection));
        result = std::set<std::pair<int, int>>(intersection.begin(), intersection.end());
    }

    return std::vector<std::pair<int, int>>(result.begin(), result.end());
}

template <typename T>
std::vector<std::pair<int, int>> naive_ineqjoin_multicond(
    const DataFrame<T>& R, const DataFrame<T>& S,
    const std::vector<std::string>& r, const std::vector<std::string>& s,
    const std::vector<std::function<bool(T, T)>>& op)
{
    // check if the arguments are consistent
    const size_t condition_len = op.size();
    assert(s.size() == condition_len);
    assert(r.size() == condition_len);

    // for each join condition check the valid tuples
    std::vector<std::vector<std::pair<int, int>>> results(condition_len);
    std::vector<size_t> res_lengths(condition_len);
    for (size_t i = 0; i < condition_len; ++i) {
        results[i] = naive_ineqjoin(R, S, r[i], s[i], op[i]);
        res_lengths[i] = results[i].size();
    }

    // only consider tuples which fulfill every join condition
    return intersect_pairs(results, res_lengths);
}