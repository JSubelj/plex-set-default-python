#!/usr/bin/env python3


from plexapi.server import PlexServer
from dotenv import load_dotenv
import os

load_dotenv()

AUDIO="audio"
SUBTITLE="subtitle"

baseurl = os.getenv('PLEX_URL')
# token can be get by inspecting traffic from plex and searchin for X-Plex-Token in url
token = os.getenv('TOKEN')
plex = PlexServer(baseurl, token)

section="Series"
series_name=None

def main():
    global section
    global series_name

    sections = [s.title for s in plex.library.sections()]
    [print(f"{c}. {s}") for c,s in enumerate(sections)]
    section_input_inx = int(input(f"Select section [{sections.index('Series')}]: "))
    if section_input_inx:
        section = sections[section_input_inx]
    print(f"Section: {section}")
    print()

    series_name_input = input("Series name: ")
    while not series_name_input:
        series_name_input = input("Series name: ")
    series_name=series_name_input
    print(f"Series name: {series_name}")
    print()

    num_of_seasons = len(plex.library.section(section).get(series_name).seasons())

    for season_num in range(num_of_seasons):
        no_of_ep = len(plex.library.section(section).get(series_name).seasons()[season_num].episodes())
        skip = input(f"Want to skip season {season_num+1}? [y/N] ")
        if str(skip).lower() == 'y':
            continue

        print(f"Choosing for season {season_num+1}. ({no_of_ep} episodes) - subtitles")
        print()
        changeStreamForSeason(season_num, SUBTITLE)
        print(f"Choosing for season {season_num+1}. ({no_of_ep} episodes) - audio")
        print()
        changeStreamForSeason(season_num, AUDIO)


def getStreamString(s):
    language = s.language if s.language else ""
    name = f"{s.title}/{language}"
    name = f"{s.displayTitle}/{language}" if s.displayTitle else name
    name = f"{s.extendedDisplayTitle}/{language}" if s.extendedDisplayTitle else name
    return name

def getStreamsFromEpisode(e, s_type):
    return e.subtitleStreams() if s_type == SUBTITLE else e.audioStreams()

def getAllTypedStreamsFromEveryEpisodeSeason(season_num,s_type):
    stream_ids = {}
    episodes_with_streams = {}
    for c,e in enumerate(plex.library.section(section).get(series_name).seasons()[season_num].episodes()):
        e.reload()
        streams_string=[getStreamString(s) for s in getStreamsFromEpisode(e,s_type)]
        ident = ",".join(streams_string)
        if ident not in stream_ids.keys():
            stream_ids[ident] = streams_string
        if ident not in episodes_with_streams.keys():
            episodes_with_streams[ident] = [c]
        else:
            episodes_with_streams[ident].append(c)
    return [(episodes_with_streams[ident], stream_ids[ident]) for ident in stream_ids.keys()]

def printStreamsForEpisodes(episodes_nums, streams, s_type):
    print(f"Select {s_type} for episodes: {','.join([str(e+1) for e in episodes_nums])}")
    [print(f"{c}. {s}") for c,s in enumerate(streams)]

def changeStreamForSeason(season_num, s_type):
    stream_sets = getAllTypedStreamsFromEveryEpisodeSeason(season_num,s_type)
    for ep_nums, stream_strings in stream_sets:
        printStreamsForEpisodes(ep_nums,stream_strings, s_type)
        selected_stream_inx = int(input(f"Enter number of {s_type}: "))
        print(f"Selected {s_type}: ",stream_strings[selected_stream_inx])
        print()
        for ep_inx in ep_nums:
            applySelectedStream(season_num,ep_inx,selected_stream_inx,s_type)
    
def applySelectedStream(season_num, episode_num, index, s_type):
    e = plex.library.section(section).get(series_name).seasons()[season_num].episodes()[episode_num]
    e.reload()
    if s_type == SUBTITLE:
        e.media[0].parts[0].setDefaultSubtitleStream(e.subtitleStreams()[index].id)
    else:
        e.media[0].parts[0].setDefaultAudioStream(e.audioStreams()[index].id)


main()




