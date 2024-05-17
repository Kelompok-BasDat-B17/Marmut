from django.shortcuts import render
from lib_database.query import *
from django.db import connection  # Ensure you have imported connection

def play_podcast(request, podcast_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT K.judul AS "Judul",
                array_agg(G.genre) AS "Genre",
                AKUN.nama AS "Podcaster",
                COALESCE(EP.total_durasi, 0) AS "Total Durasi",
                K.tanggal_rilis AS "Tanggal Rilis",
                K.tahun AS "Tahun"
            FROM PODCAST P
            JOIN KONTEN K ON P.id_konten = K.id
            LEFT JOIN GENRE G ON K.id = G.id_konten
            LEFT JOIN AKUN ON P.email_podcaster = AKUN.email
            LEFT JOIN (
                SELECT id_konten_podcast, SUM(durasi) AS total_durasi
                FROM EPISODE
                GROUP BY id_konten_podcast
            ) AS EP ON P.id_konten = EP.id_konten_podcast
            WHERE K.id = %s
            GROUP BY K.judul, AKUN.nama, K.tanggal_rilis, K.tahun, EP.total_durasi
        """, [str(podcast_id)])  # Convert UUID to string if necessary
        podcast_detail = cursor.fetchall()

        cursor.execute("""
            SELECT E.id_episode,
                    E.judul AS "Judul Episode",
                    E.deskripsi AS "Deskripsi",
                    E.durasi AS "Durasi",
                    E.tanggal_rilis AS "Tanggal"
            FROM EPISODE E
            JOIN PODCAST P ON E.id_konten_podcast = P.id_konten
            JOIN KONTEN K ON P.id_konten = K.id
            WHERE K.id = %s
            ORDER BY E.tanggal_rilis DESC
        """, [str(podcast_id)])
        episodes = cursor.fetchall()

    episode_data = [{
        'id': episode[0],
        'judul': episode[1],
        'deskripsi': episode[2],
        'durasi': episode[3],
        'tanggal_rilis': episode[4]
    } for episode in episodes]

    if not podcast_detail:
        return render(request, 'error.html', {'message': 'Podcast not found'})

    total_duration_minutes = podcast_detail[0][3]
    total_hours = total_duration_minutes // 60
    total_minutes = total_duration_minutes % 60

    context = {
        'podcast_detail': {
            'judul': podcast_detail[0][0],
            'genre': podcast_detail[0][1],
            'podcaster': podcast_detail[0][2],
            'total_durasi_hours': total_hours,
            'total_durasi_minutes': total_minutes,
            'tanggal_rilis': podcast_detail[0][4],
            'tahun': podcast_detail[0][5],
        },
        'episodes': episode_data
    }

    return render(request, 'play_podcast.html', context)