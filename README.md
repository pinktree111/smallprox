# smallprox

Ecco il README.md completamente formattato per essere facilmente copiabile e incollabile.


---

📜 M3U8 Proxy Dockerizzato

🚀 M3U8 Proxy è un server proxy basato su Flask e Requests che consente di:

Scaricare e modificare flussi M3U/M3U8.

Proxyare i segmenti .TS, mantenendo gli header personalizzati.

Superare restrizioni di accesso (es. Referer, User-Agent).

Dockerizzarlo per l'uso su qualsiasi macchina o server.



---

🔧 Installazione e Uso con Docker

1️⃣ Clonare il Repository

git clone https://github.com/tuo-username/m3u8-proxy.git
cd m3u8-proxy

2️⃣ Costruire l'Immagine Docker

docker build -t m3u8-proxy .

3️⃣ Avviare il Container

docker run -d -p 5000:5000 --name m3u8-proxy m3u8-proxy

4️⃣ Verificare che il Proxy sia Attivo

curl http://localhost:5000/

Dovresti ricevere una risposta tipo:

Errore: Parametro 'url' mancante


---

🛠️ API e Esempi di Uso

📌 Ottenere un File M3U8 Proxyato

🔹 Richiesta

GET /proxy/m3u?url=<URL_M3U8>&header_<HEADER_NAME>=<HEADER_VALUE>

🔹 Esempio

curl -L -v "http://localhost:5000/proxy/m3u?url=https://vavoo.to/play/3658277450/index.m3u8&header_Referer=https://vavoo.to/&header_User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/33.0 Mobile/15E148 Safari/605.1.15&header_Origin=https://vavoo.to"

🔹 Risposta attesa (M3U8 modificato)

#EXTM3U
#EXT-X-VERSION:6
#EXTINF:7.280000,
/proxy/ts?url=https%3A%2F%2Fqmaalhy7acgxwhm.ngolpdkyoctjcddxshli469r.org%2F67c23883_0.ts&header_Referer=https://vavoo.to/&header_User-Agent=Mozilla...
#EXTINF:4.880000,
/proxy/ts?url=https%3A%2F%2Fqmaalhy7acgxwhm.ngolpdkyoctjcddxshli469r.org%2F67c23883_1.ts&header_Referer=https://vavoo.to/&header_User-Agent=Mozilla...


---

📌 Ottenere un Segmento .TS Proxyato

🔹 Richiesta

GET /proxy/ts?url=<URL_TS>&header_<HEADER_NAME>=<HEADER_VALUE>

🔹 Esempio

curl -L -v "http://localhost:5000/proxy/ts?url=https://qmaalhy7acgxwhm.ngolpdkyoctjcddxshli469r.org/67c23883_0.ts&header_Referer=https://vavoo.to/&header_User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/33.0 Mobile/15E148 Safari/605.1.15"


---

📌 Configurare un Player IPTV per Usare il Proxy

Se vuoi usare il proxy in un player IPTV, modifica il file .m3u in questo modo:

🔹 Prima (Senza Proxy)

#EXTM3U
#EXTINF:-1 tvg-name="Canale Test" group-title="IPTV", Canale Test
https://vavoo.to/play/3658277450/index.m3u8

🔹 Dopo (Con Proxy)

#EXTM3U
#EXTINF:-1 tvg-name="Canale Proxyato" group-title="IPTV", Canale Proxyato
http://localhost:5000/proxy/m3u?url=https://vavoo.to/play/3658277450/index.m3u8&header_Referer=https://vavoo.to/&header_User-Agent=Mozilla/5.0...


---

📌 Gestione del Container Docker

🔹 Controllare i log del container

docker logs -f m3u8-proxy

🔹 Fermare il container

docker stop m3u8-proxy

🔹 Riavviare il container

docker start m3u8-proxy

🔹 Rimuovere il container

docker rm -f m3u8-proxy


---

📌 Deployment su un Server

Se vuoi eseguire il proxy su un server remoto (es. VPS con Ubuntu), segui questi passi:

1️⃣ Installa Docker su Ubuntu

sudo apt update && sudo apt install -y docker.io

2️⃣ Copia i file sul server

Se sei su Windows, usa WinSCP o scp:

scp -r m3u8-proxy user@server-ip:/home/user/

3️⃣ Accedi al server e avvia il container

ssh user@server-ip
cd /home/user/m3u8-proxy
docker build -t m3u8-proxy .
docker run -d -p 5000:5000 --name m3u8-proxy m3u8-proxy

Ora il proxy sarà raggiungibile da qualsiasi dispositivo all’indirizzo:

http://server-ip:5000/proxy/m3u?url=<URL_M3U8>


---

🎉 Conclusione

✔ Supporta .m3u e .m3u8 automaticamente
✔ Mantiene e inoltra gli header HTTP per l'autenticazione
✔ Supera restrizioni basate su Referer, User-Agent, Origin
✔ Funziona su qualsiasi player IPTV
✔ Dockerizzato per un facile deployment

🚀 Ora puoi usare il tuo proxy per guardare flussi M3U8 senza restrizioni! 🚀


---

📌 Autore: pinktree
📌 Repo GitHub: de tu sorella



