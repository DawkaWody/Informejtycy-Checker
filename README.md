# Informejtycy-Checker

System sprawdzający rozwiązania i debugger do strony informejtycy.pl

## Uwaga do dockera nr 1

Należy zignorować pojawiające się w konsoli informacje typu `can't kill container ...` - sprawdzarka próbuje zatrzymać kontener dockera, na wypadek, gdyby użytkownik podał nieskończoną pętle. Wtedy informacji takiej nie będzie, bo znajdzie się kontener do wyłączenia. W innym wypadku, pojawia się wspomniany "błąd".

## Uwaga do dockera nr 2

Jeżeli poprawny program nie chce się skompilować, może to oznaczać, że brakuje bibliotek np. `libc6-compat`. Należy w funkcji `docker_manager.manager.DockerManager.build_for_checker()` dodać tą lub/i inne do zmiennej `content` w polu `RUN apk add ...`.

### cURL-e do testów sprawdzarki
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
