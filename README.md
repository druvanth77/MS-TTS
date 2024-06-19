# MS-TTS

## Overview
This document guides you to generate meditation audio files using Microsoft Azure Cognitive Services Text-to-Speech API. The generated audio includes random pauses to simulate a natural speaking style, and different configurations are used to vary the voice style, role, and style degree.

## Prerequisites
- Python 3.x
- `requests` library
- `pydub` library
- Azure Cognitive Services Text-to-Speech API subscription key

## Installation
Install the required Python libraries:
```bash
pip install requests pydub
```
Ensure you have an Azure Cognitive Services subscription key. Replace the placeholder `subscription_key` in the code with your actual subscription key.

## Configuration
### Styles
The following styles are used to generate the audio:
- calm
- gentle
- hopeful
### Roles
The following roles are used:
- SeniorFemale
- OlderAdultFemale
### Style Degree
The `styledegree` parameter controls the intensity of the speaking style. Accepted values range from 0.01 to 2, with 1 being the default intensity.
### Random Pauses
Random pauses are inserted into the SSML using the `<break>` tag. The duration of these pauses is randomly chosen between 3 to 10 seconds.
### SSML Templates
The SSML (Speech Synthesis Markup Language) templates define the text and structure of the speech, including pauses and prosody adjustments. Each template is formatted to include placeholders for the style, style degree, role, and pause.
### Example SSML Template
```bash
<speak version='1.0' xml:lang='en-US'>
  <voice xml:lang='en-US' xml:gender='Female' name='en-US-AmberNeural' style='{style}' styledegree='{styledegree}' role='{role}'>
    <prosody rate="-20%" pitch="-10%">
        <p>
          <s>Find a comfortable seated position, either in a chair with your feet flat on the floor or sitting cross-legged on a cushion.</s>
          {pause}
          <s>Allow your hands to rest gently on your knees or in your lap.</s>
          {pause}
          <s>Close your eyes if you feel comfortable, or softly gaze at a point in front of you.</s>
          {pause}
          <s>Take a few deep breaths, inhaling through your nose and exhaling through your mouth.</s>
          {pause}
          <s>Let your breath return to its natural rhythm.</s>
          {pause}
        </p>
      </prosody>
  </voice>
</speak>
```
## Notes
- Ensure that the SSML templates are correctly formatted.
- The Azure Text-to-Speech API has limits on the length and complexity of the SSML, so test with shorter templates if you encounter issues.
- That's why we split the SSML text into multiple segments, generate the audio files for each segment, and then combine them.
- The `pydub` library is used to concatenate audio segments and export them as WAV files.
- For the complete code, refer to the Python file in the GitHub repository.


