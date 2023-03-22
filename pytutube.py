from pytube import Channel

# c = Channel('https://www.youtube.com/c/ProgrammingKnowledge')
c = Channel("https://www.youtube.com/@Max_Katz")
print(f"Downloading videos by: {c.channel_name}")
