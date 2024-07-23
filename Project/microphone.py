from scipy.io.wavfile import write
import sounddevice as sd
import os,sys,zipfile,math

microphone_time = 60
base_audio_name = "audio"

number_of_iterations = int(sys.argv[1])

def microphone():
    fs = 44100
    total_seconds = microphone_time * number_of_iterations
    print("Microphone function executed")
    print(f"Total recording time: {total_seconds} seconds")

    num_recordings = math.ceil(total_seconds / (2 * 60)) 
    count=num_recordings

    print("ceill :",num_recordings)
    for i in range(num_recordings):
        audio_filename = f"{base_audio_name}{i + 1}.wav"

        if(count==1):
            ts=total_seconds
        else:
            ts=120
            total_seconds-=120
            count-=1
            
        print(f"Recording {i + 1}: {ts} seconds...")
        myrecording = sd.rec(int(ts * fs), samplerate=fs, channels=2)
        sd.wait()
        
        write(audio_filename, fs, myrecording)
        print(f"Saved {audio_filename}")

        zip_filename = f"{base_audio_name}{i + 1}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(audio_filename, os.path.basename(audio_filename))
        print(f"Created ZIP file {zip_filename}")

        os.remove(audio_filename)
        print(f"Deleted original file {audio_filename}")

    print("Microphone function completed")

microphone()