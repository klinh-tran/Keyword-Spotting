import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

def deduplicate_clarity_dicts(origin_file, new_file):
    '''
    Remove repeated sentences that has "wavefile" values ending with x2 or x3
    '''
    
    # Read and load JSON file
    with open(origin_file, 'r') as f:
        data = json.load(f)
        print(type(data))
    
    new_data = []
    for d in data:
        if not(d.get("wavfile").endswith("x2")) and not(d.get("wavfile").endswith("x3")):
                new_data.append(d)
    
    # Write to new JSON file
    with open(new_file, 'w') as f:
        json.dump(new_data, f, indent=4)

if __name__ == '__main__':
    audio_script_file = '\\Sound files\\Sample_clarity_utterances\\clarity_master.json'
    origin_file = current_directory + audio_script_file

    new_file = 'updated_clarity_master.json'
    deduplicate_clarity_dicts(origin_file, new_file)
