<h1>Lykoris - AI VTuber Assistant</h1>
<p>Local, voice-controlled, and animated AI companion connected directly to VTube Studio</p>

<h2>Project description</h2>
<p>This project:</p>
<ol>
  <li>Loads a local AI language model (Llama-3 via Unsloth).</li>
  <li>
    <dl>
      <dt>Interacts in two ways:</dt>
      <dd>Text mode (<b>Keyboard input</b>)</dd>
      <dd>Voice mode (<b>Microphone via Speech-to-Text</b>)</dd>
    </dl>
  </li>
  <li>Generates voice responses using Edge-TTS.</li>
  <li>Synchronizes lip movements with a VTube Studio avatar using audio volume.</li>
  <li>Remembers personal notes using a local text file for long-term memory.</li>
</ol>

<h2>Project files</h2>
<table>
  <tr>
    <th colspan="2">ai-vtuber-assistant</th>
  </tr>
  <tr>
    <td>train_lykoris.py</td>
    <td>Main file for AI training</td>
  </tr>
  <tr>
    <td>teste_stimmen.py</td>
    <td>File for Voicetest</td>
  </tr>
  <tr>
    <td>chat_lykoris.py</td>
    <td>Main launch file & AI logic</td>
  </tr>
  <tr>
    <td>lykoris_notizen.txt</td>
    <td>Saved memory and notes database</td>
  </tr>
  <tr>
    <td>lykoris_fertig/</td>
    <td>Local model folder (Unsloth weights)</td>
  </tr>
  <tr>
    <td>stimmen/</td>
    <td>Voices folder (Test examples)</td>
  </tr>
</table>

<h2>Installation and launch</h2>
<ol>
  <b>
    <li>
      <dl>
        <dt>Clone the repository</dt>
        <dd>
          <code>git clone <a href>https://github.com/Kyoryuu-lab/ai-vtuber-assistant.git</a></code>
        </dd>
        <dd>
          <code>cd ai-vtuber-assistant</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Install dependencies</dt>
        <dd>
          <code>pip install unsloth transformers edge-tts pygame SpeechRecognition pyaudio</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Setup VTube Studio</dt>
        <dd>
          Open VTube Studio, set the <code>MouthOpen</code> parameter to <code>VoiceVolume</code>, and enable transparent background.
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Launch the project</dt>
        <dd>
          <code>python chat_lykoris.py</code>
        </dd>
      </dl>
    </li>
  </b>
</ol>

<h2>Example of console output</h2>
<samp>
  <p>
    Wecke Lykoris auf... (Einen Moment bitte)<br />
    ==================================================<br />
    Lykoris ist wach!<br />
    Möchtest du heute tippen (T) oder sprechen (S)? S<br />
    Sprach-Modus aktiviert. (Sag 'Merke dir bitte, dass...' für Notizen)<br />
    <br />
    🎤 Lykoris hört zu... (Sprich jetzt)<br />
    Du: Hallo Lykoris!<br />
    Lykoris: Hallo mein [user]! Wie geht es dir heute?
  </p>
</samp>

<h2>Example lykoris_notizen.txt file</h2>
<samp> 
  <p>
    - [user] liebt Regenwetter zum Programmieren.<br />
    - [user] spielt sehr erfolgreich den Tiger-Panzer.<br />
  </p>
</samp>
