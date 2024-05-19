from django.shortcuts import render
from django.db import connection  # Pastikan Anda sudah mengimpor connection

def play_user_playlist(request, user_playlist_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT U.judul AS "Judul",
                AKUN.nama AS "Pembuat",
                U.jumlah_lagu AS "Jumlah Lagu",
                U.total_durasi AS "Total Durasi",
                U.tanggal_dibuat AS "Tanggal Dibuat",
                U.deskripsi AS "Deskripsi"
            FROM USER_PLAYLIST U
            JOIN AKUN ON U.email_pembuat = AKUN.email
            WHERE U.id_user_playlist = %s
        """, [str(user_playlist_id)])
        user_playlist_detail = cursor.fetchall()

        cursor.execute("""
            SELECT S.id_konten AS "Song ID",
                K.judul AS "Judul Lagu",
                AKUN.nama AS "Oleh",
                K.durasi AS "Durasi"
            FROM USER_PLAYLIST UP
            JOIN PLAYLIST_SONG PS ON UP.id_playlist = PS.id_playlist
            JOIN SONG S ON PS.id_song = S.id_konten
            JOIN KONTEN K ON S.id_konten = K.id
            JOIN ARTIST A ON S.id_artist = A.id
            JOIN AKUN ON A.email_akun = AKUN.email
            WHERE UP.id_user_playlist = %s
        """, [str(user_playlist_id)])
        songs = cursor.fetchall()

    song_data = [{
        'id': song[0],
        'judul': song[1],
        'oleh': song[2],
        'durasi': song[3],
    } for song in songs]

    if not user_playlist_detail:
        return render(request, 'error.html', {'message': 'Playlist not found'})

    total_duration_minutes = user_playlist_detail[0][3]  # Memastikan ini adalah indeks yang benar untuk total durasi
    total_hours = total_duration_minutes // 60
    total_minutes = total_duration_minutes % 60

    context = {
        'user_playlist_detail': {
            'judul': user_playlist_detail[0][0],
            'pembuat': user_playlist_detail[0][1],
            'jumlah_lagu': user_playlist_detail[0][2],
            'total_durasi_hours': total_hours,
            'total_durasi_minutes': total_minutes,
            'tanggal_dibuat': user_playlist_detail[0][4],
            'deskripsi': user_playlist_detail[0][5],
        },
        'songs': song_data
    }

    return render(request, 'play_user_playlist.html', context)  # Pastikan template yang dipanggil sesuai
