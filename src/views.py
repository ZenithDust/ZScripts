from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import date, timedelta, datetime
from flask_login import login_user, login_required, logout_user
import json
import os

from .functions import time_ago_filter, get_video_stats, sgTime
keylog = os.environ['adminKey']

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

@views.route('/scripts', methods=['GET', 'POST'])
def scripts():
  
  if request.method == 'POST':
    form = request.form
    
    session['scriptDataInfo'] = form
    
    scData = session.get('scriptDataInfo', None)
    
    scName = scData['sName']
    
    return redirect(url_for('views.script', scriptData=scName))
  
  with open('scripts.json') as scriptFile:
    data = json.load(scriptFile)
    scripts = data['scripts']
    
  apiKey = os.environ['YTKey']
  video_stats = []
  
  for script in scripts:
    year, month, day, hour, minute = map(int, script['dateTime'])
    year2, month2, day2 = map(int, script['newDate'])
    timestamp = datetime(year, month, day, hour, minute)
    time_ago = time_ago_filter(timestamp)
    time_ago2 = sgTime(year2, month2, day2)
    script['timeAgo'] = time_ago
    
    session['timeAge'] = time_ago2
    
    youtubeURL = script['videoURL']
    stats = get_video_stats([youtubeURL], apiKey)
    
    if stats:
      video_stats.extend(stats)
    
  for stats in video_stats:
    print("URL:", stats['url'])
    print("Likes:", stats["likes"])
    print("Views:", stats["views"])
    print()
    
  return render_template('script.html', scripts=scripts, video_stats=video_stats)

@views.route('/script/<scriptData>', methods=['GET', 'POST'])
def script(scriptData):
  scDatas = session.get('scriptDataInfo', None)
  
  scTime = session.get('timeAge', None)
  
  return render_template('getScript.html', scDatas=scDatas, scTime=scTime)