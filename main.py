from spotify_helper import get_spotify_client, get_playlist_tracks
from soundcloud_helper import SoundCloudAuth, SoundCloudAPI
import json

def main():
    print("🎧 Spotify → SoundCloud")
    print("------------------------")

    # 1. Autenticación con Spotify
    sp = get_spotify_client()

    # 2. Pedir URL de playlist
    playlist_url = input("📋 Pega la URL de la playlist de Spotify: ").strip()

    # 3. Comprobar si es una playlist o "Tus canciones guardadas"
    if "playlist/" in playlist_url:
        # Es una playlist
        playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
        is_playlist = True
    elif "collection/tracks" in playlist_url:
        # Es "Tus canciones guardadas"
        is_playlist = False
        playlist_id = None
    else:
        print("❌ URL no válida.")
        return

    # 4. Obtener canciones de Spotify
    if is_playlist:
        tracks = get_playlist_tracks(sp, playlist_id)
    else:
        # "Tus canciones guardadas" -> Usamos la ruta para obtener canciones favoritas
        results = sp.current_user_top_tracks(limit=50)  # Limitar a las 50 canciones principales
        tracks = [{"name": track["name"], "artist": ", ".join([artist["name"] for artist in track["artists"]])} for track in results["items"]]

    if not tracks:
        print("😕 No se encontraron canciones.")
        return

    print(f"\n🎶 {len(tracks)} canciones encontradas.")

    # 5. Autenticación con SoundCloud
    soundcloud_auth = SoundCloudAuth()
    soundcloud_auth.get_auth_url()  # Esto abrirá la URL de autorización en el navegador

    # 6. Pedir el código de autorización de SoundCloud
    authorization_code = input("Introduce el código de autorización recibido de SoundCloud: ").strip()

    try:
        # 7. Obtener el token de acceso de SoundCloud
        access_token = soundcloud_auth.get_access_token(authorization_code)
        soundcloud_api = SoundCloudAPI(access_token)
        print("Autenticación con SoundCloud exitosa.")

    except Exception as e:
        print(f"❌ Error al obtener el token de acceso de SoundCloud: {e}")
        return

    # 8. Preguntar si van a favoritos o playlist
    print("\n📥 ¿Qué deseas hacer con estas canciones en SoundCloud?")
    print("1. Guardarlas como favoritas")
    print("2. Añadirlas a una nueva playlist")
    choice = input("Elige una opción (1 o 2): ").strip()

    if choice not in ("1", "2"):
        print("❌ Opción inválida.")
        return

    action = "favoritos" if choice == "1" else "playlist"
    output_list = []

    # 9. Buscar en SoundCloud y agregar
    for i, track in enumerate(tracks, 1):
        query = f"{track['name']} {track['artist']}"
        print(f"\n{i}. 🔍 Buscando en SoundCloud: {query}")

        results = soundcloud_api.search_tracks(query)

        if results:
            best_match = results[0]  # Tomamos el primero como mejor match
            print(f"🎯 Mejor match: {best_match['title']} - {best_match['artist']}")
            print(f"🔗 {best_match['url']}")
            output_list.append(best_match)
        else:
            print("⚠️ No se encontraron resultados en SoundCloud.")

    # 10. Guardar resultados simulados
    output_filename = f"{action}_soundcloud.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(output_list, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Canciones guardadas en '{output_filename}' como {action}.")

if __name__ == "__main__":
    main()
