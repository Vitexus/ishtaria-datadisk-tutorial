#!/usr/bin/env python3
"""Render spoken lines for the tutorial datadisk using Piper TTS.

Usage:
    python3 tools/render_voices.py --out /path/to/output --jobs N [--lang en|cs] [--only CHARACTER]
"""

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Character to voice model mapping
VOICE_MODELS = {
    "en": {
        "alara": {"model": "en_US-libritts_r-medium", "pitch": 1.0, "speed": 1.0},
        "crafton": {"model": "en_US-libritts_r-medium", "pitch": 0.9, "speed": 0.95},
        "valerian": {"model": "en_US-libritts_r-medium", "pitch": 0.85, "speed": 0.9},
        "hammerin": {"model": "en_US-libritts_r-medium", "pitch": 0.95, "speed": 0.9},
        "merchan": {"model": "en_US-libritts_r-medium", "pitch": 1.05, "speed": 1.0},
        "arcanis": {"model": "en_US-libritts_r-medium", "pitch": 1.1, "speed": 1.05},
        "portalus": {"model": "en_US-libritts_r-medium", "pitch": 0.9, "speed": 0.85},
        "tutorial_merchant": {"model": "en_US-libritts_r-medium", "pitch": 1.0, "speed": 1.1},
        "practice_wolf": {"model": "en_US-libritts_r-medium", "pitch": 0.8, "speed": 1.2},
        "practice_bear": {"model": "en_US-libritts_r-medium", "pitch": 0.75, "speed": 0.95},
    },
    "cs": {
        "alara": {"model": "cs_CZ-jirka-medium", "pitch": 1.0, "speed": 1.0},
        "crafton": {"model": "cs_CZ-jirka-medium", "pitch": 0.95, "speed": 0.95},
        "valerian": {"model": "cs_CZ-jirka-medium", "pitch": 0.9, "speed": 0.9},
        "hammerin": {"model": "cs_CZ-jirka-medium", "pitch": 0.95, "speed": 1.0},
        "merchan": {"model": "cs_CZ-jirka-medium", "pitch": 1.0, "speed": 1.05},
        "arcanis": {"model": "cs_CZ-jirka-medium", "pitch": 1.05, "speed": 1.0},
        "portalus": {"model": "cs_CZ-jirka-medium", "pitch": 0.95, "speed": 0.9},
        "tutorial_merchant": {"model": "cs_CZ-jirka-medium", "pitch": 1.0, "speed": 1.05},
    }
}


def load_i18n(lang: str, i18n_dir: Path) -> dict:
    """Load i18n file for a language."""
    i18n_file = i18n_dir / f"{lang}.yaml"
    if not i18n_file.exists():
        return {}
    
    import yaml
    with open(i18n_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_dialogues(dialogues_dir: Path) -> list:
    """Load all dialogue files."""
    dialogues = []
    for yaml_file in dialogues_dir.glob("*.yaml"):
        import yaml
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data and isinstance(data, dict):
                dialogues.append(data)
    return dialogues


def extract_text_keys(dialogues: list, i18n: dict) -> list:
    """Extract all text keys from dialogues that exist in i18n."""
    text_keys = []
    for dialogue in dialogues:
        dialogue_id = dialogue.get('id', '')
        nodes = dialogue.get('nodes', {})
        
        for node_id, node in nodes.items():
            text_key = node.get('text_key')
            if text_key and text_key in i18n:
                text_keys.append((dialogue_id, node_id, text_key, i18n[text_key]))
    
    return text_keys


def render_line(text: str, model: str, pitch: float, speed: float, output_path: Path) -> bool:
    """Render a single line using Piper TTS."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'piper',
            '--model', model,
            '--pitch', str(pitch),
            '--speed', str(speed),
            '--output_file', str(output_path),
            '--',
            text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"Error rendering: {result.stderr}", file=sys.stderr)
            return False
        
        # Convert WAV to OGG
        ogg_path = output_path.with_suffix('.ogg')
        subprocess.run([
            'ffmpeg', '-y', '-i', str(output_path),
            '-c:a', 'libvorbis', '-q:a', '5',
            str(ogg_path)
        ], capture_output=True, timeout=30)
        
        output_path.unlink(missing_ok=True)
        return ogg_path.exists()
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def process_text_key(dialogue_id: str, node_id: str, text_key: str, text: str, 
                     character: str, lang: str, models: dict, output_base: Path) -> bool:
    """Process a single text key and render it."""
    char_config = models.get(character, models.get('tutorial_merchant', {}))
    model_name = char_config.get('model', f'{lang}_US-libritts_r-medium')
    pitch = char_config.get('pitch', 1.0)
    speed = char_config.get('speed', 1.0)
    
    # Determine character name from dialogue_id
    char_name = dialogue_id.replace('_intro', '').replace('_demo', '')
    char_name = char_name if char_name in models else 'tutorial_merchant'
    
    # Create output path: media/voice/{lang}/{text_key}.ogg
    output_dir = output_base / lang
    output_path = output_dir / f"{text_key}.wav"
    
    # Render with character-specific voice
    success = render_line(text, model_name, pitch, speed, output_path)
    
    if success:
        print(f"  Rendered: {text_key}")
    else:
        print(f"  Failed: {text_key}")
    
    return success


def main():
    parser = argparse.ArgumentParser(description='Render voice lines for tutorial datadisk')
    parser.add_argument('--out', type=Path, required=True, help='Output directory for voices')
    parser.add_argument('--jobs', type=int, default=4, help='Number of parallel jobs')
    parser.add_argument('--lang', type=str, default=None, 
                       choices=['en', 'cs'], help='Language to render (default: all)')
    parser.add_argument('--only', type=str, default=None, 
                       help='Only render for specific character')
    parser.add_argument('--skip-existing', action='store_true', 
                       help='Skip files that already exist')
    args = parser.parse_args()
    
    # Create output directory structure
    args.out.mkdir(parents=True, exist_ok=True)
    
    languages = [args.lang] if args.lang else ['en', 'cs']
    
    for lang in languages:
        print(f"\nRendering {lang.upper()} voices...")
        
        # Load i18n
        i18n_dir = Path('i18n')
        i18n = load_i18n(lang, i18n_dir)
        
        if not i18n:
            print(f"  No i18n file found for {lang}")
            continue
        
        # Load dialogues
        dialogues_dir = Path('dialogues')
        dialogues = load_dialogues(dialogues_dir)
        
        # Extract text keys
        text_keys = extract_text_keys(dialogues, i18n)
        
        if not text_keys:
            print(f"  No text keys to render for {lang}")
            continue
        
        # Filter by character if specified
        if args.only:
            text_keys = [(d, n, k, t) for d, n, k, t in text_keys if args.only in k]
        
        print(f"  Found {len(text_keys)} text keys to render")
        
        # Process in parallel
        models = VOICE_MODELS.get(lang, {})
        output_base = args.out / 'media' / 'voice'
        
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = []
            for dialogue_id, node_id, text_key, text in text_keys:
                # Map dialogue_id to character
                character = dialogue_id
                if character.endswith('_intro'):
                    character = character[:-6]
                elif character.endswith('_demo'):
                    character = character[:-5]
                
                # Only render for specified character if --only
                if args.only and character != args.only:
                    continue
                
                # Skip if already exists
                ogg_path = output_base / lang / f"{text_key}.ogg"
                if args.skip_existing and ogg_path.exists():
                    print(f"  Skipped (exists): {text_key}")
                    continue
                
                futures.append(executor.submit(
                    process_text_key, dialogue_id, node_id, text_key, text,
                    character, lang, models, output_base
                ))
            
            for future in as_completed(futures):
                future.result()
        
        print(f"  {lang.upper()} voices complete!")


if __name__ == '__main__':
    main()
