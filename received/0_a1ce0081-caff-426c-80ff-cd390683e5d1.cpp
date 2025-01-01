#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

int main()
{
    int n; cin >> n;
    vector<int> numbers(n);
    for (int i = 0; i < n; i++) cin >> numbers[i];

    int result = accumulate(numbers.begin(), numbers.end(), 0);

    cout << result << endl;

    return 0;
}
