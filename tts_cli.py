#!/usr/bin/env python3
"""
Terminal-based Text-to-Speech using ElevenLabs API with streaming.

Usage:
    python tts_cli.py "Your text here"
    echo "Your text here" | python tts_cli.py
"""

import os
import sys
import click
from elevenlabs import stream, save
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        click.echo("Error: ELEVENLABS_API_KEY not found in environment variables or .env file.", err=True)
        click.echo("Please create a .env file with ELEVENLABS_API_KEY=your_api_key_here")
        sys.exit(1)
    return api_key

def get_voice_id():
    """Get the default voice ID."""
    # Default to a good multilingual voice
    return "JBFqnCBsd6RMkjVDRZzb"  # Default voice ID

def text_to_speech(text, voice_id=None):
    """Convert text to speech using ElevenLabs API with streaming."""
    if not voice_id:
        voice_id = get_voice_id()
    
    try:
        # Initialize client with API key
        client = ElevenLabs(api_key=load_environment())
        
        # Generate and stream the audio
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        
        # Play the audio
        stream(audio)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@click.command()
@click.argument('text', required=False)
def main(text):
    """Simple TTS application that converts text to speech using ElevenLabs API."""
    # Get text from argument or stdin
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            click.echo("No text provided. Please provide text as an argument or via stdin.")
            click.echo("Example: tts_cli.py \"Hello, world!\"")
            sys.exit(1)
    
    if not text.strip():
        click.echo("Error: Empty text input", err=True)
        sys.exit(1)
    
    click.echo(f"Converting to speech: {text[:50]}..." if len(text) > 50 else f"Converting to speech: {text}")
    text_to_speech(text)

if __name__ == "__main__":
    main()
