from flask import Flask, request, Response
import requests
from urllib.parse import urlparse, urljoin, quote, unquote

app = Flask(__name__)

def detect_m3u_type(content):
    """ Rileva se è un M3U (lista IPTV) o un M3U8 (flusso HLS) """
    if "#EXTM3U" in content and "#EXTINF" in content:
        return "m3u8"
    return "m3u"

@app.route('/proxy/m3u')
def proxy_m3u():
    """ Proxy per file M3U e M3U8 con supporto per redirezioni e header personalizzati """
    m3u_url = request.args.get('url', '').strip()
    if not m3u_url:
        return "Errore: Parametro 'url' mancante", 400

    # Headers di default per evitare blocchi del server
    default_headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/33.0 Mobile/15E148 Safari/605.1.15",
        "Referer": "https://vavoo.to/",
        "Origin": "https://vavoo.to"
    }

    # Puliamo gli header personalizzati
    headers = {**default_headers, **{
        unquote(key[7:]).replace("_", "-"): unquote(value).strip()
        for key, value in request.args.items()
        if key.lower().startswith("header_")
    }}

    try:
        response = requests.get(m3u_url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        final_url = response.url  
        m3u_content = response.text

        file_type = detect_m3u_type(m3u_content)

        if file_type == "m3u":
            return Response(m3u_content, content_type="audio/x-mpegurl")

        parsed_url = urlparse(final_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rsplit('/', 1)[0]}/"

        headers_query = "&".join([f"header_{quote(k)}={quote(v)}" for k, v in headers.items()])

        modified_m3u8 = []
        for line in m3u_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                segment_url = urljoin(base_url, line)  
                proxied_url = f"/proxy/ts?url={quote(segment_url)}&{headers_query}"
                modified_m3u8.append(proxied_url)
            else:
                modified_m3u8.append(line)

        modified_m3u8_content = "\n".join(modified_m3u8)
        return Response(modified_m3u8_content, content_type="application/vnd.apple.mpegurl")

    except requests.RequestException as e:
        return f"Errore durante il download del file M3U/M3U8: {str(e)}", 500

@app.route('/proxy/ts')
def proxy_ts():
    """ Proxy per segmenti .TS con headers personalizzati e gestione dei redirect """
    ts_url = request.args.get('url', '').strip()
    if not ts_url:
        return "Errore: Parametro 'url' mancante", 400

    headers = {
        unquote(key[7:]).replace("_", "-"): unquote(value).strip()
        for key, value in request.args.items()
        if key.lower().startswith("header_")
    }

    try:
        response = requests.get(ts_url, headers=headers, stream=True, allow_redirects=True)
        response.raise_for_status()
        return Response(response.iter_content(chunk_size=1024), content_type="video/mp2t")
    
    except requests.RequestException as e:
        return f"Errore durante il download del segmento TS: {str(e)}", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
