# System g³osowania kibiców na "zawodnika meczu" w chmurze AWS

Projekt zrealizowany w ramach przedmiotu **Technologie chmurowe**. Celem projektu by³o zaprojektowanie, analiza kosztów (TCO 1 rok / 3 lata) oraz praktyczna weryfikacja skalowalnej i wysoko dostêpnej architektury webowej w chmurze Amazon Web Services (region `us-east-1`).

## Architektura rozwi¹zania
* **Sieæ i bezpieczeñstwo:** Amazon VPC, grupa zabezpieczeñ `voting-web-sg` (porty `80`, `22`, `3306`).
* **Warstwa obliczeniowa:** instancje EC2 `t3.micro`, niestandardowy obraz `voting-web-ami`, szablon `voting-lt` oraz grupa `voting-asg` (zakres 1–4 instancje, polityka *Target Tracking* dla progu 50% CPU).
* **Aplikacja webowa:** Python 3, Flask, PyMySQL oraz serwer WSGI Gunicorn (3 procesy robocze) uruchomiony jako us³uga `systemd` (`voting.service`).
* **Równowa¿enie ruchu:** Application Load Balancer (`voting-alb`) oraz grupa docelowa `voting-tg` (œcie¿ka kontrolna `/health`) w uk³adzie Multi-AZ.
* **Warstwa danych:** relacyjna baza danych MySQL w us³udze Amazon RDS (`voting-db`).

## Struktura repozytorium
* `app/app.py` – kod Ÿród³owy aplikacji g³osowania (Flask + PyMySQL) ³¹cz¹cej siê z Amazon RDS.
* `app/requirements.txt` – lista bibliotek Pythona wymaganych do uruchomienia aplikacji.
* `scripts/setup_ec2.sh` – komendy konfiguracyjne z terminala EC2 (inicjalizacja bazy oraz konfiguracja us³ugi `systemd` z serwerem Gunicorn).
* `tests/load_test.py` – wielow¹tkowy skrypt w jêzyku Python (HTTP Keep-Alive) wykorzystany do testów obci¹¿eniowych.
* `docs/` – Ÿród³a sprawozdania w systemie LaTeX, zrzuty ekranu oraz wygenerowany plik PDF.