from django.shortcuts import render
from django.db import DatabaseError, InternalError, connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def play_song(request, song_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT K.judul AS "Judul",
                array_agg(G.genre) AS "Genre",
                AK.nama AS "Artist",
                array_agg(SW.nama) AS "Songwriter",
                K.durasi AS "Durasi",
                K.tanggal_rilis AS "Tanggal Rilis",
                K.tahun AS "Tahun",
                COALESCE(SUM(S.total_play), 0) AS "Total Play",
                COALESCE(SUM(S.total_download), 0) AS "Total Downloads",
                A.judul AS "Album"
            FROM SONG S
            JOIN KONTEN K ON S.id_konten = K.id
            LEFT JOIN GENRE G ON K.id = G.id_konten
            LEFT JOIN ARTIST AR ON S.id_artist = AR.id
            LEFT JOIN AKUN AK ON AR.email_akun = AK.email
            LEFT JOIN SONGWRITER_WRITE_SONG SWS ON S.id_konten = SWS.id_song
            LEFT JOIN SONGWRITER SWR ON SWS.id_songwriter = SWR.id
            LEFT JOIN AKUN SW ON SWR.email_akun = SW.email
            LEFT JOIN ALBUM A ON S.id_album = A.id
            WHERE K.id = %s
            GROUP BY K.id, AK.nama, A.judul
        """, [str(song_id)])  # Convert UUID to string if necessary
        song_detail = cursor.fetchall()

    if not song_detail:
        return render(request, 'error.html', {'message': 'Song not found'})

    print("Song details fetched:", song_detail)  # Check what data is fetched from the database

    song_data = song_detail[0]
    context = {
        'song_detail': {
            'judul': song_data[0],
            'genres': song_data[1],
            'artist': song_data[2],
            'songwriters': song_data[3],
            'durasi': song_data[4],
            'tanggal_rilis': song_data[5],
            'tahun': song_data[6],
            'total_play': song_data[7],
            'total_downloads': song_data[8],
            'album': song_data[9],
        },
    }

    return render(request, 'play_song.html', context)

def add_song_to_playlist(request, song_id):
    success_message = None
    error_message = None
    playlist_name = None
    song_title = None
    artist_name = None
    playlists = None
    other_playlist_id = None

    email_pengguna = request.COOKIES.get('email')

    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT k.judul, a.nama AS artist
                FROM song s
                JOIN konten k ON s.id_konten = k.id
                JOIN artist ar ON s.id_artist = ar.id
                JOIN akun a ON ar.email_akun = a.email
                WHERE s.id_konten = %s;
            """, [song_id])
        song_data = cursor.fetchone()
        
        if song_data:
            song_title, artist_name = song_data

        if request.method == 'POST':
            other_playlist_id = request.POST.get('other_playlist_id')
            
            cursor.execute("SELECT judul FROM user_playlist WHERE id_playlist = %s", [other_playlist_id])
            playlist_name_query = cursor.fetchone()
            if playlist_name_query:
                playlist_name = playlist_name_query[0]
            
            try:
                cursor.execute("INSERT INTO playlist_song (id_playlist, id_song) VALUES (%s, %s);", 
                            [other_playlist_id, song_id])
                connection.commit()
                success_message = f"Berhasil menambahkan Lagu dengan judul '{song_title}' oleh '{artist_name}' ke '{playlist_name}'!"
            except (DatabaseError, InternalError) as e:
                connection.rollback()
                if 'marmut.check_duplicate_song_on_playlist' in str(e):
                    error_message = f"Lagu '{song_title}' sudah ada dalam playlist '{playlist_name}'"
                else:
                    error_message = "Gagal menambahkan lagu ke playlist"

    
        cursor.execute("""
            SELECT id_playlist, judul 
            FROM user_playlist 
            WHERE email_pembuat = %s;
        """, [email_pengguna])
        playlists = cursor.fetchall()

        context = {
            'song_id': song_id,
            'song_title': song_title,
            'artist_name': artist_name,
            'success_message': success_message,
            'error_message': error_message,
            'playlist_name': playlist_name,
            'playlists' : playlists,
            'other_playlist' : other_playlist_id
        }

        cursor.close()
        connection.close()

        return render(request, 'add_song_to_playlist.html', context)


@csrf_exempt
def update_play_count(request, song_id):
    if request.method == 'POST':
        print("Received request to update play count for song ID:", song_id)  # Print debug info
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE SONG SET total_play = total_play + 1 WHERE id_konten = %s
                RETURNING total_play;
            """, [song_id])
            new_total_plays = cursor.fetchone()[0]
            print("New total plays:", new_total_plays)  # Print updated play count

        return JsonResponse({'success': True, 'new_total_plays': new_total_plays})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)