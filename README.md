# Informejtycy-Checker

System sprawdzający rozwiązania i debugger do strony informejtycy.pl. Serwer musi mieć zainstalowane zależności wymienione w `requirements.txt`.

## Przed uruchomieniem na serwerze

Zanim serwer zostanie uruchomiony, należy wykonać szereg czynności.

- Odświeżenie bazy danych apt: `sudo apt-get update && sudo apt-get upgrade`;
- Pobranie narzędzi: `python (>=3.11)`, `gcc`, `docker`, `cgroup-tools`;
- Zainstalowanie wymaganych bibliotek pythona (lista w `requirements.txt`);
- Utworzenie grupy `docker` (patrz [docker bez sudo](#Docker-bez-sudo));
- Utworzenie grupy `cgroup` (jeszcze nie wiem jak, jak się dowiem to tu wpisze);

## Docker bez sudo <a name="Docker-bez-sudo"></a>

Aby używać dockera poprzez `DockerManager()` należy utworzyć grupę docker i dodać do niej aktualnego użytkownika.

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
reboot -f
```

**Ostatnia komenda zresetuje system, aby zmiany zostały zastosowane.** Teraz, aby sprawdzić czy wszystko działa, należy wpisać:

```bash
docker ps
```

Jeżeli nie pojawi się informacja o braku permisji, wszystko poszło zgodnie z planem.

## Uwaga do dockera nr 1

Należy zignorować pojawiające się w konsoli informacje typu `can't kill container ...` - sprawdzarka próbuje zatrzymać kontener dockera, na wypadek, gdyby użytkownik podał nieskończoną pętle. Wtedy informacji takiej nie będzie, bo znajdzie się kontener do wyłączenia. W innym wypadku, pojawia się wspomniany "błąd".

## Uwaga do dockera nr 2

Jeżeli poprawny program nie chce się skompilować, może to oznaczać, że brakuje bibliotek. Należy w funkcji `docker_manager.manager.DockerManager.build_for_checker()` dodać tą lub/i inne do zmiennej `content` w polu `RUN apk add...`.
