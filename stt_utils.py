"""
Utility functions for Speech-to-Text using ElevenLabs API.
"""

import os
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

def record_audio(duration=5, sample_rate=16000):
    """
    Record audio from the microphone.
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Sample rate in Hz
        
    Returns:
        tuple: (audio_data, sample_rate)
    """
    print(f"\n録音中... {duration}秒間話してください")
    
    # 音声を録音
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )
    sd.wait()  # 録音が終了するまで待機
    
    return audio.flatten(), sample_rate

def save_temp_audio(audio_data, sample_rate):
    """
    Save audio data to a temporary WAV file.
    
    Args:
        audio_data: Audio data as numpy array
        sample_rate: Sample rate in Hz
        
    Returns:
        str: Path to the temporary audio file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    sf.write(temp_file.name, audio_data, sample_rate, format='WAV')
    return temp_file.name

def transcribe_audio(api_key, audio_file_path):
    """
    Transcribe audio using ElevenLabs Speech-to-Text API.
    
    Args:
        api_key: ElevenLabs API key
        audio_file_path: Path to the audio file to transcribe
        
    Returns:
        str: Transcribed text
    """
    client = ElevenLabs(api_key=api_key)
    
    try:
        with open(audio_file_path, 'rb') as audio_file:
            response = client.speech_to_text.convert(
                model_id="scribe_v1",
                file=audio_file,
                language_code="ja",  # 日本語を指定
                diarize=False
            )
            
        return response.text.strip()
    except Exception as e:
        print(f"文字起こしエラー: {str(e)}")
        return ""

def listen_for_speech(api_key, duration=5):
    """
    Listen for speech and return the transcribed text.
    
    Args:
        api_key: ElevenLabs API key
        duration: Maximum recording duration in seconds
        
    Returns:
        str: Transcribed text or empty string if no speech detected
    """
    # 音声を録音
    audio_data, sample_rate = record_audio(duration=duration)
    
    # 無音を検出してトリミング
    silence_threshold = 100  # 無音とみなす閾値
    audio_trimmed = audio_data[np.abs(audio_data) > silence_threshold]
    
    # 無音が長すぎる場合は何も発話されなかったと判断
    if len(audio_trimmed) < sample_rate * 0.5:  # 0.5秒以下の音声は無視
        print("音声が検出されませんでした")
        return ""
    
    # 一時ファイルに保存
    temp_file = save_temp_audio(audio_trimmed, sample_rate)
    
    try:
        # 文字起こし
        text = transcribe_audio(api_key, temp_file)
        print(f"認識されたテキスト: {text}")
        return text
    finally:
        # 一時ファイルを削除
        try:
            os.unlink(temp_file)
        except:
            pass
