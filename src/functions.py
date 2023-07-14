from datetime import date, timedelta, datetime
import requests
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

def sgTime(year, month, day):
    dateobj = date(year, month, day)
    datetimeobj = datetime.combine(dateobj, datetime.min.time())
    formatted = dateobj.strftime("%B, %d , %Y")
    
    return formatted

def time_ago_filter(timestamp):
        now = datetime.now()
        diff = now - timestamp
    
        if diff < timedelta(seconds=60):
            return 'just now'
        elif diff < timedelta(minutes=60):
            minutes = int(diff.total_seconds() / 60)
            if minutes > 1:
              return f'{minutes}ms ago'
            else:
              return f'{minutes}m ago'
        elif diff < timedelta(hours=24):
            hours = int(diff.total_seconds() / 3600)
            if hours > 1:
              return f'{hours}hs ago'
            else:
              return f'{hours}h ago'
        elif diff < timedelta(days=7):
            days = diff.days
            if days > 1:
              return f'{days}ds ago'
            else:
              return f'{days}d ago'
        elif diff < timedelta(days=30):
            weeks = int(diff.days / 7)
            if weeks > 1:
              return f'{weeks}ws ago'
            else:
              return f'{weeks}w ago'
        elif diff < timedelta(days=365):
            months = int(diff.days / 30)
            if months > 1:
              return f'{months}mos ago'
            else:
              return f'{months}mo ago'
        else:
            years = int(diff.days / 365)
            if years > 1:
              return f'{years}yrs ago'
            else:
              return f'{years}yr ago'

def get_video_stats(video_urls, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    video_stats = []

    for video_url in video_urls:
        parsed_url = urlparse(video_url)
        video_id = None

        if "youtube.com" in parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)
            if "v" in query_params:
                video_id = query_params["v"][0]
        elif "youtu.be" in parsed_url.netloc:
            video_id = parsed_url.path[1:]

        if video_id:
            response = youtube.videos().list(part="statistics", id=video_id).execute()

            if "items" in response and len(response["items"]) > 0:
                stats = response["items"][0]["statistics"]
                likes = stats.get("likeCount", 0)
                views = stats.get("viewCount", 0)
                video_stats.append({"url": video_url, "likes": likes, "views": views})
            else:
                print("No statistics found for video: ", video_url)
        else:
            print("Invalid Url: ", video_url)

    return video_stats