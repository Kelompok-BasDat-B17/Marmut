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

def daily_top(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT S.id_konten AS "Song ID",
                K.judul AS "Judul",
                AK.nama AS "Artist",
                K.tanggal_rilis AS "Tanggal Rilis",
                S.total_play AS "Total Play"
            FROM SONG S
            JOIN KONTEN K ON S.id_konten = K.id
            JOIN ARTIST AR ON S.id_artist = AR.id
            JOIN AKUN AK ON AR.email_akun = AK.email
            JOIN PLAYLIST_SONG PS ON PS.id_song = S.id_konten
            JOIN CHART CH ON CH.id_playlist = PS.id_playlist 
            WHERE PS.id_playlist = '001e4567-e89b-12d3-a456-426614174000'
            ORDER BY S.total_play DESC
            LIMIT 20;
        """)  # Convert UUID to string if necessary
        daily_top = cursor.fetchall()

    if not daily_top:
        return render(request, 'error.html', {'message': 'Chart not found'})

    print("Chart Details fetched:", daily_top)  # Check what data is fetched from the database

    context = {
        'daily_top': [
            {'id': song[0], 'judul': song[1], 'artist': song[2], 'tanggal_rilis': song[3], 'total_play': song[4]}
            for song in daily_top
        ],
    }

    return render(request, 'daily_top.html', context)

def weekly_top(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT S.id_konten AS "Song ID",
                K.judul AS "Judul",
                AK.nama AS "Artist",
                K.tanggal_rilis AS "Tanggal Rilis",
                S.total_play AS "Total Play"
            FROM SONG S
            JOIN KONTEN K ON S.id_konten = K.id
            JOIN ARTIST AR ON S.id_artist = AR.id
            JOIN AKUN AK ON AR.email_akun = AK.email
            JOIN PLAYLIST_SONG PS ON PS.id_song = S.id_konten
            JOIN CHART CH ON CH.id_playlist = PS.id_playlist 
            WHERE PS.id_playlist = '002e4567-e89b-12d3-a456-426614174001'
            ORDER BY S.total_play DESC
            LIMIT 20;
        """)  # Convert UUID to string if necessary
        weekly_top = cursor.fetchall()

    if not weekly_top:
        return render(request, 'error.html', {'message': 'Chart not found'})

    print("Chart Details fetched:", weekly_top)  # Check what data is fetched from the database

    context = {
        'weekly_top': [
            {'id': song[0], 'judul': song[1], 'artist': song[2], 'tanggal_rilis': song[3], 'total_play': song[4]}
            for song in weekly_top
        ],
    }

    return render(request, 'weekly_top.html', context)

def monthly_top(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT S.id_konten AS "Song ID",
                K.judul AS "Judul",
                AK.nama AS "Artist",
                K.tanggal_rilis AS "Tanggal Rilis",
                S.total_play AS "Total Play"
            FROM SONG S
            JOIN KONTEN K ON S.id_konten = K.id
            JOIN ARTIST AR ON S.id_artist = AR.id
            JOIN AKUN AK ON AR.email_akun = AK.email
            JOIN PLAYLIST_SONG PS ON PS.id_song = S.id_konten
            JOIN CHART CH ON CH.id_playlist = PS.id_playlist 
            WHERE PS.id_playlist = '003e4567-e89b-12d3-a456-426614174002'
            ORDER BY S.total_play DESC
            LIMIT 20;
        """)  # Convert UUID to string if necessary
        monthly_top = cursor.fetchall()

    if not monthly_top:
        return render(request, 'error.html', {'message': 'Chart not found'})

    print("Chart Details fetched:", monthly_top)  # Check what data is fetched from the database

    context = {
        'monthly_top': [
            {'id': song[0], 'judul': song[1], 'artist': song[2], 'tanggal_rilis': song[3], 'total_play': song[4]}
            for song in monthly_top
        ],
    }

    return render(request, 'monthly_top.html', context)

def yearly_top(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT S.id_konten AS "Song ID",
                K.judul AS "Judul",
                AK.nama AS "Artist",
                K.tanggal_rilis AS "Tanggal Rilis",
                S.total_play AS "Total Play"
            FROM SONG S
            JOIN KONTEN K ON S.id_konten = K.id
            JOIN ARTIST AR ON S.id_artist = AR.id
            JOIN AKUN AK ON AR.email_akun = AK.email
            JOIN PLAYLIST_SONG PS ON PS.id_song = S.id_konten
            JOIN CHART CH ON CH.id_playlist = PS.id_playlist 
            WHERE PS.id_playlist = '004e4567-e89b-12d3-a456-426614174003'
            ORDER BY S.total_play DESC
            LIMIT 20;
        """)  # Convert UUID to string if necessary
        yearly_top = cursor.fetchall()

    if not yearly_top:
        return render(request, 'error.html', {'message': 'Chart not found'})

    print("Chart Details fetched:", yearly_top)  # Check what data is fetched from the database

    context = {
        'yearly_top': [
            {'id': song[0], 'judul': song[1], 'artist': song[2], 'tanggal_rilis': song[3], 'total_play': song[4]}
            for song in yearly_top
        ],
    }

    return render(request, 'yearly_top.html', context)