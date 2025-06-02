#!/usr/bin/env python3
"""
Voice-enabled Chatbot using Gemini AI and ElevenLabs TTS & STT.

Usage:
    python chatbot.py [--voice]

Options:
    --voice  Enable voice input mode
"""

import os
import click
import google.generativeai as genai
from elevenlabs import stream, save
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from stt_utils import listen_for_speech

def load_environment():
    """Load environment variables."""
    load_dotenv()
    
    # Load API keys
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not elevenlabs_key or not gemini_key:
        print("Error: Please ensure both ELEVENLABS_API_KEY and GEMINI_API_KEY are set in .env file")
        exit(1)
        
    return elevenlabs_key, gemini_key

def initialize_apis(elevenlabs_key, gemini_key):
    """Initialize the AI APIs."""
    # Initialize ElevenLabs
    tts_client = ElevenLabs(api_key=elevenlabs_key)
    
    # Configure Gemini
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    return tts_client, model

def get_voice_id():
    """Get a cheerful and clear voice ID."""
    # より明るくハキハキとした声のIDに変更
    return "EXAVITQu4vr4xnSDxMaL"  # 明るくハキハキとした女性の声

def generate_response(chat, user_input):
    """Generate a response using Gemini."""
    try:
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"申し訳ありませんが、エラーが発生しました: {str(e)}"

def text_to_speech(tts_client, text, voice_id=None):
    """Convert text to speech using ElevenLabs with a cheerful and clear voice."""
    if not voice_id:
        voice_id = get_voice_id()
    
    try:
        # Generate and stream the audio with voice settings
        audio = tts_client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            voice_settings={
                "stability": 0.5,        # 声の安定性（0-1、低いほど感情豊かに）
                "similarity_boost": 0.9,  # 声の類似度（0-1、高いほど一貫性のある声に）
                "style": 0.7,             # 話し方のスタイル（0-1、高いほど表現豊かに）
                "use_speaker_boost": True  # 声をよりクリアにする
            }
        )
        
        # Play the audio
        stream(audio)
        
    except Exception as e:
        print(f"音声再生エラー: {str(e)}")

def chat_loop(tts_client, chat, elevenlabs_key, use_voice=False):
    """Main chat loop."""
    if use_voice:
        print("\n音声入力モードが有効です。Ctrl+Cで終了します。")
    else:
        print("\nテキスト入力モードです。'終了'と入力するか、Ctrl+Cで終了します。")
    
    while True:
        try:
            if use_voice:
                # 音声入力を待機
                print("\n録音ボタンを押して話してください... (5秒間)")
                input("Enterキーを押して録音を開始...")
                user_input = listen_for_speech(elevenlabs_key)  # APIキーを直接渡す
                if not user_input:
                    print("もう一度お試しください。")
                    continue
            else:
                # テキスト入力を取得
                user_input = input("\nあなた: ")
                
                # 終了コマンドをチェック
                if user_input.lower() in ['exit', 'quit', '終了', 'さようなら']:
                    print("チャットを終了します。")
                    break
            
            # 応答を生成
            print("考え中...")
            response = generate_response(chat, user_input)
            
            # 応答を表示して読み上げ
            print(f"\nアシスタント: {response}")
            text_to_speech(tts_client, response)
            
        except KeyboardInterrupt:
            print("\nチャットを終了します。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")

def main():
    """Main function to run the chatbot."""
    # Load API keys and initialize clients
    elevenlabs_key, gemini_key = load_environment()
    tts_client, model = initialize_apis(elevenlabs_key, gemini_key)
    
    # Start a chat session
    chat = model.start_chat(history=[])
    
    # Check for voice mode
    import sys
    use_voice = '--voice' in sys.argv
    
    # Start the chat loop
    chat_loop(tts_client, chat, elevenlabs_key, use_voice=use_voice)

if __name__ == "__main__":
    main()
