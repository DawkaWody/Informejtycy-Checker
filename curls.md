# cURL-e do testów sprawdzarki
```curl
curl --location '127.0.0.1:5000' \
--header 'Problem: 0' \
--data '#include <iostream>
#include <vector>
#include <numeric>
using namespace std;

int main()
{
    int n; cin >> n;
    vector<int> liczby(n);
    for (int i = 0; i < n; i++) cin >> liczby[i];

    cout << accumulate(liczby.begin(), liczby.end(), 0) << endl;
    return 0;
}'
```

```curl
curl --location '127.0.0.1:5000' \
--header 'Problem: 0' \
--data '#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main()
{
    int n; cin >> n;
    vector<int> liczby(n);
    for (int i = 0; i < n; i++) cin >> liczby[i];

    cout << 2 << endl; // Metoda zalesia
    return 0;
}
'
```

```curl
curl --location '127.0.0.1:5000' \
--header 'Problem: 0' \
--data '#include <iostream>
#include <vector>
#include <numeric>
using namespace std;

int main()
{
    int n; cin >> n;
    vector<int> liczby(n);
    for (int i = 0; i < n; i++) cin >> liczby[i];

    int i = 0;
    while (true)
        i++;

    return 0;
}'
```
