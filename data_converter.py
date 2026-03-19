import json
import csv
import argparse
from collections import defaultdict

# nakov_data = "/Users/selenasong/Desktop/Capstone/paraphrases_nakov.expe1.json"
# output_csv = "/Users/selenasong/Desktop/Capstone/nakov.csv"

def nakov_json_to_csv(json_file, output_csv_file):
    with open(json_file, "r") as f:
        nakov = json.load(f)

    with open(output_csv_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write header
        writer.writerow(['compound', 'relation'])

        # Write rows based on each entry in the JSON file
        for entry in nakov:
            # Extract 'compound' and 'relation' fields if they exist
            compound = entry['compound']
            relation = entry['correct']['label'].strip()
            writer.writerow([compound, relation])

def hb_annotated_csv_to_json(csv_file, output_json_file):
    data = []
    relation2paraphrase = {'CONT-R': ["装 的", "有 的"], 'PARTONOMY': ["的"], 'USG-R': ["用 的"],
                      'PRODUCTION': ["生产 的"], 'TOPIC-R': ["关于 的"], 'PURPOSE': ["为 设计的", "为 设立的"],
                      'COMP-R': ["做成的", "组成的"],'LOCATION': ["在 上的", "在 边的", "在 里的", "在 中的"],
                      'PROD-R': ["产生的", "发出的"]}

    # Read the CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Process each row
        for i, row in enumerate(reader):
            compound = row.get('\ufeffcompound')
            label = row.get('Hatcher-Bourque classification')
            paraphrase_translation = row.get('Paraphrase')
            if len(compound) == 2:
                modifier = compound[0]
                head = compound[1]
                paraphrase = paraphrase_translation
                if label == "COMP-R" or label == "PARTONOMY" or label == "PROD-R":
                    paraphrase = modifier + paraphrase + head
                else:
                    first_half, second_half = paraphrase_translation.split()
                    paraphrase = first_half + modifier + second_half + head
                incorrect = []
                copy = relation2paraphrase.copy()
                copy.pop(label)
                print(copy)
                for relation in copy:
                    for para in copy[relation]:
                        if relation == "COMP-R" or relation == "PARTONOMY" or relation == "PROD-R":
                            incorrect_para = modifier + para + head
                        else:
                            first_half, second_half = para.split()
                            incorrect_para = first_half + modifier + second_half + head
                        incorrect.append({"label": relation, "paraphrase": incorrect_para})

            # Add to data list as a dictionary with keys 'compound' and 'label'
            data.append({
                "id": i,
                "compound": compound,
                "correct": {"label": label, "paraphrase": paraphrase},
                "incorrect": incorrect,
                "num": "c"
            })
            print(data)

    # Write to JSON file
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def dev_test_separator(file, output_dev, output_test):
    with open(file, 'r', encoding='utf-8') as file:
        dev_test = json.load(file)

    compound_list = defaultdict(list)

    for item in dev_test:
        item.pop("id")
        compound_list[item['correct']['label']].append(item)

    dev = []
    test = []

    for relation in compound_list:
        middle = int(len(compound_list[relation])/2)
        print(middle)
        dev_part = compound_list[relation][0:middle]
        print(dev_part)
        test_part = compound_list[relation][middle:]
        print(test_part)
        dev.append(dev_part)
        test.append(test_part)

    with open(output_dev, 'w', encoding='utf-8') as dev_file:
        json.dump(dev, dev_file, indent=4, ensure_ascii=False)

    with open(output_test, 'w', encoding='utf-8') as test_file:
        json.dump(test, test_file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["convert", "split"], help="'convert': CSV to JSON, 'split': dev/test split")
    parser.add_argument("--input", help="Path to input file")
    parser.add_argument("--output", help="Path to output file (or dev output for split mode)")
    parser.add_argument("--output_test", help="Path to test output file (only for split mode)")
    args = parser.parse_args()

    if args.mode == "convert":
        hb_annotated_csv_to_json(args.input, args.output)
    elif args.mode == "split":
        if not args.output_test:
            print("Error: --output_test is required for split mode")
        else:
            dev_test_separator(args.input, args.output, args.output_test)