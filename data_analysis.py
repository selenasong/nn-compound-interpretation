import csv
import argparse

def surprisal_analysis(csv_file):
    stats = {}
    correct_prediction_count_dict = {'CONT-R': 0, 'PARTONOMY': 0, 'USG-R': 0, 'PRODUCTION': 0, 'TOPIC-R': 0,
                                     'COMP-R': 0, 'LOCATION': 0, 'PROD-R': 0, 'PURPOSE': 0}
    predictions_for_each_relation = {}
    for relation in correct_prediction_count_dict:
        predictions_for_each_relation.update({relation: correct_prediction_count_dict.copy()})

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        current_compound = ""
        for i, row in enumerate(reader):
            data = list(row.values())[0].split('\t')
            if i == 0:
                current_compound = data[1]
                stats.update({current_compound:{"correct":data[2], "list_of_scores":[float(data[5])], "scores_to_relation":[data[2]]}})
            else:
                if data[1] == current_compound:
                    stats[data[1]]["list_of_scores"].append(float(data[5]))
                    stats[data[1]]["scores_to_relation"].append(data[2])
                else:
                    current_compound = data[1]
                    stats.update({current_compound:{"correct":data[2], "list_of_scores":[float(data[5])], "scores_to_relation":[data[2]]}})
    print(len(stats))
    correct = 0
    incorrect = 0
    for nn_compound in stats:
        smallest = min(stats[nn_compound]["list_of_scores"])
        if stats[nn_compound]["list_of_scores"][0] == smallest:
            correct += 1
            correct_prediction_count_dict[stats[nn_compound]["correct"]] += 1
        else:
            incorrect += 1
            index = stats[nn_compound]["list_of_scores"].index(smallest)
            correct_relation = stats[nn_compound]["correct"]
            predicted_relation = stats[nn_compound]["scores_to_relation"][index]
            predictions_for_each_relation[correct_relation][predicted_relation] += 1

    print("Model: " + csv_file.split("/")[-1].split(".")[0])
    print("Number of correct predictions: " + str(correct))
    print("Number of incorrect predictions: " + str(incorrect))
    print("Accuracy: " + str(correct/(correct+incorrect)))
    print("Number of correct predictions for each relation" + str(correct_prediction_count_dict))
    for relation in correct_prediction_count_dict:
        correct_count = correct_prediction_count_dict[relation]
        incorrect_count = sum(predictions_for_each_relation[relation].values())
        print(relation)
        print("Accuracy of " + relation + " is " + str(correct_count/(correct_count+incorrect_count)))
        most_frequent_wrong_relation_prediction = max(predictions_for_each_relation[relation].values())
        for inner_relation in predictions_for_each_relation[relation]:
            if predictions_for_each_relation[relation][inner_relation] == most_frequent_wrong_relation_prediction:
                print("most frequently wrongly predicted label: " + inner_relation)
                break

def prompt_analysis(csv_files):
    correct = 0
    incorrect = 0
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            model = csv_file.split("/")[-1].split(".")[0].split("_")[0]
            for i, row in enumerate(reader):
                columns = list(row.values())[0].split(';')
                compound = columns[1]
                correct_relation = columns[2]
                correct_paraphrase = columns[3].strip()
                # # prompt_choices = list(row.values())[1][1].split("?")[1].split("Answer")[0].split(";")[:-1]
                prompt_choices = list(row.values())[1][5].split("?")[1].split("Answer")[0].split(";")[:-1]
                if model == "falcon-mamba-7b-instruct":
                    answer = list(row.values())[1][5].split(';')[10].split("assistant")[1].lstrip("Option ")[0]
                else:
                    answer = list(row.values())[1][5].split(';')[10].split(".")[0][9]
                # answer_paraphrase = list(row.values())[1][5].split(';')[10].split(".")[1].strip()
                answer_paraphrase = prompt_choices[int(answer)-1].split('.')[1].strip()
                if answer_paraphrase == correct_paraphrase:
                    correct += 1
                else:
                    incorrect += 1
    print(model)
    print(correct)
    print(incorrect)
    print("Accuracy: " + str(correct/(correct+incorrect)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["surprisal", "prompt"], help="Analysis mode: 'surprisal' or 'prompt'")
    parser.add_argument("--csv_files", nargs="+", help="Path(s) to CSV file(s) containing model outputs")
    args = parser.parse_args()

    if args.mode == "surprisal":
        for f in args.csv_files:
            surprisal_analysis(f)
    elif args.mode == "prompt":
        prompt_analysis(args.csv_files)

