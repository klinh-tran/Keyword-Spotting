# Sample of Clarity Utterances database

The Clarity Speech Corpus is a forty speaker British English speech dataset. The corpus was created for the purpose of running listening tests to gauge speech intelligibility and quality in the Clarity Project, which has the goal of advancing speech signal processing by hearing aids through a series of challenges. The dataset is suitable for machine learning and other uses in speech and hearing technology, acoustics and psychoacoustics. The data comprises recordings of approximately 10,000 sentences drawn from the British National Corpus (BNC) with suitable length, words and grammatical construction for speech intelligibility testing. The collection process involved the selection of a subset of BNC sentences, the recording of these produced by 40 British English speakers, and the processing of these recordings to create individual sentence recordings with associated prompts and metadata.

## Audio files

All audio files are stored in single channel 32-bit floating point wav format at a 44.1kHz sampling rate. For full details see the paper Graetzer et al. listed below.

## Transcription file

The transcription file is in JSON format, `clarity_master.json`. It provides a list of dictionaries with each dictionary corresponding to a single utterance. Each dictionary has the following format,

```
    {
        "prompt": "At the moment I never feel I'm working hard enough.",
        "prompt_id": "G21_00436",
        "speaker": "T037",
        "wavfile": "T037_G21_00436",
        "index": 10,
        "dot": "At the moment I never feel I\\'m working hard enough"
    },
```

The fields have the following meaning.

    - `prompt` - The punctuated prompt that was presented to the reader.
    - `prompt_id` - The British National Corpus identifier for the sentence.
    - `speaker` - The ID of the sentence's speaker.
    - `wavfile` - The name of the corresponding wav file in the audio directory
    - `index` - A unique number index for the utterance
    - `dot` - Orthographic transcription of the utterance. 

## Outtakes

For some sentences there are multiple `outtakes` where voice actors either made small mistakes or made practice attempts. These have been included in the dataset for completeness, and are tagged with a repetition label 'x2', 'x3' etc, in the file name.  

e.g.,

```
- T035_K4W_11677.wav  --  Primary utterance
- T035_K4W_11677x2.wav -- 1st outtake
- T035_K4W_11677x3.wav -- 2nd outtake
```

The audio files naming follows the convention,

`<SPEAKER>_<PROMPT_ID>[<OUTTAKE_TAG>].wav`

## Further details and referencing

For full details please see,

Simone Graetzer, Michael A Akeroyd, Jon Barker, Trevor J. Cox, John F. Culling, Graham Naylor, Eszter Porter, Rhoddy Viveros Muñoz, "Dataset of British English speech recordings for psychoacoustics and speech processing research: The Clarity Speech Corpus", Data in Brief

If using this data in publications please cite the above article.
