#Full audio files with random pauses

import requests
from IPython.display import Audio, display
from pydub import AudioSegment
from io import BytesIO
import random

subscription_key = '******private key*******'

def get_token(subscription_key):
    fetch_token_url = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    return response.text


def generate_random_pause():
    return f'<break time="{random.randint(3, 10)}s"/>'



ssml_templates = [
    """
    <speak version='1.0' xml:lang='en-US'>
      <voice xml:lang='en-US' xml:gender='Female' name='en-US-SaraNeural'>
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

            <p>
              <s>Begin by bringing your attention to the sounds around you.</s>
              {pause}
              <s>Notice the most obvious sounds first – the hum of an appliance, the chirping of birds, distant traffic, or the rustle of leaves.</s>
              {pause}
              <s>Allow yourself to simply listen without judgment or analysis.</s>
              {pause}
              <s>If a thought arises, acknowledge it, and gently bring your focus back to the sounds.</s>
              {pause}
              <s>Take a moment to notice the more subtle sounds – perhaps your own breath, the faint ticking of a clock, or the gentle creak of furniture.</s>
              {pause}
              <s>Let yourself be fully immersed in the symphony of your environment.</s>
              {pause}
            </p>
          </prosody>
      </voice>
    </speak>
    """,
    """
    <speak version='1.0' xml:lang='en-US'>
      <voice xml:lang='en-US' xml:gender='Female' name='en-US-SaraNeural'>
        <prosody rate="-20%" pitch="-10%">
            <p>
              <s>Now, gently shift your attention to your sense of smell.</s>
              {pause}
              <s>Take a deep breath in through your nose and notice any scents in the air.</s>
              {pause}
              <s>Is there a lingering aroma of food, the fresh scent of nature, or perhaps a subtle fragrance from a nearby candle or essential oil?</s>
              {pause}
              <s>If you don’t notice any particular smell, that’s perfectly okay.</s>
              {pause}
              <s>Just be present with the act of breathing and the sensation of air moving through your nostrils.</s>
              {pause}
            </p>
        
            <p>
              <s>Next, bring your awareness to your sense of taste.</s>
              {pause}
              <s>You might notice any lingering taste in your mouth from a recent meal or drink.</s>
              {pause}
              <s>Run your tongue over your teeth and the roof of your mouth, observing any subtle flavors or sensations.</s>
              {pause}
              <s>If you have a sip of water or a piece of fruit nearby, you can take a moment to taste it mindfully, noticing the texture, temperature, and flavor.</s>
              {pause}
            </p>
          </prosody>
      </voice>
    </speak>
    """,
    """
    <speak version='1.0' xml:lang='en-US'>
      <voice xml:lang='en-US' xml:gender='Female' name='en-US-SaraNeural'>
        <prosody rate="-20%" pitch="-10%">
           <p>
              <s>Now, direct your focus to your sense of touch.</s>
              {pause}
              <s>Start by noticing the points of contact between your body and the surface you are sitting on.</s>
              {pause}
              <s>Feel the ground beneath your feet, the chair or cushion supporting you.</s>
              {pause}
              <s>Bring your attention to your hands.</s>
              {pause}
              <s>Notice the texture of your clothing against your skin or the temperature of the air on your hands.</s>
              {pause}
              <s>Take a moment to feel the weight of your body, the gentle rise and fall of your chest with each breath.</s>
              {pause}
              <s>Notice any areas of tension or relaxation, and simply observe these sensations without trying to change them.</s>
              {pause}
            </p>
        
            <p>
              <s>Take a few more moments to sit with all these sensations – the sounds, the smells, the tastes, and the touches.</s>
              {pause}
              <s>Allow yourself to be fully present in this moment, grounded and connected with your surroundings.</s>
              {pause}
              <s>When you are ready, gently bring your awareness back to your breath.</s>
              {pause}
              <s>Take a deep inhale through your nose, and exhale slowly through your mouth.</s>
              {pause}
              <s>Slowly open your eyes, bringing this sense of mindfulness and grounding with you as you continue with your day.</s>
              {pause}
              <s>Remember, you can return to this practice whenever you feel the need to reconnect with the present moment.</s>
              {pause}
              <s>Take your time, and be kind to yourself.</s>
              {pause}
              <s>You are doing wonderfully.</s>
              {pause}
            </p>
          </prosody>
      </voice>
    </speak>
    """
    
]

ssml_segments = [template.format(pause=generate_random_pause()) for template in ssml_templates]

def generate_speech(segment, token):
    endpoint = 'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm'
    }
    response = requests.post(endpoint, headers=headers, data=segment)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

token = get_token(subscription_key)
if token:
    audio_segments = []
    for segment in ssml_segments:
        audio_content = generate_speech(segment, token)
        if audio_content:
            audio_segments.append(AudioSegment.from_file(BytesIO(audio_content), format="wav"))

    combined = AudioSegment.empty()
    for segment in audio_segments:
        combined += segment

    combined.export("SaraNeural(-20, -10, full).wav", format="wav")

    audio_buffer = BytesIO()
    combined.export(audio_buffer, format="wav")
    audio_buffer.seek(0)
    
    display(Audio(audio_buffer.read(), autoplay=False))
