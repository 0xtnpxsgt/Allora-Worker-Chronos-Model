import requests
import sys
import json
 
def process(argument):
    headers = {'Content-Type': 'application/json'}
    url = f"http://inference:8000/inference/{argument}"
    response = requests.get(url, headers=headers)
    return response.text
 
if __name__ == "__main__":
    # Your code logic with the parsed argument goes here
    try:
        if len(sys.argv) < 5:
            value = json.dumps({"error": f"Not enough arguments provided: {len(sys.argv)}, expected 4 arguments: topic_id, blockHeight, blockHeightEval, default_arg"})
        else:
            topic_id = sys.argv[1]
            blockHeight = sys.argv[2]
            blockHeightEval = sys.argv[3]
            default_arg = sys.argv[4]

            response_inference = process(argument=default_arg)
            response_dict = {"infererValue": response_inference}
            value = json.dumps(response_dict)
    except Exception as e:
        value = json.dumps({"error": {str(e)}})
    print(value)
