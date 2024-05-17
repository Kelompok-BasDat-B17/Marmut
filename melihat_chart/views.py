from django.shortcuts import render
from lib_database.query import *
from django.db import connection 

def melihat_chart (request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT C.tipe AS "Tipe"
            FROM CHART C
        """) 
        chart = cursor.fetchall()

    if not chart:
        return render(request, 'error.html', {'message': 'Chart not found'})

    print("Chart details fetched:", chart)  # Check what data is fetched from the database

    context = {
        'chart_list': chart,
    }

    return render(request, 'melihat_chart.html', context)

def chart_detail(request):
    with connection.cursor() as cursor:
        cursor.execute("""
        """) 
        chart = cursor.fetchall()

    if not chart:
        return render(request, 'error.html', {'message': 'Chart not found'})

    print("Chart details fetched:", chart)  # Check what data is fetched from the database

    context = {
        'chart_list': chart,
    }
    return render(request, 'chart_detail.html')

def chart_detail(request, chart_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT K.judul AS "Judul",
                AK.nama AS "Artist",
                K.tanggal_rilis AS "Tanggal Rilis",
                S.total_play AS "Total Play",
                C.tipe AS "Tipe"
            FROM SONG S
            JOIN KONTEN K ON S.id_konten = K.id
            JOIN ARTIST AR ON S.id_artist = AR.id
            JOIN AKUN AK ON AR.email_akun = AK.email
            JOIN PLAYLIST_SONG PS ON PS.id_song = K.id
            JOIN CHART C ON PS.id_playlist = C.id_playlist
            WHERE C.tipe = %s
            ORDER BY S.total_play DESC
        """, [str(chart_id)])  # Convert UUID to string if necessary
        chart_detail = cursor.fetchall()

    if not chart_detail:
        return render(request, 'error.html', {'message': 'Chart Detail not found'})

    print("Chart Details fetched:", chart_detail)  # Check what data is fetched from the database

    tipe = chart_detail[0][4] if chart_detail else 'Unknown Chart'
    context = {
        'tipe': tipe,
        'chart_details': [
            {'judul': row[0], 'artist': row[1], 'tanggal_rilis': row[2], 'total_play': row[3]}
            for row in chart_detail
        ],
    }

    return render(request, 'chart_detail.html', context)