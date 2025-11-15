# YouTube Video Analyzer

The YouTube Video Analyzer is an extension to the Blender MCP that provides comprehensive video analysis capabilities through the Model Context Protocol.

## Features

- **Download YouTube Videos**: Download videos in various qualities and extract metadata
- **Frame Extraction**: Extract frames at regular intervals for visual analysis
- **Audio Transcription**: Transcribe video audio using OpenAI Whisper
- **Comprehensive Analysis**: All-in-one tool that combines download, frame extraction, and transcription
- **Visual Analysis**: Return frames as MCP Image objects for Claude to analyze
- **Cache Management**: Clean up downloaded videos and frames to save disk space

## Installation

The YouTube Analyzer dependencies are included in the main `pyproject.toml`. When you install `blender-mcp`, the following packages will be installed:

- `yt-dlp` - YouTube video downloader
- `opencv-python` - Video processing and frame extraction
- `openai-whisper` - Audio transcription
- `pillow` - Image processing
- `torch` - Required for Whisper

## Available Tools

### 1. `download_youtube_video`

Download a YouTube video and extract its metadata.

**Parameters:**
- `url` (required): The YouTube video URL
- `quality` (optional): Video quality (360p, 480p, 720p, 1080p, best). Default: 720p

**Returns:** JSON with video metadata including:
- Video ID, title, duration, uploader
- View count, like count, upload date
- Video dimensions (width, height, fps)
- Local file path
- File size in MB

**Example:**
```python
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "title": "Example Video",
  "duration": 212,
  "uploader": "Example Channel",
  "upload_date": "20230101",
  "view_count": 1000000,
  "like_count": 50000,
  "width": 1280,
  "height": 720,
  "fps": 30,
  "local_path": "/tmp/blender_mcp_videos/dQw4w9WgXcQ.mp4",
  "filesize_mb": 15.3
}
```

### 2. `extract_video_frames`

Extract frames from a downloaded video at regular intervals.

**Parameters:**
- `video_path` (required): Path to the video file (from `download_youtube_video`)
- `interval_seconds` (optional): Time between frames in seconds. Default: 5.0
- `max_frames` (optional): Maximum number of frames to extract. Default: 10
- `output_format` (optional): Image format (jpg, png). Default: jpg

**Returns:** JSON with frame extraction results including:
- Video properties (duration, fps, total frames)
- List of extracted frames with timestamps and paths
- Frames directory path

**Example:**
```python
{
  "success": true,
  "video_duration": 212.5,
  "video_fps": 30.0,
  "extracted_frames_count": 10,
  "frames": [
    {
      "frame_number": 0,
      "timestamp": 0.0,
      "path": "/tmp/blender_mcp_videos/video_frames/frame_0000_t0.00s.jpg",
      "width": 1280,
      "height": 720
    },
    ...
  ]
}
```

### 3. `transcribe_video_audio`

Transcribe audio from a video file using OpenAI Whisper.

**Parameters:**
- `video_path` (required): Path to the video file
- `model_size` (optional): Whisper model size (tiny, base, small, medium, large). Default: base
- `language` (optional): Language code (en, de, es, etc.) or None for auto-detection

**Returns:** JSON with transcription results including:
- Detected language
- Full transcription text
- Timestamped segments

**Model Sizes:**
- `tiny`: Fastest, least accurate (~1GB RAM)
- `base`: Good balance (default, ~1GB RAM)
- `small`: Better accuracy (~2GB RAM)
- `medium`: High accuracy (~5GB RAM)
- `large`: Best accuracy (~10GB RAM)

**Example:**
```python
{
  "success": true,
  "detected_language": "en",
  "full_text": "This is the full transcription of the video...",
  "segments_count": 42,
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 3.5,
      "text": "Hello and welcome to this video"
    },
    ...
  ]
}
```

### 4. `analyze_youtube_video`

Comprehensive analysis combining download, frame extraction, and transcription.

**Parameters:**
- `url` (required): YouTube video URL
- `quality` (optional): Video quality. Default: 720p
- `extract_frames` (optional): Whether to extract frames. Default: true
- `frame_interval` (optional): Seconds between frames. Default: 10.0
- `max_frames` (optional): Maximum frames to extract. Default: 6
- `transcribe` (optional): Whether to transcribe audio. Default: true
- `whisper_model` (optional): Whisper model size. Default: base

**Returns:** Complete JSON analysis including metadata, frames, and transcription.

**Example:**
```python
{
  "success": true,
  "url": "https://youtube.com/watch?v=...",
  "analyzed_at": "2025-11-15T10:30:00",
  "metadata": { ... },
  "frames": { ... },
  "transcription": { ... }
}
```

### 5. `get_video_frame_as_image`

Get a video frame as an MCP Image object for Claude to analyze visually.

**Parameters:**
- `frame_path` (required): Path to the frame image (from `extract_video_frames`)

**Returns:** MCP Image object that Claude can analyze

### 6. `cleanup_video_cache`

Clean up cached video files and frames to free disk space.

**Parameters:**
- `video_id` (optional): Specific video ID to clean up. If None, cleans all cached videos.

**Returns:** Summary of deleted files and space freed

## Usage Examples

### Basic Video Analysis

```
Analyze this YouTube video: https://youtube.com/watch?v=example
```

Claude will use `analyze_youtube_video` to:
1. Download the video
2. Extract 6 frames at 10-second intervals
3. Transcribe the audio
4. Provide a comprehensive analysis

### Download Only

```
Download this YouTube video in 1080p: https://youtube.com/watch?v=example
```

### Extract Specific Frames

```
Extract 20 frames from this video at 2-second intervals: /tmp/blender_mcp_videos/video.mp4
```

### Transcribe in German

```
Transcribe this video in German using the small model: /tmp/blender_mcp_videos/video.mp4
```

### Visual Analysis of Frames

```
Extract frames from this video and show me what's happening visually
```

Claude will extract frames and use `get_video_frame_as_image` to display them for visual analysis.

## File Storage

All downloaded videos and extracted frames are stored in:
```
/tmp/blender_mcp_videos/
```

Structure:
```
/tmp/blender_mcp_videos/
├── {video_id}.mp4              # Downloaded videos
├── {video_id}_frames/          # Extracted frames
│   ├── frame_0000_t0.00s.jpg
│   ├── frame_0001_t5.00s.jpg
│   └── ...
```

Use `cleanup_video_cache` to remove cached files when done.

## Performance Tips

1. **Video Quality**: Use lower quality (360p, 480p) for faster downloads and processing
2. **Frame Extraction**: Reduce `max_frames` or increase `interval_seconds` for faster extraction
3. **Transcription**: Use smaller Whisper models (tiny, base) for faster transcription
4. **Disk Space**: Regularly clean up cache with `cleanup_video_cache`

## Limitations

- Downloaded videos are stored temporarily and should be cleaned up
- Whisper transcription can be slow on longer videos
- Large videos may require significant disk space
- Frame extraction quality depends on source video quality

## Error Handling

All tools return JSON with a `success` field. Check this field to determine if the operation succeeded:

```python
{
  "success": false,
  "error": "Video file not found: /path/to/video.mp4"
}
```

## Integration with Blender MCP

While the YouTube Analyzer is part of the Blender MCP server, it operates independently and doesn't require Blender to be running. The tools are available through the same MCP interface.

## Technical Details

- **yt-dlp**: Handles video downloading with support for various formats and qualities
- **OpenCV**: Processes video files and extracts frames efficiently
- **Whisper**: Provides state-of-the-art audio transcription with multi-language support
- **MCP Integration**: All tools are exposed through the Model Context Protocol for Claude

## Future Enhancements

Potential future features:
- Video summarization
- Scene detection and segmentation
- Object detection in frames
- Speaker diarization
- Subtitle generation
- Video editing capabilities
