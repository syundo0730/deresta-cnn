from viewer import GameViewer
import os


VIDEO_PATH = os.path.join(os.path.dirname(__file__), '../../data/scraped_data/video/cu_anzu_master.mp4')
NOTE_PATH = os.path.join(os.path.dirname(__file__), '../../data/scraped_data/note/song_3007_Master.json')
viewer = GameViewer(VIDEO_PATH, NOTE_PATH)
viewer.start()
