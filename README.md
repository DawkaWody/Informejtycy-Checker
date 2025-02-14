# Informejtycy-Checker

System sprawdzający rozwiązania i debugger do strony informejtycy.pl. Serwer musi mieć zainstalowane zależności wymienione w `requirements.txt`.

> Uwagi do dockera [nr 1](#Uwaga-do-dockera-nr-1) i [nr 1](#Uwaga-do-dockera-nr-2).

## Przed uruchomieniem na serwerze

**UWAGA:** aby wykonać poniższe czynności automatycznie, skorzystaj ze skrytpu `setup.sh` poprzez komendę `sudo ./setup.sh`.

Zanim serwer zostanie uruchomiony, należy wykonać szereg czynności.

- Odświeżenie baz danych i pakietów instalatorów: `sudo apt-get update && sudo apt-get upgrade && sudo snap refresh`;
- Pobranie narzędzi: `python (>=3.11)`, `python3-pip`, `gcc`, `docker`;
- Zainstalowanie wymaganych bibliotek pythona (lista w `requirements.txt`);
- Utworzenie grupy `docker` (**UWAGA:** przed utworzeniem grupy `cgroup`) (patrz [docker bez sudo](#Docker-bez-sudo));
- Utworzenie grupy `cgroup` (patrz [tworzenie grupy cgroup](#Tworzenie-grupy-cgroup));

## Docker bez sudo <a name="Docker-bez-sudo"></a>

Aby używać dockera poprzez `DockerManager()` należy utworzyć grupę docker i dodać do niej aktualnego użytkownika.

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
reboot -f
```

**Ostatnia komenda uruchomi ponownie komputer, aby zmiany zostały zastosowane.** Teraz, aby sprawdzić czy wszystko działa, należy wpisać:

```bash
docker ps
```

Jeżeli nie pojawi się informacja o braku permisji, wszystko poszło zgodnie z planem.

## Tworzenie grupy cgroup <a name="Tworzenie-grupy-cgroup"></a>

Do zabezpieczenia serwera przed wysokim zużyciem CPU przez wiele kontenerów, będziemy korzystać z systemu [cgroupv2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html). Najpierw upewniamy się, że mamy zainstalowany system `cgroupv2`, a nie `cgroupv1` oraz czy `-.slice`, czyli główna grupa, pozwala nam na zarządzanie zasobami CPU. Robimy to następującymi komendami.

```bash
mount | grep cgroup

cat /sys/fs/cgroup/cgroup.controllers
cat /sys/fs/cgroup/cgroup.subtree_control
```

Po pierwszej komendzie powinniśmy zobaczyć `cgroup2 on /sys/fs/cgroup type cgroup2...`. W innym przypadku należy zaktualizować jądro linuxa i przemountować `cgroupv1` na `cgroupv2` (nie mam pojęcia jak to zrobić). Po kolejnych dwóch komendach powinniśmy zobaczyć szereg słów, w tym `cpu`. Jeżeli `cpu` nie ma po pierwszej komendzie, oznacza to, że system z jakiegoś powodu nie pozwala nam zarządzać `cpu` (i nie wiem co wtedy zrobić, więc wrzucamy pytanie do chata gpt). Jeżeli po drugiej komendzie nie widać `cpu`, możemu dodać je manualnie.

```bash
sudo bash -c 'echo "+cpu" > /sys/fs/cgroup/cgroup.subtree_control'
```

Teraz wpisujemy ponownie komendę `cat /sys/fs/cgroup/cgroup.subtree_control` i powinno znajdować się tam `cpu`. Teraz tworzymy grupę. Serwer będzie próbował podłączyć się do grupy `informejtycy_debugger.slice`, więc nazwy tej nie należy zmieniać.

```bash
sudo systemctl set-property informejtycy_debugger.slice CPUQuota=60%
```

Dzięki temu, wszystkie uruchomione kontenery łącznie nie będą mogły zużyć więcej niż 60% mocy obliczeniowej CPU. Wartość tą można dostosować do mocy serwera, może być to więcej niż 60%. Dla komfortowego debugowania w klikunastu procesach zaleca się jednak conajmniej 60%. **Nie oznacza to, że jeden kontener może zużywać 60%** - pojedyńczo kontenery będą ograniczane przez dockera, jednak chodzi o zużycie po uruchomieniu wielu kontenerów.

Możemy sprawdzić, czy komenda została wykonana poprawnie wpisując:

```bash
cat /sys/fs/cgroup/informejtycy_debugger.slice/cgroup.controllers # Powinniśmy otrzymać szereg słów, w tym "cpu"
cat /sys/fs/cgroup/informejtycy_debugger.slice/cpu.max # Powinniśmy otrzymać dwie liczby, gdzie pierwsza jest mniejsza od drugiej
```

## Uwaga do dockera nr 1 <a name="Uwaga-do-dockera-nr-1"></a>

Należy zignorować pojawiające się w konsoli informacje typu `can't kill container ...` - sprawdzarka próbuje zatrzymać kontener dockera, na wypadek, gdyby użytkownik podał nieskończoną pętle. Wtedy informacji takiej nie będzie, bo znajdzie się kontener do wyłączenia. W innym wypadku, pojawia się wspomniany "błąd".

## Uwaga do dockera nr 2 <a name="Uwaga-do-dockera-nr-2"></a>

Jeżeli poprawny program nie chce się skompilować, może to oznaczać, że brakuje bibliotek. Należy w funkcji `docker_manager.manager.DockerManager.build_for_checker()` dodać tą lub/i inne do zmiennej `content` w polu `RUN apk add...`.
