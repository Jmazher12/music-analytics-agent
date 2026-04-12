# Spotify Audio Features Guide

## Danceability
Measures how suitable a track is for dancing based on tempo, rhythm stability, beat strength, and overall regularity. Ranges from 0.0 (least danceable) to 1.0 (most danceable). Tracks above 0.7 are generally considered highly danceable.

## Energy
Represents the intensity and activity of a track. Ranges from 0.0 to 1.0. High-energy tracks feel fast, loud, and noisy (e.g., death metal), while low-energy tracks feel calm and quiet (e.g., a Bach prelude). Perceptual features contributing to energy include dynamic range, perceived loudness, timbre, onset rate, and general entropy.

## Valence
Describes the musical positiveness of a track. Ranges from 0.0 to 1.0. High valence tracks sound happy, cheerful, or euphoric. Low valence tracks sound sad, depressed, or angry.

## Tempo
The estimated tempo of a track in beats per minute (BPM). Typical ranges: slow ballads (60-80 BPM), pop songs (100-130 BPM), dance/EDM (120-150 BPM), drum and bass (160-180 BPM).

## Loudness
The overall loudness of a track in decibels (dB). Values typically range from -60 to 0 dB. Loudness is averaged across the entire track and is useful for comparing relative loudness of tracks.

## Speechiness
Detects the presence of spoken words in a track. Values above 0.66 indicate tracks that are probably entirely spoken words (podcasts, audiobooks). Values between 0.33 and 0.66 may contain both music and speech (e.g., rap). Values below 0.33 most likely represent instrumental music or singing.

## Acousticness
A confidence measure from 0.0 to 1.0 of whether the track is acoustic. A value of 1.0 represents high confidence the track is acoustic. Acoustic tracks lack electronic amplification.

## Instrumentalness
Predicts whether a track contains no vocals. Values closer to 1.0 indicate a greater likelihood the track has no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence increases as the value approaches 1.0.

## Liveness
Detects the presence of an audience in the recording. Higher values represent an increased probability the track was performed live. A value above 0.8 provides strong likelihood the track is live.

## Key
The key the track is in. Integers map to pitches using standard pitch class notation: 0 = C, 1 = C♯/D♭, 2 = D, 3 = D♯/E♭, 4 = E, 5 = F, 6 = F♯/G♭, 7 = G, 8 = G♯/A♭, 9 = A, 10 = A♯/B♭, 11 = B. A value of -1 means no key was detected.

## Mode
Indicates the modality (major or minor) of a track. Major is represented by 1 and minor by 0. Major keys tend to sound brighter and happier, while minor keys sound darker and more melancholic.

## Time Signature
An estimated time signature. Indicates how many beats are in each bar. Most common value is 4 (representing 4/4 time).

## Popularity
A score between 0 and 100, with 100 being the most popular. Popularity is calculated by Spotify's algorithm based primarily on the total number of plays and how recent those plays are. Tracks being played frequently right now will have higher popularity than tracks played heavily in the past.

## Duration
The duration of the track in milliseconds. To convert to minutes, divide by 60,000. The average pop song is about 3-4 minutes (180,000 - 240,000 ms).

## Explicit
Whether or not the track has explicit lyrics. True indicates the track contains explicit content, False indicates it does not (or that the information is unknown).